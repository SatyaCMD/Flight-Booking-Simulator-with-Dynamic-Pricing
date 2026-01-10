import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\booking.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_listeners = """            const travelClassSelect = document.getElementById('travel-class');
            travelClassSelect.addEventListener('change', () => {
                updatePrice();
                if (!seatSelectionSection.classList.contains('hidden')) {
                    renderSeatMap();
                }
            });"""

replacement_listeners = """            const travelClassSelect = document.getElementById('travel-class');
            const tripTypeInputs = document.querySelectorAll('input[name="trip_type"]');
            const returnDateContainer = document.getElementById('return-date-container');
            const returnDateInput = document.getElementById('return-date');

            travelClassSelect.addEventListener('change', () => {
                updatePrice();
                if (!seatSelectionSection.classList.contains('hidden')) {
                    renderSeatMap();
                }
            });

            tripTypeInputs.forEach(input => {
                input.addEventListener('change', () => {
                    if (input.value === 'round_trip') {
                        returnDateContainer.classList.remove('hidden');
                        returnDateInput.setAttribute('required', 'required');
                    } else {
                        returnDateContainer.classList.add('hidden');
                        returnDateInput.removeAttribute('required');
                        returnDateInput.value = '';
                    }
                    updatePrice();
                });
            });"""

target_update_price_start = """            function updatePrice() {
                const count = passengersContainer.children.length;
                let multiplier = 1;
                let seatsDisplay = 0;
                const travelClass = document.getElementById('travel-class').value;"""

replacement_update_price_start = """            function updatePrice() {
                const count = passengersContainer.children.length;
                let multiplier = 1;
                let seatsDisplay = 0;
                const travelClass = document.getElementById('travel-class').value;"""

target_multiplier_logic = """                if (travelClass === 'First') {
                    multiplier = 2.5;
                }

                const seatsEl = document.getElementById('seats-available');"""

replacement_multiplier_logic = """                if (travelClass === 'First') {
                    multiplier = 2.5;
                }

                // Round Trip Logic
                const isRoundTrip = document.querySelector('input[name="trip_type"]:checked').value === 'round_trip';
                if (isRoundTrip) {
                    multiplier *= 2;
                }

                const seatsEl = document.getElementById('seats-available');"""

target_payload = """                    const bookResponse = await fetch('/api/flights/bookings/create/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({"""

replacement_payload = """                    const bookResponse = await fetch('/api/flights/bookings/create/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            trip_type: document.querySelector('input[name="trip_type"]:checked').value,
                            return_date: document.getElementById('return-date').value,"""

if target_listeners in content:
    content = content.replace(target_listeners, replacement_listeners)
    print("Replaced listeners.")
else:
    print("Listeners target not found.")

if target_multiplier_logic in content:
    content = content.replace(target_multiplier_logic, replacement_multiplier_logic)
    print("Replaced multiplier logic.")
else:
    print("Multiplier logic target not found.")

if target_payload in content:
    content = content.replace(target_payload, replacement_payload)
    print("Replaced payload logic.")
else:
    print("Payload target not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
