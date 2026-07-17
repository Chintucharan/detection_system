# 💤 Student Drowsiness & Yawning Detection System

A real-time **computer vision-based web application** that detects **drowsiness** and **yawning** using a webcam. The application uses **MediaPipe Face Mesh** to track facial landmarks and calculate the **Eye Aspect Ratio (EAR)** and **Mouth Aspect Ratio (MAR)**. When signs of fatigue are detected, an alarm is triggered to alert the user. The application also provides **motivational quotes** and **study tips** to help users stay focused.

---

# 📌 Features

* 🎥 Real-time webcam monitoring
* 👁️ Eye closure (Drowsiness) detection
* 🥱 Yawning detection
* 🔔 Audio alert on fatigue detection
* 📊 Live focus score
* 💬 Motivational quotes
* 📖 Study tips with reference links
* 🌐 User-friendly Flask web interface
* ⚡ Lightweight and real-time performance

---

# 🛠️ Tech Stack

## Backend

* Python
* Flask

## Computer Vision

* OpenCV
* MediaPipe Face Mesh
* SciPy

## Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

## Libraries

* NumPy
* CSV
* Random

---

# ⚙️ How It Works

1. Open the application in a web browser.
2. Click the **Start** button.
3. OpenCV captures live video from the webcam.
4. MediaPipe Face Mesh detects facial landmarks.
5. Eye and mouth landmarks are extracted.
6. The system calculates:

   * **Eye Aspect Ratio (EAR)** for eye closure detection.
   * **Mouth Aspect Ratio (MAR)** for yawning detection.
7. If the EAR stays below a predefined threshold for several consecutive frames, the system identifies **drowsiness**.
8. If the MAR stays above a predefined threshold for several consecutive frames, the system identifies **yawning**.
9. An alarm is triggered and the focus score is updated.
10. Motivational quotes and study tips are displayed to encourage better concentration.

---

# 📂 Project Structure

```text
detection_system/
│── app.py
│── requirements.txt
│── tips.csv
│── README.md
│
├── screenshots/
│   ├── home.png
│   ├── detection.png
│   ├── motivation.png
│   ├── tips.png
│   └── quotes.png
│
├── templates/
│   ├── index.html
│   └── detection.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── alarm.wav
```

---

# 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/Chintucharan/detection_system.git
```

### Navigate to the project folder

```bash
cd detection_system
```

### Install the required packages

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

### Open the application

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

## 🏠 Home Page

![Home Page](screenshots/home.png)

---

## 🎥 Detection Page

![Detection Page](screenshots/detection.png)

---

## 💪 Motivation Section

![Motivation Section](screenshots/motivation.png)

---

## 📖 Study Tips

![Study Tips](screenshots/tips.png)

---

## 💬 Quote of the Day

![Quote of the Day](screenshots/quotes.png)

---

# 💡 Applications

* 🎓 Student study monitoring
* 🚗 Driver drowsiness detection
* 🏢 Workplace fatigue monitoring
* 🧠 Attention and focus monitoring
* 💻 Computer vision learning projects

---

# 🔮 Future Improvements

* 👥 Support multiple users
* 🌙 Improve detection accuracy under different lighting conditions
* 📈 User analytics and session history
* ☁️ Cloud deployment
* 📱 Mobile application
* 🧠 AI-based fatigue prediction
* 🎯 Head pose and distraction detection

---

# 👨‍💻 Author

**Gowni Venkat Charan**

---

⭐ If you found this project useful, please consider giving it a **Star ⭐** on GitHub.
