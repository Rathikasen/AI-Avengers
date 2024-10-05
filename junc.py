from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock  # For scheduling signal switching
import cv2
import math
import numpy as np
class VehicleDetector:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.net = cv2.dnn.readNet(r"D:\COLLEGE VIT\Projects\AI traffic\project\yolov3.weights", r"D:\COLLEGE VIT\Projects\AI traffic\project\yolov3.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        with open(r"D:\COLLEGE VIT\Projects\AI traffic\project\coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def count_vehicles(self):
        lane_counts = [0] * len(self.video_paths)  # Initialize counts for each lane
        for i, video_path in enumerate(self.video_paths):
            cap = cv2.VideoCapture(video_path)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                height, width, _ = frame.shape
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                self.net.setInput(blob)
                outs = self.net.forward(self.output_layers)

                boxes, confidences, class_ids = [], [], []
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > 0.5:  # Confidence threshold
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)
                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                # Apply Non-Maximum Suppression (NMS) to avoid multiple detections of the same object
                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                if len(indices) > 0:
                    for index in indices:
                        idx = index
                        box = boxes[idx]
                        x, y, w, h = box
                        label = str(self.classes[class_ids[idx]])
                        if label in ["car", "truck", "bus"]:  # Count vehicles
                            lane_counts[i] += 1
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Display the vehicle count for the lane
                cv2.putText(frame, f'Lane {i + 1} Count: {lane_counts[i]//10}', (10, 50 + i * 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                cv2.imshow(f'Lane {i + 1}', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
        cv2.destroyAllWindows()
        return lane_counts

# VehicleDetectionScreen with dynamic vehicle count display and signal switching
class VehicleDetectionScreen(Screen):
    def __init__(self, **kwargs):
        super(VehicleDetectionScreen, self).__init__(**kwargs)
        
        # Create layout only once
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Vehicle Detection Screen')
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

        # Start vehicle detection process
        self.vehicle_detector = VehicleDetector([
            r"D:\COLLEGE VIT\Competitions\Coimbatore Hackathon\Vid1.mp4",
            r"D:\COLLEGE VIT\Competitions\Coimbatore Hackathon\Vid2.mp4",
            r"D:\COLLEGE VIT\Competitions\Coimbatore Hackathon\Vid3.mp4",
            r"D:\COLLEGE VIT\Competitions\Coimbatore Hackathon\Vid4.mp4"
        ])
        self.counts = self.vehicle_detector.count_vehicles()
        # Dynamically update layout
        self.update_vehicle_count_display()

        # Initialize signal states and current lane index
        self.current_lane = 0
        self.lane_signals = ["Red"] * len(self.counts)
        self.lane_signals[self.current_lane] = "Green"  # First lane starts with green

        # Start switching signals based on time allocations
        self.switch_signals()
    #     self.back_button = Button(text="Back to Profile Selection", size_hint=(1, 0.15), background_normal="", background_color=(0.6, 0.6, 0.6, 1), font_size=18, bold=True)
    #     self.back_button.bind(on_press=self.go_back)
    #     self.layout.add_widget(self.back_button)
    # def go_back(self, instance):
    #     self.manager.current = "Junction Control Dashboard"


    def update_vehicle_count_display(self):
        # Clear previous counts if needed
        for child in list(self.layout.children):
            if isinstance(child, Label) and 'vehicles' in child.text:
                self.layout.remove_widget(child)

        # Calculate total and average count
        total_count = sum(self.counts)
        avg_count = total_count / len(self.counts) if total_count > 0 else 0

        total_cycle_time = 10  # example time
        self.time_allocations = [(count / total_count) * total_cycle_time if total_count > 0 else total_cycle_time / len(self.counts) for count in self.counts]

        # Add new labels to display vehicle counts and time allocation
        for i, lane_count in enumerate(self.counts):
            self.layout.add_widget(Label(text=f"Lane {i + 1}: {lane_count//10} vehicles, Time allocated: {math.ceil(self.time_allocations[i])} seconds"))

        # Display average vehicle count
        self.layout.add_widget(Label(text=f"Average vehicle count: {avg_count:.2f}"))

    def switch_signals(self, dt=None):
        # Set the current lane signal to red and switch to the next lane
        self.lane_signals[self.current_lane] = "Red"
        self.current_lane = (self.current_lane + 1) % len(self.counts)
        self.lane_signals[self.current_lane] = "Green"

        # Update the display to show the signal states
        self.update_signal_display()

        # Schedule the next signal switch
        Clock.schedule_once(self.switch_signals, math.ceil(self.time_allocations[self.current_lane]))

    def update_signal_display(self):
        # Clear previous signal displays
        for child in list(self.layout.children):
            if isinstance(child, Label) and 'Signal' in child.text:
                self.layout.remove_widget(child)

        # Display the current signal states for each lane
        for i, signal in enumerate(self.lane_signals):
            self.layout.add_widget(Label(text=f"Lane {i + 1} Signal: {signal}"))

        # Log signal states
        print("Lane Signals:", self.lane_signals)

# Define different screens
# class LoginScreen(Screen):
#     def __init__(self, **kwargs):
#         super(LoginScreen, self).__init__(**kwargs)
#         layout = BoxLayout(orientation='vertical')
#         self.username_input = TextInput(hint_text='Username')
#         self.password_input = TextInput(hint_text='Password', password=True)
#         login_button = Button(text='Login')
#         login_button.bind(on_press=self.login)
#         layout.add_widget(self.username_input)
#         layout.add_widget(self.password_input)
#         layout.add_widget(login_button)
#         self.add_widget(layout)

#     def login(self, instance):
#         username = self.username_input.text
#         password = self.password_input.text

#         if username == 'junction' and password == 'password1':
#             self.manager.current = 'vehicle_detection'
#         elif username == 'emergency' and password == 'password2':
#             self.manager.current = 'dummy_screen'
#         else:
#             print("Invalid login")

# class DummyScreen(Screen):
#     def __init__(self, **kwargs):
#         super(DummyScreen, self).__init__(**kwargs)
#         layout = BoxLayout(orientation='vertical')
#         layout.add_widget(Label(text='Dummy Screen for Junctions'))
#         layout.add_widget(Button(text='Back to Login', on_press=self.back_to_login))
#         self.add_widget(layout)

#     def back_to_login(self, instance):
#         self.manager.current = 'login'

# App and Screen Management
class VehicleApp(App):
    def build(self):
        sm = ScreenManager()
        #sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(VehicleDetectionScreen(name='vehicle_detection'))
        #qsm.add_widget(DummyScreen(name='dummy_screen'))
        return sm

# Run the app
if __name__ == '__main__':
    VehicleApp().run()
