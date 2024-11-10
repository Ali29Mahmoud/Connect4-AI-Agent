import customtkinter as ctk
from assets.guiAssets import *


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
                                  anchor=ctk.CENTER)

    return NewGameButton
