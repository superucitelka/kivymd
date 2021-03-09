from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDIconButton, MDFillRoundFlatIconButton, MDRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
import json


class Content(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)
        if id:
            person = next((obj for obj in app.persons.person_list if obj['id'] == id), None)
        else:
            person = {"id":app.persons.person_list[len(app.persons.person_list) - 1]["id"] + 1, "name": "", "state": "Stát"}
            print(person)

        self.ids.person_name.text = person['name']

        STATES = ['CAN', 'CZE', 'FIN', 'GBR', 'GER', 'JAP', 'NOR', 'POL', 'RUS', 'SVK', 'SWE', 'USA']
        menu_items = [{"icon": "git", "text": f"{state}"} for state in STATES]
        self.menu = MDDropdownMenu(
            caller=self.ids.state_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.ids.state_item.set_item(person['state'])
        self.menu.bind(on_release=self.set_item)

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.state_item.set_item(instance_menu_item.text)
        self.ids.state_item.text = instance_menu_item.text
        self.menu.dismiss()


class MyDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(MyDialog, self).__init__(
            type="custom", title='Záznam osoby',
            text=self.text,
            size_hint=(.8, 1),
            content_cls=Content(id=id),
            buttons=[
                MDFlatButton(text='Save', on_release=self.save_dialog),
                MDFlatButton(text='Cancel', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        person = {}
        person['name'] = self.content_cls.ids.person_name.text
        person['state'] = self.content_cls.ids.state_item.text
        if self.id:
            person["id"] = self.id
            app.persons.update(person)
        else:
            app.persons.create(person)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()

"""
Třída MyItem řeší akce související s jednou položkou (osobou) v seznamu
"""
class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        """
        Konstruktoru se předává parametr item - datový objekt jedné osoby
        """
        super(MyItem, self).__init__()
        # Předání informací o osobě do parametrů widgetu
        self.id = item['id']
        self.text = item['name']
        self.secondary_text = item['state']
        self._no_ripple_effect = True
        # Zobrazení vlajky podle státu osoby
        self.image = ImageLeftWidget(source=f"images/{item['state']}.png")
        self.add_widget(self.image)
        # Vložení ikony pro vymazání osoby ze seznamu
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        """
        Metoda je vyvolána po stisknutí tlačítka v oblasti widgetu
        Otevře se dialogové okno pro editaci osobních dat
        """
        self.dialog = MyDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        """
        Metoda je vyvolána po kliknutí na ikonu koše - vymazání záznamu
        """
        yes_button = MDFlatButton(text='Ano', text_color=self.theme_cls.primary_color, on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', text_color=self.theme_cls.primary_color, on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.persons.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


"""
Třída Persons řeší akce související se seznamem osob
"""
class Persons(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Persons, self).__init__(orientation="vertical")
        # Globální proměnná - obsahuje kontext aplikace
        global app
        app = App.get_running_app()
        # Vytvoření rolovacího seznamu
        scrollview = ScrollView()
        self.list = MDList()
        # Volání metody, která načte seznam osob ze souboru JSON
        self.person_list = self.read()
        # Volání metody, která načte přepíše seznam osob na obrazovku
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        # Přidání tlačítka pro vložení nového záznamu
        self.add_widget(MDFillRoundFlatIconButton(
            text="Nový záznam",
            icon="plus",
            icon_color=[0.9,0.9,0.9,1],
            text_color=[0.9,0.9,0.9,1],
            md_bg_color=[0,0.5,0.8,1],
            font_style="Button",
            pos_hint={"center_x": .5},
            on_release=self.on_create)
        )

    def rewrite_list(self):
        """
        Metoda přepíše seznam osob na obrazovce
        """
        self.list.clear_widgets()
        # Pro všechny osoby v seznamu self.person_list vytváří widget MyItem
        for person in self.person_list:
            self.list.add_widget(MyItem(item=person))

    def on_create(self, *args):
        """
        Metoda reaguje na tlačítko Nový záznam a vyvolá dialogové okno MyDialog
        """
        self.dialog = MyDialog(id=None)
        self.dialog.open()

    def create(self, person):
        """
        Metoda vytvoří nový záznam
        """
        self.person_list.append({
            "id": self.person_list[len(self.person_list) - 1]["id"] + 1,
            "name": person["name"],
            "state": person["state"]
        })
        self.rewrite_list()
        self.save_data()

    def update(self, person):
        """
        Metoda aktualizuje záznam
        """
        update_person = next((obj for obj in self.person_list if obj['id'] == person["id"]), None)
        update_person["name"] = person["name"]
        update_person["state"] = person["state"]
        self.rewrite_list()
        self.save_data()


    def read(self):
        """
        Metoda načítá data ze souboru JSON
        """
        with open('files/person.json', encoding='utf-8') as f:
            return json.load(f)

    def delete(self, id):
        """
        Metoda smaže záznam o osobě
        """
        person = next((obj for obj in self.person_list if obj['id'] == int(id)), None)
        self.person_list.remove(person)
        self.rewrite_list()
        self.save_data()

    def save_data(self):
        """
        Metoda ukládá data do souboru JSON
        """
        with open('files/person.json', 'w', encoding='utf-8') as f:
            json.dump(self.person_list, f)
