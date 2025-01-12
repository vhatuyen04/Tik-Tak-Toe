import pygame
import sys

pygame.init()
CELL_SIZE = 20 
GRID_SIZE = 1000 
DISPLAY_GRID = 30
SCREEN_SIZE = CELL_SIZE * DISPLAY_GRID
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Tic-Tac-Toe 5-in-a-Row")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 36)

def draw_grid():
    for x in range(DISPLAY_GRID):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, SCREEN_SIZE))
    for y in range(DISPLAY_GRID):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (SCREEN_SIZE, y * CELL_SIZE))

def display_winner_message(winner):
    if winner == "X":
        message = "Player 1 wins!"
        color = RED
    else:
        message = "Player 2 wins!"
        color = BLUE
    win_text = font.render(message, True, color)
    text_rect = win_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 - 120))
    screen.blit(win_text, text_rect)

def draw_buttons():
    replay_button = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 - 60, 200, 50)
    menu_button = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 + 20, 200, 50)
    
    pygame.draw.rect(screen, WHITE, replay_button)
    pygame.draw.rect(screen, WHITE, menu_button)
    
    replay_text = font.render("Replay", True, BLACK)
    menu_text = font.render("Main Menu", True, BLACK)
    screen.blit(replay_text, (replay_button.x + (replay_button.width - replay_text.get_width()) // 2, 
                               replay_button.y + (replay_button.height - replay_text.get_height()) // 2))
    screen.blit(menu_text, (menu_button.x + (menu_button.width - menu_text.get_width()) // 2, 
                             menu_button.y + (menu_button.height - menu_text.get_height()) // 2))
    
    return replay_button, menu_button

def game_over_screen(winner):
    screen.fill(GRAY)
    display_winner_message(winner)
    replay_button, menu_button = draw_buttons()
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse_pos):
                    return "restart"
                elif menu_button.collidepoint(mouse_pos):
                    return "menu"  

def check_five_in_a_row(board, row, col, current_player):
    def count_consecutive(dx, dy):
        count = 0
        r, c = row, col
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == current_player:
            count += 1
            r += dy
            c += dx
        return count

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = count_consecutive(dx, dy) + count_consecutive(-dx, -dy) - 1
        if count >= 5:
            return True
    return False

def main_game():
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    offset_x, offset_y = 0, 0
    dragging = False
    dragged = False  
    drag_start_pos = (0, 0)
    accumulated_dx, accumulated_dy = 0, 0 
    game_over = False 
    winner = None 

    while True:  
        screen.fill(WHITE)
        draw_grid()
        
        for row in range(DISPLAY_GRID):
            for col in range(DISPLAY_GRID):
                board_row = row + offset_y
                board_col = col + offset_x
                if board[board_row][board_col] == "X":
                    color = RED
                elif board[board_row][board_col] == "O":
                    color = BLUE
                else:
                    continue
                mark_text = font.render(board[board_row][board_col], True, color)
                text_rect = mark_text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(mark_text, text_rect)

        if game_over:
            pygame.display.flip()
            pygame.time.delay(2000)
            result = game_over_screen(winner)
            if result == "menu":
                return  
            elif result == "restart":
                main_game() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        dragging = True
                        dragged = False  
                        drag_start_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  
                        if dragging and not dragged:  
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            row, col = (mouse_y // CELL_SIZE) + offset_y, (mouse_x // CELL_SIZE) + offset_x
                            if board[row][col] == "":
                                board[row][col] = current_player
                                if check_five_in_a_row(board, row, col, current_player):
                                    winner = current_player  
                                    game_over = True  

                                current_player = "O" if current_player == "X" else "X"
                        dragging = False
                        accumulated_dx, accumulated_dy = 0, 0  

                elif event.type == pygame.MOUSEMOTION and dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    accumulated_dx += drag_start_pos[0] - mouse_x
                    accumulated_dy += drag_start_pos[1] - mouse_y

                    while abs(accumulated_dx) >= CELL_SIZE:
                        if accumulated_dx > 0:
                            offset_x = min(GRID_SIZE - DISPLAY_GRID, offset_x + 1)
                            accumulated_dx -= CELL_SIZE
                        else:
                            offset_x = max(0, offset_x - 1)
                            accumulated_dx += CELL_SIZE

                    while abs(accumulated_dy) >= CELL_SIZE:
                        if accumulated_dy > 0:
                            offset_y = min(GRID_SIZE - DISPLAY_GRID, offset_y + 1)
                            accumulated_dy -= CELL_SIZE
                        else:
                            offset_y = max(0, offset_y - 1)
                            accumulated_dy += CELL_SIZE

                    drag_start_pos = pygame.mouse.get_pos()
                    dragged = True

        pygame.display.flip()

def main_menu():
    menu_font = pygame.font.Font(None, 50)
    play_button = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 - 60, 200, 50)
    exit_button = pygame.Rect(SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 + 20, 200, 50)

    while True:
        screen.fill(GRAY)
        title_text = menu_font.render("Tic-Tac-Toe 5-in-a-Row", True, BLACK)
        screen.blit(title_text, (SCREEN_SIZE // 2 - title_text.get_width() // 2, SCREEN_SIZE // 4))

        pygame.draw.rect(screen, WHITE, play_button)
        pygame.draw.rect(screen, WHITE, exit_button)

        play_text = font.render("Play", True, BLACK)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(play_text, (play_button.x + 70, play_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 70, exit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    main_game()  # Start the game
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

main_menu()
