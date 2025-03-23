#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define TEXT_AREA_WIDTH 64
#define BLOCK_SIZE 8

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
String receivedText = "";

void setup() {
  Serial.begin(115200);
  Wire.setClock(400000);
  display.begin();
  display.clearDisplay();
  display.display();
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    
    if (input.startsWith("TEXT:")) {
      receivedText = input.substring(5);
      displayText();
    } else {
      processImageData(input);
    }
  }
}

void displayText() {
  display.fillRect(0, 0, TEXT_AREA_WIDTH, SCREEN_HEIGHT, SH110X_BLACK);
  display.setTextSize(1);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(2, 2);
  display.println(receivedText);
  display.display();
}

void processImageData(String input) {
  int x = input[0];
  int y = input[1];
  for (int i = 0; i < BLOCK_SIZE; i++) {
    uint8_t rowData = input[i + 2];
    for (int j = 0; j < BLOCK_SIZE; j++) {
      bool pixel = rowData & (1 << (BLOCK_SIZE - 1 - j));
      display.drawPixel(TEXT_AREA_WIDTH + x + j, y + i, pixel ? SH110X_WHITE : SH110X_BLACK);
    }
  }
  display.display();
}
