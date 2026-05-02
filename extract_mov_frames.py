import cv2
from pathlib import Path

# Folder containing your .mov videos
video_dir = Path(r"C:\Users\1000001573\Downloads\continuous_fire.v1-new-dataset.yolov8\train\images")
label_dir = Path(r"C:\Users\1000001573\Downloads\continuous_fire.v1-new-dataset.yolov8\train\labels")

video_files = list(video_dir.glob("*.mov"))

if not video_files:
    print("No .mov files found in train\\images")
    raise SystemExit

for video_path in video_files:
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Could not open video: {video_path.name}")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    # Save about 1 frame per second
    frame_interval = max(1, int(round(fps)))

    frame_count = 0
    saved_count = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            image_name = f"{video_path.stem}_{saved_count:04d}.jpg"
            image_path = video_dir / image_name

            cv2.imwrite(str(image_path), frame)

            # Create empty label file (no fire)
            label_name = f"{video_path.stem}_{saved_count:04d}.txt"
            label_path = label_dir / label_name
            label_path.write_text("", encoding="utf-8")

            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"{video_path.name}: saved {saved_count - 1} frames")

print("Done.")