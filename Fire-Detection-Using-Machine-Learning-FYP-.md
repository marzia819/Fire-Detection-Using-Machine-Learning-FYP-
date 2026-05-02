# Artificial Intelligence-Based Fire Detection System

**Final Year Project Report**  
**Project Title:** Artificial Intelligence-Based Fire Detection System  
**Domain:** Artificial Intelligence, Computer Vision, Real-Time Monitoring  
**Core Technologies:** YOLOv8, OpenCV, FastAPI, HTML/CSS/JavaScript, SQLite  
**Prepared by:** [Student Name]  
**Supervisor:** [Supervisor Name]  
**Institution:** [Institution Name]  
**Academic Year:** [Academic Year]

## 1. Abstract

Fire is a major safety risk in homes, workplaces, industrial sites, forests, and public spaces. Traditional fire detection systems usually depend on smoke, heat, or flame sensors. These systems are useful, but they may be limited by installation location, environmental conditions, delayed response, and lack of visual confirmation. This project presents an Artificial Intelligence-Based Fire Detection System that uses computer vision to identify fire in real-time video streams. The system is built around the YOLOv8 object detection model, OpenCV video processing, a FastAPI backend, and a browser-based HTML/CSS/JavaScript monitoring dashboard.

The project uses a labelled fire detection dataset in YOLO format, containing fire images and hard negative non-fire images such as lights, reflections, and visually similar bright regions. The inclusion of hard negatives is important because fire-like colours and light sources can cause false alarms in real-world environments. The system processes frames from a webcam or video stream, detects fire using the trained model, applies confidence thresholds and temporal filtering, logs incidents in SQLite, and displays live monitoring information through a dashboard. The dashboard supports real-time status updates, incident history, snapshots, and alert management.

Experimental results show that the trained YOLO-based detector can identify fire with strong validation performance, reaching approximately 0.91 mAP@50 in the best observed training run. The project demonstrates that deep learning and real-time web technologies can be combined to create a practical, low-cost visual fire monitoring system. Future work should improve dataset diversity, test in more real deployment environments, support edge hardware, and strengthen notification and security features.

## 2. Acknowledgements

I would like to thank my supervisor, lecturers, classmates, and family for their support during the development of this final year project. Their guidance and encouragement helped me improve both the technical implementation and the written documentation of the system. I am also grateful to the open-source software community, especially the contributors of YOLO, OpenCV, FastAPI, and related libraries, whose tools made it possible to build and test a complete artificial intelligence-based fire detection prototype.

## 3. Table of Contents

1. Abstract  
2. Acknowledgements  
3. Table of Contents  
4. Lists  
   4.1 List of Abbreviations  
   4.2 List of Figures  
   4.3 List of Tables  
5. Statement of Authorship  
6. Main Content  
   6.1 Introduction  
      6.1.1 Project Aim  
      6.1.2 Project Objectives  
      6.1.3 Project Contributions  
      6.1.4 Business and Social Benefits  
   6.2 Literature Review  
   6.3 Methodology  
   6.4 System Architecture  
   6.5 Implementation  
      6.5.11 Functional Requirements  
      6.5.12 Non-Functional Requirements  
      6.5.13 Database Design  
   6.6 Empirical Study / Results  
      6.6.5 Testing and Validation  
   6.7 Discussion  
   6.8 Conclusion & Future Work  
7. References  
8. Appendix  

## 4. Lists

### 4.1 List of Abbreviations

| Abbreviation | Meaning |
| --- | --- |
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| CNN | Convolutional Neural Network |
| CPU | Central Processing Unit |
| CSS | Cascading Style Sheets |
| DB | Database |
| FPS | Frames Per Second |
| GPU | Graphics Processing Unit |
| HTML | HyperText Markup Language |
| IoU | Intersection over Union |
| JS | JavaScript |
| mAP | mean Average Precision |
| ML | Machine Learning |
| NMS | Non-Maximum Suppression |
| RTSP | Real Time Streaming Protocol |
| SQL | Structured Query Language |
| UI | User Interface |
| YOLO | You Only Look Once |

### 4.2 List of Figures

| Figure | Title |
| --- | --- |
| Figure 1 | General workflow of the AI-based fire detection system |
| Figure 2 | YOLOv8 fire detection pipeline |
| Figure 3 | System architecture showing dataset, model, backend, database, and dashboard |
| Figure 4 | Real-time monitoring dashboard layout |
| Figure 5 | Incident logging and alert flow |
| Figure 6 | Example training and validation result plots |
| Figure 7 | Examples of hard negative images such as lights and reflections |

### 4.3 List of Tables

| Table | Title |
| --- | --- |
| Table 1 | Comparison of traditional and AI-based fire detection |
| Table 2 | Main tools and technologies used |
| Table 3 | Dataset split summary |
| Table 4 | Model training configuration |
| Table 5 | Validation performance summary |
| Table 6 | Backend API endpoints |
| Table 7 | Risks, limitations, and mitigation strategies |
| Table 8 | Functional and non-functional requirements |
| Table 9 | Testing and validation cases |

## 5. Statement of Authorship

I declare that this project report, titled "Artificial Intelligence-Based Fire Detection System", is my own work and has been prepared as part of my Final Year Project. The implementation, experiments, and analysis described in this report are based on the project files and development work completed for the system. Any external tools, datasets, libraries, documentation, and research papers used to support the project have been acknowledged and referenced appropriately. I understand that plagiarism, fabrication of results, and unacknowledged use of external work are academic offences.

### 5.1 Declaration by Author

I certify that this report has been written by me and that the project implementation described in it was developed, tested, and documented as part of my Final Year Project. All sources of information, datasets, software libraries, frameworks, and external references used in this work have been cited where appropriate.

**Student Name:** [Student Name]  
**Student ID:** [Student ID]  
**Signature:** ____________________  
**Date:** ____________________

### 5.2 Declaration by Supervisor

I confirm that this project report has been submitted under my supervision and is suitable for assessment as a Final Year Project report, subject to institutional review and evaluation.

**Supervisor Name:** [Supervisor Name]  
**Signature:** ____________________  
**Date:** ____________________

## 6. Main Content

### 6.1 Introduction

Fire detection is an important problem in public safety, building security, industrial monitoring, and environmental protection. A delayed response to fire can result in serious damage to property, injury, loss of life, and environmental harm. For this reason, automatic fire detection systems are widely used in residential, commercial, and industrial environments.

Traditional fire detection methods normally use physical sensors. Smoke detectors identify smoke particles in the air. Heat detectors respond to temperature changes. Flame detectors identify radiation patterns produced by flames. These technologies are effective in many situations, but they also have limitations. A smoke detector may not respond quickly if smoke does not reach the sensor. A heat detector may respond only after the fire has grown. A flame detector can be affected by line-of-sight limitations and environmental interference. In many modern environments, cameras already exist for surveillance and monitoring. This creates an opportunity to use computer vision as an additional layer of fire detection.

Artificial intelligence has improved significantly in recent years, especially in image recognition and object detection. Deep learning models can learn visual patterns from large datasets and identify objects in images or video frames. YOLO, which stands for You Only Look Once, is one of the most popular real-time object detection families. It is suitable for applications where both speed and accuracy are important. Fire detection is one such application because a useful system must identify fire quickly while avoiding false alarms.

This project develops an Artificial Intelligence-Based Fire Detection System using YOLOv8. The system detects fire in real-time video using OpenCV and sends the results to a FastAPI backend. A web dashboard built with HTML, CSS, and JavaScript allows users to monitor the camera feed, view detection status, update settings, and review previous incidents. The system also stores incident records in SQLite. To reduce false alarms, the dataset and implementation consider hard negative examples such as lights, reflections, and other bright objects that may look similar to fire.

#### 6.1.1 Project Aim

The main aim of the project is to design, implement, and evaluate a working prototype that can detect fire from video input and support real-time monitoring.

#### 6.1.2 Project Objectives

The objectives are:

1. To prepare and use a YOLO-format dataset for fire detection.
2. To train and evaluate a YOLOv8-based fire detection model.
3. To process live video frames using OpenCV.
4. To develop a FastAPI backend for detection, settings, status, and incident management.
5. To build a browser-based dashboard for real-time monitoring.
6. To reduce false positives using confidence thresholds, hard negative images, and temporal filtering.
7. To log incidents using SQLite for later review.

#### 6.1.3 Project Contributions

The project makes the following practical and academic contributions:

1. It demonstrates a complete AI-based fire detection pipeline from dataset preparation to dashboard monitoring.
2. It applies YOLOv8 to a custom fire detection dataset with both fire and hard negative non-fire images.
3. It integrates real-time video processing, backend APIs, database logging, and frontend visualization into one working prototype.
4. It addresses false positives using confidence thresholding, hard negative examples, cooldown logic, and temporal filtering.
5. It provides a foundation that can be extended for CCTV monitoring, edge deployment, smoke detection, and multi-camera safety systems.

#### 6.1.4 Business and Social Benefits

The system has several potential benefits. In a business environment, it can support faster monitoring of warehouses, offices, kitchens, laboratories, parking areas, and industrial zones where cameras are already installed. It can reduce the need for continuous manual observation by automatically highlighting possible fire events. In social and safety contexts, it can provide earlier visual awareness, preserve incident evidence, and support emergency response decisions. The system is also relatively low-cost because it uses common cameras and open-source software tools.

The scope of the project is a prototype system for real-time visual fire detection. It is not intended to fully replace certified fire alarm systems. Instead, it provides an intelligent visual monitoring layer that can support faster awareness and additional confirmation.

#### Table 1. Comparison of traditional and AI-based fire detection

| Feature | Traditional sensor-based detection | AI-based visual detection |
| --- | --- | --- |
| Input | Smoke, heat, flame radiation | Images or video frames |
| Confirmation | Usually no visual confirmation | Visual evidence through snapshots/video |
| Response condition | Depends on physical sensor exposure | Depends on camera visibility and model confidence |
| False alarm causes | Dust, steam, heat sources | Lights, reflections, orange objects, shadows |
| Deployment | Requires sensors in target areas | Can use existing cameras |
| Main limitation | Sensor location and environmental delay | Model accuracy, lighting, camera quality |

### 6.2 Literature Review

Fire detection has traditionally been studied using sensor-based methods, image-processing methods, and machine-learning methods. Sensor-based methods remain common because they are reliable, standardized, and relatively low cost. However, they do not always provide information about the size, position, or visual appearance of the fire. For surveillance and monitoring applications, video-based methods provide useful additional information.

Early computer vision approaches to fire detection often used colour segmentation and motion analysis. Fire normally appears in red, orange, yellow, or white regions, and flames often move irregularly. Researchers used colour spaces such as RGB, HSV, and YCbCr to isolate possible flame regions. These methods are simple and fast, but they are sensitive to lighting conditions. Bright lamps, sunlight, reflections, vehicle headlights, and orange-coloured objects can be incorrectly classified as fire. This is a major weakness in real-world environments.

Machine learning improved fire detection by allowing models to learn patterns from examples. Traditional machine learning methods used hand-crafted features such as colour histograms, texture descriptors, edges, and motion features. These features were then passed to classifiers such as support vector machines or decision trees. Although these methods improved performance, they still depended heavily on manually designed features.

Deep learning changed the field by allowing neural networks to learn image features automatically. Convolutional Neural Networks are especially effective for image classification and object detection because they learn spatial patterns from image data. Instead of manually defining what fire looks like, a CNN-based model can learn flame shapes, colour transitions, textures, and contextual patterns directly from labelled images.

Object detection models identify both the class and location of objects. This is important for fire detection because the system should not only say that fire exists, but also show where it appears in the frame. Two-stage detectors such as Faster R-CNN are often accurate but may be slower. One-stage detectors such as YOLO and SSD are designed for faster inference, making them suitable for real-time applications.

YOLO is a widely used object detection approach because it predicts bounding boxes and class probabilities in a single pass through the neural network. This makes it efficient for real-time video processing. YOLOv8, provided by the Ultralytics ecosystem, is a modern YOLO implementation that supports detection, segmentation, classification, tracking, and export workflows. It is practical for student and prototype projects because it provides training, validation, prediction, and visualization tools.

A major challenge in fire detection is false positives. Fire-like objects can include sunlight, candles, lamps, traffic lights, reflections on glass, welding sparks, and orange clothing. A model trained only on obvious fire images may perform well on validation images but fail in real deployment. For this reason, hard negative examples are important. Hard negatives are non-fire images that look similar to fire. By including these images during training, the model learns to distinguish real flames from visually similar objects.

Temporal filtering is another important concept. If a model detects fire in only one frame, it may be a random error. A safer system can require detection across multiple consecutive frames or over a short time window before triggering a high-level alarm. This reduces false alarms caused by momentary visual noise. However, temporal filtering must be designed carefully because too much delay can reduce safety.

Modern fire detection systems also require practical software architecture. A model alone is not enough. The system must capture video, process frames, display results, store incidents, and notify users. FastAPI is suitable for building a lightweight backend API in Python. OpenCV is widely used for video capture and frame processing. SQLite is useful for small local systems because it does not require a separate database server. A web dashboard allows users to interact with the system through a browser.

In summary, the literature supports the use of deep learning and YOLO-style detectors for real-time fire detection. The strongest systems combine model training, hard negative data, real-time processing, temporal filtering, and clear user interfaces.

### 6.3 Methodology

The project followed an applied software engineering and experimental machine learning methodology. The work was divided into dataset preparation, model training, system implementation, testing, and evaluation.

#### 6.3.1 Dataset Preparation

The dataset is stored in YOLOv8 format. It contains three main splits: training, validation, and testing. Each image has a corresponding label file. Label files contain bounding box annotations in normalized YOLO format:

```text
class_id x_center y_center width height
```

The project uses one class: `fire`. Therefore, the class identifier is `0`.

The dataset includes positive fire examples and hard negative examples. Positive examples contain visible fire regions. Hard negative examples contain non-fire scenes that may confuse the model, such as bright lights, sky glow, reflections, and similar colours. Empty label files are used for negative images, meaning the image contains no fire object.

#### Table 3. Dataset split summary

| Split | Images | Label files | Empty label files | Valid fire boxes |
| --- | ---: | ---: | ---: | ---: |
| Train | 1,208 | 1,210 | 208 | 1,537 |
| Validation | 806 | 806 | 54 | 950 |
| Test | 751 | 751 | 2 | 963 |

The dataset was exported from Roboflow and later extended with additional images. The original Roboflow README indicates 2,509 images, while the local workspace contains 2,765 images across the train, validation, and test splits. This suggests that extra images, including hard negatives and extracted frames, were added after the initial export.

During inspection, one corrupted label file was identified. The file contained JavaScript text instead of YOLO bounding box annotations. Two orphan label files were also present without matching image files. These quality issues should be cleaned before future training runs to prevent training errors or unreliable results.

#### 6.3.2 Model Selection

YOLOv8 was selected because it is designed for real-time object detection and is easy to train using custom datasets. YOLO models are suitable for detecting fire because they can localize the fire region in each frame and return confidence scores. Confidence scores are useful for filtering uncertain detections.

The model was trained using 640 x 640 image size. The project contains multiple trained runs, including `FINAL_FIRE`, `FINAL_FIRE_V2`, and `FINAL_FIRE_V3_AND151NEG_V1`. The system also stores pretrained weights such as `yolov8s.pt` and `yolo11n.pt`.

#### 6.3.3 Training Approach

The training process used the YOLO training pipeline. The dataset configuration file defines the training, validation, and test image directories and class names. Model training produces output files such as:

- `best.pt`
- `last.pt`
- `results.csv`
- `results.png`
- precision, recall, F1, and PR curves
- confusion matrices
- labelled validation prediction images

The best model is selected based on validation metrics, especially mAP@50 and mAP@50-95.

#### Table 4. Model training configuration

| Parameter | Value |
| --- | --- |
| Task | Object detection |
| Model family | YOLOv8 |
| Image size | 640 |
| Number of classes | 1 |
| Class name | fire |
| Batch size | 16 |
| Optimizer | Automatic optimizer selection |
| Main metric | mAP@50 and mAP@50-95 |
| Deployment weights | `best.pt` |

#### 6.3.4 Real-Time Detection Method

Real-time detection is performed by capturing frames from a video source using OpenCV. The video source may be a webcam, a local video file, or an RTSP stream. Each frame is passed to the YOLO model. The model returns bounding boxes, confidence scores, and class information.

The basic detection flow is:

1. Open the video source.
2. Read a frame.
3. Run YOLO inference on the frame.
4. Filter detections using confidence threshold.
5. Apply temporal filtering.
6. Draw bounding boxes on the frame.
7. Update dashboard status.
8. Save incident snapshot if alarm condition is met.
9. Store incident record in SQLite.

#### 6.3.5 False Positive Reduction

False positives are a serious concern in fire detection. The project uses several methods to reduce them:

1. Hard negative images are included in the dataset.
2. Confidence thresholds are used to ignore weak detections.
3. Temporal filtering is applied to avoid alarms from single-frame errors.
4. Incident cooldown logic can prevent repeated alarms for the same event.
5. The dashboard allows monitoring and adjustment of threshold settings.

This approach balances sensitivity and reliability. A lower threshold may detect fire earlier but can increase false alarms. A higher threshold may reduce false alarms but can miss small or early fire events.

### 6.4 System Architecture

The system architecture contains five main layers:

1. Data layer
2. Model layer
3. Video processing layer
4. Backend/API layer
5. Frontend monitoring layer

#### Figure 1. General workflow of the AI-based fire detection system

This figure would show the flow from camera input to frame capture, model inference, temporal filtering, alert decision, incident logging, and dashboard visualization.

#### Figure 2. YOLOv8 fire detection pipeline

This figure would show an input video frame entering the YOLOv8 model, followed by bounding box prediction, confidence scoring, non-maximum suppression, and final fire localization.

#### Figure 3. System architecture showing dataset, model, backend, database, and dashboard

This figure would show the dataset and training process producing a model file. The trained model is loaded by the FastAPI backend. OpenCV supplies video frames to the backend. SQLite stores incident records. The frontend dashboard communicates with backend API endpoints and displays real-time results.

#### 6.4.1 Data Layer

The data layer contains the image dataset and YOLO label files. The `data.yaml` file describes the dataset structure and class names. Images are stored in `train/images`, `valid/images`, and `test/images`. Labels are stored in matching `labels` directories.

#### 6.4.2 Model Layer

The model layer contains trained YOLO weights. The most important deployment file is usually `best.pt`, which represents the best-performing model checkpoint according to validation results. The model receives an image frame and returns detections.

#### 6.4.3 Video Processing Layer

OpenCV is used to access the video source. It handles webcam input, frame reading, frame resizing when needed, and frame output for display. OpenCV is also used to save incident snapshots as image files.

#### 6.4.4 Backend/API Layer

The backend is implemented using FastAPI. It loads the YOLO model, starts the detection process, manages system state, stores incident records, and exposes API endpoints. It also serves the web dashboard and video stream.

The backend includes:

- model loading
- detection worker
- video feed generation
- settings management
- incident database operations
- status endpoint
- camera source handling

#### 6.4.5 Database Layer

SQLite is used for local incident logging. Each incident record stores information such as timestamp, confidence score, and snapshot path. SQLite is appropriate for this prototype because it is lightweight and does not require a separate database server.

#### 6.4.6 Frontend Layer

The frontend is a browser-based dashboard using HTML, CSS, and JavaScript. It displays the video feed, system status, confidence information, performance statistics, and incident history. JavaScript is used to call backend APIs and update the interface dynamically.

#### Figure 4. Real-time monitoring dashboard layout

This figure would show the main dashboard components: live video area, status indicator, confidence chart, settings panel, incident list, and system performance information.

### 6.5 Implementation

The implementation combines machine learning, backend development, frontend development, and database management.

#### 6.5.1 Project Structure

The main workspace contains:

```text
continuous_fire.v1-new-dataset.yolov8/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
├── runs/
│   └── detect/
│       ├── FINAL_FIRE/
│       ├── FINAL_FIRE_V2/
│       └── FINAL_FIRE_V3_AND151NEG_V1/
├── extract_mov_frames.py
├── live_alarm_add_morepics.py
├── yolov8s.pt
└── yolo11n.pt
```

The `runs/detect/FINAL_FIRE` folder also contains the FastAPI application, frontend files, settings file, incident database, model weights, and snapshots.

#### 6.5.2 Technologies Used

#### Table 2. Main tools and technologies used

| Technology | Purpose |
| --- | --- |
| Python | Main programming language |
| YOLOv8 / Ultralytics | Fire object detection |
| OpenCV | Video capture and frame processing |
| FastAPI | Backend web framework |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Dashboard interactivity |
| SQLite | Incident logging |
| Uvicorn | ASGI server for FastAPI |
| Roboflow | Dataset export and annotation format |

#### 6.5.3 Dataset Configuration

The dataset configuration file defines one class:

```yaml
nc: 1
names: ['fire']
```

The dataset paths should point to the local image split directories. For a project executed from the workspace root, the correct structure should be:

```yaml
train: train/images
val: valid/images
test: test/images
```

If the paths are set as parent directories, such as `../train/images`, training may fail unless the command is executed from a different folder. Therefore, dataset path consistency is important.

#### 6.5.4 Model Training

YOLO training uses the dataset configuration and a starting weight file. During training, the model learns to predict bounding boxes around fire regions. The training process saves model checkpoints. The `best.pt` checkpoint is used for deployment because it represents the best validation performance.

Training outputs include visual plots. These help evaluate whether the model is improving, overfitting, or struggling with validation data.

#### Figure 6. Example training and validation result plots

This figure would show loss curves, precision curves, recall curves, mAP curves, and confusion matrix outputs generated by YOLO training.

#### 6.5.5 Live Alarm Script

The standalone live alarm script uses OpenCV and YOLO to detect fire from a webcam. The script:

1. Loads the YOLO model.
2. Opens the camera source.
3. Reads frames continuously.
4. Runs prediction on each frame.
5. Draws detection boxes.
6. Saves alarm frames when fire is detected.
7. Plays a beep sound on Windows.
8. Allows the user to quit using the Q key.

This script is useful for quick testing without the full web dashboard.

#### 6.5.6 FastAPI Backend

The FastAPI backend provides a more complete deployment structure. It serves the dashboard and manages the detection pipeline. Important backend responsibilities include:

- loading the YOLO model
- processing frames in a detection worker
- saving snapshots
- logging incident records
- serving the video feed
- returning status information
- receiving settings updates
- managing camera sources

#### Table 6. Backend API endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Open main dashboard |
| `/login` | GET | Display login page |
| `/login` | POST | Authenticate user |
| `/logout` | GET | End session |
| `/video_feed` | GET | Stream annotated video |
| `/api/settings` | POST | Update threshold, model path, contact settings, and camera source |
| `/api/status` | GET | Return current detection and system status |
| `/api/incidents` | GET | Return incident history |
| `/api/incidents/{incident_id}` | DELETE | Delete an incident |
| `/api/cameras` | GET | List available cameras |

#### 6.5.7 Incident Logging

When the system detects fire above the configured threshold and temporal conditions are satisfied, it saves a snapshot and inserts a record into the SQLite database. The incident table stores:

- incident ID
- timestamp
- confidence score
- snapshot path

This allows the dashboard to display historical alerts and gives the user visual evidence of detected events.

#### Figure 5. Incident logging and alert flow

This figure would show detection confidence passing through threshold and temporal filtering. If the alarm condition is met, the system saves a snapshot, stores a database record, updates the dashboard, and triggers notification logic.

#### 6.5.8 Frontend Dashboard

The frontend dashboard is implemented with HTML, CSS, and JavaScript. It displays the system in a form that is understandable to users. The dashboard includes:

- live video feed
- fire detection status
- confidence display
- system performance information
- settings form
- incident list
- alert overlay
- snapshot display

JavaScript updates the interface by requesting status and incident data from the backend. The dashboard is important because a detection system must communicate clearly with the user. It should not only detect fire internally; it should also show what is happening in real time.

#### 6.5.9 Temporal Filtering

Temporal filtering reduces false alarms by requiring persistence across time. Instead of immediately declaring a fire from a single detection, the system can check whether detections continue over several frames or within a short time window. This is useful because false positives may occur briefly due to camera noise, reflections, or movement.

A simple temporal filtering strategy is:

```text
if fire confidence is above threshold for N frames within T seconds:
    trigger alarm
else:
    continue monitoring
```

The advantage is fewer false alarms. The disadvantage is a small delay before triggering an alarm. The value of `N` and `T` must be selected carefully.

#### 6.5.10 Alert Handling

The system supports real-time alerts and monitoring. The prototype includes visual dashboard alerts, incident snapshots, local alarm behaviour, and support for external notification logic such as email or SMS. In a production system, these alerts should be carefully tested to avoid alert fatigue and ensure that emergency messages are sent only when needed.

#### 6.5.11 Functional Requirements

Functional requirements describe what the system must do. The main functional requirements of the proposed system are:

1. The system shall capture frames from a webcam, video source, or RTSP camera stream.
2. The system shall load a trained YOLO fire detection model.
3. The system shall detect fire regions in real-time video frames.
4. The system shall display annotated video frames on a web dashboard.
5. The system shall allow the confidence threshold to be configured.
6. The system shall reduce false alarms using temporal filtering and alert cooldown logic.
7. The system shall save snapshots when a fire incident is detected.
8. The system shall store incident records in a SQLite database.
9. The system shall provide API endpoints for status, settings, incidents, video feed, and camera information.
10. The system shall allow users to view recent fire incidents through the dashboard.

#### 6.5.12 Non-Functional Requirements

Non-functional requirements describe quality expectations such as performance, reliability, usability, and security.

#### Table 8. Functional and non-functional requirements

| Requirement type | Requirement | Description |
| --- | --- | --- |
| Functional | Fire detection | Detect visible fire in video frames using YOLOv8 |
| Functional | Video monitoring | Display live or near-real-time camera output |
| Functional | Incident logging | Save timestamp, confidence, and snapshot path |
| Functional | Settings management | Allow threshold, model path, and camera source configuration |
| Functional | Alert handling | Trigger visual/audio/notification logic when fire persists |
| Non-functional | Performance | Maintain usable frame rate for real-time monitoring |
| Non-functional | Reliability | Continue monitoring unless camera or model loading fails |
| Non-functional | Usability | Provide a clear dashboard for non-technical users |
| Non-functional | Maintainability | Keep dataset, model, backend, frontend, and database logically separated |
| Non-functional | Security | Protect dashboard access and keep credentials outside source code |

#### 6.5.13 Database Design

The database design is intentionally simple because the prototype only needs to store incident history. SQLite was selected because it is lightweight, local, and easy to integrate with Python. The main table is `incidents`. Each record represents one confirmed fire event. The database fields are:

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | Integer | Unique incident identifier |
| `timestamp` | DateTime | Time when the incident was logged |
| `confidence` | Real | Highest fire detection confidence for the incident |
| `snapshot_path` | Text | File path of the saved incident image |

The database supports traceability because users can review when an alarm occurred and inspect the corresponding snapshot. In a larger system, the schema could be expanded with camera ID, location, event severity, user acknowledgement status, and notification delivery status.

### 6.6 Empirical Study / Results

The empirical study evaluates the trained YOLO fire detector using validation metrics from the training runs. The main metrics are precision, recall, mAP@50, and mAP@50-95.

Precision measures how many predicted fire detections are correct. High precision means fewer false positives.

Recall measures how many true fire objects are detected. High recall means fewer missed fires.

mAP@50 measures mean average precision using an IoU threshold of 0.50. mAP@50-95 is stricter because it averages over multiple IoU thresholds from 0.50 to 0.95.

#### Table 5. Validation performance summary

| Training run | Best observed epoch | Precision | Recall | mAP@50 | mAP@50-95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| FINAL_FIRE | 119 | 0.89259 | 0.80477 | 0.89284 | 0.65729 |
| Nested FINAL_FIRE_V3 | 28 | 0.92396 | 0.81789 | 0.91241 | 0.67604 |
| FINAL_FIRE_V3_AND151NEG_V1 | 20 | 0.89136 | 0.82051 | 0.89562 | 0.66020 |

The best observed validation result was from the nested `FINAL_FIRE_V3` run, with mAP@50 of approximately 0.912 and mAP@50-95 of approximately 0.676. The `FINAL_FIRE_V3_AND151NEG_V1` run achieved slightly lower mAP but similar recall. Since this run included additional hard negatives, it may be more conservative in some real-world cases even if its validation mAP is lower.

#### 6.6.1 Interpretation of Results

The results show that YOLOv8 can detect fire with useful accuracy in the available dataset. A mAP@50 above 0.89 indicates that the detector can correctly localize many fire objects under validation conditions. The recall values around 0.82 indicate that most fire instances are detected, but some are still missed. This is important for safety, because missed fire detections can be serious.

Precision values around 0.89 to 0.92 suggest that false positives are reduced but not eliminated. This is expected because fire-like visual patterns are common. The use of hard negative data and temporal filtering is therefore necessary for practical deployment.

#### 6.6.2 Observed Strengths

The system has several strengths:

1. It can perform real-time visual fire detection.
2. It uses a modern object detector suitable for video processing.
3. It provides visual evidence through snapshots.
4. It stores incident records in a local database.
5. It includes a monitoring dashboard.
6. It considers false positives using hard negative examples.
7. It can be extended to webcams or RTSP streams.

#### 6.6.3 Observed Limitations

The system also has limitations:

1. It depends on camera visibility. Smoke or obstacles can block the fire.
2. It may still confuse fire with lights or reflections.
3. Performance depends on dataset quality and diversity.
4. Validation metrics do not guarantee identical performance in real-world deployment.
5. The prototype should not replace certified fire safety systems.
6. Some dataset label issues need cleaning before further training.
7. Security features need improvement before production deployment.

#### 6.6.4 Dataset Quality Findings

Dataset inspection found that the dataset contains both valid labels and empty labels for negative examples. This is useful. However, one corrupted label file was found, and two label files had no matching image. These issues should be fixed because object detection training expects label files to contain only valid YOLO annotation lines. Dataset cleaning is a critical step in machine learning projects.

#### 6.6.5 Testing and Validation

Testing was considered at both the machine learning level and the software system level. Model validation used YOLO metrics such as precision, recall, mAP@50, and mAP@50-95. System validation focused on whether the application could load the model, process video frames, display the dashboard, save incidents, and return API responses correctly.

#### Table 9. Testing and validation cases

| Test case | Expected result | Status |
| --- | --- | --- |
| Load trained YOLO model | Model loads without error and is ready for inference | Passed in project runs |
| Open webcam/video source | Camera stream opens and frames are read continuously | Supported by OpenCV implementation |
| Fire frame detection | Fire is detected and bounding boxes are displayed | Supported by validation outputs |
| Non-fire hard negative frame | Lights/reflections should not immediately trigger alarm | Addressed through hard negatives and temporal filtering |
| Incident logging | Snapshot path, timestamp, and confidence are stored in SQLite | Implemented in backend |
| Dashboard loading | User can open the web dashboard and view monitoring panels | Implemented in frontend |
| API status request | Backend returns current system state | Implemented through `/api/status` |
| Incident history request | Backend returns stored incident records | Implemented through `/api/incidents` |
| Threshold update | New threshold changes detection sensitivity | Implemented through `/api/settings` |
| Dataset integrity check | Labels must match images and contain valid YOLO rows | Needs cleanup before future training |

#### Figure 7. Examples of hard negative images such as lights and reflections

This figure would show non-fire images that contain bright or orange regions. These examples help train the model to avoid classifying lights, reflections, or sky glow as fire.

### 6.7 Discussion

The project demonstrates that an AI-based visual fire detection system can be built using accessible tools and a clear software architecture. YOLOv8 provides the detection capability, while OpenCV handles real-time frame capture. FastAPI organizes the backend into endpoints and services. SQLite provides a simple local incident database. The frontend dashboard allows users to observe system behaviour in real time.

One of the most important design decisions is the use of hard negative images. A model trained only on clear fire images may perform well in controlled tests but fail when exposed to lights, reflections, sunlight, or other fire-like objects. By adding hard negatives, the model learns a more realistic boundary between fire and non-fire. This is especially important in surveillance environments where many bright objects may appear.

Temporal filtering is another important design decision. A single-frame detection should not always trigger a serious alarm. In a real system, false alarms can reduce trust and cause users to ignore future alerts. Temporal filtering improves reliability by requiring detections to persist over time. However, this creates a trade-off. If the filter is too strict, the system may respond late. If it is too weak, false alarms may remain frequent. The best settings depend on the deployment environment.

The project also shows that machine learning performance metrics must be interpreted carefully. The best validation mAP does not always mean the best real-world performance. A model with slightly lower mAP but better resistance to false positives may be preferable for deployment. Therefore, future evaluation should include controlled real-world scenarios, such as lamps, sunlight, smoke, small fires, large fires, and camera movement.

The dashboard is valuable because AI detection systems need transparency. Users should be able to see the video feed, confidence level, incident snapshots, and current system state. Without a clear interface, even a strong model may be difficult to use. The incident log also supports auditing and later review.

Security and privacy should be considered in future versions. Camera feeds and incident snapshots may contain sensitive information. Authentication, secure environment variable management, access controls, and safe storage should be improved before deployment outside a controlled environment.

#### Table 7. Risks, limitations, and mitigation strategies

| Risk or limitation | Impact | Mitigation |
| --- | --- | --- |
| False positives from lights/reflections | Unnecessary alarms | Add hard negatives, raise threshold, apply temporal filtering |
| Missed small fire | Safety risk | Add more early-stage fire examples, tune recall, test in real scenes |
| Poor camera angle | Fire may not be visible | Use multiple cameras and good placement |
| Low light or overexposure | Reduced detection accuracy | Improve camera quality and training diversity |
| Dataset label errors | Poor training quality | Run dataset validation before training |
| Slow hardware | Low FPS | Use smaller model, GPU, or edge-optimized export |
| Weak authentication | Security risk | Use stronger passwords, HTTPS, and secure sessions |
| Alert fatigue | Users ignore alarms | Use cooldowns, severity levels, and confirmation logic |

### 6.8 Conclusion & Future Work

This project developed an Artificial Intelligence-Based Fire Detection System using YOLOv8, OpenCV, FastAPI, HTML/CSS/JavaScript, and SQLite. The system detects fire from video frames, displays results through a web dashboard, logs incidents, and supports alert workflows. The project demonstrates that a modern object detection model can be integrated into a practical real-time monitoring system.

The trained model achieved strong validation results, with the best observed run reaching approximately 0.912 mAP@50 and 0.676 mAP@50-95. These results show that the model can detect many fire objects correctly in the validation dataset. The project also highlights the importance of hard negative examples and temporal filtering for reducing false alarms.

The system has practical value as a prototype. It can be used for research, demonstration, and further development. However, it should not be treated as a replacement for certified fire alarm systems. A production version would require more testing, better security, stronger deployment procedures, and compliance with safety standards.

Future work should focus on:

1. Cleaning and validating all dataset labels.
2. Adding more hard negative examples from real environments.
3. Adding smoke detection as a second class.
4. Testing the system on CCTV, RTSP, and edge devices.
5. Exporting the model to ONNX or TensorRT for faster inference.
6. Improving temporal filtering with event-based confidence smoothing.
7. Adding role-based authentication and HTTPS.
8. Improving alert delivery through email, SMS, and mobile notifications.
9. Evaluating the system in controlled real-world fire and non-fire scenarios.
10. Creating a deployment guide for low-cost hardware such as NVIDIA Jetson or Raspberry Pi with acceleration.

## 7. References

Bochkovskiy, A., Wang, C.-Y., & Liao, H.-Y. M. (2020). YOLOv4: Optimal speed and accuracy of object detection. *arXiv*. https://arxiv.org/abs/2004.10934

Bradski, G. (2000). The OpenCV library. *Dr. Dobb's Journal of Software Tools*.

GeeksforGeeks. (n.d.). SQLite using Python. Retrieved April 26, 2026, from https://www.geeksforgeeks.org/python-sqlite/

Lin, T.-Y., Goyal, P., Girshick, R., He, K., & Dollar, P. (2017). Focal loss for dense object detection. *Proceedings of the IEEE International Conference on Computer Vision*, 2980-2988. https://doi.org/10.1109/ICCV.2017.324

Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You only look once: Unified, real-time object detection. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 779-788. https://doi.org/10.1109/CVPR.2016.91

Roboflow. (2026). *continuous_fire dataset*. Roboflow Universe. https://universe.roboflow.com/fire-detection-2xe3o/continuous_fire-0shcw

Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L.-C. (2018). MobileNetV2: Inverted residuals and linear bottlenecks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 4510-4520. https://doi.org/10.1109/CVPR.2018.00474

Tiangolo. (n.d.). *FastAPI documentation*. Retrieved April 26, 2026, from https://fastapi.tiangolo.com/

Ultralytics. (n.d.). *Ultralytics YOLO documentation*. Retrieved April 26, 2026, from https://docs.ultralytics.com/

Viola, P., & Jones, M. (2001). Rapid object detection using a boosted cascade of simple features. *Proceedings of the IEEE Computer Society Conference on Computer Vision and Pattern Recognition*, 1, I-511-I-518. https://doi.org/10.1109/CVPR.2001.990517

## 8. Appendix

### Appendix A. Dataset Details

The dataset is arranged in YOLO format:

```text
train/images
train/labels
valid/images
valid/labels
test/images
test/labels
```

Each image should have a matching `.txt` label file with the same base filename. Negative images should have empty label files.

Example YOLO label:

```text
0 0.5123 0.4812 0.2200 0.3100
```

The values represent:

| Field | Meaning |
| --- | --- |
| `0` | Class ID for fire |
| `0.5123` | Normalized x-center |
| `0.4812` | Normalized y-center |
| `0.2200` | Normalized width |
| `0.3100` | Normalized height |

### Appendix B. Dataset Configuration

Recommended local `data.yaml`:

```yaml
train: train/images
val: valid/images
test: test/images

nc: 1
names: ['fire']
```

### Appendix C. Example YOLO Training Command

```bash
yolo detect train model=yolov8s.pt data=data.yaml epochs=50 imgsz=640 batch=16 name=fire_detection_training
```

### Appendix D. Example Validation Command

```bash
yolo detect val model=runs/detect/FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt data=data.yaml imgsz=640
```

### Appendix E. Simplified Real-Time Detection Code

```python
import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/FINAL_FIRE_V3_AND151NEG_V1/weights/best.pt")
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model.predict(frame, conf=0.4, verbose=False)
    annotated = results[0].plot()

    cv2.imshow("AI Fire Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

### Appendix F. Temporal Filtering Pseudocode

```python
fire_counter = 0
required_frames = 3
threshold = 0.75

if highest_fire_confidence >= threshold:
    fire_counter += 1
else:
    fire_counter = 0

if fire_counter >= required_frames:
    trigger_alarm()
    save_snapshot()
    log_incident()
```

### Appendix G. SQLite Incident Table

```sql
CREATE TABLE incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    confidence REAL,
    snapshot_path TEXT
);
```

### Appendix H. API Endpoint Summary

```text
GET     /
GET     /login
POST    /login
GET     /logout
GET     /video_feed
POST    /api/settings
GET     /api/status
GET     /api/incidents
DELETE  /api/incidents/{incident_id}
GET     /api/cameras
```

### Appendix I. Example System Requirements

```text
fastapi
uvicorn
ultralytics
opencv-python
sse-starlette
psutil
python-multipart
twilio
python-dotenv
starlette
```

### Appendix J. Recommended Dataset Cleaning Checklist

1. Confirm every image has a matching label file.
2. Confirm every label file has a matching image.
3. Confirm label files contain only YOLO annotation rows.
4. Confirm all class IDs are valid.
5. Confirm bounding box values are between 0 and 1.
6. Remove stale `labels.cache` files after changing labels.
7. Re-run validation after cleaning.

### Appendix K. Suggested Future Model Improvements

1. Train with more diverse indoor, outdoor, industrial, and night-time scenes.
2. Add smoke as a second class.
3. Add more hard negatives such as lamps, reflections, welding, traffic lights, and sunsets.
4. Test multiple model sizes for speed and accuracy.
5. Export the model to ONNX or TensorRT.
6. Compare YOLOv8 with newer YOLO versions using the same dataset.
