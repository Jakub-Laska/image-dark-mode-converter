# Image Dark Mode Converter

A simple Python application that converts images into a "dark mode" style by replacing white and black areas with user-defined colors. Built using **Tkinter** and **Pillow**, it provides an easy GUI for selecting and processing images.

---

## Features

- Replace white and black areas with custom colors (hex, RGB, or color names)  
- Darken yellow and red regions automatically for a consistent dark mode look  
- Supports multiple image formats: PNG, JPEG, BMP, TIFF, GIF  
- Simple, user-friendly GUI with file dialogs for input/output  
- Optional drag-and-drop support (requires `tkinterdnd2`)  

---

## Installation

1. Clone or download the repository  
2. Install the required Python packages:

```bash
pip install Pillow numpy
````

> For drag-and-drop support, also install:

```bash
pip install tkinterdnd2
```

3. Ensure Tkinter is installed (usually included with Python; on Linux, you may need `sudo apt install python3-tk`)

---

## Usage

1. Run the application:

```bash
python image_dark_mode_converter.py
```

2. Click **Select Image** to choose your input file
3. Enter replacement colors for white and black areas (hex, RGB, or color names)
4. Click **Process & Save Image** and choose the output file location
5. Your image will be saved with dark mode colors applied

---

## Color Input

* Hex format: `#1a1a1a`
* RGB format: `26,26,26`
* Named colors: `black`, `white`, `red`, etc.

---

## Notes

* The app automatically darkens yellow (`255,255,153`) and red (`255,102,102`) regions for consistency
* Drag-and-drop functionality is optional and requires `tkinterdnd2`

---
<!-- 
_______/\\\\\\\_______/\\\_____________        
 ______\/////\\\______\/\\\_____________       
  __________\/\\\______\/\\\_____________      
   __________\/\\\______\/\\\_____________     
    __________\/\\\______\/\\\_____________    
     __________\/\\\______\/\\\_____________   
      ___/\\\___\/\\\______\/\\\_____________  
       __\//\\\\\\\\\_______\/\\\\\\\\\\\\\___ 
        ___\/////////________\/////////////____ 
-->
