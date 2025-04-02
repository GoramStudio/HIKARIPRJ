import os
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def image_to_rle(image_path, width=64, height=32):
    """Convertit une image en bitmap compressé avec RLE"""
    img = Image.open(image_path).convert('1')  # Convertir en monochrome
    img = img.resize((width, height), Image.Resampling.NEAREST)
    pixels = np.array(img, dtype=np.uint8)

    bitmap = []
    count = 0
    last_pixel = pixels[0, 0]

    for y in range(height):
        for x in range(width):
            pixel = 0 if pixels[y, x] == 0 else 1
            if pixel == last_pixel:
                count += 1
            else:
                bitmap.append(count)
                last_pixel = pixel
                count = 1
    bitmap.append(count)  # Ajouter le dernier comptage

    return bitmap

def process_images(input_folder, output_file, width=64, height=32):
    """Traite les images et génère un fichier .h compressé"""
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'bmp'))]
    
    with open(output_file, 'w') as f:
        f.write("#ifndef BITMAPS_H\n#define BITMAPS_H\n\n")
        f.write(f"#define IMAGE_WIDTH {width}\n#define IMAGE_HEIGHT {height}\n\n")
        
        for idx, image_name in enumerate(sorted(images)):
            image_path = os.path.join(input_folder, image_name)
            bitmap = image_to_rle(image_path, width, height)
            
            f.write(f"const PROGMEM uint8_t image_{idx}[] = {{\n    ")
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
        print("Fichier bitmaps.h généré avec compression RLE!")

if __name__ == "__main__":
    select_folder()
