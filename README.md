
---
# 🌊 Diving Gesture Recognition in VR

**XR P3 Studio 3 · University of Michigan EECS 440**

> **Learn scuba diving hand signals safely, intuitively, and immersively — powered by VR, hand tracking, and machine learning.**

---

## ✨ Overview

**Diving Gesture Recognition in VR** is an immersive XR training system that teaches scuba diving hand signals using real-time hand tracking and machine learning-based gesture classification.

Scuba diving relies heavily on non-verbal communication. Memorizing gestures is difficult, and mistakes underwater can be life-threatening. Our project provides a **safe, at-home VR environment** where users can build muscle memory and receive instant feedback *before* ever touching the water.

---

## 🎯 Motivation

### The Problem

* **Cognitive Load:** Scuba gestures are hard to memorize all at once during stressful initial dives.
* **Safety Risks:** Miscommunication underwater is a leading cause of diver panic or accidents.
* **Static Learning:** Traditional manuals lack the interactive, real-time feedback needed to perfect hand positioning.

### Our Solution

By leveraging **AI-powered gesture detection**, we:

* 🌍 Make scuba diving knowledge accessible globally.
* 🧠 Help learners build physical muscle memory through repetition.
* 🏊 Bridge the gap between classroom theory and open-water practice.

---

## 🖐️ Supported Gestures

The system currently recognizes core scuba gestures and supports **contextual combinations** (e.g., *Question + Up* → "Should we ascend?").

| Gesture | Meaning | Visual Context |
| --- | --- | --- |
| **OK** | Confirm safety / "Are you OK?" | Thumb and index form a circle. |
| **Go This Direction** | Indicate movement direction | Pointing with a flat hand or index. |
| **Question** | Prefix for yes/no questions | A specific palm-up or side-tilt signal. |

---

## 🧠 System Architecture

The pipeline bridges the gap between high-fidelity XR rendering in Unreal Engine and high-speed inference in Python.

### Technical Workflow

1. **Meta Quest Hand Tracking:** Captures 26 joints per hand using OpenXR.
2. **Unreal Engine (UE 5.2.1):** Extracts joint coordinates per frame.
3. **TCP Socket Communication:** Streams raw joint data to the ML server.
4. **Keras ML Classifier:** Processes the features and predicts the gesture.
5. **UI Feedback:** Unreal displays the recognized gesture and provides instructional guidance.

---

## 🧬 Technical Implementation

### Hand Tracking & Feature Engineering

* **Joint Extraction:** Tracks 26 joints per hand (Point, Pinch, Drag, Palm).
* **Normalization:** Feature vectors are normalized to a (-1, 1) range.
* **Translation Invariance:** Joint 0 (Wrist) is anchored at the origin to ensure gestures are recognized regardless of where the user's hand is in 3D space.

### Machine Learning Model

* **Framework:** Keras with TensorFlow backend.
* **Architecture:** Sequential fully-connected network with optimized **Dropout layers (20% - 40%)** to prevent overfitting.
* **Input:** x, y coordinates from 26 joints \rightarrow 52-dimensional feature vector.

---

## 📊 Results

We conducted two primary training trials to refine the system:

* **Trial 1:** Identified confusion between "OK" and "Question" signals. Led to improved data normalization.
* **Trial 2:** Achieved near-perfect classification accuracy. Refined the model to balance between high accuracy and "real-world" robustness to prevent overfitting.

> **Note:** We prioritize "Realism over Accuracy"—meaning the system is designed to reward correct form rather than just "getting close."

---

## 🛠️ Development Setup

### Prerequisites

* **Unreal Engine:** 5.2.1
* **Python:** 3.9+ (with `tensorflow`, `numpy`, and `socket` libraries)
* **Hardware:** Meta Quest 2, 3, or Pro (Link cable or AirLink recommended)

### Project Structure

```text
├── /Scenes            # VR Training environments
├── /Blueprints       # Hand tracking and Socket logic
├── /ML                # Python scripts
│   ├── /training      # Keras model definitions & datasets
│   └── /inference     # Real-time TCP listener
├── /Meshes            # Custom underwater assets
└── /Docs              # Presentation slides and research

```

---

## ⚠️ Limitations & Future Work

* **Current Constraints:** Slight latency in TCP communication and failure at extreme hand rotations.
* **Future Roadmap:** * Transition to **3D joint coordinates (x, y, z)** for better depth detection.
* Implement **Temporal Modeling (LSTMs)** to recognize motion-based gestures (e.g., "Out of Air").
* Add multi-player support for buddy-system practice.



---

## 👥 Team & Course

**Developed for EECS 440: XR P3 Studio 3**
**University of Michigan**

---

## 📜 License

This project is intended for educational use only.
© 2024 University of Michigan

---
