NHTSA_API_VARIBLE_ID_MAPPING = {
    'Suggested VIN': 142,
    'Error Code': 143,
    'Possible Values': 144,
    'Additional Error Text': 156,
    'Error Text': 191,
    'Vehicle Descriptor': 196,
    'Destination Market': 10,
    'Make': 26,
    'Manufacturer Name': 27,
    'Model': 28,
    'Model Year': 29,
    'Plant City': 31,
    'Series': 34,
    'Trim': 38,
    'Vehicle Type': 39,
    'Plant Country': 75,
    'Plant Company Name': 76,
    'Plant State': 77,
    'Trim2': 109,
    'Series2': 110,
    'Note': 114,
    'Base Price ($)': 136,
    'Non-Land Use': 195,
    'Body Class': 5,
    'Doors': 14,
    'Windows': 40,
    'Wheel Base Type': 60,
    'Track Width (inches)': 159,
    'Gross Vehicle Weight Rating From': 25,
    'Bed Length (inches)': 49,
    'Curb Weight (pounds)': 54,
    'Wheel Base (inches) From': 111,
    'Wheel Base (inches) To': 112,
    'Gross Combination Weight Rating From': 184,
    'Gross Combination Weight Rating To': 185,
    'Gross Vehicle Weight Rating To': 190,
    'Bed Type': 3,
    'Cab Type': 4,
    'Trailer Type Connection': 116,
    'Trailer Body Type': 117,
    'Trailer Length (feet)': 118,
    'Other Trailer Info': 155,
    'Number of Wheels': 115,
    'Wheel Size Front (inches)': 119,
    'Wheel Size Rear (inches)': 120,
    'Entertainment System': 23,
    'Steering Location': 36,
    'Number of Seats': 33,
    'Number of Seat Rows': 61,
    'Transmission Style': 37,
    'Transmission Speeds': 63,
    'Drive Type': 15,
    'Axles': 41,
    'Axle Configuration': 145,
    'Brake System Type': 42,
    'Brake System Description': 52,
    'Other Battery Info': 1,
    'Battery Type': 2,
    'Number of Battery Cells per Module': 48,
    'Battery Current (Amps) From': 57,
    'Battery Voltage (Volts) From': 58,
    'Battery Energy (kWh) From': 59,
    'EV Drive Unit': 72,
    'Battery Current (Amps) To': 132,
    'Battery Voltage (Volts) To': 133,
    'Battery Energy (kWh) To': 134,
    'Number of Battery Modules per Pack': 137,
    'Number of Battery Packs per Vehicle': 138,
    'Charger Level': 127,
    'Charger Power (kW)': 128,
    'Engine Number of Cylinders': 9,
    'Displacement (CC)': 11,
    'Displacement (CI)': 12,
    'Displacement (L)': 13,
    'Engine Stroke Cycles': 17,
    'Engine Model': 18,
    'Engine Power (kW)': 21,
    'Fuel Type - Primary': 24,
    'Valve Train Design': 62,
    'Engine Configuration': 64,
    'Fuel Type - Secondary': 66,
    'Fuel Delivery / Fuel Injection Type': 67,
    'Engine Brake (hp) From': 71,
    'Cooling Type': 122,
    'Engine Brake (hp) To': 125,
    'Electrification Level': 126,
    'Other Engine Info': 129,
    'Turbo': 135,
    'Top Speed (MPH)': 139,
    'Engine Manufacturer': 146,
    'Pretensioner': 78,
    'Seat Belt Type': 79,
    'Other Restraint System Info': 121,
    'Curtain Air Bag Locations': 55,
    'Seat Cushion Air Bag Locations': 56,
    'Front Air Bag Locations': 65,
    'Knee Air Bag Locations': 69,
    'Side Air Bag Locations': 107,
    'Anti-lock Braking System (ABS)': 86,
    'Electronic Stability Control (ESC)': 99,
    'Traction Control': 100,
    'Tire Pressure Monitoring System (TPMS) Type': 168,
    'Active Safety System Note': 169,
    'Auto-Reverse System for Windows and Sunroofs': 172,
    'Automatic Pedestrian Alerting Sound (for Hybrid and EV only)': 173,
    'Event Data Recorder (EDR)': 175,
    'Keyless Ignition': 176,
    'SAE Automation Level From': 181,
    'SAE Automation Level To': 182,
    'Adaptive Cruise Control (ACC)': 81,
    'Crash Imminent Braking (CIB)': 87,
    'Blind Spot Warning (BSW)': 88,
    'Forward Collision Warning (FCW)': 101,
    'Lane Departure Warning (LDW)': 102,
    'Lane Keeping Assistance (LKA)': 103,
    'Backup Camera': 104,
    'Parking Assist': 105,
    'Bus Length (feet)': 147,
    'Bus Floor Configuration Type': 148,
    'Bus Type': 149,
    'Other Bus Info': 150,
    'Custom Motorcycle Type': 151,
    'Motorcycle Suspension Type': 152,
    'Motorcycle Chassis Type': 153,
    'Other Motorcycle Info': 154,
    'Dynamic Brake Support (DBS)': 170,
    'Pedestrian Automatic Emergency Braking (PAEB)': 171,
    'Automatic Crash Notification (ACN) / Advanced Automatic Crash Notification (AACN)': 174,
    'Daytime Running Light (DRL)': 177,
    'Headlamp Light Source': 178,
    'Semiautomatic Headlamp Beam Switching': 179,
    'Adaptive Driving Beam (ADB)': 180,
    'Rear Cross Traffic Alert': 183,
    'Rear Automatic Emergency Braking': 192,
    'Blind Spot Intervention (BSI)': 193,
    'Lane Centering Assistance': 194,
}

NHTSA_API_VARIABLE_IDS = list(NHTSA_API_VARIBLE_ID_MAPPING.values())
NHTSA_API_VARIABLE_NAMES = list(NHTSA_API_VARIBLE_ID_MAPPING.keys())

POPULAR_NHTSA_VARIBLE_NAMES = [
    'Error Code', 'Error Text',
    'Manufacturer Name', 'Plant Company Name', 'Plant City', 'Plant State', 'Plant Country',
    'Make', 'Model Year', 'Model', 'Top Speed (MPH)', 'Series', 'Series2', 'Trim', 'Trim2', 'Vehicle Type', 'Gross Vehicle Weight Rating From', 'Curb Weight (pounds)',
    'Drive Type', 'Body Class', 'Doors', 'Windows', 'Number of Seats', 'Seat Belt Type',
    'Number of Wheels', 'Wheel Base Type', 'Wheel Base (inches) From', 'Wheel Base (inches) To',
    'Axles', 'Axle Configuration',
    'Front Air Bag Locations', 'Knee Air Bag Locations',
    'Headlamp Light Source', 'Semiautomatic Headlamp Beam Switching', 'Daytime Running Light (DRL)',
    'Transmission Style', 'Transmission Speeds',
    'Engine Model', 'Engine Power (kW)', 'Engine Manufacturer', 'Engine Configuration', 'Engine Brake (hp) From', 'Engine Brake (hp) To', 'Valve Train Design',
    'Engine Number of Cylinders', 'Displacement (CC)', 'Displacement (CI)', 'Displacement (L)', 'Engine Stroke Cycles', 'Turbo',
    'Fuel Type - Primary', 'Fuel Type - Secondary',  'Cooling Type',
    'Anti-lock Braking System (ABS)', 'Brake System Type', 'Brake System Description', 'Dynamic Brake Support (DBS)',
    'Traction Control', 'Entertainment System', 'Event Data Recorder (EDR)',
    'Keyless Ignition', 'Backup Camera', 'Parking Assist', 'Tire Pressure Monitoring System (TPMS) Type',
    'Lane Centering Assistance', 'Blind Spot Warning (BSW)', 'Rear Automatic Emergency Braking', 'Forward Collision Warning (FCW)',
    'Automatic Crash Notification (ACN) / Advanced Automatic Crash Notification (AACN)', 'Adaptive Cruise Control (ACC)',
    'Crash Imminent Braking (CIB)', 'Pedestrian Automatic Emergency Braking (PAEB)', 'Rear Cross Traffic Alert'

    # the following are EVs related
    'Electrification Level', 'Other Engine Info', 'EV Drive Unit',
    'Automatic Pedestrian Alerting Sound (for Hybrid and EV only)',
    'Battery Type', 'Other Battery Info', 'Number of Battery Cells per Module', 'Number of Battery Modules per Pack', 'Number of Battery Packs per Vehicle'
    'Battery Current (Amps) From', 'Battery Voltage (Volts) From', 'Battery Energy (kWh) From',
    'Battery Current (Amps) To', 'Battery Voltage (Volts) To', 'Battery Energy (kWh) To',
    'Charger Level', 'Charger Power (kW)',
]

POPULAR_NHTSA_VARIABLE_IDS = [NHTSA_API_VARIBLE_ID_MAPPING[name]
                              for name in POPULAR_NHTSA_VARIBLE_NAMES
                              if name in NHTSA_API_VARIBLE_ID_MAPPING]
