import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageColor, ImageTk
import numpy as np
from tkinterdnd2 import DND_FILES, TkinterDnD

class ImageDarkModeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Dark Mode Converter")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Variables
        self.input_path = None
        self.image_preview = None
        self.processed_preview = None

        # Build UI
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Drag and drop an image here OR use 'Select Image' button").pack(pady=5)

        # Drag-and-drop area
        self.drop_area = tk.Label(self.root, text="Drop Image Here", relief="ridge", width=50, height=5)
        self.drop_area.pack(pady=5)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        # Input selection button
        tk.Button(self.root, text="Select Image", command=self.select_input_file).pack(pady=5)
        self.input_label = tk.Label(self.root, text="No file selected", wraplength=580)
        self.input_label.pack(pady=5)

        # Color entries
        tk.Label(self.root, text="White replacement color (name, hex, or R,G,B):").pack()
        self.entry_white = tk.Entry(self.root)
        self.entry_white.insert(0, "#1a1a1a")
        self.entry_white.pack(pady=3, fill='x', padx=20)
        self.entry_white.bind("<KeyRelease>", self.update_preview)

        tk.Label(self.root, text="Black replacement color (name, hex, or R,G,B):").pack()
        self.entry_black = tk.Entry(self.root)
        self.entry_black.insert(0, "#ffffff")
        self.entry_black.pack(pady=3, fill='x', padx=20)
        self.entry_black.bind("<KeyRelease>", self.update_preview)

        # Save button
        self.btn_save = tk.Button(self.root, text="Save Processed Image", command=self.save_image, state="disabled")
        self.btn_save.pack(pady=15)

        # Previews
        tk.Label(self.root, text="Preview:").pack()
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack(pady=5)

    def darken(self, color, factor=0.6):
        return tuple(int(c * factor) for c in color)

    def parse_color(self, text):
        text = text.strip()
        try:
            rgb = ImageColor.getrgb(text)
            return (*rgb, 255)
        except ValueError:
            parts = text.split(',')
            if len(parts) == 3:
                r, g, b = (int(p.strip()) for p in parts)
                if all(0 <= c <= 255 for c in (r, g, b)):
                    return (r, g, b, 255)
        raise ValueError(f"Invalid color format: '{text}'")

    def process_image(self, img, white_text, black_text):
        white_color = self.parse_color(white_text)
        black_color = self.parse_color(black_text)

        img = img.convert('RGBA')
        data = np.array(img)
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

        mask_white = (r > 250) & (g > 250) & (b > 250)
        mask_black = (r < 10) & (g < 10) & (b < 10)
        mask_yellow = (r > 230) & (g > 230) & (b < 180) & (~mask_white)
        mask_red = (r > 230) & (g < 180) & (b < 180)

        data[mask_white] = white_color
        data[mask_black] = black_color
        data[mask_yellow] = self.darken((255, 255, 153)) + (255,)
        data[mask_red] = self.darken((255, 102, 102)) + (255,)

        return Image.fromarray(data)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.set_input_file(file_path)

    def on_drop(self, event):
        file_path = event.data.replace("{", "").replace("}", "")
        self.set_input_file(file_path)

    def set_input_file(self, file_path):
        self.input_path = file_path
        self.input_label.config(text=file_path)
        self.btn_save.config(state="normal")
        self.update_preview()

    def update_preview(self, event=None):
        if not self.input_path:
            return
        try:
            img = Image.open(self.input_path)
            white_text = self.entry_white.get()
            black_text = self.entry_black.get()
            processed_img = self.process_image(img, white_text, black_text)

            processed_img.thumbnail((400, 400))
            self.processed_preview = ImageTk.PhotoImage(processed_img)
            self.preview_label.config(image=self.processed_preview)
        except Exception as e:
            print("Preview update failed:", e)

    def save_image(self):
        if not self.input_path:
            return
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Images", "*.png"),
                ("JPEG Images", "*.jpg *.jpeg"),
                ("BMP Images", "*.bmp"),
                ("TIFF Images", "*.tiff"),
                ("GIF Images", "*.gif"),
                ("All files", "*.*")
            ],
            title="Save Processed Image"
        )
        if not output_path:
            return
        try:
            img = Image.open(self.input_path)
            processed_img = self.process_image(img, self.entry_white.get(), self.entry_black.get())
            processed_img.save(output_path)
            messagebox.showinfo("Saved", f"Image saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageDarkModeConverter(root)
    root.mainloop()
