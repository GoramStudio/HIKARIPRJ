
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#include "bitmaps.h"

const uint8_t* frames[] = {
    image_0,
    image_1,
    image_2,
    image_3,
    image_4,
    image_5,
    image_6,
    image_7,
    image_8,
    image_9,
    image_10,
    image_11,
    image_12,
    image_13,
    image_14,
    image_15,
    image_16,
    image_17,
    image_18,
    image_19,
    image_20,
    image_21,
    image_22,
    image_23,
    image_24,
    image_25,
    image_26,
    image_27,
    image_28,
    image_29,
    image_30,
    image_31,
    image_32,
    image_33,
};
#define FRAME_COUNT 34

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
