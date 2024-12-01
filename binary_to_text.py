import requests
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
import random

def binary_to_text(binary_str):
    binary_values = binary_str.split(' ')
    ascii_str = ''.join([chr(int(bv, 2)) for bv in binary_values])
    return ascii_str

def text_to_binary(text):
    binary_str = ' '.join(format(ord(char), '08b') for char in text)
    return binary_str

def generate_image_from_text(description, api_key):
    url = 'https://api.your-image-generation-service.com/generate'
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'prompt': description, 'size': '512x512'}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        image_data = response.json().get('image')
        img_bytes = base64.b64decode(image_data)
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'wb') as img_file:
                img_file.write(img_bytes)
            messagebox.showinfo("Success", "Image created successfully!")
    else:
        messagebox.showerror("Error", f"Failed to create image: {response.status_code}")

def on_preview_binary():
    binary_input = binary_entry.get()
    text_description = binary_to_text(binary_input)
    translated_text_box.delete("1.0", tk.END)
    translated_text_box.insert(tk.END, text_description)

def on_preview_text():
    text_input = text_entry.get("1.0", tk.END).strip()
    binary_description = text_to_binary(text_input)
    translated_text_box.delete("1.0", tk.END)
    translated_text_box.insert(tk.END, binary_description)

def on_generate():
    text_description = translated_text_box.get("1.0", tk.END).strip()
    api_key = api_entry.get()
    generate_image_from_text(text_description, api_key)

def on_paste_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "rb") as img_file:
            img_bytes = img_file.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            image_binary = ' '.join(format(byte, '08b') for byte in img_bytes)
            translated_text_box.delete("1.0", tk.END)
            translated_text_box.insert(tk.END, image_binary)
            image = Image.open(io.BytesIO(img_bytes))
            image = ImageTk.PhotoImage(image)
            image_label.config(image=image)
            image_label.image = image

def on_clear():
    binary_entry.delete(0, tk.END)
    text_entry.delete("1.0", tk.END)
    translated_text_box.delete("1.0", tk.END)
    image_label.config(image='')
    image_label.image = None
    api_entry.delete(0, tk.END)

def on_quit():
    root.destroy()

def add_matrix_effect(canvas, width, height):
    for _ in range(100):
        x = random.randint(0, width)
        for y in range(0, height, 15):
            text = random.choice(['1', '0'])
            canvas.create_text(x, y, text=text, fill='green', font=("Courier", 10), anchor='nw', tags='matrix')

def resize(event):
    canvas.delete('matrix')
    add_matrix_effect(canvas, event.width, event.height)

# Create GUI
root = tk.Tk()
root.title("Binary to Image Generator ® by Admir")

# Maximize window to screen size
root.state('zoomed')

root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas.bind('<Configure>', resize)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
add_matrix_effect(canvas, screen_width, screen_height)

frame = tk.Frame(root, bg='black')
frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(frame, text="Enter Binary Data (separated by space):", fg='green', bg='black', font=("Courier", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
binary_entry = tk.Entry(frame, width=50, bg='black', fg='green', font=("Courier", 12))
binary_entry.grid(row=0, column=1, padx=5, pady=5)

preview_binary_button = tk.Button(frame, text="Preview Binary", command=on_preview_binary, bg='green', fg='black', font=("Courier", 12))
preview_binary_button.grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame, text="Paste Text Here:", fg='green', bg='black', font=("Courier", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
text_entry = tk.Text(frame, height=5, width=50, bg='black', fg='green', font=("Courier", 12))
text_entry.grid(row=1, column=1, padx=5, pady=5)

preview_text_button = tk.Button(frame, text="Preview Text", command=on_preview_text, bg='green', fg='black', font=("Courier", 12))
preview_text_button.grid(row=1, column=2, padx=5, pady=5)

tk.Label(frame, text="Translated Text / Binary:", fg='green', bg='black', font=("Courier", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
translated_text_box = tk.Text(frame, height=5, width=50, bg='black', fg='green', font=("Courier", 12))
translated_text_box.grid(row=2, column=1, padx=5, pady=5)

copy_button = tk.Button(frame, text="Copy", command=lambda: root.clipboard_append(translated_text_box.get("1.0", tk.END)), bg='green', fg='black', font=("Courier", 12))
copy_button.grid(row=2, column=2, padx=5, pady=5)

tk.Label(frame, text="API Key:", fg='green', bg='black', font=("Courier", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
api_entry = tk.Entry(frame, width=50, show='*', bg='black', fg='green', font=("Courier", 12))
api_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

generate_button = tk.Button(frame, text="Generate Image", command=on_generate, bg='green', fg='black', font=("Courier", 12))
generate_button.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

paste_image_button = tk.Button(frame, text="Paste Image", command=on_paste_image, bg='green', fg='black', font=("Courier", 12))
paste_image_button.grid(row=5, column=0, columnspan=3, padx=5, pady=10)

clear_button = tk.Button(frame, text="Clear", command=on_clear, bg='green', fg='black', font=("Courier", 12))
clear_button.grid(row=6, column=0, columnspan=3, padx=5, pady=10)

quit_button = tk.Button(frame, text="Quit", command=on_quit, bg='red', fg='black', font=("Courier", 12))
quit_button.grid(row=7, column=0, columnspan=3, padx=5, pady=10)

image_label = tk.Label(frame, bg='black')
image_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

# Bind window controls for maximizing, minimizing, and closing
root.protocol("WM_DELETE_WINDOW", on_quit)
root.bind('<Escape>', lambda e: root.state('iconic'))
root.bind('<F11>', lambda e: root.state('zoomed'))

root.mainloop()
