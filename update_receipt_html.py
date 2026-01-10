import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\receipt.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_block = """        <div class="grid-info">
            <div class="info-group">
                <label>Payment Method</label>
                <div class="value">
                    {{ payment_method }}
                </div>
            </div>
            <div class="info-group" style="text-align: right;">
                <label>Booking Reference</label>
                <div class="value" style="font-family: 'Fira Code', monospace;">{{ booking.booking_reference }}</div>
            </div>
        </div>"""

replacement_block = """        <div class="grid-info">
            <div class="info-group">
                <label>Payment Method</label>
                <div class="value">
                    {{ payment_method }}
                </div>
            </div>
            <div class="info-group" style="text-align: right;">
                <label>Booking Reference</label>
                <div class="value" style="font-family: 'Fira Code', monospace;">{{ booking.booking_reference }}</div>
            </div>
        </div>

        <div class="grid-info">
            <div class="info-group">
                <label>Trip Type</label>
                <div class="value" style="text-transform: capitalize;">
                    {{ booking.trip_type }}
                </div>
            </div>
            {% if booking.return_date %}
            <div class="info-group" style="text-align: right;">
                <label>Return Date</label>
                <div class="value">{{ booking.return_date }}</div>
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
