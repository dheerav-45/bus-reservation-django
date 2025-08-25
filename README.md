# 🚌 QuickBus ,Bus Reservation System (Django Full Stack)

A full-stack **Django** project that allows users to register, book bus tickets and make secure payments via **Razorpay**.  
The project includes authentication with email otp  and phone number .
---

## 🚀 Features
- ✅ User registration, login ,logout
- ✅ Email and Phone number 
- ✅ Bus route management and seat reservation
- ✅ Interactive seat selection with availability
- ✅ Razorpay payment integration
- ✅ Profile with image upload (Pillow)
- ✅ Responsive UI with Bootstrap /font awesome JavaScript interactivity
- ✅ Email Notifications

---

## 🛠️ Tech Stack
- **Backend:** Django ,python
- **Frontend:** HTML, CSS, Bootstrap, font awesome ,JavaScript  
- **Database:** MySQL (configurable for SQLite)
- **Auth:** Email (OTP),phone (OTP)  
- **Payments:** Razorpay API
- **Gmail:** SMTP setup for notifications
- **Deployment Ready:** python anywhere 

---
🎯 Usage Guide

Open browser → thinkbuildgrow.pythonanywhere.com

**User Authentication**

Register as a new user or login with existing credentials.

Manage your profile (update name, email, password, and profile image).

**Search & Filter Buses**

Enter source, destination, and travel date to search available buses.

eg.kochi to bangalore date: 1/9/2025 

Apply filters:

Bus type (AC, Non-AC, Sleeper, Seater, etc.)

**View Bus & Route Details**

Click on a bus to view full details:

Bus operator

Route details with stops and timings

Available seats

Seat Selection & Booking

Choose seats from the interactive seat layout.

View total fare before confirming.

Proceed to secure payment via Razorpay.

Booking Confirmation

Once payment is successful, booking details are saved.

Download/print ticket (with QR code).

View booking history anytime in the dashboard.

Reviews & Ratings

After traveling, users can leave a review and rating for the bus/operator.

Helps other passengers in selecting quality services.

Profile Management

Update profile details and profile picture.

View personal booking history.

Manage saved payment preferences.

Admin Panel Features

Admin can add/update buses, routes, and other operators.

Manage all bookings and registered users.

View analytics (optional).

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

 
- ⚙️ **Others**
  - Secure `.env` configuration  
  - `.gitignore` for sensitive files  
  - Requirements file for easy setup
