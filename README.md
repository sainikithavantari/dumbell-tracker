# Dumbbell Movement Tracker

## Overview
The Dumbbell Movement Tracker is a Python-based application that uses computer vision and machine learning to track and analyze dumbbell movements in real-time. The application leverages the MediaPipe Pose estimation model to detect key body points and provides feedback on the user's form during exercises. It also includes features like live video feed, video recording, and movement analysis.

## Features
- **Real-time Pose Tracking**: Uses MediaPipe to detect and track key body points (shoulders, elbows, wrists).
- **Live Video Feed**: Displays the live video feed from the webcam with overlays of detected body points.
- **Video Recording**: Records the live video feed and saves it to a specified directory.
- **Movement Analysis**: Provides real-time feedback on the user's form (e.g., arm extension).
- **Video Upload**: Allows users to upload pre-recorded videos for analysis.
- **Text-to-Speech Feedback**: Provides audio feedback based on the user's form.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- PyQt5 (`PyQt5`)
- Matplotlib (`matplotlib`)
- pyttsx3 (`pyttsx3`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dumbbell-movement-tracker.git
   cd dumbbell-movement-tracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. **Start Live Feed**: Click the "Start Live Feed" button to begin capturing video from your webcam.
2. **Start Recording**: Click the "Start Recording" button to start recording the live feed. Click "Stop Recording" to stop.
3. **Upload Video**: Click the "Upload Video" button to upload a pre-recorded video for analysis.
4. **Analyze Movement**: Click the "Analyze Movement" button to analyze the movement in the live feed or uploaded video.
5. **Feedback**: The application will provide real-time feedback on your form using text-to-speech.

## Directory Structure
```
dumbbell-movement-tracker/
│
├── main.py                  # Main application script
├── README.md                # Project documentation
├── requirements.txt         # List of dependencies
└── recorded_videos/         # Directory to store recorded videos
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [MediaPipe](https://mediapipe.dev/) for the pose estimation model.
- [OpenCV](https://opencv.org/) for computer vision capabilities.
- [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework.
- [Matplotlib](https://matplotlib.org/) for plotting and visualization.
- [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech functionality.

## Contact
For any questions or feedback, please contact [mail](mailto:sainikithavantari@gmail.com).
