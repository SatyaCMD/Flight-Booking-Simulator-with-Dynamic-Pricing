import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\ticket.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_block = """                        <div class="info-item" style="text-align: right;">
                            <label>Seat Number</label>
                            <div class="seat-badge">
                                {% if booking.passenger_details %}
                                {{ booking.passenger_details.0.seat_number }}
                                {% else %}
                                ANY
                                {% endif %}
                            </div>
                        </div>"""

replacement_block = """                        <div class="info-item" style="text-align: right;">
                            <label>Seat Number</label>
                            <div class="seat-badge">
                                {% if booking.passenger_details %}
                                {{ booking.passenger_details.0.seat_number }}
                                {% else %}
                                ANY
                                {% endif %}
                            </div>
                            {% if booking.passenger_details.0.return_seat_number %}
                            <div style="margin-top: 0.5rem;">
                                <label style="font-size: 0.7rem; display: block; margin-bottom: 0.2rem;">Return Seat</label>
                                <div class="seat-badge" style="font-size: 1rem; background: #64748b;">
                                    {{ booking.passenger_details.0.return_seat_number }}
                                </div>
                            </div>
                            {% endif %}
                        </div>"""

if target_block in content:
    content = content.replace(target_block, replacement_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced content.")
else:
    print("Target block not found.")
