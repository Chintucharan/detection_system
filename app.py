from flask import Flask, render_template, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
import base64
import random
import csv
from scipy.spatial import distance as dist

app = Flask(__name__)
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
except:
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

mp_face = mp.solutions.face_mesh

face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE=[33,160,158,133,153,144]
RIGHT_EYE=[362,385,387,263,373,380]
MOUTH=[61,291,81,178,13,14,17,402]

EAR_THRESHOLD=0.21
MAR_THRESHOLD=0.55

EYE_FRAMES=0
MOUTH_FRAMES=0

EYE_LIMIT=5
MOUTH_LIMIT=4

focus_score=80

alarm=False
alarm_type="none"

def eye_aspect_ratio(eye):
    A=dist.euclidean(eye[1],eye[5])
    B=dist.euclidean(eye[2],eye[4])
    C=dist.euclidean(eye[0],eye[3])
    return (A+B)/(2*C)

def mouth_aspect_ratio(mouth):
    A=dist.euclidean(mouth[2],mouth[6])
    B=dist.euclidean(mouth[3],mouth[5])
    C=dist.euclidean(mouth[0],mouth[1])
    return (A+B)/(2*C)
def process_frame(frame):

    global EYE_FRAMES, MOUTH_FRAMES
    global focus_score
    global alarm
    global alarm_type

    alarm = False
    alarm_type = "none"

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    status = "NO FACE"

    if results.multi_face_landmarks:

        face = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        def pts(idx):
            return [
                (int(face.landmark[i].x * w),
                 int(face.landmark[i].y * h))
                for i in idx
            ]

        left = pts(LEFT_EYE)
        right = pts(RIGHT_EYE)
        mouth = pts(MOUTH)

        ear = (eye_aspect_ratio(left) + eye_aspect_ratio(right)) / 2
        mar = mouth_aspect_ratio(mouth)

        if ear < EAR_THRESHOLD:
            EYE_FRAMES = min(EYE_FRAMES + 1, 30)
        else:
            EYE_FRAMES = max(EYE_FRAMES - 1, 0)

        if mar > MAR_THRESHOLD:
            MOUTH_FRAMES = min(MOUTH_FRAMES + 1, 30)
        else:
            MOUTH_FRAMES = max(MOUTH_FRAMES - 1, 0)

        if EYE_FRAMES >= EYE_LIMIT:

            status = "DROWSY 😴"

            focus_score = max(0, focus_score - 3)

            alarm = True
            alarm_type = "drowsy"

        elif MOUTH_FRAMES >= MOUTH_LIMIT:

            status = "YAWNING 🥱"

            focus_score = max(0, focus_score - 2)

            alarm = True
            alarm_type = "yawning"

        else:

            status = "FOCUSED 🙂"

            focus_score = min(100, focus_score + 1)

    return {
        "status": status,
        "focus_score": focus_score,
        "eye_frames": EYE_FRAMES,
        "mouth_frames": MOUTH_FRAMES,
        "alarm": alarm,
        "type": alarm_type
    }
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detection")
def detection():
    return render_template(
        "detection.html",
        tips=tips_list,
        quotes=quotes_list
    )


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json["frame"]

    encoded = data.split(",")[1]

    img = base64.b64decode(encoded)

    npimg = np.frombuffer(img, np.uint8)

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result = process_frame(frame)

    return jsonify(result)


@app.route("/status")
def status():

    return jsonify({
        "alarm": alarm,
        "type": alarm_type
    })


@app.route("/get_quote")
def get_quote():

    return jsonify(random.choice(quotes_list))


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )