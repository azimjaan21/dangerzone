# ⚡ AI-Powered Danger Zone Monitoring System 🚀

> **Real-time worker safety monitoring using AI & Computer Vision**  
> **Detects workers in hazardous zones & issues instant alerts**  

![2025-03-2014-14-33-ezgif com-video-to-gif-converter+(1)](https://github.com/user-attachments/assets/00a7b22b-5cf0-4039-b091-11de38cc74da)

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
![image](https://github.com/user-attachments/assets/0ef38820-8299-4378-8478-11f49a3097cb)
![image](https://github.com/user-attachments/assets/93e66a1f-314d-4753-bfea-09c098730f2e)


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
```
### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
### **3️⃣ Run the Django Server**
```bash
python manage.py runserver
```
-------
**⚙️ Usage Guide**

🔹 Drawing & Saving Danger Zones
Open the web interface.

Click "Draw Polygon" to outline restricted areas.

Click "Save" to store the zones.

🔹 Worker Detection & Alerts

If a worker enters a danger zone, their bounding box turns RED and an alert appears.
If the worker is safe, their bounding box remains GREEN.


**🤝 Contributions & Support**

💡 Have ideas to improve this project? Feel free to contribute!

📧 For questions & code requests: azimjaan21@gmail.com

📌 GitHub Issues & PRs are welcome!
