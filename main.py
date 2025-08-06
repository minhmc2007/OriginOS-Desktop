
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.uix.switch import Switch
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
import time
import os
try:
    import psutil
except ImportError:
    psutil = None

class WindowControls(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.adaptive_size = True
        self.spacing = "5dp"
        self.pos_hint = {'x': 0.02, 'top': 0.98}
        
        close_button = MDIconButton(
            icon='close-circle',
            icon_color=(1, 0.3, 0.3, 1),
            on_release=lambda x: MDApp.get_running_app().close_app()
        )
        minimize_button = MDIconButton(
            icon='minus-circle',
            icon_color=(1, 0.8, 0.2, 1)
        )
        maximize_button = MDIconButton(
            icon='arrow-up-circle',
            icon_color=(0.2, 0.8, 0.2, 1)
        )
        
        self.add_widget(close_button)
        self.add_widget(minimize_button)
        self.add_widget(maximize_button)

# Kivy Language string for the UI layout
Builder.load_string("""
#:import time time
#:import Clock kivy.clock.Clock
#:import Window kivy.core.window.Window

<IconCard>:
    radius: 20
    ripple_behavior: True
    ripple_alpha: .2
    elevation: 0

<AppIcon>:
    orientation: 'vertical'
    size_hint: None, None
    size: "60dp", "80dp"
    spacing: "5dp"

    IconCard:
        id: icon_card
        size_hint: None, None
        size: "60dp", "60dp"
        pos_hint: {'center_x': .5}
        md_bg_color: root.bg_color
        on_release: app.open_app(root)

        MDIcon:
            id: icon
            icon: root.icon
            halign: 'center'
            valign: 'center'
            pos_hint: {'center_x': .5, 'center_y': .5}
            font_size: "30sp"

    MDLabel:
        id: label
        text: root.text
        halign: 'center'
        font_style: "Caption"

<HomeScreen>:
    name: 'home'
    MDFloatLayout:
        id: float_layout

        Image:
            id: wallpaper_bg
            source: app.wallpaper_path
            fit_mode: "cover"

        # Top Dock
        MDBoxLayout:
            id: top_bar
            orientation: 'horizontal'
            size_hint: 1, None
            height: "40dp"
            pos_hint: {'top': 1}
            md_bg_color: app.theme_cls.primary_color
            padding: "5dp"
            spacing: "10dp"

            # Left side of the dock
            MDBoxLayout:
                id: top_bar_left
                orientation: 'horizontal'
                size_hint_x: None
                width: self.minimum_width
                spacing: "10dp"
                padding: "10dp", 0, 0, 0
                pos_hint: {'center_y': .5}
                MDIcon:
                    icon: "linux" # Placeholder logo
                    pos_hint: {'center_y': .5}

            # Spacer
            MDBoxLayout:

            # Right side of the dock
            MDBoxLayout:
                id: top_bar_right
                orientation: 'horizontal'
                adaptive_size: True
                spacing: "15dp"
                padding: 0, 0, "10dp", 0
                pos_hint: {'center_y': .5}
                MDLabel:
                    id: battery_label
                    text: "100%"
                    adaptive_size: True
                    pos_hint: {'center_y': .5}
                MDLabel:
                    id: time_label
                    text: "12:00"
                    adaptive_size: True
                    pos_hint: {'center_y': .5}
        
        # Desktop App Icons
        MDGridLayout:
            id: desktop_app_grid
            cols: 2
            adaptive_height: True
            size_hint_x: None
            width: "180dp"
            pos_hint: {'x': 0.02, 'top': 1 - top_bar.height/Window.height if Window.height > 0 else 1}
            spacing: "20dp"
            padding: "10dp"
            
<LockScreen>:
    name: 'lock'
    time: ''
    on_enter:
        self.time = time.strftime("%H:%M")
        Clock.schedule_interval(root.update_time, 1)

    MDFloatLayout:
        Image:
            id: lock_wallpaper_bg
            source: app.wallpaper_path
            fit_mode: "cover"

        MDLabel:
            text: root.time
            halign: 'center'
            font_style: 'H2'
            pos_hint: {'center_y': .7}

        MDRaisedButton:
            text: "Unlock"
            pos_hint: {'center_x': .5, 'center_y': .2}
            on_release: app.root.current = 'home'

<SettingsWidget>:
    orientation: 'vertical'
    padding: "10dp"
    spacing: "10dp"

    OneLineListItem:
        text: "About"
        on_release: app.show_about_dialog()

    OneLineListItem:
        text: "Animation Speed"
        on_release: app.show_animation_speed_dialog()
    
    OneLineListItem:
        text: "Theme"
        on_release: app.root.current = 'theme'

<ThemeScreen>:
    name: 'theme'
    orientation: 'vertical'
    MDTopAppBar:
        title: "Theme"
        left_action_items: [["arrow-left", lambda x: app.close_settings()]]

    MDBoxLayout:
        orientation: 'vertical'
        padding: "10dp"
        spacing: "10dp"

        OneLineListItem:
            text: "Wallpaper"
            on_release: app.show_wallpaper_dialog()

        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            padding: "12dp", 0
            MDLabel:
                text: "Dark Mode"
                font_style: "Body1"
                valign: "center"
            MDBoxLayout:
            Switch:
                id: theme_switch
                size_hint_x: None
                width: "48dp"
                active: app.theme_cls.theme_style == "Dark"
                on_active: app.toggle_theme(self.active)

<PhoneApp>:
    orientation: 'vertical'
    MDTextField:
        id: number_display
        halign: 'center'
        font_size: '40sp'
        readonly: True
        pos_hint: {'center_x': .5, 'top': .95}
        size_hint_x: .9
        line_color_focus: [0,0,0,0]
        fill_color_normal: [0,0,0,0]
    MDGridLayout:
        cols: 3
        spacing: '20dp'
        size_hint: .8, .5
        pos_hint: {'center_x': .5, 'center_y': .5}
        MDRoundFlatButton:
            text: "1"
            on_release: root.add_char("1")
        MDRoundFlatButton:
            text: "2"
            on_release: root.add_char("2")
        MDRoundFlatButton:
            text: "3"
            on_release: root.add_char("3")
        MDRoundFlatButton:
            text: "4"
            on_release: root.add_char("4")
        MDRoundFlatButton:
            text: "5"
            on_release: root.add_char("5")
        MDRoundFlatButton:
            text: "6"
            on_release: root.add_char("6")
        MDRoundFlatButton:
            text: "7"
            on_release: root.add_char("7")
        MDRoundFlatButton:
            text: "8"
            on_release: root.add_char("8")
        MDRoundFlatButton:
            text: "9"
            on_release: root.add_char("9")
        MDRoundFlatButton:
            text: "*"
            on_release: root.add_char("*")
        MDRoundFlatButton:
            text: "0"
            on_release: root.add_char("0")
        MDRoundFlatButton:
            text: "#"
            on_release: root.add_char("#")
    MDFloatLayout:
        pos_hint: {'center_x': .5, 'y': .1}
        size_hint_x: .8
        MDIconButton:
            icon: 'phone'
            pos_hint: {'center_x': .5, 'center_y': .5}
            user_font_size: "30sp"
        MDIconButton:
            icon: 'backspace'
            pos_hint: {'right': 1, 'center_y': .5}
            on_release: root.del_char()
""")


class IconCard(MDCard):
    radius: 20
    ripple_behavior: True
    ripple_alpha: .2
    elevation: 0

class AppIcon(MDBoxLayout):
    icon = StringProperty()
    text = StringProperty()
    bg_color = ObjectProperty()


class HomeScreen(MDScreen):
    pass


class LockScreen(MDScreen):
    time = StringProperty()

    def update_time(self, *args):
        self.time = time.strftime("%H:%M")

class SettingsWidget(MDBoxLayout):
    pass

class ThemeScreen(MDScreen):
    pass

class PhoneApp(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
    def add_char(self, char):
        self.ids.number_display.text += char

    def del_char(self):
        self.ids.number_display.text = self.ids.number_display.text[:-1]

class OriginOSApp(MDApp):
    current_app_window = None
    opened_from_icon = None
    animation_speed = NumericProperty(0.5)
    wallpaper_path = StringProperty("originos_data/wallpaper_3.png") # Default wallpaper
    app_widgets = {}
    open_app_icons = {}
    wallpaper_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        self.app_widgets = {
            "Settings": SettingsWidget(),
            "Phone": PhoneApp(),
            "Default": MDLabel(text="Nothing", halign="center", font_style="H3")
        }

        sm = ScreenManager()
        sm.add_widget(LockScreen())
        home_screen = HomeScreen()
        self.populate_home_screen(home_screen)
        sm.add_widget(home_screen)
        sm.add_widget(ThemeScreen(name='theme'))
        
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_battery, 5) # Update battery every 5 seconds
        return sm

    def update_battery(self, *args):
        home_screen = self.root.get_screen('home')
        if home_screen:
            if psutil:
                battery = psutil.sensors_battery()
                if battery:
                    percent = int(battery.percent)
                    home_screen.ids.battery_label.text = f"{percent}%"
                else:
                    home_screen.ids.battery_label.text = "N/A"
            else:
                home_screen.ids.battery_label.text = "N/A"

    def update_time(self, *args):
        home_screen = self.root.get_screen('home')
        if home_screen:
            home_screen.ids.time_label.text = time.strftime("%H:%M")

    def on_start(self):
        Window.bind(on_keyboard=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        print(f"Key pressed: keycode={keycode}, text='{text}'")
        if self.root.current == 'home':
            if text and text.isdigit() and 1 <= int(text) <= 8:
                self.open_app_by_index(int(text) - 1)
            elif keycode == 42:  # Backspace key
                self.close_app()

    def open_app_by_index(self, index):
        home_screen = self.root.get_screen('home')
        if index < len(home_screen.ids.desktop_app_grid.children):
            self.open_app(home_screen.ids.desktop_app_grid.children[-(index + 1)])

    def populate_home_screen(self, screen):
        apps = [
            {"icon": "phone", "text": "Phone", "color": (0.2, 0.7, 0.3, 1)},
            {"icon": "message", "text": "Messages", "color": (0.9, 0.2, 0.4, 1)},
            {"icon": "web", "text": "Browser", "color": (0.2, 0.5, 0.9, 1)},
            {"icon": "camera", "text": "Camera", "color": (0.5, 0.5, 0.5, 1)},
            {"icon": "image-multiple", "text": "Gallery", "color": (0.9, 0.5, 0.1, 1)},
            {"icon": "cog", "text": "Settings", "color": (0.7, 0.7, 0.7, 1)},
            {"icon": "map-marker", "text": "Maps", "color": (0.1, 0.8, 0.5, 1)},
            {"icon": "music", "text": "Music", "color": (1, 0.4, 0.4, 1)},
        ]
        
        for i, app_info in enumerate(apps):
            app_icon = AppIcon(
                icon=app_info["icon"],
                text=app_info["text"],
                bg_color=app_info["color"]
            )
            screen.ids.desktop_app_grid.add_widget(app_icon)

    def open_app(self, icon_widget):
        if self.current_app_window and self.opened_from_icon == icon_widget:
            return

        if self.current_app_window:
            self.close_app()

        self.opened_from_icon = icon_widget
        
        content = self.app_widgets.get(icon_widget.text, self.app_widgets["Default"])
        if content.parent:
            content.parent.remove_widget(content)
        content.opacity = 0

        app_bg_color = icon_widget.bg_color
        if self.theme_cls.theme_style == "Dark":
            app_bg_color = (0.2, 0.2, 0.2, 1)
        else:
            app_bg_color = (0.95, 0.95, 0.95, 1)

        app_window = MDCard(
            radius=[0,0,20,20],
            md_bg_color=app_bg_color,
            size_hint=(None, None),
            size=icon_widget.size,
            pos=icon_widget.to_window(*icon_widget.pos),
            elevation=0,
            orientation='vertical'
        )
        app_window.add_widget(content)
        app_window.add_widget(WindowControls())
        
        self.root.get_screen('home').ids.float_layout.add_widget(app_window)
        self.current_app_window = app_window

        top_bar = self.root.get_screen('home').ids.top_bar
        target_pos = (0, 0)
        target_size = (Window.width, Window.height - top_bar.height)
        
        anim = Animation(pos=target_pos, size=target_size, duration=self.animation_speed, t='out_quad')
        anim.start(self.current_app_window)
        
        content_anim = Animation(opacity=1, duration=self.animation_speed / 2, d=self.animation_speed / 2)
        content_anim.start(content)
        
        self.add_app_to_dock(icon_widget)

    def _animate_close(self, window_to_close, icon_to_return_to):
        Animation.cancel_all(window_to_close)
        target_pos = icon_to_return_to.to_window(*icon_to_return_to.pos)
        target_size = icon_to_return_to.size

        # Clear the window's content and set a lighter background for the animation
        window_to_close.clear_widgets()
        window_to_close.radius = 20
        
        # Calculate a lighter version of the icon's color for the background
        original_color = icon_to_return_to.bg_color
        r, g, b, a = original_color
        lighten_factor = 0.7  # Mix 70% white into the original color
        lighter_color = (
            r + (1 - r) * lighten_factor,
            g + (1 - g) * lighten_factor,
            b + (1 - b) * lighten_factor,
            a
        )
        window_to_close.md_bg_color = lighter_color

        # Create a new icon to place inside the shrinking window
        closing_icon_container = MDFloatLayout()
        icon_card = IconCard(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={'center_x': .5, 'center_y': .5},
            md_bg_color=icon_to_return_to.bg_color,
            radius=20
        )
        icon_card.add_widget(MDIcon(
            icon=icon_to_return_to.icon,
            halign='center',
            valign='center',
            pos_hint={'center_x': .5, 'center_y': .5},
            font_size="30sp"
        ))
        closing_icon_container.add_widget(icon_card)
        window_to_close.add_widget(closing_icon_container)

        # Animate the window shrinking to the original icon's position and size
        anim = Animation(pos=target_pos, size=target_size, duration=self.animation_speed, t='in_quad')

        def on_close_complete(*args):
            if window_to_close.parent:
                window_to_close.parent.remove_widget(window_to_close)

        anim.bind(on_complete=on_close_complete)
        anim.start(window_to_close)
        
        self.remove_app_from_dock(icon_to_return_to)

    def close_app(self):
        if not self.current_app_window:
            return

        self._animate_close(self.current_app_window, self.opened_from_icon)
        self.current_app_window = None
        self.opened_from_icon = None

    def close_settings(self):
        self.root.current = 'home'
        self.open_app(self.opened_from_icon)

    def add_app_to_dock(self, icon_widget):
        if icon_widget.text in self.open_app_icons:
            return
        
        dock_icon = MDIconButton(
            icon=icon_widget.icon,
            on_release=lambda x: self.open_app(icon_widget),
            pos_hint={'center_y': .5}
        )
        self.root.get_screen('home').ids.top_bar_left.add_widget(dock_icon)
        self.open_app_icons[icon_widget.text] = dock_icon

    def remove_app_from_dock(self, icon_widget):
        if icon_widget.text in self.open_app_icons:
            dock_icon = self.open_app_icons.pop(icon_widget.text)
            self.root.get_screen('home').ids.top_bar_left.remove_widget(dock_icon)

    def show_about_dialog(self):
        dialog = MDDialog(title="About", text="dev: minhmc2007, Gemini AI")
        dialog.open()

    def show_animation_speed_dialog(self):
        speeds = ["0.2", "0.5", "1.0"]
        buttons = []
        dialog = MDDialog(
            title="Animation Speed",
            type="custom",
            content_cls=MDBoxLayout(orientation="vertical", adaptive_height=True, spacing="10dp"),
        )
        for speed in speeds:
            button = MDFlatButton(
                text=speed,
                on_release=lambda x, s=speed, d=dialog: self.set_animation_speed(s, d)
            )
            dialog.content_cls.add_widget(button)

        dialog.open()

    def show_wallpaper_dialog(self):
        if not self.wallpaper_dialog:
            # Use the system's file chooser
            file_chooser = FileChooserListView(
                path=os.path.expanduser("~"),  # Start in the user's home directory
                filters=[lambda folder, filename: not filename.startswith('.'),
                         lambda folder, filename: filename.lower().endswith(('.png', '.jpg', '.jpeg'))],
            )
            
            def set_and_dismiss(path):
                self.set_wallpaper(path)
                if self.wallpaper_dialog:
                    self.wallpaper_dialog.dismiss()

            content = MDBoxLayout(orientation='vertical', size_hint_y=None, height="500dp")
            content.add_widget(file_chooser)
            
            button_box = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing="10dp", padding="10dp")
            ok_button = MDRaisedButton(text="Select", on_release=lambda x: set_and_dismiss(file_chooser.selection and file_chooser.selection[0] or None))
            cancel_button = MDFlatButton(text="Cancel", on_release=lambda x: self.wallpaper_dialog.dismiss())
            button_box.add_widget(MDBoxLayout()) # Spacer
            button_box.add_widget(ok_button)
            button_box.add_widget(cancel_button)
            content.add_widget(button_box)

            self.wallpaper_dialog = MDDialog(
                title="Choose Wallpaper",
                type="custom",
                content_cls=content,
            )
            self.wallpaper_dialog.bind(on_dismiss=lambda *args: setattr(self, 'wallpaper_dialog', None))
        self.wallpaper_dialog.open()

    def set_wallpaper(self, path):
        if path and os.path.exists(path):
            self.wallpaper_path = path

    def set_animation_speed(self, speed, dialog):
        self.animation_speed = float(speed)
        dialog.dismiss()

    def toggle_theme(self, active):
        if active:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    OriginOSApp().run()
