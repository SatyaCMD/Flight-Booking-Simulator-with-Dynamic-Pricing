# 💾 Database Design

This system uses Django ORM with SQLite.

---

## **1. Flight Model**
id
origin
destination
date
time
base_price
seats_total
seats_left

---

## **2. Booking Model**
id
flight (FK)
passenger_name
passenger_email
price_paid
booking_time

---

## **Relationships**
- **One Flight → Many Bookings**

---

## **Important Constraints**
- Cannot book when seats_left = 0  
- seats_left reduces after each booking  

---

## **Indexing**  
For optimization, indexes can be added to:
- `date`, `origin`, `destination`

