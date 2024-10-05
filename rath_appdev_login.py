from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView
from kivy.core.window import Window

# Set window background color
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# Profile Selection Screen
class ProfileSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileSelectionScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Emergency Vehicle Clearance", font_size=32, bold=True, color=(0, 0, 0, 1)))

        # Profile selection section
        profile_section = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=20)

        # Emergency Vehicle Button
        self.vehicle_button = Button(text="Emergency Vehicle", font_size=18, bold=True, background_normal="", background_color=(0.2, 0.6, 1, 1))
        self.vehicle_button.bind(on_press=self.select_vehicle_profile)

        # Junction Button
        self.junction_button = Button(text="Junction", font_size=18, bold=True, background_normal="", background_color=(0.9, 0.3, 0.3, 1))
        self.junction_button.bind(on_press=self.select_junction_profile)

        profile_section.add_widget(self.vehicle_button)
        profile_section.add_widget(self.junction_button)
        self.layout.add_widget(profile_section)
        self.add_widget(self.layout)

    def select_vehicle_profile(self, instance):
        self.manager.get_screen('login').set_profile_type('vehicle')
        self.manager.current = 'login'

    def select_junction_profile(self, instance):
        self.manager.get_screen('login').set_profile_type('junction')
        self.manager.current = 'login'


# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 50], spacing=20)
        self.profile_type = None  # This will hold whether 'vehicle' or 'junction' was selected

        # Title
        self.title_label = Label(text="Login", font_size=32, bold=True, color=(0, 0, 0, 1))
        self.layout.add_widget(self.title_label)

        # Username/Email Field
        self.username_label = Label(text="Username", font_size=16, color=(0, 0, 0, 1))
        self.username_input = TextInput(multiline=False, background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.username_label)
        self.layout.add_widget(self.username_input)

        # Password Field
        self.password_label = Label(text="Password", font_size=16, color=(0, 0, 0, 1))
        self.password_input = TextInput(password=True, multiline=False, background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.password_label)
        self.layout.add_widget(self.password_input)

        # Login Button
        self.login_button = Button(text="Login", background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.login_button.bind(on_press=self.validate_login)
        self.layout.add_widget(self.login_button)

        # Back Button (to go back to Profile Selection)
        self.back_button = Button(text="Back", background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def set_profile_type(self, profile_type):
        self.profile_type = profile_type
        self.title_label.text = f"Login - {profile_type.capitalize()}"

    def validate_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Placeholder login validation logic (replace with actual logic)
        if username == "admin" and password == "admin123":
            if self.profile_type == 'vehicle':
                self.manager.current = 'emergency_vehicle_main'
            else:
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
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Emergency Vehicle Dashboard", font_size=28, bold=True, color=(0, 0, 0, 1)))

        # Emergency Button
        self.emergency_button = Button(text="Send Emergency Alert", size_hint=(1, 0.2), background_normal="", background_color=(1, 0, 0, 1), font_size=18, bold=True)
        self.emergency_button.bind(on_press=self.send_emergency_alert)
        self.layout.add_widget(self.emergency_button)

        # Profile Button
        self.profile_button = Button(text="Profile Information", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.profile_button.bind(on_press=self.show_profile_info)
        self.layout.add_widget(self.profile_button)

        self.add_widget(self.layout)

    def send_emergency_alert(self, instance):
        self.manager.current = 'alert_confirmation'

    def show_profile_info(self, instance):
        self.manager.current = 'vehicle_info'


# Alert Confirmation Screen
class AlertConfirmationScreen(Screen):
    def __init__(self, **kwargs):
        super(AlertConfirmationScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Emergency Alert Sent", font_size=28, bold=True, color=(0, 0, 0, 1)))

        # Confirmation message
        self.layout.add_widget(Label(text="Your emergency alert has been sent to nearby traffic signals.", font_size=18, color=(0, 0, 0, 1)))

        # Back to Main Page Button
        self.back_button = Button(text="Back to Dashboard", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = 'emergency_vehicle_main'


# Vehicle Information Screen (Editable Fields)
class VehicleInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(VehicleInfoScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Vehicle Information", font_size=28, bold=True, color=(0, 0, 0, 1)))

        self.layout.add_widget(Label(text="Vehicle Type:", font_size=18, color=(0, 0, 0, 1)))
        self.vehicle_type_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.vehicle_type_input)

        self.layout.add_widget(Label(text="License Plate Number:", font_size=18, color=(0, 0, 0, 1)))
        self.license_plate_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.license_plate_input)

        self.layout.add_widget(Label(text="Driver Name:", font_size=18, color=(0, 0, 0, 1)))
        self.driver_name_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.driver_name_input)
        # Back to Main Page Button
        self.back_button = Button(text="Back to Dashboard", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = 'emergency_vehicle_main'


# Junction Main Page
class JunctionMainPage(Screen):
    def __init__(self, **kwargs):
        super(JunctionMainPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Junction Dashboard", font_size=28, bold=True, color=(0, 0, 0, 1)))

        # Map View
        self.mapview = MapView(zoom=15, lat=12.9716, lon=77.5946)
        self.layout.add_widget(self.mapview)

        # Vehicle Information Section
        self.vehicle_info = Label(text="Vehicle Type: Ambulance\nLicense Plate: XYZ 1234\nETA: 3 mins", font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.3))
        self.layout.add_widget(self.vehicle_info)

        # List of Vehicles Button
        self.list_vehicles_button = Button(text="List of Vehicles", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.list_vehicles_button.bind(on_press=self.show_vehicle_list)
        self.layout.add_widget(self.list_vehicles_button)

        # Profile Button
        self.profile_button = Button(text="Junction Information", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.profile_button.bind(on_press=self.show_junction_info)
        self.layout.add_widget(self.profile_button)

        self.add_widget(self.layout)

    def show_vehicle_list(self, instance):
        self.manager.current = 'vehicle_list'

    def show_junction_info(self, instance):
        self.manager.current = 'junction_info'


# Junction Information Screen (Editable Fields)
class JunctionInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(JunctionInfoScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="Junction Information", font_size=28, bold=True, color=(0, 0, 0, 1)))

        # Junction Information Fields
        self.layout.add_widget(Label(text="Junction ID:", font_size=18, color=(0, 0, 0, 1)))
        self.junction_id_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.junction_id_input)

        self.layout.add_widget(Label(text="Location:", font_size=18, color=(0, 0, 0, 1)))
        self.location_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.location_input)

        self.layout.add_widget(Label(text="Junction Name:", font_size=18, color=(0, 0, 0, 1)))
        self.junction_name_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.junction_name_input)

        self.layout.add_widget(Label(text="Junction Incharge:", font_size=18, color=(0, 0, 0, 1)))
        self.junction_incharge_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.junction_incharge_input)

        self.layout.add_widget(Label(text="Police Control Unit No:", font_size=18, color=(0, 0, 0, 1)))
        self.police_unit_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.police_unit_input)

        self.layout.add_widget(Label(text="Nearby Landmarks:", font_size=18, color=(0, 0, 0, 1)))
        self.landmarks_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.landmarks_input)

        self.layout.add_widget(Label(text="Connected Junctions:", font_size=18, color=(0, 0, 0, 1)))
        self.connected_junctions_input = TextInput(multiline=False, size_hint=(1, 1), background_color=(1, 1, 1, 1), padding=[10, 10, 10, 10])
        self.layout.add_widget(self.connected_junctions_input)

        # Back to Junction Main Page Button
        self.back_button = Button(text="Back to Junction Dashboard", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = 'junction_main'


# Vehicle List Screen (Placeholder)
class VehicleListScreen(Screen):
    def __init__(self, **kwargs):
        super(VehicleListScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=20)

        # Title
        self.layout.add_widget(Label(text="List of Vehicles", font_size=28, bold=True, color=(0, 0, 0, 1)))

        # Placeholder Vehicle List
        self.layout.add_widget(Label(text="1. Ambulance XYZ 1234\n2. Ambulance ABC 5678\n3. Ambulance DEF 9012", font_size=18, color=(0, 0, 0, 1)))

        # Back to Junction Main Page Button
        self.back_button = Button(text="Back to Junction Dashboard", size_hint=(1, 0.2), background_normal="", background_color=(0.1, 0.7, 0.3, 1), font_size=18, bold=True)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = 'junction_main'


# Main App
class EmergencyVehicleApp(App):
    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()

        # Add ProfileSelectionScreen, LoginScreen, and Main Pages
        sm.add_widget(ProfileSelectionScreen(name='profile_selection'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(EmergencyVehicleMainPage(name='emergency_vehicle_main'))
        sm.add_widget(AlertConfirmationScreen(name='alert_confirmation'))
        sm.add_widget(VehicleInfoScreen(name='vehicle_info'))
        sm.add_widget(JunctionMainPage(name='junction_main'))
        sm.add_widget(VehicleListScreen(name='vehicle_list'))
        sm.add_widget(JunctionInfoScreen(name='junction_info'))
        return sm

if __name__ == "__main__":
    EmergencyVehicleApp().run()
