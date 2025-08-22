# 🚌 Bus Reservation System (Django Full Stack)

A full-stack **Django** project that allows users to register, book bus tickets and make secure payments via **Razorpay**.  
The project includes authentication with email otp  and phone number .
---

## 🚀 Features
- ✅ User registration, login
- ✅ Email and Phone number 
- ✅ Bus route management and seat reservation
- ✅ Interactive seat selection with availability
- ✅ Razorpay payment integration
- ✅ Profile with image upload (Pillow)
- ✅ Responsive UI with Bootstrap /font awesome JavaScript interactivity

---

## 🛠️ Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap, font awesome ,JavaScript  
- **Database:** SQLite(default) / Mysql (developed)  
- **Auth:** Email (OTP),phone (OTP)  
- **Payments:** Razorpay API  
- **Deployment Ready:** python anywhere 

---

## ⚙️ Setup Instructions

1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/bus-reservation.git
cd bus-reservation

2️⃣ Create Virtual Environment
```bash

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

4️⃣ Setup Environment Variables
```bash
cp .env

5️⃣ Run Migrations
```bash
python manage.py migrate

6️⃣ Create Superuser
```bash
python manage.py createsuperuser

7️⃣ Run Development Server
```bash
python manage.py runserver
Now visit http://127.0.0.1:8000/
