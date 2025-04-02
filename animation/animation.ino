#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define i2c_Address 0x3C
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define BUTTON_PIN 2

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

unsigned long previousMillis = 0;
int hours = 12, minutes = 0, seconds = 0;
bool buttonPressed = false;

void setup() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), adjustHours, FALLING);
    Serial.begin(9600);
    display.begin(i2c_Address, true);
    display.clearDisplay();
}

void loop() {
    unsigned long currentMillis = millis();
    unsigned long elapsedMillis = currentMillis - previousMillis;
    if (elapsedMillis >= 1000) {
        previousMillis = currentMillis;
        updateClock();
    }
    animatedDisplayClock(currentMillis % 1000);
}

void updateClock() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours = (hours + 1) % 24;
        }
    }
}

void animatedDisplayClock(int millisecs) {
    static int yOffset = SCREEN_HEIGHT;
    if (yOffset > 20) {
        yOffset -= 2;
    }
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SH110X_WHITE);
    int textWidth = 12 * 8;
    display.setCursor((SCREEN_WIDTH - textWidth) / 2, yOffset);
    
    if (hours < 10) display.print("0");
    display.print(hours);
    display.print(":");
    if (minutes < 10) display.print("0");
    display.print(minutes);
    display.print(":");
    if (seconds < 10) display.print("0");
    display.println(seconds);
    
    display.setTextSize(1);
    display.setCursor((SCREEN_WIDTH - 8 * 10) / 2, yOffset + 20);
    display.print("UwU : ");
    display.println(millisecs);
    display.print("   tah l'horloge");
    
    display.display();
}

void adjustHours() {
    if (!buttonPressed) {
        buttonPressed = true;
        hours = (hours + 1) % 24;
        delay(200);
        buttonPressed = false;
    }
}

