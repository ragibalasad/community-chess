import os
import cairosvg


INPUT_FOLDER = "assets/svg_pieces"
OUTPUT_FOLDER = "assets/png_pieces"
WIDTH = HEIGHT = 90

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def convert_svg_to_png(svg_path, png_path, width, height):

    for filename in os.listdir(svg_path):
        if filename.lower().endswith(".svg"):
            svg_path = os.path.join(svg_path, filename)
            png_filename = os.path.splitext(filename)[0] + ".png"
            png_path = os.path.join(png_path, png_filename)

            with open(svg_path, "rb") as svg_file:
                cairosvg.svg2png(
                    file_obj=svg_file,
                    write_to=png_path,
                    output_width=width,
                    output_height=height,
                )
            print(f"✔ Converted {filename} → {png_filename}")


if __name__ == "__main__":
    convert_svg_to_png(INPUT_FOLDER, OUTPUT_FOLDER, WIDTH, HEIGHT)
    print("SVG to PNG conversion complete.")
