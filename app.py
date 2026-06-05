from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import threading
import time
import csv
import random
import winsound
import atexit

app = Flask(__name__)

tips_list = []

try:
    with open("tips.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                tips_list.append({
                    "title": row[0],
                    "description": row[1],
                    "link": row[2]
                })
except FileNotFoundError:
    pass


quotes_list = [
    {"content": "Stay consistent. Small daily improvements lead to massive long-term success.", "author": "Unknown"},
    {"content": "Discipline is choosing between what you want now and what you want most.", "author": "Abraham Lincoln"},
    {"content": "Success is built on daily habits, not overnight miracles.", "author": "Unknown"},
    {"content": "Your future depends on what you do today, not tomorrow.", "author": "Robert Kiyosaki"},
    {"content": "Focus is the ability to say no to distractions.", "author": "Steve Jobs"},
    {"content": "Work hard in silence, let success make noise.", "author": "Frank Ocean"},
    {"content": "Don’t stop when you’re tired. Stop when you’re done.", "author": "Unknown"},
    {"content": "Push yourself beyond limits, that’s where growth happens.", "author": "Unknown"},
    {"content": "Small steps every day create big results over time.", "author": "Unknown"},
    {"content": "You don’t need motivation, you need discipline.", "author": "Unknown"},
    {"content": "Success is the sum of small efforts repeated daily.", "author": "Robert Collier"},
    {"content": "Dream big. Start small. Act now.", "author": "Robin Sharma"},
    {"content": "Hard work beats talent when talent doesn’t work hard.", "author": "Tim Notke"},
    {"content": "Don’t wait for opportunity. Create it.", "author": "Unknown"},
    {"content": "Your only limit is your mind.", "author": "Unknown"},
    {"content": "Stay patient. Trust the process.", "author": "Unknown"},
    {"content": "Focus on progress, not perfection.", "author": "Unknown"},
    {"content": "Great things never come from comfort zones.", "author": "Unknown"},
    {"content": "Wake up with determination, sleep with satisfaction.", "author": "Unknown"},
    {"content": "Success is built when no one is watching.", "author": "Unknown"},
]

camera = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [61, 291, 81, 178, 13, 14, 17, 402]

EAR_THRESHOLD = 0.21
MAR_THRESHOLD = 0.55   # improved (more stable)

EYE_FRAMES = 0
MOUTH_FRAMES = 0

EYE_LIMIT = 5
MOUTH_LIMIT = 4   # improved stability

focus_score = 80
alarm_active_eye = False
alarm_active_mouth = False

last_eye_alarm = 0
last_mouth_alarm = 0

atexit.register(lambda: camera.release())


def play_alarm():
    winsound.Beep(1200, 900)


def play_big_alarm():
    winsound.Beep(1500, 600)
    winsound.Beep(1200, 600)


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[2], mouth[6])
    B = dist.euclidean(mouth[3], mouth[5])
    C = dist.euclidean(mouth[0], mouth[1])
    return (A + B) / (2.0 * C)


def generate_frames():

    global EYE_FRAMES, MOUTH_FRAMES
    global focus_score, alarm_active_eye, alarm_active_mouth
    global last_eye_alarm, last_mouth_alarm

    while True:

        success, frame = camera.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        status = "NO FACE"
        action = "STAY VISIBLE"
        color = (200, 200, 200)

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]
            h, w, _ = frame.shape

            def pts(idx):
                return [(int(face.landmark[i].x * w),
                         int(face.landmark[i].y * h)) for i in idx]

            left_eye = pts(LEFT_EYE)
            right_eye = pts(RIGHT_EYE)
            mouth = pts(MOUTH)

            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2
            mar = mouth_aspect_ratio(mouth)

            # =========================
            # EYE LOGIC
            # =========================
            if ear < EAR_THRESHOLD:
                EYE_FRAMES += 1
            else:
                EYE_FRAMES = max(0, EYE_FRAMES - 1)
                alarm_active_eye = False

            # =========================
            # MOUTH LOGIC (FIXED)
            # =========================
            if mar > MAR_THRESHOLD:
                MOUTH_FRAMES += 1
            else:
                MOUTH_FRAMES = max(0, MOUTH_FRAMES - 1)
                alarm_active_mouth = False

            # =========================
            # DROWSY
            # =========================
            if EYE_FRAMES >= EYE_LIMIT:

                status = "DROWSY 😴"
                action = "WAKE UP ⚠️"
                color = (0, 0, 255)

                focus_score = max(0, focus_score - 3)

                now = time.time()
                if not alarm_active_eye and (now - last_eye_alarm > 2):

                    alarm_active_eye = True
                    last_eye_alarm = now
                    threading.Thread(target=play_alarm, daemon=True).start()

            # =========================
            # YAWNING (FIXED + BIG SOUND)
            # =========================
            elif MOUTH_FRAMES >= MOUTH_LIMIT:

                status = "YAWNING 🥱"
                action = "TAKE BREAK ☕"
                color = (0, 165, 255)

                focus_score = max(0, focus_score - 2)

                now = time.time()
                if not alarm_active_mouth and (now - last_mouth_alarm > 2):

                    alarm_active_mouth = True
                    last_mouth_alarm = now
                    threading.Thread(target=play_big_alarm, daemon=True).start()

            # =========================
            # FOCUSED
            # =========================
            else:

                status = "FOCUSED 🙂"
                action = "KEEP GOING 💪"
                color = (0, 255, 0)

                focus_score = min(100, focus_score + 1)

            for p in left_eye + right_eye + mouth:
                cv2.circle(frame, p, 1, color, -1)

        cv2.putText(frame, f"STATUS: {status}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.putText(frame, f"ACTION: {action}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.putText(frame, f"FOCUS: {focus_score}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.putText(frame, f"EYE: {EYE_FRAMES}", (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.putText(frame, f"MOUTH: {MOUTH_FRAMES}", (20, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detection")
def detection():
    return render_template("detection.html",
                           tips=tips_list,
                           quotes=quotes_list)


@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/get_quote")
def get_quote():
    return jsonify(random.choice(quotes_list))


if __name__ == "__main__":
    app.run(debug=False)