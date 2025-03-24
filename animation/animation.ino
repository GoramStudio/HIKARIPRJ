
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#include "bitmaps.h"

const uint8_t* frames[] = {
};
#define FRAME_COUNT 0

void setup() {
    display.begin(0x3C, true);
    display.clearDisplay();
}

void loop() {
    for (int i = 0; i < FRAME_COUNT; i++) {
        display.clearDisplay();
        display.drawBitmap(0, 0, frames[i], IMAGE_WIDTH, IMAGE_HEIGHT, SH110X_WHITE);
        display.display();
        delay(100);
    }
}
