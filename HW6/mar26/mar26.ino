#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT11.h>

const char* ssid = "SSID";
const char* password = "PASSWORD";
#define DHTPIN 4 // Pin where the DHT11 is connected 
#define DHTTYPE DHT11 // Type of the DHT sensor 
DHT11 dht11(DHTPIN); // Replace these with your Firebase project credentials 
const char *serverAddress = "http://IP Address:Port Number/post_data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
}

void sendSensorData(float temperature, float humidity) {
  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;
    http.begin(serverAddress); // Change IP address and port as per your Flask server
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";
    
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }
}

void loop() {
  delay(2000); // Delay between sensor readings

  int temperature = 0, humidity = 0;
  int result = dht11.readTemperatureHumidity(temperature, humidity);
  if (result != 0) { 
    Serial.println("Failed to read from DHT sensor"); 
    return; 
  }
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C\tHumidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  sendSensorData(temperature, humidity);
}
