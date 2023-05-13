#include <WiFi.h>
#include <Adafruit_NeoPixel.h>

// Replace with your Wi-Fi credentials
const char* ssid = "TechPublic";
const char* password = "";
bool wifi_connected = false;

// NeoPixel configuration
const int ledPin = 5;
const int numLeds = 132;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(numLeds, ledPin, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  connectWiFi();

  // Initialize NeoPixel strip
  strip.begin();
  strip.setBrightness(255);
  strip.show();
}

void loop() {
  // Blink all LEDs in red
  if (wifi_connected) {
      setColor(255, 0, 0); // Set color to red
      delay(500);
      setColor(0, 0, 0); // Set color to black (off)
      delay(500);
  }
}

void connectWiFi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wi-Fi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  wifi_connected = true;
}

void setColor(uint8_t r, uint8_t g, uint8_t b) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(r, g, b));
  }
  strip.show();
}