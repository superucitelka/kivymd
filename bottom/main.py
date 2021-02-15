from kivymd.app import MDApp
from kivy.lang import Builder


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Yellow"
        return Builder.load_file('bottom.kv')


Test().run()