from retico import *


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
        for incremental_unit, update_type in update_message:
            if update_type == UpdateType.ADD:
                self.current_input.append(incremental_unit)
            elif update_type == UpdateType.REVOKE:
                self.revoke(incremental_unit)
            elif update_type == UpdateType.COMMIT:
                self.commit(incremental_unit)

        current_text = " ".join([iu.text for iu in self.current_input])
        current_translation = self.translator.translate(current_text)

        update_msg, new_tokens = helper.get_text_increment(self, current_translation)

        for token in new_tokens:
            new_iu = self.create_iu(grounded_in=incremental_unit)
            new_iu.text = token
            self.current_output.append(new_iu)
            update_msg.add_iu(new_iu, UpdateType.ADD)

        if self.input_committed():
            for iu in self.current_output:
                self.commit(iu)
                update_msg.add_iu(iu, UpdateType.COMMIT)
            self.current_input = []
            self.current_output = []

        return update_msg


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
