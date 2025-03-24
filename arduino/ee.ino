#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Wire.h>
#include <RH_ASK.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
RH_ASK driver;

const char* messages[] = {
  "Hikari HF UwU",
  "Yo la team",
  "433mhz over here",
  "spaghettis UwU",
  "OwO kawaiiiii",
  "bay city tududududu",
  "Hello World",
  "Arduino Nano",
  "R433 Module",
  "OLED Display"
};

const char* frames[] = {
  "Frame 1: ASCII Art",
  "Frame 2: ASCII Art",
  "Frame 3: ASCII Art",
  "Frame 4: ASCII Art",
  "Frame 5: ASCII Art"
};

void setup() {
  Serial.begin(9600);
  if (!driver.init()) {
    Serial.println("init failed");
  }
  display.begin(SH1106_SWITCHCAPVCC, 0x3C);
  display.display();
  delay(2000);
  display.clearDisplay();
}

void loop() {
  static unsigned long lastSendTime = 0;
  static unsigned long lastFrameTime = 0;
  static int messageIndex = 0;
  static int frameIndex = 0;

  unsigned long currentTime = millis();

  // Send message every 2 seconds
  if (currentTime - lastSendTime >= 2000) {
    driver.send((uint8_t *)messages[messageIndex], strlen(messages[messageIndex]));
    driver.waitPacketSent();
    messageIndex = (messageIndex + 1) % (sizeof(messages) / sizeof(messages[0]));
    lastSendTime = currentTime;
  }

  // Update frame every 500 milliseconds
  if (currentTime - lastFrameTime >= 500) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print(frames[frameIndex]);
    display.display();
    frameIndex = (frameIndex + 1) % (sizeof(frames) / sizeof(frames[0]));
    lastFrameTime = currentTime;
  }
}
