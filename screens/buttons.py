from game_screen import *
import customtkinter as ctk


def crete_start_button(app):
    NewGameButton = ctk.CTkButton(master=app,
                                  width=250,
                                  height=50,
                                  font=get_font(40),
                                  fg_color=dark_green,
                                  bg_color="#FED59A",
                                  hover_color=bright_green,
                                  border_color=dark_green,
                                  corner_radius=100,
                                  text='New Game',
                                  anchor=ctk.CENTER,
                                  command=initiate_game_screen)

    return NewGameButton
