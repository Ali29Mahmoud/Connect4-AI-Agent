import customtkinter as ctk
from assets.guiAssets import *
from PIL import Image, ImageTk

turn = 1


def initiate_game_screen(app):
    app.configure(fg_color="#000000")
    # Clear main screen widgets if necessary
    for widget in app.winfo_children():
        widget.pack_forget()

    original_image1 = Image.open(circle_tile_image_path)
    resized_image1 = original_image1.resize((cell_size, cell_size))
    c_image = ImageTk.PhotoImage(resized_image1)

    original_image2 = Image.open(umbrella_tile_image_path)
    resized_image2 = original_image2.resize((cell_size, cell_size))
    u_image = ImageTk.PhotoImage(resized_image2)

    # Additional assets for Squid Game theme
    soldier_tri = Image.open(soldier_tri_path)
    resized_image_soldier_tri = soldier_tri.resize((73, 125))
    soldier_tri_image = ImageTk.PhotoImage(resized_image_soldier_tri)

    soldier_squ = Image.open(soldier_square_path)
    resized_image_soldier_squ = soldier_squ.resize((73, 125))
    soldier_squ_image = ImageTk.PhotoImage(resized_image_soldier_squ)

    soldier_cir = Image.open(soldier_cir_path)
    resized_image_soldier_cir = soldier_cir.resize((73, 125))
    soldier_cir_image = ImageTk.PhotoImage(resized_image_soldier_cir)

    soldier_tri_w_gun = Image.open(soldier_tri_w_gun_path)
    resized_image_soldier_tri_w_gun = soldier_tri_w_gun.resize((120, 125))
    soldier_tri_w_gun_image = ImageTk.PhotoImage(resized_image_soldier_tri_w_gun)

    Seon_Gi_Hun = Image.open(Seon_Gi_Hun_path)
    resized_image_Seon_Gi_Hun = Seon_Gi_Hun.resize((92, 129))
    Seon_Gi_Hun_image = ImageTk.PhotoImage(resized_image_Seon_Gi_Hun)

    board = ctk.CTkFrame(master=app,
                         width=cols * cell_size + 200,
                         height=rows * cell_size + 300,
                         bg_color="black",
                         fg_color="black",
                         corner_radius=25)

    board.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    quote_label = ctk.CTkLabel(master=board,
                               text="You've Got a Reason \nTo Get Out Of This Place,\n But I Don't.",
                               font=get_written_font(25))
    quote_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    soldier_label = ctk.CTkLabel(board, image=soldier_tri_image, text="")
    soldier_label.place(relx=1, rely=1, anchor="se", x=-70, y=-10)

    soldier_label = ctk.CTkLabel(board, image=soldier_squ_image, text="")
    soldier_label.place(relx=1, rely=1, anchor="se", x=-150, y=-10)

    soldier_label = ctk.CTkLabel(board, image=soldier_cir_image, text="")
    soldier_label.place(relx=1, rely=1, anchor="se", x=-230, y=-10)

    soldier_label = ctk.CTkLabel(board, image=soldier_tri_w_gun_image, text="")
    soldier_label.place(relx=1, rely=1, anchor="se", x=-310, y=-10)

    soldier_label = ctk.CTkLabel(board, image=Seon_Gi_Hun_image, text="")
    soldier_label.place(relx=1, rely=1, anchor="se", x=-420, y=-10)

    # Game board setup
    main_board = ctk.CTkFrame(master=app,
                              width=cols * cell_size,
                              height=rows * cell_size + 4,
                              bg_color="#037a76",
                              fg_color="#037a76",
                              corner_radius=0)
    main_board.place(relx=0.497, rely=0.495, anchor=ctk.CENTER)

    canvas = ctk.CTkCanvas(app,
                           width=cols * (cell_size + padding),
                           height=rows * (cell_size + padding),
                           bg="#249f9c",
                           highlightbackground="#249f9c")
    canvas.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    circle_positions = {}
    image_refs = {}

    column_heights = [0] * cols

    def on_circle_click(event):
        global turn

        clicked_item = canvas.find_withtag("current")[0]
        circleRow, circleCol = circle_positions[clicked_item]

        if column_heights[circleCol] < rows:
            drop_row = rows - 1 - column_heights[circleCol]
            circle_x = circleCol * (cell_size + padding) + padding // 2
            circle_y = drop_row * (cell_size + padding) + padding // 2

            if turn == 1:
                image_id = canvas.create_image(circle_x + cell_size // 2, circle_y + cell_size // 2 + 1, image=c_image)
                turn = 2
            else:
                image_id = canvas.create_image(circle_x + cell_size // 2, circle_y + cell_size // 2 + 1, image=u_image)
                turn = 1

            image_refs[(circleCol, drop_row)] = image_id
            column_heights[circleCol] += 1

    for row in range(rows):
        for col in range(cols):
            x = col * (cell_size + padding) + padding // 2
            y = row * (cell_size + padding) + padding // 2
            circle_id = canvas.create_oval(x, y, x + cell_size, y + cell_size, outline="black", fill="#D4F06F")
            circle_positions[circle_id] = (row, col)
            canvas.tag_bind(circle_id, "<Button-1>", on_circle_click)

    app.mainloop()
