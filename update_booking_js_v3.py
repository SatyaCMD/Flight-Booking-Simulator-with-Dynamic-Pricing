import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\booking.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_payload_loop = """                        if (input.name.startsWith('seat_number')) p.seat_number = input.value;
                    });"""

replacement_payload_loop = """                        if (input.name.startsWith('seat_number')) p.seat_number = input.value;
                        if (input.name.startsWith('return_seat_number')) p.return_seat_number = input.value;
                    });"""

if target_payload_loop in content:
    content = content.replace(target_payload_loop, replacement_payload_loop)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced payload loop.")
else:
    print("Payload loop target not found.")
