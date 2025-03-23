#include <Adafruit_GFX.h>        
#include <Adafruit_SH110X.h>     
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
    Serial.begin(9600);  // Démarrage de la communication série
    display.begin(0x3C, true);  // Initialisation de l'écran OLED (adresse I2C 0x3C)
    display.display();
    delay(1000);
    display.clearDisplay();
}

void loop() {
    static String receivedText = "";

    while (Serial.available()) {  // Vérifie si des données arrivent
        char c = Serial.read();
        if (c == '\n') {  // Nouvelle ligne -> Affichage
            display.clearDisplay();
            display.setTextSize(1);
            display.setTextColor(SH110X_WHITE);
            display.setCursor(0, 20);
            display.print(receivedText);
            display.display();
            receivedText = "";  // Réinitialisation du texte reçu
        } else {
            receivedText += c;
        }
    }
}