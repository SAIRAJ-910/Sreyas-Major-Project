#include <DHT11.h>

DHT11 dht11(2);

int soilPin = A0;   // Soil sensor connected to A0

void setup() {
    Serial.begin(9600);
}

void loop() {
    int temperature = 0;
    int humidity = 0;
    int soilValue = analogRead(soilPin);

    int result = dht11.readTemperatureHumidity(temperature, humidity);

    if (result == 0) {
        Serial.println(
            "Temperature:" + String(temperature) +
            ",Humidity:" + String(humidity) +
            ",Soil:" + String(soilValue)
        );
    } else {
        Serial.println("Sensor Error");
    }

    delay(2000);
}
