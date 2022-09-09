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
        self.translator = aux.HFTranslate("en", "de")
        self._latest_text = ""
        self._latest_translation = ""
        self.current_output_ius = []
        self.latest_input_iu = None

    def current_text(self):
        return " ".join([iu.text for iu in self.current_ius])

    def process_update(self, update_message):
        for incremental_unit, update_type in update_message:
            if update_type == UpdateType.ADD:
                self.current_ius.apend(incremental_unit)
            elif update_type == UpdateType.REVOKE:
                self.revoke(incremental_unit)

        current_text = self.current_text()
        current_translation = self.translator.translate(current_text)
