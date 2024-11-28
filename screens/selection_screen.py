from game_screen import *
import pygame


def show_game_screen(app, turn):
    initiate_game_screen(app, turn)


def on_selection(app, starter):
    ctk.CTkFrame(master=app, fg_color="black", width=400, height=200).place(relx=0.5, rely=0.8, anchor="center")
    starter_label = ctk.CTkLabel(master=app, text=f"{starter} will start", font=get_font(30), text_color="white")
    starter_label.place(relx=0.5, rely=0.7, anchor='center')

    if starter == "Human Agent":
        turn = 1
    else:
        turn = 2

    Start_button = ctk.CTkButton(master=app,
                                 fg_color="#DA0045",
                                 width=100, height=50,
                                 text="Start Game",
                                 font=get_font(30),
                                 command=lambda:show_game_screen(app, turn))

    Start_button.configure()
    Start_button.place(relx=0.5, rely=0.8, anchor='center')


def initiate_selection_screen(app):
    app.configure(fg_color="black")

    # Title label
    label = ctk.CTkLabel(master=app, text="Select Who Starts", font=get_font(45))
    label.place(relx=0.5, rely=0.1, anchor='center')

    # Load and resize images
    original_image1 = Image.open(circle_tile_image_path)
    resized_image1 = original_image1.resize((100, 100))
    c_image = ImageTk.PhotoImage(resized_image1)

    original_image2 = Image.open(umbrella_tile_image_path)
    resized_image2 = original_image2.resize((100, 100))
    u_image = ImageTk.PhotoImage(resized_image2)

    # Buttons for Human and AI
    player1_button = ctk.CTkButton(
        master=app,
        image=c_image,
        text="",
        fg_color="transparent",
        hover_color="gray",
        width=100,
        height=100,
        command=lambda: on_selection(app, "Human Agent")
    )
    player1_button.place(relx=0.3, rely=0.3, anchor='center')

    player1_label = ctk.CTkLabel(master=app, text="You", font=get_font(45))
    player1_label.place(relx=0.4, rely=0.3, anchor='center')

    player2_button = ctk.CTkButton(
        master=app,
        image=u_image,
        text="",
        fg_color="transparent",
        hover_color="gray",
        width=100,
        height=100,
        command=lambda: on_selection(app, "AI Agent")
    )
    player2_button.place(relx=0.3, rely=0.5, anchor='center')

    player2_label = ctk.CTkLabel(master=app, text="AI Agent", font=get_font(45))
    player2_label.place(relx=0.45, rely=0.5, anchor='center')

    app.mainloop()
