import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\booking.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_passenger_form = """                            <label class="block text-gray-700 font-medium mb-2">Assigned Seat</label>
                            <input type="text" name="seat_number_${count}" readonly
                                class="w-full p-4 text-lg bg-gray-200 border-2 border-gray-300 rounded-xl focus:outline-none transition-colors text-center font-mono">
                        </div>"""

replacement_passenger_form = """                            <label class="block text-gray-700 font-medium mb-2">Assigned Seat</label>
                            <div class="grid grid-cols-2 gap-2">
                                <input type="text" name="seat_number_${count}" readonly placeholder="Outbound"
                                    class="w-full p-4 text-lg bg-gray-200 border-2 border-gray-300 rounded-xl focus:outline-none transition-colors text-center font-mono">
                                <input type="text" name="return_seat_number_${count}" readonly placeholder="Return"
                                    class="w-full p-4 text-lg bg-gray-200 border-2 border-gray-300 rounded-xl focus:outline-none transition-colors text-center font-mono hidden return-seat-input">
                            </div>
                        </div>"""

target_js_vars = """            let flightDetails = null;
            let seatMapData = null;
            let passengerSeatAssignments = {};"""

replacement_js_vars = """            let flightDetails = null;
            let seatMapData = null;
            let passengerSeatAssignments = {};
            let passengerReturnSeatAssignments = {};
            let isSelectingReturnSeats = false;"""

target_confirm_seats = """            confirmSeatsBtn.addEventListener('click', () => {
                const totalPassengers = passengersContainer.children.length;
                const selectedSeatsCount = Object.keys(passengerSeatAssignments).length;

                if (selectedSeatsCount < totalPassengers) {
                    alert('Please select a seat for each passenger.');
                    return;
                }

                seatSelectionSection.classList.add('hidden');
                paymentSection.classList.remove('hidden');
                document.querySelector('[data-step="seats"]').classList.remove('step-active');
                document.querySelector('[data-step="payment"]').classList.add('step-active');
            });"""

replacement_confirm_seats = """            confirmSeatsBtn.addEventListener('click', async () => {
                const totalPassengers = passengersContainer.children.length;
                const isRoundTrip = document.querySelector('input[name="trip_type"]:checked').value === 'round_trip';
                
                if (!isSelectingReturnSeats) {
                    // Outbound Seat Selection Validation
                    const selectedSeatsCount = Object.keys(passengerSeatAssignments).length;
                    if (selectedSeatsCount < totalPassengers) {
                        alert('Please select an outbound seat for each passenger.');
                        return;
                    }

                    if (isRoundTrip) {
                        // Switch to Return Seat Selection
                        isSelectingReturnSeats = true;
                        alert('Outbound seats confirmed. Now please select your RETURN seats.');
                        
                        // Clear map for return selection (in a real app we'd fetch a different seat map)
                        // For prototype, we just clear selections and reuse the map
                        document.querySelectorAll('.seat.selected').forEach(el => el.classList.remove('selected'));
                        document.querySelector('#seat-selection-section h2').innerHTML = '<i class="fas fa-couch text-secondary"></i> Select Return Seats';
                        confirmSeatsBtn.textContent = 'Confirm Return Seats & Proceed';
                        return;
                    }
                } else {
                    // Return Seat Selection Validation
                    const selectedReturnSeatsCount = Object.keys(passengerReturnSeatAssignments).length;
                    if (selectedReturnSeatsCount < totalPassengers) {
                        alert('Please select a return seat for each passenger.');
                        return;
                    }
                }

                seatSelectionSection.classList.add('hidden');
                paymentSection.classList.remove('hidden');
                document.querySelector('[data-step="seats"]').classList.remove('step-active');
                document.querySelector('[data-step="payment"]').classList.add('step-active');
            });"""

target_handle_seat = """            function handleSeatSelection(event) {
                const seatEl = event.target;
                const seatNumber = seatEl.dataset.seatNumber;

                if (seatEl.classList.contains('occupied') || seatEl.classList.contains('disabled')) return;

                const totalPassengers = passengersContainer.children.length;
                const selectedSeats = document.querySelectorAll('.seat.selected');

                if (seatEl.classList.contains('selected')) {
                    seatEl.classList.remove('selected');
                    for (const passengerId in passengerSeatAssignments) {
                        if (passengerSeatAssignments[passengerId] === seatNumber) {
                            delete passengerSeatAssignments[passengerId];
                            document.querySelector(`input[name="seat_number_${passengerId}"]`).value = '';
                            break;
                        }
                    }
                } else {
                    if (selectedSeats.length >= totalPassengers) {
                        alert(`All passengers already have seats. To change a selection, please click on a selected seat to deselect it first.`);
                        return;
                    }

                    seatEl.classList.add('selected');
                    let assigned = false;
                    for (let i = 1; i <= totalPassengers; i++) {
                        if (!passengerSeatAssignments[i]) {
                            passengerSeatAssignments[i] = seatNumber;
                            document.querySelector(`input[name="seat_number_${i}"]`).value = seatNumber;
                            assigned = true;
                            break;
                        }
                    }
                }
            }"""

replacement_handle_seat = """            function handleSeatSelection(event) {
                const seatEl = event.target;
                const seatNumber = seatEl.dataset.seatNumber;

                if (seatEl.classList.contains('occupied') || seatEl.classList.contains('disabled')) return;

                const totalPassengers = passengersContainer.children.length;
                const currentAssignments = isSelectingReturnSeats ? passengerReturnSeatAssignments : passengerSeatAssignments;
                const inputNamePrefix = isSelectingReturnSeats ? 'return_seat_number_' : 'seat_number_';

                // Count currently selected seats for THIS phase
                let currentPhaseSelectedCount = 0;
                document.querySelectorAll('.seat.selected').forEach(el => {
                    // We need to check if this seat is actually in our current assignments
                    // Because visually we might have cleared classes, but let's rely on our data structure
                });
                // Actually, simpler: just count keys in currentAssignments
                currentPhaseSelectedCount = Object.keys(currentAssignments).length;

                if (seatEl.classList.contains('selected')) {
                    seatEl.classList.remove('selected');
                    for (const passengerId in currentAssignments) {
                        if (currentAssignments[passengerId] === seatNumber) {
                            delete currentAssignments[passengerId];
                            document.querySelector(`input[name="${inputNamePrefix}${passengerId}"]`).value = '';
                            break;
                        }
                    }
                } else {
                    if (currentPhaseSelectedCount >= totalPassengers) {
                        alert(`All passengers already have seats for this leg. To change a selection, please click on a selected seat to deselect it first.`);
                        return;
                    }

                    seatEl.classList.add('selected');
                    for (let i = 1; i <= totalPassengers; i++) {
                        if (!currentAssignments[i]) {
                            currentAssignments[i] = seatNumber;
                            document.querySelector(`input[name="${inputNamePrefix}${i}"]`).value = seatNumber;
                            break;
                        }
                    }
                }
            }"""

target_trip_type_listener = """            tripTypeInputs.forEach(input => {
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

replacement_trip_type_listener = """            tripTypeInputs.forEach(input => {
                input.addEventListener('change', () => {
                    const returnInputs = document.querySelectorAll('.return-seat-input');
                    if (input.value === 'round_trip') {
                        returnDateContainer.classList.remove('hidden');
                        returnDateInput.setAttribute('required', 'required');
                        returnInputs.forEach(el => el.classList.remove('hidden'));
                    } else {
                        returnDateContainer.classList.add('hidden');
                        returnDateInput.removeAttribute('required');
                        returnDateInput.value = '';
                        returnInputs.forEach(el => el.classList.add('hidden'));
                    }
                    updatePrice();
                });
            });"""

target_payload_collection = """                        passengers.push({
                            name: formData.get(`name_${id}`),
                            age: formData.get(`age_${id}`),
                            phone: formData.get(`phone_${id}`),
                            email: formData.get(`email_${id}`),
                            seat_number: formData.get(`seat_number_${id}`)
                        });"""

replacement_payload_collection = """                        passengers.push({
                            name: formData.get(`name_${id}`),
                            age: formData.get(`age_${id}`),
                            phone: formData.get(`phone_${id}`),
                            email: formData.get(`email_${id}`),
                            seat_number: formData.get(`seat_number_${id}`),
                            return_seat_number: formData.get(`return_seat_number_${id}`)
                        });"""

if target_passenger_form in content:
    content = content.replace(target_passenger_form, replacement_passenger_form)
    print("Replaced passenger form.")
else:
    print("Passenger form target not found.")

if target_js_vars in content:
    content = content.replace(target_js_vars, replacement_js_vars)
    print("Replaced JS vars.")
else:
    print("JS vars target not found.")

if target_confirm_seats in content:
    content = content.replace(target_confirm_seats, replacement_confirm_seats)
    print("Replaced confirm seats logic.")
else:
    print("Confirm seats target not found.")

if target_handle_seat in content:
    content = content.replace(target_handle_seat, replacement_handle_seat)
    print("Replaced handle seat logic.")
else:
    print("Handle seat target not found.")

if target_trip_type_listener in content:
    content = content.replace(target_trip_type_listener, replacement_trip_type_listener)
    print("Replaced trip type listener.")
else:
    print("Trip type listener target not found.")

if target_payload_collection in content:
    content = content.replace(target_payload_collection, replacement_payload_collection)
    print("Replaced payload collection.")
else:
    print("Payload collection target not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
