import os
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import re

def image_to_bitmap(image_path, width=120, height=64):
    """Convertit une image en bitmap monochrome avec redimensionnement"""
    img = Image.open(image_path).convert('1')  # Convertir en monochrome (1 bit par pixel)
    img = img.resize((width, height), Image.LANCZOS)
    pixels = np.array(img, dtype=np.uint8)
    
    bitmap = []
    for y in range(height):
        byte = 0
        for x in range(width):
            if pixels[y, x] == 0:  # 0 = noir, 255 = blanc
                byte |= (1 << (7 - (x % 8)))
            if x % 8 == 7:
                bitmap.append(byte)
                byte = 0
        if width % 8 != 0:
            bitmap.append(byte)
    
    return bitmap

def process_images(input_folder, output_file, width=120, height=64):
    """Traite toutes les images du dossier et génère un fichier .h pour Arduino"""
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'bmp'))]
    
    with open(output_file, 'w') as f:
        f.write("#ifndef BITMAPS_H\n#define BITMAPS_H\n\n")
        f.write(f"#define IMAGE_WIDTH {width}\n#define IMAGE_HEIGHT {height}\n\n")
        
        for idx, image_name in enumerate(sorted(images)):
            image_path = os.path.join(input_folder, image_name)
            bitmap = image_to_bitmap(image_path, width, height)
            
            f.write(f"const uint8_t image_{idx}[] PROGMEM = {{\n    ")
            f.write(", ".join(f"0x{byte:02X}" for byte in bitmap))
            f.write("\n};\n\n")
        
        f.write("#endif")

def select_folder():
    """Ouvre une boîte de dialogue pour sélectionner un dossier et générer le fichier .h"""
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Sélectionner le dossier des images")
    if folder_selected:
        process_images(folder_selected, "bitmaps.h")
        print("Fichier bitmaps.h généré avec succès!")

def generate_arduino_code(header_file, output_file="animation.ino"):
    """Lit le fichier .h et génère un code Arduino pour afficher l'animation"""
    with open(header_file, 'r') as f:
        content = f.read()
    
    images = re.findall(r'const uint8_t image_\d+\[] PROGMEM = \{([^}]*)\};', content)
    
    with open(output_file, 'w') as f:
        f.write("""
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#include "bitmaps.h"

const uint8_t* frames[] = {
""")
        
        for idx in range(len(images)):
            f.write(f"    image_{idx},\n")
        
        f.write("};\n")
        f.write(f"#define FRAME_COUNT {len(images)}\n")
        
        f.write("""
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
""")
    print("Code Arduino généré avec succès dans animation.ino")

if __name__ == "__main__":
    select_folder()
    generate_arduino_code("bitmaps.h")
