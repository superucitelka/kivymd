from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.selection import MDSelectionList
from kivy.uix.pagelayout import PageLayout
from kivymd.utils.fitimage import FitImage

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: app.theme_cls.bg_light

    MDToolbar:
        id: toolbar
        title: "Inbox"
        left_action_items: [["menu"]]
        right_action_items: [["magnify"], ["dots-vertical"]]
        md_bg_color: app.theme_cls.bg_light
        specific_text_color: 0, 0, 0, 1

    MDBoxLayout:
        padding: "24dp", "8dp", 0, "8dp"
        adaptive_size: True

        MDLabel:
            text: "Today"
            adaptive_size: True

    ScrollView:

        MDSelectionList:
            id: selection_list
            padding: "24dp", 0, "24dp", "24dp"
            cols: 3
            spacing: "12dp"
            overlay_color: app.overlay_color[:-1] + [.2]
            icon_bg_color: app.overlay_color
            progress_round_color: app.progress_round_color
            on_selected: self.parent.parent.parent.on_selected(*args)
            on_unselected: self.parent.parent.parent.on_unselected(*args)
            on_selected_mode: self.parent.parent.parent.set_selection_mode(*args)
'''



class Selection(PageLayout):
    overlay_color = get_color_from_hex("#aaaaaa")
    progress_round_color = get_color_from_hex("#ef514b")

    def __init__(self, *args, **kwargs):
        super(Selection, self).__init__(*args, **kwargs)
        self.builder = Builder.load_string(KV)
        print(self.builder.ids)
        for i in range(10):
            self.builder.ids.selection_list.add_widget(
                FitImage(
                    source="image.png",
                    size_hint_y=None,
                    height="240dp",
                )
            )
        self.add_widget(self.builder)


    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.builder.ids.selection_list.unselected_all(),
                ]
            ]
            right_action_items = [["trash-can"], ["dots-vertical"]]
        else:
            md_bg_color = (1, 1, 1, 1)
            left_action_items = [["menu"]]
            right_action_items = [["magnify"], ["dots-vertical"]]
            self.builder.ids.toolbar.title = "Inbox"

        Animation(md_bg_color=md_bg_color, d=0.2).start(self.builder.ids.toolbar)
        self.builder.ids.toolbar.left_action_items = left_action_items
        self.builder.ids.toolbar.right_action_items = right_action_items


    def on_selected(self, instance_selection_list, instance_selection_item):
        print('selected')
        print(str(
            len(instance_selection_list.get_selected_list_items())
        ))


    def on_unselected(self, instance_selection_list, instance_selection_item):
        if instance_selection_list.get_selected_list_items():
            self.builder.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )
