# Creating an incremental translation system

In this second part of the tutorial, you will have a look at the inner workings of incremental modules by implementing your own incremental translation module. The translation will be performed with the huggingface transformer library. An already implemented non-incremental version of the translator can be found in retico's `helper` module:

```python
from retico import *

translator = helper.HFTranslate(from_lang="en",to_lang="de")
print(translator.translate("Hello KONVENS, this is a test."))
```

You can test out the behavior of the module (and sometimes find some funny exceptions where the transformer generates nonsense). The translator supports the following language combinations:

- English to French
- French to English
- English to German
- German to English
- Spanish to English
- English to Spanish
- French to German
- German to French

As the translator is not incremental yet, you have to write additional code to make it incremental. That means that the new incremental translation module will have to keep track of all the incremental units that it has received to build the current sentence that should be translated. Also, it needs to keep track of all the incremental units it has created and compare the current prediction of the translator model with the currently predicted IUs. Then, it has to revoke IUs that are no longer valid and add new IUs to reflect the new hypothesis.

## Creating a new incremental module

As with the WordChangerModule in the last part of the tutorial, you need to create a new incremental module:

```python
class TranslationModule(AbstractModule):
    @staticmethod
    def name():
        return "Translation Module from the KONVENS 2022 retico tutorial"

    @staticmethod
    def description():
        return "A module that translates between languages."

    @staticmethod
    def input_ius():
        return [ius.TextIU]

    @staticmethod
    def output_iu():
        return ius.TextIU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translator = helper.HFTranslate("en", "de")

    def process_update(self, update_message):
        pass
```

In this code, the module already has it's four mandatory static methods `name`, `description`, `input_ius` and `output_iu`. The module takes TextIUs as an input and also produces TextIUs as an output. Also, in the initializer of the module, a translater is initialized that translates text from English to German (you can, of course, change that to another available language combination).

The `process_update` method will be the difficult part of this module, so you can leave it empty for now to build it up step by step.

## Handling incoming incremental units

The first task of the `process_update` method is to handle incoming incremental units. They are bundled in an `UpdateMessage`, and each IU has an `UpdateType` (ADD, REVOKE, COMMIT) that defines what to do with it. That is why the method first iterates over all incremental units in the incoming update message and, depending on the update type, processes them:

```python
def process_update(self, update_message):
    for incremental_unit, update_type in update_message:
        if update_type == UpdateType.ADD:
            self.current_input.append(incremental_unit)
        elif update_type == UpdateType.REVOKE:
            self.revoke(incremental_unit)
        elif update_type == UpdateType.COMMIT:
            self.commit(incremental_unit)
```

Somehow, the module needs to keep track of which incremental units are currently part of the hypothesis, which IUs are revoked, and which IUs have been committed (i.e., they won't be changed anymore). For this, the `AbstractModule` has a useful structure to handle that: `current_input` is a list of IUs that are currently being used to form a new output hypothesis (in this case the translation).

When the update type of an IU is "add" (in the code explicitly written as `UpdateType.ADD`) the new IU is appended to that `current_input` list.

When the update type of an IU is "revoke", the `revoke`-method of the module is called. This method is inherited from retico's `AbstractModule`, goes through the list of IUs in the `current_input`, and if it finds the previously added IU, it flags it as revoked and removes it. That way, it will no longer be considered in the forming of new hypotheses.

When the update type is "commit", the `commit`-method of the module is called. Similar to the `revoke`-method, the corresponding IU is located in the `current_input` list and flagged as committed (but not removed!).

## Reconstructing the current text and translating it

Now, to reconstruct the text that is stored in the `current_input`, you need to iterate over every IU in that list and extract the containing text:

```python
current_text = " ".join([iu.text for iu in self.current_input])
current_translation = self.translator.translate(current_text)
```

In the first line, all the text contained in the IUs of `self.current_input` is *joined* with the space character `" "`. That means if the list of IUs contains `["this", "is", "a", "test"]`, it will be converted to `"this is a test"`. Then, the translation is generated using the `translator` that was instantiated in the initializer.

## Converting translations into increments

Now the translation hypothesis is ready, but not incremental. If in the previous `process_update` call the module generated two IUs `["das", "ist"]`, and the new translation result is `"das ist ein test"` the module should not output the complete translation, but rather the *difference* to the earlier prediction (i.e., two new IUs `["ein", "test"]` with the update type "add").

For this, there is a data structure very similar to `current_input` called `current_output`, where all currently valid incremental units produced by the modules themselves can be stored. In order to calculate the increment from the translated text (`current_translation`) to the text that is contained in the `current_output` list, the translation has to be split into words and compared to every previously generated IU.

Luckily, there is a helper function of retico that does exactly that:

```python
update_msg, new_tokens = helper.get_text_increment(self, current_translation)
```

The `get_text_increment` function takes a reference to the current module (`self`) and the full translated text (`current_translation`) and returns an update message and a list of new tokens. The update message contains IUs from the `current_output` that are revoked (and thus removed from the `current_output`-list) with the corresponding update type "revoke". The new tokens list contains the words that need to be turned into a new incremental unit.

Let's look at an example. The `process_update` method is called for the first time, and there are no IUs in the `current_output`. The `current_translation` is `"The quick bright"`. In this case, the `get_text_increment` function would return an empty update message (as there are no IUs to revoke) and a list of new tokens `["the", "quick", "bright"]`.

Let's say the `process_update` method is called a second time, and the current translation is `"The quick brown fox"`. Now, the `get_text_increment` function would return an update message, revoking the IU `"bright"` and the new token list would contain `["brown", "fox"]`.

## Adding the new tokens

Now the `process_update` method needs to convert all words in the `new_token` list into their own IUs and add them to the update message containing the revoked IUs:

```python
for token in new_tokens:
    new_iu = self.create_iu(grounded_in=incremental_unit)
    new_iu.text = token
    self.current_output.append(new_iu)
    update_msg.add_iu(new_iu, UpdateType.ADD)
```

To create a new incremental unit the `create_iu` method can be used. It takes the `grounded_in` incremental module as the argument that should point to the incoming incremental unit that the current prediction is *grounded in*. The method also automatically adds links to the IU previously created by the module. Also, the text of the IU is set to be the token.

Finally, the new IU has to be appended to the `current_output` and to the update message (with the update type "add").

## Cleaning up when IUs are committed

As the last step, when all incremental units in the `current_input` are committed (i.e., they will not be revoked or updated anymore), the module should also flag the corresponding output IUs as committed. That way, the `current_input` and `current_output` does not need to keep track of these IUs anymore:

```python
if self.input_committed():
    for iu in self.current_output:
        self.commit(iu)
        update_msg.add_iu(iu, UpdateType.COMMIT)
    self.current_input = []
    self.current_output = []
return update_msg
```

The method `input_committed` checks if *every* IU in the `current_input` is committed and only then returns True. Then, all the IUs in the current output are flagged as committed with the `self.commit` method and the IUs are added to the update message with the "commit" update type. The `current_input` and `current_output` lists are cleared, as the module no longer needs to keep track of these IUs.

Finally, the update message that may contain IUs to revoke, add, and/or commit is returned and forwarded to the subscribed module.

## Building the network

With the newly created translation module, you can now create your network:

```python
microphone = modules.MicrophoneModule(rate=16000)
asr = modules.Wav2VecASRModule(language="en")
translation = TranslationModule()
printer = modules.TextPrinterModule()

microphone.subscribe(asr)
asr.subscribe(translation)
translation.subscribe(printer)

run(microphone)

print("Network is running")
input()

stop(microphone)
```

## Exercises for you

- Add the input and output languages as parameters to the initializer of the module
- Create a translation module chain that translates from English to German, to French, to Spanish, and back to English
- Add a SpeechbrainTTS and a Speaker Module and listen to the translation (currently only in English)
