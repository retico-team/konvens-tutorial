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
