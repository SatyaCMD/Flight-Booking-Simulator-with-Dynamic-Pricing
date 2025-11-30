# 🧮 Dynamic Pricing Logic
```markdown

This project simulates airline-style real-time price adjustments based on multiple variables.

```

## **Pricing Formula**
final_price = base_price × seat_factor × time_factor × demand_factor × market_randomness

---

## **Factors Explained**

### ✔ Base Price  
Stored in the Flight model.

### ✔ Seat Factor  
Fewer seats → Higher cost.

### ✔ Time Factor  
Closer to departure → Higher price.

### ✔ Demand Factor  
Popular routes cost more.

### ✔ Market Randomness  
Adds unpredictability (±5–15%).

---

## **Example Calculation**
Base Price: 3000
Seat Factor: 1.12
Demand Factor: 1.20
Randomness: 0.91
Final = 3000 × 1.12 × 1.20 × 0.91 = ₹3661

---

## **Why This Matters**
This model resembles real airline strategies like:
- Revenue optimization  
- Last-minute spike pricing  
- Dynamic seat-based inventory control  


