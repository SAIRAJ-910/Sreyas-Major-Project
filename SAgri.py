import serial
import time
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import re

# ---------- SERIAL ----------
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)
print("Success")
SOIL_DRY_THRESHOLD = 500

# ---------- TRAINING DATA ----------
data = {
    'Temperature': [28, 32, 22, 18, 26, 35, 30, 24, 20, 34],
    'Humidity':    [70, 55, 60, 65, 80, 45, 50, 75, 68, 40],
    'Soil':        [450, 600, 520, 400, 350, 650, 580, 420, 390, 700],
    'Crop': [
        'Rice', 'Cotton', 'Wheat', 'Potato', 'Sugarcane',
        'Cotton', 'Wheat', 'Rice', 'Potato', 'Cotton'
    ]
}

df = pd.DataFrame(data)
X = df[['Temperature', 'Humidity' , 'Soil' ]] 
y = df['Crop']

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

print("✅ ML Model Trained Successfully")

# ---------- SENSOR STORAGE ----------
temp_list = []
hum_list = []
soil_list = []


def read_sensor_data():
    try:
        line = arduino.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            return

        print("RAW:", line)

        temp_match = re.search(r'Temperature:(\d+)', line)
        hum_match  = re.search(r'Humidity:(\d+)', line)
        soil_match = re.search(r'Soil:(\d+)', line)

        if temp_match and hum_match and soil_match:
            temp = int(temp_match.group(1))
            hum  = int(hum_match.group(1))
            soil = int(soil_match.group(1))

            temp_list.append(temp)
            hum_list.append(hum)
            soil_list.append(soil)

            print(f"Live → Temp:{temp}°C  Hum:{hum}%  Soil:{soil}")
        else:
            print("⚠️ Incomplete sensor data")

    except Exception as e:
        print("Read error:", e)





def predict_crop():
    avg_temp = sum(temp_list) / len(temp_list)
    avg_hum  = sum(hum_list) / len(hum_list)
    avg_soil = sum(soil_list) / len(soil_list)

    input_df = pd.DataFrame(
        [[avg_temp, avg_hum, avg_soil]],
        columns=['Temperature', 'Humidity', 'Soil']
    )

    crop = model.predict(input_df)[0]

    print("\n🌾 SMART FARM ADVISORY 🌾")
    print(f"🌡 Avg Temperature : {avg_temp:.1f} °C")
    print(f"💧 Avg Humidity    : {avg_hum:.1f} %")
    print(f"🌱 Avg Soil Value  : {avg_soil:.1f}")
    print(f"✅ Recommended Crop: {crop}")
    print("=" * 50)

    temp_list.clear()
    hum_list.clear()
    soil_list.clear()




while True:
    read_sensor_data()
    time.sleep(0.5)

    command = input("\nEnter Command (FORWARD/BACKWARD/LEFT/RIGHT/STOP): ").upper()
    arduino.write((command + '\n').encode())

    if command == "STOP":
        if len(temp_list) >= 1:
            predict_crop()
        else:
            print("⚠️ Collecting sensor data... please wait")

