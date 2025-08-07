import time
import threading
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.button import Button
from kivy.clock import Clock
from datetime import datetime
from car.full_self_driving import FullSelfDriving
from car.car_config import MINIMUM_GAP

Window.size = (1000, 700)
Window.clearcolor = get_color_from_hex("#1c232c")


class CurvedBox(FloatLayout):  # Inherit from FloatLayout
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.152, 0.192, 0.223, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class VerticalLineWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0)  # Black line
            self.line = Line(points=[], width=2)

        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        x = self.center_x
        y1 = self.y
        y2 = self.top
        self.line.points = [x, y1, x, y2]


class UserInterface(App):
    def build(self):
        self.title = 'Self-Driving Car UI'

        # Default values
        
        self.function = 'Not Assigned'
        self.angle = '0°'
        self.speed = '0  km/h'
        self.distance_front = '0 m'
        self.distance_edge_r = '0 m'
        self.distance_edge_l = '0 m'
        self.distance_back = '0 m'

        layout = FloatLayout()

        # Left top box
        box1 = CurvedBox(
            size_hint=(None, None),
            size=(500, 350),
            pos_hint={'x': 0.01, 'top': 0.99}
        )

        # Left bottom box
        box2 = CurvedBox(
            size_hint=(None, None),
            size=(500, 325),
            pos_hint={'x': 0.01, 'top': 0.47}
        )

        # Vertical line divider
        line = VerticalLineWidget(
            size_hint=(None, None),
            size=(2, 800),
            pos_hint={'x': 0.54, 'center_y': 0.5}
        )

        # Top right title label
        label1 = Label(
            text='Smart Log System',
            font_size='25sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0.67, 'top': 0.95}
        )

        # Sensor data label on the right side
        label2 = Label(
            text=f"""
            Function: {self.function}
            Angle: {self.angle}
            Speed: {self.speed}

            Distance Front: {self.distance_front}
            Distance Edge,
            R: {self.distance_edge_r}
            L: {self.distance_edge_l}

            Distance Back: {self.distance_back}
            """,
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='top',
            size_hint=(None, None),
            size=(400, 300),
            pos_hint={'x': 0.425, 'top': 0.915}
        )

        # Title inside box1
        label_in_box = Label(
            text='Full Self Driving',
            font_size='25sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.15, 'top': 0.95}
        )
        label2_in_box = Label(
            text=f'[b]{self.speed}[/b]',
            font_size='100sp',
            markup=True,  # Enables bold tags
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.15, 'top': 0.65}
        )
        label3_in_box = Label(
            text=f'Heading Direction: {self.angle}',
            font_size='25sp',
            markup=True,  # Enables bold tags
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.19, 'top': 0.35}
        )
        self.clock_label = Label(
            text="--:--:--",
            font_size='50sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'x': 0.315, 'top': 0.2}
        )
        

        self.button = Button(
            text='Start FSD',
            markup=True,
            font_size='20sp',
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'x': 0.67, 'top': 0.1},
            # from #00CFFF,  # Optional color
            background_color=(0.0, 0.711, 1.0, 1.0),
            color=(1, 1, 1, 1)  # Text color
        )


        # Add widgets
        self.button.bind(on_press=self.on_start_button_press)
        box2.add_widget(self.clock_label)
        box1.add_widget(label_in_box)
        box1.add_widget(label2_in_box)
        box1.add_widget(label3_in_box)
        layout.add_widget(box1)
        layout.add_widget(box2)
        layout.add_widget(line)
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(self.button)
        Clock.schedule_interval(self.update_clock, 1)  # every 1 second

        return layout

    def on_start_button_press(self, instance):
        if self.button.text == 'Start FSD':
            self.button.text = 'Stop FSD'

            # Start FSD system in a new thread
            self.fsd_thread = threading.Thread(target=self.start_fsd, daemon=True)
            self.fsd_thread.start()
            print("FSD Started")

        else:
            self.button.text = 'Start FSD'
            self.auto_driver.stop_loop()
            self.auto_driver.cleanup()
            self.auto_driver = None
            print("FSD Stopped")
            
    def start_fsd(self):
        try:
            self.auto_driver = FullSelfDriving()
            self.auto_driver.drive(MINIMUM_GAP)
        except KeyboardInterrupt:
            self.auto_driver.stop_loop()
            self.auto_driver.cleanup()
            self.auto_driver = None


        # You can also stop the FSD system here

        
    def update_clock(self, dt):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")  # or "%I:%M:%S %p" for AM/PM
        self.clock_label.text = current_time


UserInterface().run()
