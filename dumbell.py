import sys
import cv2
import mediapipe as mp
import math
import pyttsx3
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DumbbellTrackerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.capture = None
        self.is_recording = False
        self.video_writer = None
        self.output_directory = "C:\\Users\\dell\\OneDrive\\Desktop\\RESEARCH\\Project"
        os.makedirs(self.output_directory, exist_ok=True)
        self.trajectory_points = []

        # MediaPipe Pose initialization
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

    def initUI(self):
        self.setWindowTitle("Dumbbell Movement Tracker")
        self.setGeometry(100, 100, 1000, 600)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        self.start_btn = QPushButton("Start Live Feed", self)
        self.start_btn.clicked.connect(self.start_video)

        self.record_btn = QPushButton("Start Recording", self)
        self.record_btn.clicked.connect(self.toggle_recording)

        self.upload_btn = QPushButton("Upload Video", self)
        self.upload_btn.clicked.connect(self.upload_video)

        self.analyze_btn = QPushButton("Analyze Movement", self)
        self.analyze_btn.clicked.connect(self.analyze_movement)

        self.stop_btn = QPushButton("Stop Recording", self)
        self.stop_btn.clicked.connect(self.stop_recording)

        self.figure, self.ax = plt.subplots()  # Initialize figure and axis for plotting
        self.canvas = FigureCanvas(self.figure)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.record_btn)
        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.analyze_btn)
        button_layout.addWidget(self.stop_btn)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_video(self):
        self.capture = cv2.VideoCapture(0)
        self.timer.start(30)

    def calculate_angle(self, a, b, c):
        """Calculate the angle between three points: a, b, and c."""
        # Vector AB and BC
        ab = (a[0] - b[0], a[1] - b[1])
        bc = (c[0] - b[0], c[1] - b[1])

        # Dot product of AB and BC
        dot_product = ab[0] * bc[0] + ab[1] * bc[1]

        # Magnitudes of vectors AB and BC
        magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
        magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

        # Calculate angle in radians
        angle = math.acos(dot_product / (magnitude_ab * magnitude_bc))
        return math.degrees(angle)  # Return angle in degrees

    def preprocess_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return blurred

    def update_frame(self):
        if self.capture is not None and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Convert BGR frame to RGB for MediaPipe processing
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(rgb_frame)

                if results.pose_landmarks:
                    self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                    # Accessing key body parts (shoulders, elbows, wrists)
                    left_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    left_elbow = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
                    right_elbow = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
                    left_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

                    # Convert 3D coordinates to 2D
                    h, w, c = frame.shape
                    left_shoulder_coords = int(left_shoulder.x * w), int(left_shoulder.y * h)
                    right_shoulder_coords = int(right_shoulder.x * w), int(right_shoulder.y * h)
                    left_elbow_coords = int(left_elbow.x * w), int(left_elbow.y * h)
                    right_elbow_coords = int(right_elbow.x * w), int(right_elbow.y * h)
                    left_wrist_coords = int(left_wrist.x * w), int(left_wrist.y * h)
                    right_wrist_coords = int(right_wrist.x * w), int(right_wrist.y * h)

                    # Calculate angles for feedback (e.g., left elbow)
                    angle = self.calculate_angle(left_shoulder_coords, left_elbow_coords, left_wrist_coords)
                    if angle < 40:
                        feedback = "Extend your arm more!"
                        self.engine.say(feedback)
                        self.engine.runAndWait()

                    # Draw points and lines between key body parts
                    cv2.circle(frame, left_shoulder_coords, 5, (255, 0, 0), -1)
                    cv2.circle(frame, right_shoulder_coords, 5, (255, 0, 0), -1)
                    cv2.circle(frame, left_elbow_coords, 5, (255, 0, 0), -1)
                    cv2.circle(frame, right_elbow_coords, 5, (255, 0, 0), -1)
                    cv2.circle(frame, left_wrist_coords, 5, (255, 0, 0), -1)
                    cv2.circle(frame, right_wrist_coords, 5, (255, 0, 0), -1)
                    cv2.line(frame, left_shoulder_coords, left_elbow_coords, (255, 255, 0), 2)
                    cv2.line(frame, right_shoulder_coords, right_elbow_coords, (255, 255, 0), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                step = channel * width
                q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(q_img))

                if self.is_recording and self.video_writer:
                    self.video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        if self.capture is None or not self.capture.isOpened():
            return

        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        video_path = os.path.join(self.output_directory, f'recorded_video_{date_str}.avi')
        frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(video_path, fourcc, 30, (frame_width, frame_height))
        self.is_recording = True
        print(f"Recording started: {video_path}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            print("Recording stopped.")

    def upload_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Video", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.capture = cv2.VideoCapture(file_path)
            self.timer.start(30)

    def analyze_movement(self):
        # Placeholder for movement analysis logic
        print("Analyzing movement...")

    def closeEvent(self, event):
        if self.capture:
            self.capture.release()
        if self.video_writer:
            self.video_writer.release()
        self.timer.stop()
        cv2.destroyAllWindows()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DumbbellTrackerGUI()
    window.show()
    sys.exit(app.exec_())
