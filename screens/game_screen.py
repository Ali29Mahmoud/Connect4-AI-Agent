import customtkinter as ctk
from assets.guiAssets import *
from PIL import Image, ImageTk
from minmax import *
from expectiminmax import *

turn = 1

board_state = "0" * (rows * cols)
player_scores = {1: 0, 2: 0}


def get_cell(row, col, board):
    return board[row * cols + col]


def set_cell(row, col, value):
    global board_state
    index = row * cols + col
    board_state = board_state[:index] + value + board_state[index + 1:]


def make_ai_move(canvas, u_image, selected_algorithm, algo, levels):
    global turn, board_state, column_heights, image_refs
    if algo != "Expected Minimax":
        best_move, tree_root = selected_algorithm(board_state, 0)
        circleCol = best_move[0][1]
    else:
        print(board_state)
        expecti = ExpectiMinMax(board_state, levels, 2)
        best_move, node = expecti.solve_expectiminmax(1, 2)
        print(f"best move is {best_move}")
        circleCol = best_move

    if column_heights[circleCol] < rows:
        drop_row = rows - 1 - column_heights[circleCol]
        circle_x = circleCol * (cell_size + padding) + padding // 2
        circle_y = drop_row * (cell_size + padding) + padding // 2

        image_id = canvas.create_image(circle_x + cell_size // 2, circle_y + cell_size // 2 + 1, image=u_image)
        set_cell(drop_row, circleCol, "2")
        turn = 1

        image_refs[(circleCol, drop_row)] = image_id
        column_heights[circleCol] += 1

        update_scores()


def check_connected_4(board, player):
    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    connected_count = 0

    for row in range(rows):
        for col in range(cols):
            if get_cell(row, col, board) == str(player):
                for dx, dy in directions:
                    count = 1
                    for step in range(1, 4):
                        nx, ny = row + dx * step, col + dy * step
                        if in_bounds(nx, ny) and get_cell(nx, ny, board) == str(player):
                            count += 1
                        else:
                            break
                    if count == 4:
                        connected_count += 1

    return connected_count


def update_scores():
    player_scores[1] = check_connected_4(board_state, 1)
    player_scores[2] = check_connected_4(board_state, 2)

    score_label_1.configure(text=f"Human Agent: {player_scores[1]}")
    score_label_2.configure(text=f"AI Agent: {player_scores[2]}")


def initiate_game_screen(app, updated_turn, algo, levels):
    global turn, score_label_1, score_label_2, column_heights, image_refs, circle_positions
    turn = updated_turn

    ai = Connect4AI(user=1, comp=2, k=levels)

    selected_algorithm = None
    if algo == "Minimax without alpha-beta pruning" or algo == "Minimax with alpha-beta pruning":
        algo_selection = {
            "Minimax without alpha-beta pruning": ai.Maximize,
            "Minimax with alpha-beta pruning": ai.MaximizeWithPruning,
            "Expected Minimax": ExpectiMinMax(board_state, levels, 2).solve_expectiminmax
        }

        if algo in algo_selection:
            selected_algorithm = algo_selection[algo]

    app.configure(fg_color="#000000")
    for widget in app.winfo_children():
        widget.pack_forget()

    original_image1 = Image.open(circle_tile_image_path)
    resized_image1 = original_image1.resize((cell_size, cell_size))
    c_image = ImageTk.PhotoImage(resized_image1)

    original_image2 = Image.open(umbrella_tile_image_path)
    resized_image2 = original_image2.resize((cell_size, cell_size))
    u_image = ImageTk.PhotoImage(resized_image2)

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

    score_board_1 = ctk.CTkFrame(master=app,
                                 height=100,
                                 width=200,
                                 bg_color="black",
                                 fg_color="black",
                                 border_color="#DA0045",
                                 border_width=5,
                                 corner_radius=50)

    score_board_1.place(relx=0.15, rely=0.35, anchor=ctk.CENTER)

    score_board_2 = ctk.CTkFrame(master=app,
                                 height=100,
                                 width=200,
                                 bg_color="black",
                                 fg_color="black",
                                 border_color="#DA0045",
                                 border_width=5,
                                 corner_radius=50)

    score_board_2.place(relx=0.15, rely=0.6, anchor=ctk.CENTER)

    score_label_1 = ctk.CTkLabel(master=score_board_1, text=f"Human Agent: {player_scores[1]}",
                                 font=get_written_font(20))
    score_label_1.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    score_label_2 = ctk.CTkLabel(master=score_board_2, text=f"AI Agent: {player_scores[2]}", font=get_written_font(20))
    score_label_2.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    circle_positions = {}
    image_refs = {}
    column_heights = [0] * cols

    if updated_turn == 2:
        print("AI starts")
        make_ai_move(canvas, u_image, selected_algorithm, algo, levels)

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
                set_cell(drop_row, circleCol, "1")
                turn = 2
                image_refs[(circleCol, drop_row)] = image_id
                column_heights[circleCol] += 1
                update_scores()

                # Automatically make AI move after a short delay
                app.after(500, lambda: make_ai_move(canvas, u_image, selected_algorithm, algo, levels))

    for row in range(rows):
        for col in range(cols):
            x = col * (cell_size + padding) + padding // 2
            y = row * (cell_size + padding) + padding // 2
            circle_id = canvas.create_oval(x, y, x + cell_size, y + cell_size, outline="black", fill="#D4F06F")
            circle_positions[circle_id] = (row, col)
            canvas.tag_bind(circle_id, "<Button-1>", on_circle_click)

    app.mainloop()
