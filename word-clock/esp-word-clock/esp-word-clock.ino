#include <WiFi.h>
#include <Adafruit_NeoPixel.h>

// const char* ssid = "Vanila";
// const char* password = "0507887875";
// const char* ssid = "AroinaHome";
// const char* password = "11235813";
// const char* ssid = "Roy";
// const char* password = "12345678";
// const char* ssid = "Michal iPhone";
// const char* password = "Boobie1998";
const char* ssid = "Nadav iPhone";
const char* password = "01111997";
// const char* ssid = "TechPublic";
// const char* password = "";

#define PIN       5 // NeoPixel data pin
#define NUMPIXELS 132 // Number of pixels in your matrix (11x12)

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

WiFiServer server(80); // Set up the server on port 80

void setup() {
  Serial.begin(115200);
  pixels.begin();
  pixels.show(); // Initialize all pixels to 'off'

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");

  // Start the server
  server.begin();
  Serial.print("Server started. IP: ");
  Serial.println(WiFi.localIP());
}

unsigned long frame_time = millis();

void loop() {
  WiFiClient client = server.available(); // Listen for incoming clients

  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\n');
        // client.flush();

        // Record the start time
        unsigned long start_time = millis();

        Serial.print(request.c_str());
        // Example command format: "C123,255,255,255" (Set pixel 123 to RGB color 255,255,255)
        if (request.startsWith("C")) {
          int pixelIndex = request.substring(1, request.indexOf(',')).toInt();
          int red = request.substring(request.indexOf(',') + 1, request.indexOf(',', request.indexOf(',') + 1)).toInt();
          int green = request.substring(request.indexOf(',', request.indexOf(',') + 1) + 1, request.indexOf(',', request.indexOf(',', request.indexOf(',') + 1) + 1)).toInt();
          int blue = request.substring(request.indexOf(',', request.indexOf(',', request.indexOf(',') + 1) + 1) + 1).toInt();

          // Set pixel color and show the change
          pixels.setPixelColor(pixelIndex, pixels.Color(red, green, blue));
        } else if (request.startsWith("S")) {
          pixels.show();
          Serial.printf("\nframe time:%lu\n", millis() - frame_time);
          frame_time = millis();
        }
        Serial.printf(" command time:%lu\n", millis() - start_time);
      }
    }
    client.stop(); // Close the connection
  }
}
