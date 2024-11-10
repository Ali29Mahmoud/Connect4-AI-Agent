import customtkinter as ctk
from guiAssets import *
from PIL import Image, ImageTk


root = ctk.CTk()
root.geometry("960x650")
root.configure(fg_color="#000000")
root.resizable(False, False)

#Tile 1
original_image1 = Image.open(circle_tile_image_path)
resized_image1 = original_image1.resize((cell_size, cell_size))
c_image = ImageTk.PhotoImage(resized_image1)


#Tile 2
original_image2 = Image.open(umbrella_tile_image_path)
resized_image2 = original_image2.resize((cell_size, cell_size))
u_image = ImageTk.PhotoImage(resized_image2)

#Soldier triangle
soldier_tri = Image.open(soldier_tri_path)
resized_image_soldier_tri = soldier_tri.resize((73, 125))
soldier_tri_image = ImageTk.PhotoImage(resized_image_soldier_tri)

#Soldier square
soldier_squ = Image.open(soldier_square_path)
resized_image_soldier_squ = soldier_squ.resize((73, 125))
soldier_squ_image = ImageTk.PhotoImage(resized_image_soldier_squ)

#Soldier circle
soldier_cir = Image.open(soldier_cir_path)
resized_image_soldier_cir = soldier_cir.resize((73, 125))
soldier_cir_image = ImageTk.PhotoImage(resized_image_soldier_cir)

#Soldier triangle with a gun
soldier_tri_w_gun= Image.open(soldier_tri_w_gun_path)
resized_image_soldier_tri_w_gun = soldier_tri_w_gun.resize((120, 125))
soldier_tri_w_gun_image = ImageTk.PhotoImage(resized_image_soldier_tri_w_gun)

#Participant
Seon_Gi_Hun = Image.open(Seon_Gi_Hun_path)
resized_image_Seon_Gi_Hun = Seon_Gi_Hun.resize((92, 129))
Seon_Gi_Hun_image = ImageTk.PhotoImage(resized_image_Seon_Gi_Hun)



board = ctk.CTkFrame(master=root,
                     width=cols * cell_size + 200,
                     height=rows * cell_size + 300,
                     bg_color="black",
                     fg_color="black",
                     corner_radius=25)

board.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

Quote = "You've Got a Reason \nTo Get Out Of This Place,\n But I Don't."

quote_label = ctk.CTkLabel(master=board,
                           text=Quote,
                           font= get_written_font(25))

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


main_board = ctk.CTkFrame(master=root,
                          width=cols * cell_size,
                          height=rows * cell_size + 4,
                          bg_color="#037a76",
                          fg_color="#037a76",
                          corner_radius=0)
main_board.place(relx=0.497, rely=0.495, anchor=ctk.CENTER)

upper_bar = ctk.CTkFrame(master=main_board,
                         width=cols * cell_size - 12,
                         height=4,
                         bg_color="#A0A0A0",
                         fg_color="#A0A0A0")
upper_bar.place(relx=0.505, rely=0.01, anchor=ctk.CENTER)

canvas = ctk.CTkCanvas(root,
                       width=cols * (cell_size + padding),
                       height=rows * (cell_size + padding),
                       bg="#249f9c",
                       highlightbackground="#249f9c")
canvas.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

circle_positions = {}
image_refs = {}

column_heights = [0] * cols

turn = 1

def on_circle_click(event):
    global turn

    clicked_item = canvas.find_withtag("current")[0]
    row, col = circle_positions[clicked_item]

    if column_heights[col] < rows:
        drop_row = rows - 1 - column_heights[col]
        x = col * (cell_size + padding) + padding // 2
        y = drop_row * (cell_size + padding) + padding // 2

        if turn == 1:
            image_id = canvas.create_image(x + cell_size // 2, y + cell_size // 2 + 1, image=c_image)
            turn = 2
        else:
            image_id = canvas.create_image(x + cell_size // 2, y + cell_size // 2 + 1, image=u_image)
            turn = 1

        image_refs[(col, drop_row)] = image_id
        column_heights[col] += 1


for row in range(rows):
    for col in range(cols):
        x = col * (cell_size + padding) + padding // 2
        y = row * (cell_size + padding) + padding // 2
        circle_id = canvas.create_oval(x, y, x + cell_size, y + cell_size, outline="black", fill="#D4F06F")
        circle_positions[circle_id] = (row, col)
        canvas.tag_bind(circle_id, "<Button-1>", on_circle_click)

root.mainloop()
