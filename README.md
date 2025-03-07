# Real Time Flood Monitoring
Basic web tool built with a Django backend to interact with the 
Real Time flood-monitoring API (https://environment.data.gov.uk/flood-monitoring/doc/reference) 
provided by the Environmental Agency.
---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- Python (>= 3.x)
- pip
- Virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```sh
   git clone [https://github.com/<url>](https://github.com/DanHamer1996/real-time-flood-monitor.git)
   cd real-time-flood-monitor
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv  
   source venv/bin/activate  # On macOS/Linux  
   venv\Scripts\activate  # On Windows  
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt  
   ```

---

## 🛠 Usage
- ```sh
   python manage.py runserver
   ```
- Visit `http://127.0.0.1:8000/` in your browser. 

---

## Example Usage
An API feeds station data into the select dropdown:
![image](https://github.com/user-attachments/assets/293882de-d0a2-43ac-a042-7900e52ef658)

On select, an API call is made to return the last 24 hours readings for the selected station. This is displayed in the chart & associated table:
![image](https://github.com/user-attachments/assets/b76f165e-8f22-4552-b981-32f51d1a39af)

User can select further stations and the data will refresh:
![image](https://github.com/user-attachments/assets/289f232a-4db0-432b-a3f7-de83b927ab63)

![image](https://github.com/user-attachments/assets/7ad7d84d-8f1d-46a9-85aa-d4bad5e9a76b)



