from kivy.uix.screenmanager import Screen

from kivymid.app import MDApp
from kivymid.uix.button import MDRectangleFlatButton


class MainApp(MDApp):
    def build(self):
        screen = Screen()
        screen.add_widget(
            MDRectangleFlatButton(
                text="Hello, World",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        return screen


MainApp().run()