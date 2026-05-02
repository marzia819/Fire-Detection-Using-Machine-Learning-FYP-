# Artificial Intelligence-Based Fire Detection System

This project is a computer-vision fire detection prototype built with YOLO object detection, OpenCV, and a small real-time alarm/dashboard workflow. It contains a labelled fire dataset in YOLO format, pretrained/trained model weights, training outputs, a standalone webcam alarm script, and a FastAPI-based monitoring prototype.

The goal of the project is to detect visible fire in images or live video streams and support faster visual awareness through bounding boxes, alarm snapshots, and incident records.

> Safety note: this project is a research/prototype system. It should not be used as a replacement for certified smoke, heat, flame, or building fire alarm systems.

## Project Features

- Single-class YOLO object detection for `fire`
- YOLOv8-format train, validation, and test dataset
- Roboflow-exported annotations with additional local hard negative examples
- Pretrained weights included for YOLOv8/YOLO11 experimentation
- Trained model outputs under `runs/detect`
- Standalone live webcam alarm script with saved detection frames
- FastAPI dashboard prototype with video stream, settings, incident records, snapshots, and alert hooks
- Final Year Project report included as `Fire-Detection-Using-Machine-Learning-FYP-.md`

## Repository Structure

```text
continuous_fire.v1-new-dataset.yolov8/
|-- data.yaml
|-- README.md
|-- README.dataset.txt
|-- README.roboflow.txt
|-- Fire-Detection-Using-Machine-Learning-FYP-.md
|-- extract_mov_frames.py
|-- live_alarm_add_morepics.py
|-- yolo11n.pt
|-- yolov8s.pt
|-- alarm_frames/
|-- train/
|   |-- images/
|   `-- labels/
|-- valid/
|   |-- images/
|   `-- labels/
|-- test/
|   |-- images/
|   `-- labels/
`-- runs/
    `-- detect/
        |-- FINAL_FIRE/
        |-- FINAL_FIRE_V2/
        |-- FINAL_FIRE_V3_AND151NEG_V1/
        |-- val/
        `-- val2/
```

## Dataset

The dataset is in YOLO detection format. Each image has a matching `.txt` label file using normalized bounding boxes:

```text
class_id x_center y_center width height
```

This project uses one class:

```yaml
names: ['fire']
```

### Dataset Source

The original dataset was exported from Roboflow:

- Workspace: `fire-detection-2xe3o`
- Project: `continuous_fire-0shcw`
- Version: `1`
- License: `CC BY 4.0`
- URL: `https://universe.roboflow.com/fire-detection-2xe3o/continuous_fire-0shcw/dataset/1`

The Roboflow export README states that the exported dataset contained 2,509 images. The current local workspace contains 2,765 images, which suggests additional local images or extracted frames were added after export.

### Local Split Summary

| Split | Images | Label files | Empty label files | Non-empty label files |
| --- | ---: | ---: | ---: | ---: |
| Train | 1,208 | 1,212 | 208 | 1,004 |
| Validation | 806 | 806 | 54 | 752 |
| Test | 751 | 751 | 2 | 749 |
| Total | 2,765 | 2,769 | 264 | 2,505 |

Empty label files are valid for negative images where no fire object is present. These negative examples are useful because they help the model learn not to trigger on lights, reflections, sky glow, and other fire-like visual patterns.

### Dataset Quality Notes

During local inspection, the training split had more label files than image files. Before future training runs, it is recommended to:

- Remove orphan label files that do not have matching images.
- Confirm every label row follows valid YOLO format.
- Keep empty `.txt` files only for true negative images.
- Re-check `data.yaml` paths before training.

## `data.yaml`

Current dataset configuration:

```yaml
train: ../train/images
val: ../valid/images
test: ../test/images

nc: 1
names: ['fire']
```

If you run YOLO commands from this repository root, the paths may need to be changed to:

```yaml
train: train/images
val: valid/images
test: test/images
```

Use whichever path style matches the directory from which your YOLO command resolves the dataset.

## Requirements

Recommended environment:

- Python 3.9+
- `ultralytics`
- `opencv-python`
- `fastapi`
- `uvicorn`
- `sse-starlette`
- `psutil`
- `python-multipart`
- `twilio`
- `python-dotenv`
- `starlette`

Install the main dependencies:

```bash
pip install ultralytics opencv-python fastapi uvicorn sse-starlette psutil python-multipart twilio python-dotenv starlette
```

The dashboard-specific dependency list is also available at:

```text
runs/detect/FINAL_FIRE/requirements.txt
```

## Training

A typical YOLO training command is:

```bash
yolo detect train model=yolov8s.pt data=data.yaml epochs=50 imgsz=640 batch=16 name=fire_detection_training
```

The `FINAL_FIRE` run used a longer training configuration:

- Task: detection
- Epochs: 120
- Image size: 640
- Batch size: 16
- Optimizer: auto
- Device: GPU `0`
- Main output folder: `runs/detect/FINAL_FIRE`

Training outputs normally include:

- `weights/best.pt`
- `weights/last.pt`
- `results.csv`
- `results.png`
- precision, recall, F1, PR, and confusion matrix plots
- train/validation batch previews

## Validation

Validate a trained checkpoint:

```bash
yolo detect val model=runs/detect/FINAL_FIRE/weights/best.pt data=data.yaml imgsz=640
```

Or validate the hard-negative model:

```bash
yolo detect val model=runs/detect/FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt data=data.yaml imgsz=640
```

## Prediction

Run inference on a single image:

```bash
yolo detect predict model=runs/detect/FINAL_FIRE/weights/best.pt source=test/images conf=0.25
```

Run inference on a webcam:

```bash
yolo detect predict model=runs/detect/FINAL_FIRE/weights/best.pt source=0 conf=0.25 show=True
```

## Model Weights

Included weights:

| File / Folder | Purpose |
| --- | --- |
| `yolov8s.pt` | YOLOv8 small pretrained starting point |
| `yolo11n.pt` | YOLO11 nano pretrained model |
| `runs/detect/FINAL_FIRE/weights/best.pt` | Best checkpoint from the `FINAL_FIRE` training run |
| `runs/detect/FINAL_FIRE/weights/last.pt` | Last checkpoint from the `FINAL_FIRE` training run |
| `runs/detect/FINAL_FIRE_V2/weights/best.pt` | Additional trained checkpoint |
| `runs/detect/FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt` | Trained checkpoint with additional negative examples |

The FYP report notes that the best observed validation result reached approximately `0.912 mAP@50` and `0.676 mAP@50-95` in a `FINAL_FIRE_V3` run. The `FINAL_FIRE` run ended around `0.890 mAP@50` and `0.652 mAP@50-95` at epoch 120.

## Standalone Live Alarm Script

`live_alarm_add_morepics.py` loads a YOLO model, reads frames from a webcam or stream, draws detections, beeps on Windows when fire is detected, and saves alarm frames to `alarm_frames/`.

Run it with:

```bash
python live_alarm_add_morepics.py
```

Important settings inside the script:

```python
MODEL_PATH = r"runs\detect\FINAL_FIRE\weights\best.pt"
SOURCE = 0
CONF = 0.25
ALARM_COOLDOWN_SEC = 3.0
SAVE_DETECTIONS = True
SAVE_DIR = "alarm_frames"
```

Change `SOURCE` to a video file path or RTSP stream if you do not want to use the default webcam.

## FastAPI Dashboard Prototype

The dashboard prototype is stored in:

```text
runs/detect/FINAL_FIRE/
```

Important files:

| File | Purpose |
| --- | --- |
| `app.py` | FastAPI backend, YOLO inference, video stream, settings, incidents |
| `static/index.html` | Main dashboard page |
| `static/login.html` | Login page |
| `static/app.js` | Frontend dashboard logic |
| `static/styles.css` | Dashboard styling |
| `incidents.db` | SQLite incident database |
| `settings.json` | Dashboard/runtime settings |
| `.env.example` | Example environment variables |

Install dependencies:

```bash
cd runs/detect/FINAL_FIRE
pip install -r requirements.txt
```

Run the dashboard:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

### Dashboard API Endpoints

The backend includes endpoints for:

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Main dashboard |
| `GET /login` | Login page |
| `POST /login` | Login action |
| `GET /logout` | Logout action |
| `GET /video_feed` | Live video stream |
| `POST /api/settings` | Update detection/settings values |
| `GET /api/status` | Current system status |
| `GET /api/incidents` | Recent incidents |
| `DELETE /api/incidents/{incident_id}` | Delete an incident |
| `GET /api/cameras` | Camera/source discovery |

### Dashboard Configuration Notes

`runs/detect/FINAL_FIRE/app.py` contains a hardcoded model path:

```python
MODEL_PATH = r"C:/Users/1000001573/Downloads/continuous_fire.v1-new-dataset.yolov8/runs/detect/FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt"
```

If you move the project, update this path or change it to a relative path such as:

```python
MODEL_PATH = r"../FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt"
```

The app also contains settings for confidence threshold, alarm behavior, snapshots, email/SMS hooks, and incident storage.

## Frame Extraction Utility

`extract_mov_frames.py` extracts about one frame per second from `.mov` files placed in `train/images` and creates empty label files in `train/labels`.

Run it with:

```bash
python extract_mov_frames.py
```

Use this only for videos that should become negative examples. The script creates empty label files, meaning no fire boxes are annotated for the extracted frames.

## Suggested Workflow

1. Clean and validate the dataset labels.
2. Confirm `data.yaml` paths match your working directory.
3. Train or fine-tune YOLO using `yolov8s.pt` or another starting model.
4. Validate the best checkpoint on the validation and test splits.
5. Test predictions on realistic non-fire scenes such as lamps, reflections, sunlight, and bright screens.
6. Run `live_alarm_add_morepics.py` for quick webcam testing.
7. Run the FastAPI dashboard for a fuller monitoring prototype.

## Common Issues

### YOLO cannot find images

Check the paths in `data.yaml`. If you are in the repository root, use:

```yaml
train: train/images
val: valid/images
test: test/images
```

### Webcam does not open

Try another camera index:

```python
SOURCE = 1
```

or use a video file path:

```python
SOURCE = r"path/to/video.mp4"
```

### Dashboard cannot load the model

Update `MODEL_PATH` in `runs/detect/FINAL_FIRE/app.py` so it points to an existing `.pt` file.

### Too many false alarms

Try increasing the confidence threshold, adding more hard negative images, and using temporal filtering so the alarm triggers only after fire is detected across multiple frames.

### Fire is missed

Try lowering the confidence threshold, adding more fire examples similar to the target environment, and evaluating different YOLO model sizes.

## Results Summary

The project report records strong validation performance for the trained YOLO fire detector. The best observed run reached approximately:

| Metric | Approximate value |
| --- | ---: |
| Precision | 0.89 to 0.92 |
| Recall | around 0.82 |
| mAP@50 | 0.912 |
| mAP@50-95 | 0.676 |

These results are promising for a prototype, but real-world fire detection requires careful testing under varied lighting, camera quality, viewing angle, smoke, reflections, and small early-stage fire conditions.

## Limitations

- The model detects visible fire only; it cannot detect hidden fire, heat, gas, or smoke without visual cues.
- Camera angle, lighting, blur, low resolution, and occlusion can affect performance.
- Fire-like objects may still cause false positives.
- Dataset issues should be cleaned before future training.
- The prototype needs stronger security and deployment hardening before real use.
- It should not replace certified fire safety systems.

## Future Improvements

- Clean orphan or malformed label files.
- Add more diverse fire and non-fire examples.
- Add controlled real-world test videos.
- Improve temporal filtering and event confirmation logic.
- Compare YOLOv8, YOLO11, and larger/smaller model variants.
- Export models to ONNX/TensorRT for faster deployment.
- Improve dashboard authentication and configuration handling.
- Add reliable notification channels for email, SMS, calls, or messaging apps.
- Test on edge devices such as Jetson, Raspberry Pi with accelerator, or mini PCs.

## License and Attribution

The original dataset export is licensed under `CC BY 4.0` and was provided through Roboflow Universe:

```text
https://universe.roboflow.com/fire-detection-2xe3o/continuous_fire-0shcw
```

Please preserve dataset attribution if you share, modify, or publish work based on this dataset.
