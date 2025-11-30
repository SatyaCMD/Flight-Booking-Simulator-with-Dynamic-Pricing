# 🌐 API Documentation

Although primarily a template-rendered Django app, certain endpoints behave like APIs.

---

## **GET /flights/**
Returns available flights with dynamically updated prices.

### Response Example:
```json
[
  {
    "id": 1,
    "origin": "Delhi",
    "destination": "Mumbai",
    "price": 4520,
    "seats_left": 38
  }
]

GET /flights/<id>/
Returns a specific flight.

POST /book/
Creates a booking.
```

### Payload ##
{
  "flight_id": 4,
  "name": "John Doe",
  "email": "john@example.com"
}

### Response ##
{
  "status": "success",
  "booking_id": 1021
}

### Error Codes may be occured or get during execution ###
400 – Missing data
404 – Flight does not exist
409 – No seats available

