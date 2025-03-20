# ⚡ AI-Powered Danger Zone Monitoring System 🚀

> **Real-time worker safety monitoring using AI & Computer Vision**  
> **Detects workers in hazardous zones & issues instant alerts**  

![Demo](assets/demo.gif)  <!-- Replace with actual demo image or GIF -->

---

## 🧠 **Overview**
This **AI-powered danger zone monitoring system** enhances **workplace safety** by:  
✅ Detecting workers in **real-time** using **YOLOv8**  
✅ Mapping **danger zones** with **polygon-based detection**  
✅ Issuing **alerts** when workers enter restricted areas  
✅ Enabling **customizable zones** for dynamic safety measures  

Used in **construction sites, factories, and industrial zones** to **reduce accidents and improve safety**.  

---

## 🎯 **Key Features**
🔹 **Real-time worker detection** using **YOLOv8**  
🔹 **Polygon-based danger zones** for flexible area marking  
🔹 **Live video processing** with alerts on hazardous entry  
🔹 **Optimized for speed** using **GPU acceleration**  
🔹 **Django-based web interface** with **Konva.js** for easy zone setup  

---

## 📸 **Demo**
![Danger Zone Monitoring](assets/demo.png)  <!-- Replace with actual demo image -->

---

## 🛠️ **Tech Stack**
| Component        | Technology |
|-----------------|------------|
| **Model**       | YOLOv8 (Ultralytics) |
| **Backend**     | Django, OpenCV |
| **Frontend**    | Konva.js, JavaScript |
| **Polygon Processing** | Shapely (for area detection) |
| **GPU Acceleration** | PyTorch (CUDA support) |

---

## 🚀 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/DangerZoneMonitoring.git
cd DangerZoneMonitoring
