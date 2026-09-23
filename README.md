\# 🍉 Fruit Ninja - Hand Gesture Controlled Game



A real-time \*\*hand gesture controlled Fruit Ninja game\*\* built with Python, OpenCV, MediaPipe, and Pygame.



Instead of using a mouse or keyboard to slice fruits, the player uses \*\*hand movements in front of a webcam\*\* to interact with the game.



\## 🎥 Demo



Watch the full gameplay demonstration on LinkedIn:



🔗 \*\*\[View Fruit Ninja Demo on LinkedIn](https://lnkd.in/p/gst7CUaY)\*\*



\## ✨ Features



\* ✋ Real-time hand tracking

\* 🎯 Finger-based fruit slicing

\* 📷 Webcam-based interaction

\* 🎮 Pygame-powered gameplay

\* 🍎 Random fruit generation

\* 💥 Collision detection for slicing

\* 🏆 Score and high-score tracking

\* ⚡ Real-time gesture interaction



\## 🧠 How It Works



The project combines \*\*computer vision and game development\*\* to turn hand movement into game controls.



```text

Webcam

&#x20;  ↓

OpenCV captures video

&#x20;  ↓

MediaPipe detects the hand

&#x20;  ↓

Finger position is extracted

&#x20;  ↓

Finger position is checked against fruits

&#x20;  ↓

Collision detected

&#x20;  ↓

Fruit is sliced

&#x20;  ↓

Score is updated

```



The webcam continuously captures video frames. MediaPipe detects the player's hand and identifies the finger position. The game uses this position to determine whether the player is interacting with a fruit.



\## 🛠️ Tech Stack



| Technology | Purpose                              |

| ---------- | ------------------------------------ |

| Python     | Core programming language            |

| OpenCV     | Webcam and video processing          |

| MediaPipe  | Hand tracking and landmark detection |

| Pygame     | Game engine, graphics and audio      |

| JSON       | High-score data storage              |



\## 🎮 Controls



| Action        | Control                         |

| ------------- | ------------------------------- |

| Slice fruit   | Move your finger across a fruit |

| Move cursor   | Move your hand                  |

| Game controls | Keyboard                        |



The main gameplay interaction is performed using \*\*hand gestures through the webcam\*\*.



\## 💻 Requirements



\* Python 3.10+

\* Webcam

\* Windows, Linux, or macOS

\* Internet connection for installing dependencies



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Sadhwi-ops/Fruit-Ninja-Hand-Gesture.git

cd Fruit-Ninja-Hand-Gesture

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



\*\*Windows:\*\*



```powershell

venv\\Scripts\\activate

```



\*\*Linux/macOS:\*\*



```bash

source venv/bin/activate

```



\### 4. Install dependencies



```bash

pip install opencv-python mediapipe pygame

```



\### 5. Run the game



```bash

python main.py

```



Allow webcam access when prompted.



\## 📁 Project Structure



```text

Fruit-Ninja-Hand-Gesture/

│

├── main.py

├── models/

│   └── hand\_landmarker.task

├── .gitignore

└── README.md

```



\## 🧩 Key Concepts



This project demonstrates practical implementation of:



\* Computer Vision

\* Hand Landmark Detection

\* Real-time Video Processing

\* Collision Detection

\* Coordinate Mapping

\* Object Movement

\* Game Event Handling

\* Score Management

\* File-based Data Storage



\## 🚀 Future Improvements



\* 🍉 Add more fruit types

\* 💣 Add bombs and power-ups

\* 🔪 Improve slicing effects and animations

\* 🏆 Add a leaderboard system

\* 🎨 Improve the game interface

\* 🔊 Add more interactive sound effects

\* ⚡ Improve hand-tracking performance

\* 🌐 Add online score tracking



\## 🎯 Project Goal



The goal of this project was to explore how \*\*computer vision can be combined with interactive game development\*\* to create a natural, touch-free gaming experience.



Instead of relying on traditional input devices, the project uses real-time hand tracking to create an interactive gameplay experience.



\## 👩‍💻 Author



\*\*Sadhwi\*\*



GitHub: \*\*\[@Sadhwi-ops](https://github.com/Sadhwi-ops)\*\*



\---



⭐ If you found this project interesting, consider giving the repository a star!



