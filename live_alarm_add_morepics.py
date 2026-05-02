import cv2
import time
from ultralytics import YOLO

# -------- SETTINGS --------
MODEL_PATH = r"runs\detect\FINAL_FIRE\weights\best.pt"
SOURCE = 0  # 0 = webcam, or RTSP string like: "rtsp://user:pass@ip:554/stream"
CONF = 0.25

ALARM_COOLDOWN_SEC = 3.0      # don't spam alarms
SAVE_DETECTIONS = True        # save frames when fire is detected
SAVE_DIR = "alarm_frames"
# --------------------------

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(SOURCE)
if not cap.isOpened():
    raise RuntimeError("Could not open video source. Check camera index or RTSP URL.")

last_alarm_time = 0.0

# Create save dir if needed
if SAVE_DETECTIONS:
    import os
    os.makedirs(SAVE_DIR, exist_ok=True)

print("Press Q to quit.")
while True:
    ok, frame = cap.read()
    if not ok:
        print("Frame read failed. Stream ended or connection issue.")
        break

    results = model.predict(frame, conf=CONF, verbose=False)
    r = results[0]

    fire_detected = (r.boxes is not None) and (len(r.boxes) > 0)

    # draw boxes
    annotated = r.plot()

    # alarm + save
    now = time.time()
    if fire_detected and (now - last_alarm_time) >= ALARM_COOLDOWN_SEC:
        last_alarm_time = now

        # beep (Windows)
        try:
            import winsound
            winsound.Beep(1200, 500)
        except Exception:
            pass

        if SAVE_DETECTIONS:
            ts = time.strftime("%Y%m%d_%H%M%S")
            out_path = f"{SAVE_DIR}/fire_{ts}.jpg"
            cv2.imwrite(out_path, frame)
            print(f"[ALARM] Fire detected! Saved: {out_path}")

    cv2.imshow("LIVE FIRE DETECTION", annotated)

    if cv2.waitKey(1) & 0xFF in (ord('q'), ord('Q')):
        break

cap.release()
cv2.destroyAllWindows()