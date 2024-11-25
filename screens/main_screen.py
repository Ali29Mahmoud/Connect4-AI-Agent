from game_screen import *
import pygame


def resize_bg_to_initial():
    global bg_photo
    window_width = app.winfo_width()
    window_height = app.winfo_height()
    resized_bg_image = bg_image.resize((window_width, window_height))
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
app.after(100, resize_bg_to_initial)

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

start_button = ctk.CTkButton(master=app,
                             width=250,
                             height=50,
                             font=get_font(40),
                             fg_color=dark_green,
                             bg_color="#FED59A",
                             hover_color=bright_green,
                             border_color=dark_green,
                             corner_radius=100,
                             text='New Game',
                             anchor=ctk.CENTER)
start_button.configure(command=show_game_screen)
start_button.place(relx=0.3, rely=0.5)

option1 = ctk.CTkCheckBox(master=app,
                          text="Minimax without alpha-beta pruning",
                          text_color='black',
                          font=get_written_font(18),
                          bg_color="#FED59A",
                          corner_radius=20).place(relx=0.425, rely=0.65, anchor=ctk.CENTER)


option2 = ctk.CTkCheckBox(master=app,
                          text="Minimax with alpha-beta pruning",
                          text_color='black',
                          font=get_written_font(18),
                          bg_color="#FED59A",
                          corner_radius=20).place(relx=0.425, rely=0.7, anchor=ctk.CENTER)


option3 = ctk.CTkCheckBox(master=app,
                          text="Expected Minimax",
                          text_color='black',
                          font=get_written_font(18),
                          bg_color="#FED59A",
                          corner_radius=20).place(relx=0.425, rely=0.75, anchor=ctk.CENTER)

app.resizable(False, False)

show_main_screen()
app.mainloop()
