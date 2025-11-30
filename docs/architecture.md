# 🏗 Architecture Overview

This project follows a modular Django-based architecture designed for clarity, scalability, and realistic flight-price simulation.

---

## 1. Application Layers

### **Presentation Layer**
- Located in:  
  `/templates/`  
  `/static/`
- Handles UI rendering, flight search pages, booking screens, and ticket output.
- Uses Django Template Engine for server-side rendering.

---

## **2. Business Logic Layer**
Located inside:
/flights/views.py
/flights/utils/

Responsibilities:
- Dynamic pricing engine  
- Booking validation  
- Seat allocation  
- Input sanitization  
- Real-time updates for fare calculation  

---

## **3. Data Layer**
Located in:
/flights/models.py
db.sqlite3


### **Models**
- **Flight** – route, schedule, base price, seats  
- **Booking** – passenger details, price paid, timestamp  

Django ORM is used for all database interaction.

---

## **4. Admin & Management Layer**
Django admin panel:
flights/admin.py

Allows adding flights, adjusting prices, and viewing booking logs.

---

## **5. Utility Tools**
Scripts:
debug_flights_script.py
debug_bookings.py
debug_booking_model.py
verify_api.py
fix_bookings.py

Used for:
- Inspecting pricing behavior  
- Validating system logic  
- Repairing database entries  

---

## **6. Request Flow**
User → View → Business Logic → ORM → Database → Rendered HTML Response

---

## **7. Tech Stack**
- Python 3.10+
- Django Framework
- SQLite (default)
- HTML/CSS (Django Templates)

This architecture provides a clean separation between logic, data, and presentation.
