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


def show_main_screen():
    canvas.pack(fill="both", expand=True)
    start_button.place(relx=0.3, rely=0.5)


def show_game_screen():
    canvas.pack_forget()
    start_button.place_forget()
    sound_slider.place_forget()
    initiate_game_screen(app)


def update_sound(volume):
    pygame.mixer.music.set_volume(float(volume) / 100)


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
pygame.mixer.music.load("screens/assets/soundtrack.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

volume_icon = Image.open(sound_icon_path)
volume_icon_resized = volume_icon.resize((35, 35))
volume_icon_image = ImageTk.PhotoImage(volume_icon_resized)

soldier_label = ctk.CTkLabel(app, image=volume_icon_image, text="", bg_color="#FDCF8F")
soldier_label.place(relx=1, rely=1, anchor="se", x=-200, y=-13)

sound_slider = ctk.CTkSlider(app,
                             width=120,
                             height=20,
                             from_=0,
                             to=100,
                             number_of_steps=100,
                             bg_color="#FDCF8F",
                             border_color="transparent",
                             button_color="black",
                             progress_color="black",
                             command=update_sound)
sound_slider.set(10)
sound_slider.place(relx=1, rely=1, anchor="se", x=-80, y=-16)

start_button = crete_start_button(app)
start_button.configure(command=show_game_screen)  # Updated command to call show_game_screen
start_button.place(relx=0.3, rely=0.5)

app.bind("<Configure>", resize_bg)
app.resizable(False, False)

show_main_screen()
app.mainloop()
