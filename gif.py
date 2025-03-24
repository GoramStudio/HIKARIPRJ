from PIL import Image, ImageSequence
import sys

def convert_gif_to_arduino(gif_path, output_path):
    try:
        image = Image.open(gif_path)
        frames = [frame.convert('1') for frame in ImageSequence.Iterator(image)]
    except Exception as e:
        print(f"Erreur lors de la lecture du GIF : {e}")
        return
    
    frame_data = []
    for frame in frames:
        frame_bytes = []
        for y in range(frame.height):
            row = []
            for x in range(frame.width):
                pixel = frame.getpixel((x, y))
                row.append('1' if pixel == 0 else '0')
            frame_bytes.append("0b" + "".join(row))
        frame_data.append(frame_bytes)
    
    with open(output_path, "w") as f:
        f.write("#include <SPI.h>\n")
        f.write("#include <Wire.h>\n")
        f.write("#include <Adafruit_GFX.h>\n")
        f.write("#include <Adafruit_SH110X.h>\n\n")
        f.write("#define SCREEN_WIDTH 128\n")
        f.write("#define SCREEN_HEIGHT 64\n")
        f.write("#define OLED_RESET -1\n")
        f.write("Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);\n\n")
        f.write("const uint8_t animation[][SCREEN_HEIGHT] PROGMEM = {\n")
        for frame in frame_data:
            f.write("  {" + ", ".join(frame) + "},\n")
        f.write("};\n\n")
        f.write("void setup() {\n")
        f.write("  display.begin(0x3C, true);\n")
        f.write("  display.clearDisplay();\n")
        f.write("}\n\n")
        f.write("void loop() {\n")
        f.write("  for (int i = 0; i < sizeof(animation)/sizeof(animation[0]); i++) {\n")
        f.write("    display.clearDisplay();\n")
        f.write("    for (int y = 0; y < SCREEN_HEIGHT; y++) {\n")
        f.write("      for (int x = 0; x < SCREEN_WIDTH; x++) {\n")
        f.write("        if (pgm_read_byte(&animation[i][y]) & (1 << x)) {\n")
        f.write("          display.drawPixel(x, y, SH110X_WHITE);\n")
        f.write("        }\n")
        f.write("      }\n")
        f.write("    }\n")
        f.write("    display.display();\n")
        f.write("    delay(100);\n")
        f.write("  }\n")
        f.write("}\n")
    print(f"Code Arduino généré et enregistré dans {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_gif> <output_ino>")
    else:
        convert_gif_to_arduino(sys.argv[1], sys.argv[2])
