# Detection-Of-Fake-Wifi-Points
A deep learning–based Wi-Fi intrusion detection system that detects abnormal network behavior and classifies known attacks in real time. It identifies fake access points that impersonate real networks, protecting users from credential theft and zero-day threats through an intelligent, web-based interface.
# 🧠 Smart Wi-Fi Intrusion Detection System using Deep Learning



## 📘 Overview

Wi-Fi networks are widely used everywhere — in homes, colleges, airports, and cafés — but they remain vulnerable to **fake access points (Evil Twins)** that impersonate real networks and steal user credentials.  
Traditional intrusion detection systems (IDS) fail against **zero-day or unknown attacks**, which follow no known pattern.

This project proposes a **two-stage deep learning–based system** capable of detecting both known and unknown Wi-Fi attacks in real time through a web-based interface.

---

## ⚙️ Problem Statement

Existing Wi-Fi IDS solutions:
- ❌ Fail to detect zero-day or unseen attacks  
- ⚠️ Cannot distinguish between real and fake access points  
- 🧩 Lack real-time adaptability  

### ✅ Objectives
- Detect **abnormal Wi-Fi behavior** using unsupervised deep learning  
- Accurately **classify known attack types**  
- Build a **real-time web dashboard** for monitoring and alerts  

---

## 🧩 System Architecture

### 🔹 Stage 1 — **Anomaly Detection (Autoencoder / VAE)**
- Trained only on **normal traffic**
- Learns the latent representation of normal Wi-Fi behavior  
- High reconstruction error → potential anomaly  
- Detects **zero-day or unknown attacks**  

### 🔹 Stage 2 — **Attack Classification (CNN–BiLSTM)**
- Operates on anomalous traffic flagged by Stage 1  
- **CNN** extracts spatial (packet-level) features  
- **BiLSTM** captures temporal (sequence) dependencies  
- Classifies samples into **13 known attack types**  

---

## 🧮 Dataset Details

**Dataset:** [Aegean Wi-Fi Intrusion Dataset v3 (AWID3)](https://icsdweb.aegean.gr/awid/)  
- 🧾 **~2.6 million** Wi-Fi frames  
- ⚙️ **155+ features** (signal stats, duration, MACs, retry count, etc.)  
- 🕵️‍♂️ **Classes:** Normal + Multiple attack types  
- 🧰 **Attack examples:** Evil Twin, Deauthentication, Authentication Flood, Probe Flood, Rogue AP, Krack, Kr00k, Botnet, SQL Injection, Website Spoofing, etc.  
- 📈 Used to train and evaluate both stages  

---

## 📊 Model Workflow

| Stage | Model | Input | Output | Purpose |
|-------|--------|--------|---------|----------|
| 1 | Autoencoder / VAE | Normal traffic | Reconstruction error | Detect anomalies |
| 2 | CNN-BiLSTM | Anomalous traffic | Attack label | Classify attack type |

---

## 🖥️ Tech Stack

**Frontend:** React.js, Bootstrap, Chart.js  
**Backend:** Flask (Python)  
**Database:** MySQL  
**Libraries:** TensorFlow, Keras, Pandas, Scikit-learn  

The web app allows:
- Real-time visualization of network status  
- Upload of traffic data for live analysis  
- Display of detected attacks with probability and timestamp  

---

## 📈 Evaluation Metrics

- **Accuracy**  
- **Precision**  
- **Recall**  
- **F1-Score**

The models are validated on AWID3 and UNSW-NB15 benchmark datasets to ensure reliability.

---

## 🔐 Security Recommendations

- Use trusted **VPNs** to encrypt data traffic  
- Regularly **update routers and devices**  
- Enable **MAC address filtering**  
- Deploy **honeypot networks** to detect attackers  
- Connect only to **WPA3-secured** networks  

---

## 📚 References
1. C. Hamroun *et al.*, *“Intrusion detection in 5G and Wi-Fi networks,”* IEEE Access, 2025.  
2. G. Yin *et al.*, *“Evasion attacks and countermeasures in deep learning–based Wi-Fi gesture recognition,”* IEEE TMC, 2025.  
3. F. Palmese & A. Redondi, *“Collecting CSI in Wi-Fi APs for IoT forensics,”* arXiv:2305.10554, 2023.  
4. M. Cunha *et al.*, *“Fingerprinting users from Wi-Fi data in mobile devices,”* ACM SAC, 2025.

---


