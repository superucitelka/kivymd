from kivy.uix.screenmanager import Screen
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class Kniha(PageLayout):

    def __init__(self, nazev, *args, **kwargs):
        super(Kniha, self).__init__(*args, **kwargs)

        #Vytvoříme obal, který bude vše držet pospolu
        self.obal_layout = BoxLayout(orientation = "vertical")

        #Vytvoříme si obal pro knížku
        self.layout = PageLayout(size_hint = (1, .9))
        #Vytvoříme si stránku
        self.strana1 = BoxLayout(orientation = "vertical")
        #Přidáme barvu do canvasu
        self.strana1.canvas.before.add(Color(rgba = (0.5, 0, 0.5, 1)))
        #Přidáme čtverec do canvasu
        self.ctverec1 = Rectangle(size = self.strana1.size, pos = self.strana1.pos)
        self.strana1.canvas.before.add(self.ctverec1)
        #Přidáme Label, který se zobrazí na stránce
        self.strana1.add_widget(Label(text = nazev))

        #Vytvoříme si stránku
        self.strana2 = BoxLayout(orientation = "vertical")
        #Přidáme barvu do canvasu
        self.strana2.canvas.before.add(Color(rgba = (0.5, 0.5, 0, 1)))
        #Přidáme čtverec do canvasu
        self.ctverec2 = Rectangle(size = self.strana2.size, pos = self.strana2.pos)
        self.strana2.canvas.before.add(self.ctverec2)
        #Přidáme Label, který se zobrazí na stránce
        self.strana2.add_widget(Label(text = "Strana"))

        #Přídáme strany do PageLayoutu a ten přídáme do obalu
        self.layout.add_widget(self.strana1)
        self.layout.add_widget(self.strana2)
        self.obal_layout.add_widget(self.layout)

        #ZDE BUDE OVLÁDACÍ PANEL

        self.add_widget(self.obal_layout)

        self.strana1.bind(size = self.update, pos = self.update)
        self.strana2.bind(size = self.update, pos = self.update)

    def update(self, *args):
        self.ctverec1.size = self.size
        self.ctverec1.pos = self.strana1.pos

        self.ctverec2.size = self.size
        self.ctverec2.pos = self.strana2.pos