from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
import tkinter as tk
from tkinter import filedialog
from kivy.uix.floatlayout import FloatLayout
import csv
import os

class StyledLabel(Label):
    def __init__(self, **kwargs):
        if 'color' not in kwargs:
            kwargs['color'] = (1, 1, 1, 1)  # White text by default
        if 'font_size' not in kwargs:
            kwargs['font_size'] = 32  # Increased font size for better readability
        super().__init__(**kwargs)
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 22
        self.background_normal = ''
        self.background_color = (0.1, 0.3, 0.7, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = 64
        self.size_hint_x = None      # Ensures fixed width
        self.width = 300             # All buttons have the same width
        self.pos_hint = {'center_x': 0.5}  # All buttons are centered horizontally

class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 22
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 1)
        self.multiline = False
        self.padding = [16, 20]
        self.size_hint_y = None
        self.height = 64

class WeaponManager(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_file = os.path.join(os.path.dirname(__file__), 'data.csv')
        # Add background image (b_K)
        self.bg_image = Image(
            source=r"C:\Users\Lenovo\Downloads\Real life vigilante  - Chris_black reaper info.jpeg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.add_widget(self.bg_image)

        # Main content area
        self.content = BoxLayout(orientation='vertical', padding=30, spacing=18, size_hint=(1, 1))
        with self.content.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 0.3)  # Semi-transparent overlay
            self.bg_rect = Rectangle(pos=self.content.pos, size=self.content.size)
        self.content.bind(pos=self._update_bg, size=self._update_bg)

        self.weapons = []
        self.menu_layout()
        self.add_widget(self.content)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.content.pos
        self.bg_rect.size = self.content.size

    def menu_layout(self):
        self.content.clear_widgets()
        self.content.add_widget(StyledLabel(text="Weapon Management System", font_size=99, color=(0.5, 0, 0, 1), height=900))
        self.content.add_widget(StyledLabel(text="An Ideal Solution For Management of Arsenals.", font_size=2))
        btn_add = StyledButton(text="Add Weapon")
        btn_view = StyledButton(text="View Weapons")
        btn_update = StyledButton(text="Update Weapon")
        btn_delete = StyledButton(text="Delete Weapon")
        btn_exit = StyledButton(text="Exit")
        btn_add.bind(on_release=lambda x: self.add_weapon_layout())
        btn_view.bind(on_release=lambda x: self.view_weapons_layout())
        btn_update.bind(on_release=lambda x: self.update_weapon_layout())
        btn_delete.bind(on_release=lambda x: self.delete_weapon_layout())
        btn_exit.bind(on_release=lambda x: App.get_running_app().stop())
        for btn in [btn_add, btn_view, btn_update, btn_delete, btn_exit]:
            self.content.add_widget(btn)

    def add_weapon_layout(self):
        self.content.clear_widgets()
        self.content.add_widget(StyledLabel(text="Add Weapon", font_size=32))
        name_input = StyledTextInput(hint_text="Weapon Name")
        type_input = StyledTextInput(hint_text="Weapon Type")
        damage_input = StyledTextInput(hint_text="Weapon Damage", input_filter='int')
        img_path = [None]
        btn_choose_img = StyledButton(text="Choose Image")
        img_label = StyledLabel(text="No image selected", font_size=20)
        def choose_image(instance):
            root = tk.Tk()
            root.withdraw()
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
            filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
            root.destroy()
            if filename:
                img_path[0] = filename
                img_label.text = f"Selected: {filename.split('/')[-1]}"
        btn_choose_img.bind(on_release=choose_image)
        btn_save = StyledButton(text="Save")
        btn_back = StyledButton(text="Back")
        self.content.add_widget(name_input)
        self.content.add_widget(type_input)
        self.content.add_widget(damage_input)
        self.content.add_widget(btn_choose_img)
        self.content.add_widget(img_label)
        self.content.add_widget(btn_save)
        self.content.add_widget(btn_back)
        def save_weapon(instance):
            name = name_input.text.strip()
            wtype = type_input.text.strip()
            try:
                damage = int(damage_input.text.strip())
            except ValueError:
                self.show_popup("Invalid damage value. Must be an integer.")
                return
            if not name or not wtype:
                self.show_popup("Please fill all fields.")
                return
            self.weapons.append({
                "name": name,
                "type": wtype,
                "damage": damage,
                "image": img_path[0]
            })
            self.save_weapons()  # Add this line
            self.show_popup("Weapon added successfully.")
            self.menu_layout()
        btn_save.bind(on_release=save_weapon)
        btn_back.bind(on_release=lambda x: self.menu_layout())

    def view_weapons_layout(self):
        self.content.clear_widgets()
        self.content.add_widget(StyledLabel(text="List of Weapons", font_size=28))
        if not self.weapons:
            self.content.add_widget(StyledLabel(text="No weapons to display.", font_size=22))
        else:
            scroll = ScrollView(size_hint=(1, 0.8))
            box = BoxLayout(orientation='vertical', size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))
            for idx, weapon in enumerate(self.weapons, 1):
                btn = StyledButton(
                    text=f"{idx}. Name: {weapon['name']}, Type: {weapon['type']}, Damage: {weapon['damage']}",
                    size_hint_y=None, height=40
                )
                btn.bind(on_release=lambda inst, i=idx-1: self.show_weapon_detail(i))
                box.add_widget(btn)
            scroll.add_widget(box)
            self.content.add_widget(scroll)
        btn_back = StyledButton(text="Back")
        btn_back.bind(on_release=lambda x: self.menu_layout())
        self.content.add_widget(btn_back)

    def update_weapon_layout(self):
        self.content.clear_widgets()
        self.content.add_widget(StyledLabel(text="Update Weapon", font_size=20))
        if not self.weapons:
            self.content.add_widget(StyledLabel(text="No weapons to update."))
            btn_back = StyledButton(text="Back")
            btn_back.bind(on_release=lambda x: self.menu_layout())
            self.content.add_widget(btn_back)
            return
        for idx, weapon in enumerate(self.weapons, 1):
            btn = StyledButton(text=f"{idx}. {weapon['name']}")
            btn.bind(on_release=lambda inst, i=idx-1: self.edit_weapon_form(i))
            self.content.add_widget(btn)
        btn_back = StyledButton(text="Back")
        btn_back.bind(on_release=lambda x: self.menu_layout())
        self.content.add_widget(btn_back)

    def show_weapon_detail(self, idx):
        self.content.clear_widgets()
        weapon = self.weapons[idx]
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(StyledLabel(text="Weapon Management System", font_size=32))
        if weapon.get('image'):
            img_widget = Image(source=weapon['image'], allow_stretch=True, keep_ratio=False, size_hint=(1, 0.6))
            layout.add_widget(img_widget)
            btn_full = StyledButton(text="View Full Image", size_hint=(1, None), height=40)
            def show_full_image(instance):
                popup_layout = BoxLayout(orientation='vertical')
                full_img = Image(source=weapon['image'], allow_stretch=True, keep_ratio=True)
                btn_back_popup = StyledButton(text="Back", size_hint=(1, None), height=50)
                popup = Popup(
                    title="Full Image",
                    content=popup_layout,
                    size_hint=(1, 1)
                )
                btn_back_popup.bind(on_release=popup.dismiss)
                popup_layout.add_widget(full_img)
                popup_layout.add_widget(btn_back_popup)
                popup.open()
            btn_full.bind(on_release=show_full_image)
            layout.add_widget(btn_full)
        else:
            layout.add_widget(StyledLabel(text="No image for this weapon.", size_hint=(1, 0.6)))
        layout.add_widget(StyledLabel(text=f"Name: {weapon['name']}"))
        layout.add_widget(StyledLabel(text=f"Type: {weapon['type']}"))
        layout.add_widget(StyledLabel(text=f"Damage: {weapon['damage']}"))
        btn_back = StyledButton(text="Back")
        btn_back.bind(on_release=lambda x: self.view_weapons_layout())
        layout.add_widget(btn_back)
        self.content.add_widget(layout)

    def edit_weapon_form(self, idx):
        self.clear_widgets()
        weapon = self.weapons[idx]
        self.add_widget(StyledLabel(text=f"Editing Weapon #{idx+1}", font_size=20))
        name_input = StyledTextInput(text=weapon['name'])
        type_input = StyledTextInput(text=weapon['type'])
        damage_input = StyledTextInput(text=str(weapon['damage']), input_filter='int')
        img_path = [weapon.get('image')]
        btn_choose_img = StyledButton(text="Choose Image")
        img_label = StyledLabel(text=f"Selected: {img_path[0].split('/')[-1]}" if img_path[0] else "No image selected", color=(0, 0, 0, 1))
        def choose_image(instance):
            root = tk.Tk()
            root.withdraw()
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
            filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
            root.destroy()
            if filename:
                img_path[0] = filename
                img_label.text = f"Selected: {filename.split('/')[-1]}"
        btn_choose_img.bind(on_release=choose_image)
        btn_save = StyledButton(text="Save")
        btn_back = StyledButton(text="Back")
        self.add_widget(name_input)
        self.add_widget(type_input)
        self.add_widget(damage_input)
        self.add_widget(btn_choose_img)
        self.add_widget(img_label)
        self.add_widget(btn_save)
        self.add_widget(btn_back)
        def save_edit(instance):
            name = name_input.text.strip()
            wtype = type_input.text.strip()
            try:
                damage = int(damage_input.text.strip())
            except ValueError:
                self.show_popup("Invalid damage value. Keeping current value.")
                damage = weapon['damage']
            weapon['name'] = name
            weapon['type'] = wtype
            weapon['damage'] = damage
            weapon['image'] = img_path[0]
            self.save_weapons()  # Add this line
            self.show_popup("Weapon updated successfully.")
            self.menu_layout()
        btn_save.bind(on_release=save_edit)
        btn_back.bind(on_release=lambda x: self.menu_layout())

    def update_weapon_layout(self):
        self.clear_widgets()
        self.add_widget(StyledLabel(text="Update Weapon", font_size=20))
        if not self.weapons:
            self.add_widget(StyledLabel(text="No weapons to update."))
            btn_back = StyledButton(text="Back")
            btn_back.bind(on_release=lambda x: self.menu_layout())
            self.add_widget(btn_back)
            return
        for idx, weapon in enumerate(self.weapons, 1):
            btn = StyledButton(text=f"{idx}. {weapon['name']}")
            btn.bind(on_release=lambda inst, i=idx-1: self.edit_weapon_form(i))
            self.add_widget(btn)
        btn_back = StyledButton(text="Back")
        btn_back.bind(on_release=lambda x: self.menu_layout())
        self.add_widget(btn_back)

    def delete_weapon_layout(self):
        self.clear_widgets()
        self.add_widget(StyledLabel(text="Delete Weapon", font_size=20))
        if not self.weapons:
            self.add_widget(StyledLabel(text="No weapons to delete."))
            btn_back = StyledButton(text="Back")
            btn_back.bind(on_release=lambda x: self.menu_layout())
            self.add_widget(btn_back)
            return
        for idx, weapon in enumerate(self.weapons, 1):
            btn = StyledButton(text=f"Delete {idx}. {weapon['name']}")
            btn.bind(on_release=lambda inst, i=idx-1: self.confirm_delete(i))
            self.add_widget(btn)
        btn_back = StyledButton(text="Back")
        btn_back.bind(on_release=lambda x: self.menu_layout())
        self.add_widget(btn_back)

    def confirm_delete(self, idx):
        weapon = self.weapons[idx]
        popup = Popup(title="Confirm Delete", size_hint=(0.6, 0.4))
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(StyledLabel(text=f"Delete {weapon['name']}?"))
        btns = BoxLayout()
        btn_yes = StyledButton(text="Yes")
        btn_no = StyledButton(text="No")
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        layout.add_widget(btns)
        popup.content = layout

        def do_delete(instance):
            self.weapons.pop(idx)
            self.save_weapons()  # Add this line
            popup.dismiss()
            self.show_popup("Weapon deleted successfully.")
            self.menu_layout()
        btn_yes.bind(on_release=do_delete)
        btn_no.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def show_popup(self, message):
        popup = Popup(title="Info", content=StyledLabel(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def load_weapons(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                self.weapons = list(reader)
                # Convert damage back to int
                for weapon in self.weapons:
                    weapon['damage'] = int(weapon['damage'])

    def save_weapons(self):
        with open(self.data_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'type', 'damage', 'image'])
            writer.writeheader()
            writer.writerows(self.weapons)

class WeaponApp(App):
    def build(self):
        return WeaponManager()

if __name__ == "__main__":
    WeaponApp().run()