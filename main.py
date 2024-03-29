import kivy
kivy.require('2.1.0')
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from calculate import calcular
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.utils import platform


Window.fullscreen = 'auto'

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class MainWindow(MDScreen):
    pass

class SecondWindow(MDScreen):
    pass

class WindowManager(ScreenManager):
    pass

class MyGridLayout(GridLayout):

    dialog = None
    amistades_claras = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_fields = []


    def limpiar(self):
        for child in self.children[:]:
            if isinstance(child, MDTextField):
                child.text = ""
                self.remove_text_field(self)


    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Error",
                text="No dejar campos vacíos"
                #buttons = [MDFlatButton(text="OK", on_release = Dialog.dismiss(Dialog))]
            )
        self.dialog.open()


    def remove_text_field(self, instance):
        num_dynamic_fields = len(self.dynamic_fields)
        if num_dynamic_fields >= 2:
            # remove the last 2 dynamically created fields from the list
            last_fields = self.dynamic_fields[-2:]
            self.dynamic_fields = self.dynamic_fields[:-2]

            # remove the last 2 dynamically created fields from the parent widget
            for field in last_fields:
                self.remove_widget(field)

   
    def add_text_field(self):

        self.createMDTextField("Ingresar nombre", "account")
        self.createMDTextField("Ingresar monto", "cash")


    def createMDTextField(self, hint_text, icon_right):
        new_name_field = MDTextField(
            line_color_focus = (0, 0, 0, 0),
            hint_text=hint_text,
            helper_text_mode="on_focus",
            icon_right=icon_right,
            pos_hint={"center_x": 0.5, "top": 1},
            helper_text = "Doble tap para eliminar",
            font_size=50,
            adaptive_height=True
        )
        new_name_field.bind(on_double_tap=self.remove_text_field)
        self.add_widget(new_name_field)
        self.dynamic_fields.extend([new_name_field])


    def calcular_func(self):    # sourcery skip: extract-method, split-or-ifs
        text_inputs = [
            child.text for child in self.children if isinstance(child, MDTextField)
        ]
        print(f"text_inputs: {text_inputs}")
        # Chequeo si son numeros
        try:
            for i in range(0, len(text_inputs), 2):
                
                if text_inputs[i] == "":
                    text_inputs[i] = 0

            print(f"text_inputs: {text_inputs}")
            
            global amistades_claras
            amistades_claras = calcular(text_inputs)
            print(f"amistades_claras in main: {amistades_claras}")

            return amistades_claras
    
        except Exception:
            self.show_alert_dialog()
            
            


class MySecondGridLayout(GridLayout):
    
    amistades_claras = MyGridLayout.amistades_claras
    print(f"amistades_claras_MySecondGridLayout: {amistades_claras}")

    def setLabel(self):  # sourcery skip: extract-method

        # Remove existing labels from the widget
        for child in self.children[:]:
            if isinstance(child, MDLabel):
                self.remove_widget(child)


        todos_deben = MDLabel(text=amistades_claras[0])
        todos_deben.font_size = 30
        todos_deben.color = "#00796B"
        todos_deben.bold
        todos_deben.size_hint_x = 0.9
        self.add_widget(todos_deben)

        # Quien debe a quien LABEL
        for amistad in amistades_claras[1:]:
            label_amistad = MDLabel(text=amistad, markup=True)
            label_amistad.adaptive_height = True
            label_amistad.halign = "center"
            label_amistad.font_size = 30
            label_amistad.size_hint_x = 0.5

            # Set the label text with the first and last words colored
            words = amistad.split(" ")

            if words[0] == "A":
                label_text = f"{words[0]}" + f" [color=#0099ff]{words[1].title()}[/color]"

                for word in words[2:-1]:
                    label_text += f" {word}"

            else:
                label_text = f"[color=#009688]{words[0].title()}[/color]"

                for word in words[1:-1]:
                    label_text += f" {word}"

            label_text += f" [color=#009688]{words[-1].title()}[/color]"

            label_amistad.text = label_text

            self.add_widget(label_amistad)
                




class AmistadesClaras(MDApp):

    def build(self):
        Window.size
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        #['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        return Builder.load_file("main.kv")


if __name__ == '__main__':
    AmistadesClaras().run() 