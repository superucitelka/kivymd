from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder


class TextScreen(Screen):
    pass


class FormScreen(Screen):
    pass


class TableScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file('bottom.kv')


Test().run()