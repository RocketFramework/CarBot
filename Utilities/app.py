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
from FSD.Full_Self_Driving import FullSelfDriving
from LOG.Logger import Logger

Window.size = (1000, 700)
Window.clearcolor = get_color_from_hex("#1c232c")


class CurvedBox(FloatLayout):
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
            Color(0, 0, 0)
            self.line = Line(points=[], width=2)

        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        x = self.center_x
        y1 = self.y
        y2 = self.top
        self.line.points = [x, y1, x, y2]


class UserInterface(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fsd = None
        self.fsd_thread = None
        self.fsd_running = False
        self.logger = Logger()
        
        # Data storage for UI updates
        self.ui_data = {
            'function': 'Not Assigned',
            'angle': '0°',
            'speed': '0 m/s',
            'distance_front': '0 m',
            'distance_edge_r': '0 m', 
            'distance_edge_l': '0 m',
            'distance_back': '0 m'
        }

    def build(self):
        self.title = 'Self-Driving Car UI'

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
        self.sensor_label = Label(
            text=self.get_sensor_text(),
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='top',
            size_hint=(None, None),
            size=(400, 300),
            pos_hint={'x': 0.425, 'top': 0.915}
        )

        # Title inside box1
        self.label_in_box = Label(
            text='Full Self Driving',
            font_size='25sp',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.15, 'top': 0.95}
        )
        
        self.speed_label = Label(
            text=f'[b]{self.ui_data["speed"]}[/b]',
            font_size='100sp',
            markup=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'x': 0.15, 'top': 0.65}
        )
        
        self.heading_label = Label(
            text=f'Heading Direction: {self.ui_data["angle"]}',
            font_size='25sp',
            markup=True,
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
            background_color=(0.0, 0.711, 1.0, 1.0),
            color=(1, 1, 1, 1)
        )

        # Add widgets
        self.button.bind(on_press=self.on_start_button_press)
        box2.add_widget(self.clock_label)
        box1.add_widget(self.label_in_box)
        box1.add_widget(self.speed_label)
        box1.add_widget(self.heading_label)
        layout.add_widget(box1)
        layout.add_widget(box2)
        layout.add_widget(line)
        layout.add_widget(label1)
        layout.add_widget(self.sensor_label)
        layout.add_widget(self.button)
        
        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_interval(self.update_ui, 0.1)  # Faster update for real-time data
        return layout

    def get_sensor_text(self):
        return f"""
        Function: {self.ui_data['function']}
        Angle: {self.ui_data['angle']}
        Speed: {self.ui_data['speed']}

        Distance Front: {self.ui_data['distance_front']}
        Distance Edge:
            R: {self.ui_data['distance_edge_r']}
            L: {self.ui_data['distance_edge_l']}

        Distance Back: {self.ui_data['distance_back']}
        """

    def update_fsd_data(self):
        """Update UI data from FSD system"""
        if self.fsd_running and self.fsd:
            try:
                # Update function status from logger (which should be updated by FSD)
                self.ui_data['function'] = self.logger.function
                
                # Try to get distance data from FSD if available
                try:
                    self.ui_data['distance_front'] = f"{getattr(self.fsd, 'front_distance', 0):.2f} m"
                    self.ui_data['distance_edge_r'] = f"{getattr(self.fsd, 'right_distance', 0):.2f} m"
                    self.ui_data['distance_edge_l'] = f"{getattr(self.fsd, 'left_distance', 0):.2f} m"
                    self.ui_data['distance_back'] = f"{getattr(self.fsd, 'rear_distance', 0):.2f} m"
                except:
                    # If FSD doesn't have distance data, use defaults
                    self.ui_data['distance_front'] = "0.00 m"
                    self.ui_data['distance_edge_r'] = "0.00 m"
                    self.ui_data['distance_edge_l'] = "0.00 m"
                    self.ui_data['distance_back'] = "0.00 m"
                
            except Exception as e:
                print(f"Error updating FSD data: {e}")

    def update_from_logger(self):
        """Update data from logger - this is our main data source"""
        try:
            # Use the property getters, not the private variables
            self.ui_data['speed'] = f"{self.logger.speed:.1f} m/s"  # Use the property with formatting
            self.ui_data['angle'] = f"{self.logger.angle}°"        # Use the property
            self.ui_data['function'] = self.logger.function         # Use the property
                
        except Exception as e:
            print(f"Error updating from logger: {e}")
            # Fallback values
            self.ui_data['speed'] = "0.0 m/s"
            self.ui_data['angle'] = "0°"
            self.ui_data['function'] = "Error"

    def update_ui(self, dt):
        """Update the UI with current data"""
        try:
            # Always update from logger (main data source)
            self.update_from_logger()
            
            # If FSD is running, update additional FSD data
            if self.fsd_running:
                self.update_fsd_data()
            
            # Update UI elements with current data
            self.speed_label.text = f'[b]{self.ui_data["speed"]}[/b]'
            self.heading_label.text = f'Heading: {self.ui_data["angle"]}'
            self.sensor_label.text = self.get_sensor_text()
            
            # Debug: Print current values to console
            print(f"Speed: {self.ui_data['speed']}, Angle: {self.ui_data['angle']}, Function: {self.ui_data['function']}")
            
        except Exception as e:
            print(f"Error updating UI: {e}")

    def on_start_button_press(self, instance):
        if self.button.text == 'Start FSD':
            self.start_fsd_system()
        else:
            self.stop_fsd_system()

    def start_fsd_system(self):
        """Start the FSD system"""
        try:
            self.button.text = 'Stop FSD'
            self.fsd_running = True
            
            # Create and start FSD instance
            self.fsd = FullSelfDriving()
            self.fsd_thread = threading.Thread(target=self.run_fsd, daemon=True)
            self.fsd_thread.start()
            
            print("FSD Started")
            
        except Exception as e:
            print(f"Error starting FSD: {e}")
            self.button.text = 'Start FSD'
            self.fsd_running = False

    def run_fsd(self):
        """Wrapper to run FSD and handle updates"""
        try:
            if self.fsd:
                self.fsd.drive()
        except Exception as e:
            print(f"Error in FSD thread: {e}")
        finally:
            # If we get here, FSD has stopped
            self.fsd_running = False
            # Schedule UI update on main thread
            Clock.schedule_once(lambda dt: setattr(self.button, 'text', 'Start FSD'))
            self.update_from_logger()

    def stop_fsd_system(self):
        """Stop the FSD system"""
        try:
            self.button.text = 'Start FSD'
            self.fsd_running = False
            
            if self.fsd:
                self.fsd.stop()
                if hasattr(self.fsd, 'cleanup'):
                    self.fsd.cleanup()
                self.fsd = None
            
            print("FSD Stopped")
            
        except Exception as e:
            print(f"Error stopping FSD: {e}")

    def update_clock(self, dt):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.clock_label.text = current_time

    def on_stop(self):
        """Clean up when app is closed"""
        if self.fsd_running:
            self.stop_fsd_system()


def run():
    UserInterface().run()