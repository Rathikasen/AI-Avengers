from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from plyer import gps
import platform
import cv2
import subprocess
from openvino.runtime import Core
# Set window background color
Window.clearcolor = (0.95, 0.95, 0.95, 1)
class OpenVINOModel:
    def __init__(self, model_path, weights_path):
        self.ie = Core()
        self.model = self.ie.read_model(model=model_path)
        self.compiled_model = self.ie.compile_model(self.model, "CPU")
        self.input_blob = self.model.input(0)
        self.output_blob = self.model.output(0)

    def predict(self, image):
        input_shape = self.input_blob.shape
        n, c, h, w = input_shape

        image_resized = cv2.resize(image, (w, h))
        image_resized = image_resized.transpose((2, 0, 1))
        image_resized = image_resized.reshape((n, c, h, w))

        result = self.compiled_model([image_resized])
        return result[self.output_blob]

# Base Layout Class for Consistency
class BaseLayout(BoxLayout):
    def __init__(self, title, **kwargs):
        super(BaseLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 20

        # Title Label
        self.add_widget(Label(text=title, font_size=28, bold=True, color=(0, 0, 0, 1)))

# Profile Selection Screen
class ProfileSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileSelectionScreen, self).__init__(**kwargs)
        layout = BaseLayout(title="Emergency Vehicle Clearance")

        # Profile selection buttons
        profile_section = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=20)
        self.vehicle_button = Button(text="Emergency Vehicle", font_size=18, bold=True, background_normal="", background_color=(0.2, 0.6, 1, 1))
        self.junction_button = Button(text="Junction", font_size=18, bold=True, background_normal="", background_color=(0.9, 0.3, 0.3, 1))

        self.vehicle_button.bind(on_press=self.select_vehicle_profile)
        self.junction_button.bind(on_press=self.select_junction_profile)

        profile_section.add_widget(self.vehicle_button)
        profile_section.add_widget(self.junction_button)
        layout.add_widget(profile_section)

        self.add_widget(layout)

    def select_vehicle_profile(self, instance):
        self.manager.get_screen('vehicle_login').set_profile_type('vehicle')
        self.manager.current = 'vehicle_login'

    def select_junction_profile(self, instance):
        self.manager.get_screen('junction_login').set_profile_type('junction')
        self.manager.current = 'junction_login'

# Vehicle Login Screen
class VehicleLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(VehicleLoginScreen, self).__init__(**kwargs)
        layout = BaseLayout(title="Vehicle Login")
        self.profile_type = None

        # Username and Password Fields
        self.username_input = TextInput(hint_text="Username", multiline=False, background_color=(1, 1, 1, 1))
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, background_color=(1, 1, 1, 1))

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        # Login and Back Buttons
        self.login_button = Button(text="Login", background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button = Button(text="Back", background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)

        self.login_button.bind(on_press=self.validate_login)
        self.back_button.bind(on_press=self.go_back)

        layout.add_widget(self.login_button)
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def set_profile_type(self, profile_type):
        self.profile_type = profile_type

    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == "vehicle" and password == "vehicle123":
            self.manager.current = 'vehicle_info'
        else:
            self.login_failed()

    def login_failed(self):
        popup = Popup(title="Login Failed", content=Label(text="Invalid username or password!"), size_hint=(0.6, 0.4))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'profile_selection'

# Junction Login Screen
class JunctionLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(JunctionLoginScreen, self).__init__(**kwargs)
        layout = BaseLayout(title="Junction Login")
        self.profile_type = None

        # Username and Password Fields
        self.username_input = TextInput(hint_text="Username", multiline=False, background_color=(1, 1, 1, 1))
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, background_color=(1, 1, 1, 1))

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        # Login and Back Buttons
        self.login_button = Button(text="Login", background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button = Button(text="Back", background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)

        self.login_button.bind(on_press=self.validate_login)
        self.back_button.bind(on_press=self.go_back)

        layout.add_widget(self.login_button)
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def set_profile_type(self, profile_type):
        self.profile_type = profile_type

    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == "junction" and password == "junction123":
            self.manager.current = 'junction_main'
        else:
            self.login_failed()

    def login_failed(self):
        popup = Popup(title="Login Failed", content=Label(text="Invalid username or password!"), size_hint=(0.6, 0.4))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'profile_selection'

# Emergency Vehicle Main Page
class EmergencyVehicleMainPage(Screen):
    def __init__(self, **kwargs):
        super(EmergencyVehicleMainPage, self).__init__(**kwargs)
        layout = BaseLayout(title="Emergency Vehicle Dashboard")

        # Emergency and Profile Buttons
        self.emergency_button = Button(text="Send Emergency Alert", size_hint=(1, 0.15), background_normal="", background_color=(1, 0, 0, 1), font_size=18, bold=True)
        self.emergency_off_button = Button(text="Emergency Off", size_hint=(1, 0.15), background_normal="", background_color=(0, 1, 0, 1), font_size=18, bold=True)
        self.profile_button = Button(text="Profile Information", size_hint=(1, 0.15), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)

        self.emergency_button.bind(on_press=self.send_emergency_alert)
        self.emergency_off_button.bind(on_press=self.send_emergency_off_alert)
        self.profile_button.bind(on_press=self.show_profile_info)

        layout.add_widget(self.emergency_button)
        layout.add_widget(self.emergency_off_button)
        layout.add_widget(self.profile_button)

        # GPS Tracking Display
        self.gps_label = Label(text="Current Location: (Lat: 12, Lon: 17)", font_size=16, color=(0, 0, 0, 1))
        layout.add_widget(self.gps_label)

        # Profile Info Display
        self.profile_info_label = Label(text="Profile Info: None", font_size=16, color=(0, 0, 0, 1))
        layout.add_widget(self.profile_info_label)

        # Back Button
        self.back_button = Button(text="Back to Profile Selection", size_hint=(1, 0.15), background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

        # Start GPS tracking only for supported platforms
        self.start_gps()

    def start_gps(self):
        if platform.system() == 'Android':
            gps.configure(on_location=self.update_gps_label)
            gps.start()

    def update_gps_label(self, location):
        self.gps_label.text = f"Current Location: (Lat: {location['latitude']}, Lon: {location['longitude']})"

    def send_emergency_alert(self, instance):
        # Logic to send emergency alert to traffic control
        print("Emergency alert sent!")

    def send_emergency_off_alert(self, instance):
        # Logic to inform traffic control that the emergency is off
        print("Emergency off alert sent!")

    def show_profile_info(self, instance):
        # Logic to show the vehicle's profile information
        self.profile_info_label.text = "Profile Info: Vehicle ID: XYZ123, Status: Active"

    def go_back(self, instance):
        self.manager.current = 'profile_selection'

# Junction Main Page
import subprocess

class JunctionMainPage(Screen):
    def __init__(self, **kwargs):
        super(JunctionMainPage, self).__init__(**kwargs)
        layout = BaseLayout(title="Junction Control Dashboard")

        # Start and Stop Buttons
        self.start_button = Button(text="Start Monitoring", size_hint=(1, 0.15), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.stop_button = Button(text="Stop Monitoring", size_hint=(1, 0.15), background_normal="", background_color=(1, 0, 0, 1), font_size=18, bold=True)

        self.start_button.bind(on_press=self.start_monitoring)
        self.stop_button.bind(on_press=self.stop_monitoring)

        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)

        # Back Button
        self.back_button = Button(text="Back to Profile Selection", size_hint=(1, 0.15), background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

        # Initialize the subprocess variable
        self.monitoring_process = None

    def start_monitoring(self, instance):
        # Logic to run the junc.py script
        if self.monitoring_process is None:
            self.monitoring_process = subprocess.Popen(["python", "junc.py"])  # Adjust the command if necessary based on your setup
            print("Monitoring started!")
                # Back Button
        

    def stop_monitoring(self, instance):
        # Logic to stop monitoring vehicles
        if self.monitoring_process is not None:
            self.monitoring_process.terminate()  # Terminate the subprocess
            self.monitoring_process = None  # Reset the process reference
            print("Monitoring stopped!")

    def go_back(self, instance):
        self.manager.current = 'profile_selection'
class TrafficControlApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ProfileSelectionScreen(name='profile_selection'))
        sm.add_widget(VehicleLoginScreen(name='vehicle_login'))
        sm.add_widget(JunctionLoginScreen(name='junction_login'))
        sm.add_widget(EmergencyVehicleMainPage(name='vehicle_info'))
        sm.add_widget(JunctionMainPage(name='junction_main'))
        return sm

if __name__ == '__main__':
    TrafficControlApp().run()
