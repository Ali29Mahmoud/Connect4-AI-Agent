import pygame
from pygame.locals import *



def drawTreeMinMax(root, depth):
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 16000, 2000  # Larger virtual surface for scrolling
    global virtual_surface
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 1200, 800

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Interactive Tree with Node Content")

    # Create a virtual surface for drawing


    # Scrollbar dimensions
    SCROLLBAR_THICKNESS = 20

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    NODE_COLOR = (100, 200, 255)
    CONTENT_BG = (240, 240, 240)
    SCROLLBAR_BG = (220, 220, 220)
    SCROLLBAR_FG = (180, 180, 180)

    # Font
    font = pygame.font.SysFont(None, 24)

    # Scroll position
    scroll_x = 0
    scroll_y = 0
    dragging_horizontal = False
    dragging_vertical = False

    def calculate_subtree_width(node, horizontal_spacing=150):
        if not node.children or not node.expanded:
            return horizontal_spacing
        return sum(calculate_subtree_width(child, horizontal_spacing) for child in node.children)


    def draw_trapezoid(surface, color, x, y, width, height, upside_down=False):
        top_width = width // 2
        bottom_width = width
        if upside_down:
            points = [
                (x - bottom_width // 2, y),  # top-left
                (x + bottom_width // 2, y),  # top-right
                (x + top_width // 2, y + height),  # bottom-right
                (x - top_width // 2, y + height)  # bottom-left
            ]
        else:
            points = [
                (x - top_width // 2, y),  # top-left
                (x + top_width // 2, y),  # top-right
                (x + bottom_width // 2, y + height),  # bottom-right
                (x - bottom_width // 2, y + height)  # bottom-left
            ]
        pygame.draw.polygon(surface, color, points)


    def wrap_text(text, font, max_width):
        lines = []
        words = text.split(" ")
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_text = font.render(test_line, True, BLACK)
            if test_text.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        return lines


    def get_node_level(node, level=0):

        if node == root:
            return 0

        def find_level(current_node, target, current_level):
            if current_node == target:
                return current_level
            if not current_node.children:
                return None
            for child in current_node.children:
                result = find_level(child, target, current_level + 1)
                if result is not None:
                    return result
            return None

        return find_level(root, node, 0) or 0


    def is_point_in_polygon(x, y, points):
        """Ray casting algorithm to determine if point is inside polygon"""
        n = len(points)
        inside = False

        j = n - 1
        for i in range(n):
            if ((points[i][1] > y) != (points[j][1] > y)) and \
                    (x < (points[j][0] - points[i][0]) * (y - points[i][1]) /
                     (points[j][1] - points[i][1]) + points[i][0]):
                inside = not inside
            j = i

        return inside


    def get_clicked_node(node, pos):
        # Adjust click position for scrolling
        adjusted_x = pos[0] + scroll_x
        adjusted_y = pos[1] + scroll_y

        # Define trapezoid boundaries
        node_width = 60
        node_height = 40
        level = get_node_level(node)
        upside_down = level % 2 != 0

        # Calculate trapezoid points
        top_width = node_width // 2
        bottom_width = node_width

        if upside_down:
            points = [
                (node.x - bottom_width // 2, node.y),  # top-left
                (node.x + bottom_width // 2, node.y),  # top-right
                (node.x + top_width // 2, node.y + node_height),  # bottom-right
                (node.x - top_width // 2, node.y + node_height)  # bottom-left
            ]
        else:
            points = [
                (node.x - top_width // 2, node.y),  # top-left
                (node.x + top_width // 2, node.y),  # top-right
                (node.x + bottom_width // 2, node.y + node_height),  # bottom-right
                (node.x - bottom_width // 2, node.y + node_height)  # bottom-left
            ]

        # Check if click is inside trapezoid
        if is_point_in_polygon(adjusted_x, adjusted_y, points):
            return node

        # Check children if expanded
        if node.expanded:
            for child in node.children:
                result = get_clicked_node(child, pos)
                if result:
                    return result
        return None


    def render_tree(node, x, y, level=0, horizontal_spacing=150):
        global virtual_surface

        # Set the node's position
        node.x, node.y = x, y

        # Determine trapezoid orientation
        upside_down = level % 2 != 0
        node_width = 60
        node_height = 40

        # Draw the trapezoid representing the node
        draw_trapezoid(virtual_surface, NODE_COLOR, x, y, node_width, node_height, upside_down)

        # Render the node's value in the trapezoid
        value_text = font.render(str(node.val), True, BLACK)
        text_rect = value_text.get_rect(center=(x, y + node_height // 2))
        virtual_surface.blit(value_text, text_rect)

        # If the node is expanded, recursively draw its children
        if node.expanded:
            total_width = calculate_subtree_width(node, horizontal_spacing)
            child_x = x - total_width // 2

            for child in node.children:
                child_width = calculate_subtree_width(child, horizontal_spacing)

                # Draw connecting lines to children
                pygame.draw.line(
                    virtual_surface, GRAY,
                    (x, y + node_height // 2),
                    (child_x + child_width // 2, y + node_height + 20)
                )

                # Recursively render the subtree
                render_tree(child, child_x + child_width // 2, y + node_height + 20, level + 1, horizontal_spacing)
                child_x += child_width




    def is_click_inside_content_window(pos, node):
        if node:
            window_width, window_height = 200, 100
            window_x = min(node.x - scroll_x + 50, WIDTH - window_width)
            window_y = max(node.y - scroll_y - 50, 0)
            if (window_x <= pos[0] <= window_x + window_width) and (window_y <= pos[1] <= window_y + window_height):
                return True
        return False


    def render_content_window(node):
        if node:
            window_width, window_height = 500, 150
            window_x = min(node.x - scroll_x + 50, WIDTH - window_width)
            window_y = max(node.y - scroll_y - 50, 0)

            # Draw the content window background
            pygame.draw.rect(screen, CONTENT_BG, (window_x, window_y, window_width, window_height))
            pygame.draw.rect(screen, BLACK, (window_x, window_y, window_width, window_height), 2)

            attributes = [
                f"State: {node.state}",
                f"Column: {node.col}",
                f"Value: {node.val}",
                f"Alpha: {node.alpha}",
                f"Beta: {node.beta}",
            ]

            # Render each attribute
            for i, attr in enumerate(attributes):
                text = font.render(attr, True, BLACK)
                screen.blit(text, (window_x + 10, window_y + 10 + i * 20))



    def draw_scrollbars():
        # Horizontal scrollbar
        pygame.draw.rect(screen, SCROLLBAR_BG,
                         (0, HEIGHT - SCROLLBAR_THICKNESS, WIDTH - SCROLLBAR_THICKNESS, SCROLLBAR_THICKNESS))
        scroll_ratio_x = WIDTH / VIRTUAL_WIDTH
        thumb_width = max(50, scroll_ratio_x * (WIDTH - SCROLLBAR_THICKNESS))
        thumb_x = (scroll_x / (VIRTUAL_WIDTH - WIDTH)) * (WIDTH - SCROLLBAR_THICKNESS - thumb_width)
        pygame.draw.rect(screen, SCROLLBAR_FG, (thumb_x, HEIGHT - SCROLLBAR_THICKNESS, thumb_width, SCROLLBAR_THICKNESS))

        # Vertical scrollbar
        pygame.draw.rect(screen, SCROLLBAR_BG,
                         (WIDTH - SCROLLBAR_THICKNESS, 0, SCROLLBAR_THICKNESS, HEIGHT - SCROLLBAR_THICKNESS))
        scroll_ratio_y = HEIGHT / VIRTUAL_HEIGHT
        thumb_height = max(50, scroll_ratio_y * (HEIGHT - SCROLLBAR_THICKNESS))
        thumb_y = (scroll_y / (VIRTUAL_HEIGHT - HEIGHT)) * (HEIGHT - SCROLLBAR_THICKNESS - thumb_height)
        pygame.draw.rect(screen, SCROLLBAR_FG, (WIDTH - SCROLLBAR_THICKNESS, thumb_y, SCROLLBAR_THICKNESS, thumb_height))


    # Main loop
    running = True
    selected_node = None

    while running:
        virtual_surface.fill(WHITE)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.pos[1] > HEIGHT - SCROLLBAR_THICKNESS and event.pos[0] < WIDTH - SCROLLBAR_THICKNESS:
                    dragging_horizontal = True
                elif event.pos[0] > WIDTH - SCROLLBAR_THICKNESS and event.pos[1] < HEIGHT - SCROLLBAR_THICKNESS:
                    dragging_vertical = True
                else:
                    clicked_node = get_clicked_node(root, event.pos)
                    if clicked_node:
                        clicked_node.toggle()
                        if selected_node == clicked_node:
                            selected_node = None
                        else:
                            selected_node = clicked_node
                    elif not is_click_inside_content_window(event.pos, selected_node):
                        selected_node = None
            elif event.type == MOUSEBUTTONUP:
                dragging_horizontal = False
                dragging_vertical = False
            elif event.type == MOUSEMOTION:
                if dragging_horizontal:
                    scroll_ratio_x = (VIRTUAL_WIDTH - WIDTH) / (WIDTH - SCROLLBAR_THICKNESS)
                    scroll_x = min(max(0, scroll_x + event.rel[0] * scroll_ratio_x), VIRTUAL_WIDTH - WIDTH)
                if dragging_vertical:
                    scroll_ratio_y = (VIRTUAL_HEIGHT - HEIGHT) / (HEIGHT - SCROLLBAR_THICKNESS)
                    scroll_y = min(max(0, scroll_y + event.rel[1] * scroll_ratio_y), VIRTUAL_HEIGHT - HEIGHT)

        # Render the tree on virtual surface
        render_tree(root, VIRTUAL_WIDTH // 2, 50, horizontal_spacing=150)

        # Draw the visible portion of the virtual surface onto the screen
        screen.blit(virtual_surface, (-scroll_x, -scroll_y))

        # Draw scrollbars
        draw_scrollbars()

        # Render content window for the selected node
        render_content_window(selected_node)

        pygame.display.flip()

    pygame.quit()
