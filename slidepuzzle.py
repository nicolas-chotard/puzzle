import pygame
import random

pygame.init()

FPS = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
TILE_SIZE = SCREEN_WIDTH // 3
BOARD_SIZE = 3
NUM_TILES = BOARD_SIZE ** 2 - 1
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 50
FONT_NAME = pygame.font.match_font('arial')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Slide Puzzle')

bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_image.fill(BG_COLOR)

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def draw_board(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            tile = board[row][col]
            if tile != None:
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                pygame.draw.rect(screen, BG_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
                draw_text(screen, str(tile), FONT_SIZE, x + TILE_SIZE // 2, y + TILE_SIZE // 2)

def get_blank_position(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == None:
                return row, col

def is_legal_move(board, row, col):
    blank_row, blank_col = get_blank_position(board)
    return (row == blank_row and abs(col - blank_col) == 1) or \
           (col == blank_col and abs(row - blank_row) == 1)

def get_random_move(board):
    blank_row, blank_col = get_blank_position(board)
    move_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(move_offsets)
    for row_offset, col_offset in move_offsets:
        row = blank_row + row_offset
        col = blank_col + col_offset
        if row >= 0 and row < BOARD_SIZE and col >= 0 and col < BOARD_SIZE and is_legal_move(board, row, col):
            return row, col
    return None, None

def do_move(board, row, col):
    blank_row, blank_col = get_blank_position(board)
    board[blank_row][blank_col], board[row][col] = board[row][col], None

def is_solved(board):
    return all(board[row][col] == row * BOARD_SIZE + col + 1 for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if not (row == BOARD_SIZE - 1 and col == BOARD_SIZE - 1))

board = [[None for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
for i in range(1, NUM_TILES + 1):
    row, col = divmod(i - 1, BOARD_SIZE)
    board[row][col] = i

for i in range(100):
    row, col = get_random_move(board)
    do_move(board, row, col)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            col = mouse_pos[0] // TILE_SIZE
            row = mouse_pos[1] // TILE_SIZE
            if is_legal_move(board, row, col):
                do_move(board, row, col)

    screen.blit(bg_image, (0, 0))
    draw_board(board)
    pygame.display.flip()

    if is_solved(board):
        draw_text(screen, "Bravo, vous avez gagné !", FONT_SIZE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

pygame.quit()
