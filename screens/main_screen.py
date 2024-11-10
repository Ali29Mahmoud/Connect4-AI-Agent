from PIL import Image, ImageTk
from buttons import *
from assets.guiAssets import *
import pygame
import time


def resize_bg(event):
    global last_resize_time, last_width, last_height
    current_time = time.time()

    if current_time - last_resize_time < 0.1:
        return

    if abs(event.width - last_width) < 20 and abs(event.height - last_height) < 20:
        return

    last_resize_time = current_time
    last_width, last_height = event.width, event.height

    resized_bg_image = bg_image.resize((event.width, event.height))
    bg_photo = ImageTk.PhotoImage(resized_bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo


ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("960x650")
app.title("Connect 4")
app.iconbitmap(icon_path)
bg_image = Image.open(bg_image_path)

canvas = ctk.CTkCanvas(app, highlightthickness=0)
canvas.pack(fill="both", expand=True)

last_resize_time = 0
last_width, last_height = app.winfo_width(), app.winfo_height()


pygame.mixer.init()
pygame.mixer.music.load("assets/soundtrack.mp3")  # Replace with your audio file path
pygame.mixer.music.set_volume(0.5)  # Set volume between 0.0 and 1.0
pygame.mixer.music.play(-1)  # Loop indefinitely

crete_start_button(app).place(relx=0.3, rely=0.5)

app.bind("<Configure>", resize_bg)
app.resizable(False, False)
app.mainloop()
