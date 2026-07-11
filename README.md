# 💤 Student Drowsiness & Yawning Detection System

A real-time computer vision project that detects **drowsiness** and **yawning** using a webcam. The system monitors the user's eyes and mouth and plays an alert sound when signs of fatigue are detected.

## 📌 Features

* Real-time webcam monitoring
* Eye closure (drowsiness) detection
* Yawning detection
* Audio alert when fatigue is detected
* Simple and lightweight application

## 🛠️ Technologies Used

* Python
* OpenCV
* NumPy
* dlib / MediaPipe *(if used)*
* Flask *(if used for the web interface)*

## ⚙️ How It Works

1. Captures live video from the webcam.
2. Detects the user's face.
3. Tracks the eyes and mouth.
4. Checks for:

   * Prolonged eye closure (drowsiness)
   * Yawning
5. Plays an alert sound when fatigue is detected.

## 📂 Project Structure

```text
drowsiness_detection_system/
│── app.py
│── main.py
│── requirements.txt
│── models/
│── static/
│── templates/
│── alarm.wav
└── README.md
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Chintucharan/detection_system.git
```

Go to the project folder:

```bash
cd detection_system
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python app.py
```

or

```bash
python main.py
```

## 💡 Applications

* Student study monitoring
* Driver drowsiness detection
* Workplace fatigue monitoring
* Computer vision learning projects

## 🔮 Future Improvements

* Support multiple users
* Improve detection accuracy using deep learning
* Mobile application support
* Performance dashboard

## 👨‍💻 Author

**Chintucharan Gowni**

If you found this project helpful, consider giving it a ⭐ on GitHub.
