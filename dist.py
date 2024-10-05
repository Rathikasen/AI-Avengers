from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from plyer import gps
from geopy.distance import geodesic
import platform

class GPSApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="GPS Status: Waiting for location...")
        self.start_button = Button(text="Start GPS")
        self.start_button.bind(on_press=self.start_gps)
        
        layout.add_widget(self.label)
        layout.add_widget(self.start_button)
        return layout

    def start_gps(self, instance):
        if platform.system() == "Linux" or platform.system() == "Android":
            try:
                gps.configure(on_location=self.on_gps_location)
                gps.start()
                self.label.text = "GPS started. Waiting for location..."
            except NotImplementedError:
                self.label.text = "GPS not supported."
        else:
            # For non-mobile platforms (Windows/Mac), simulate GPS coordinates
            self.label.text = "Simulating GPS for desktop..."
            self.on_gps_location(lat=12.9715987, lon=77.594566)  # Example coordinates

    def on_gps_location(self, **kwargs):
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        self.label.text = f"Current location: {latitude}, {longitude}"
        
        # Replace with actual second device's coordinates
        second_device_coords = (12.9715987, 77.594566)  # Example coords (latitude, longitude)
        current_coords = (latitude, longitude)
        
        # Calculate distance
        distance = geodesic(current_coords, second_device_coords).meters
        if distance <= 200:
            self.label.text += "\nYou are within 200 meters of the second device!"
        else:
            self.label.text += f"\nDistance from second device: {distance:.2f} meters"

if __name__ == '__main__':
    GPSApp().run()
