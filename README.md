# ✈️ Flight Price Simulator & Dynamic Booking System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-Backend-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-purple)
![Stars](https://img.shields.io/github/stars/yourname/yourrepo?style=social)

A fully functioning **dynamic airline fare simulator and booking platform** built using **Django**, capable of real-time price fluctuation, seat tracking, flight listings, and booking confirmation pages.

It mimics real airline pricing strategies using time-to-departure, demand, remaining seats, and random market influence.

---

## 🌐 Live Demo (Optional)
> Add deployment link here  
Example: **https://your-flight-app.vercel.app/**

---

## 🚀 Features

### **🎨 Frontend**
- Search flights
- View dynamically changing prices
- Interactive booking flow
- Clean ticket/confirmation pages
- Template-based UI (Django Templates)

### **🖥️ Backend**
- Django-based pricing algorithm
- Auto seat assignment
- Booking storage & history
- Admin panel for managing flights
- Multiple debugging tools:
  - Inspect flights
  - Fix corrupted bookings
  - Price calculation tester
  - Booking table exploration

### **🧮 Dynamic Fare Algorithm Includes**
- Base price  
- Demand multiplier  
- Random market factor  
- Seasonal adjustments  
- Time-to-departure adjustment  
- Remaining seat penalty  

---

project/
│── core/ # Django settings
│── flights/ # Main business logic
│── flight_simulator/ # Backend helpers
│── static/ # CSS/JS/Images
│── templates/ # HTML templates
│── docs/ # Documentation (generated)
│── manage.py
│── requirements.txt
│── debug_*.py # Debug tools
│── fix_bookings.py


---

## 🛠 Installation

### 1. Clone Project
```bash
git clone <repo-url>
cd flight_simulator

**### 2. Create Virtual Environment**
```python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

## 📁 Project Structure

