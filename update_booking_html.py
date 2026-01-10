import os

file_path = r'C:\Users\SATYA\OneDrive\Desktop\flight_simulator\templates\booking.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_block = """                        <div class="form-group">
                            <label class="block text-gray-700 font-medium mb-3 text-lg">Travel Class</label>
                            <div class="relative">
                                <select id="travel-class" name="travel_class"
                                    class="w-full p-4 text-lg bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none transition-colors appearance-none cursor-pointer">
                                    <option value="Economy">Economy (1x Fare)</option>
                                    <option value="Business">Business (1.5x Fare)</option>
                                    <option value="First">First Class (2.5x Fare)</option>
                                </select>
                                <div
                                    class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                                    <i class="fas fa-chevron-down"></i>
                                </div>
                            </div>
                        </div>"""

replacement_block = """                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="form-group">
                                <label class="block text-gray-700 font-medium mb-3 text-lg">Trip Type</label>
                                <div class="flex gap-4">
                                    <label class="cursor-pointer relative group flex-1">
                                        <input type="radio" name="trip_type" value="one_way" checked
                                            class="peer absolute opacity-0">
                                        <div
                                            class="p-4 rounded-xl border-2 border-gray-200 peer-checked:border-primary peer-checked:bg-red-50 transition-all flex flex-col items-center justify-center gap-2 h-full group-hover:border-gray-300">
                                            <i class="fas fa-arrow-right text-xl text-gray-400 peer-checked:text-primary"></i>
                                            <span class="text-sm font-medium text-gray-600 peer-checked:text-primary">One Way</span>
                                        </div>
                                    </label>
                                    <label class="cursor-pointer relative group flex-1">
                                        <input type="radio" name="trip_type" value="round_trip"
                                            class="peer absolute opacity-0">
                                        <div
                                            class="p-4 rounded-xl border-2 border-gray-200 peer-checked:border-primary peer-checked:bg-red-50 transition-all flex flex-col items-center justify-center gap-2 h-full group-hover:border-gray-300">
                                            <i class="fas fa-exchange-alt text-xl text-gray-400 peer-checked:text-primary"></i>
                                            <span class="text-sm font-medium text-gray-600 peer-checked:text-primary">Round Trip</span>
                                        </div>
                                    </label>
                                </div>
                            </div>
                            <div class="form-group hidden" id="return-date-container">
                                <label class="block text-gray-700 font-medium mb-3 text-lg">Return Date</label>
                                <input type="date" id="return-date" name="return_date"
                                    class="w-full p-4 text-lg bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none transition-colors">
                            </div>
                        </div>
                        <div class="form-group mt-6">
                            <label class="block text-gray-700 font-medium mb-3 text-lg">Travel Class</label>
                            <div class="relative">
                                <select id="travel-class" name="travel_class"
                                    class="w-full p-4 text-lg bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-primary focus:outline-none transition-colors appearance-none cursor-pointer">
                                    <option value="Economy">Economy (1x Fare)</option>
                                    <option value="Business">Business (1.5x Fare)</option>
                                    <option value="First">First Class (2.5x Fare)</option>
                                </select>
                                <div
                                    class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                                    <i class="fas fa-chevron-down"></i>
                                </div>
                            </div>
                        </div>"""

if target_block in content:
    new_content = content.replace(target_block, replacement_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced content.")
else:
    print("Target block not found.")
    start_idx = content.find('Travel Class')
    if start_idx != -1:
        print("Found 'Travel Class' at index:", start_idx)
        print("Surrounding content:")
        print(content[start_idx-100:start_idx+500])
    else:
        print("'Travel Class' not found at all.")
