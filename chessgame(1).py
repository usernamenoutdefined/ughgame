import pygame

pygame.Surface.blits
#making the prototype of the board
pygame.init() 
width = 1000
height = 900
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2-player pygame chess')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop','knight', 'rook', 
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_locations = [(0, 0), (1,0), (2,0), (3,0), (4,0), (5,0),(6,0), (7,0), 
                   (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),(6,1),(7,1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen','bishop','knight', 'rook', 
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1,7), (2,7), (3,7), (4,7), (5,7),(6,7), (7,7), 
                   (0,6), (1,6), (2,6), (3,6), (4,6), (5,6),(6,6),(7,6)]

captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []


#load game piece images
white_king = pygame.image.load('white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))


white_queen = pygame.image.load('white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))


white_rook = pygame.image.load('white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))

white_knight = pygame.image.load('white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80,80))


white_bishop = pygame.image.load('white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop,(80, 80))


white_pawn = pygame.image.load('white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))


black_king = pygame.image.load('black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))


black_queen = pygame.image.load('black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))

black_rook = pygame.image.load('black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))

black_knight = pygame.image.load('black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))


black_bishop = pygame.image.load('black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))

black_pawn = pygame.image.load('black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False

# draw game board
def draw_board():
    """
    Draw the chessboard on the screen.

    This function draws the chessboard grid and the status bar at the bottom.
    """

    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'dark gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'dark gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'light blue', [0, 800, width, 100])
        pygame.draw.rect(screen, 'silver', [0, 800, width, 100], 5)
        pygame.draw.rect(screen, 'silver', [800, 0, 200, height], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'silver', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'silver', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))

# draw pieces onto board
def draw_pieces():
    """
    Draw the chess pieces on the board.

    This function draws the chess pieces based on their current positions and types.
    It also highlights the selected piece if applicable.
    """
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'black', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'black', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)
 
#116 and 126 is the frame around the cell and figure
                                                
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    """
    Check and return valid moves for each piece on the board.

    Parameters:
    - pieces (list): List of pieces (e.g., ['rook', 'knight']).
    - locations (list): List of piece locations (e.g., [(0, 0), (1, 0)]).
    - turn (str): Current turn ('white' or 'black').

    Returns:
    - list: List of lists containing valid moves for each piece.
    """

    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# checking king valid moves
def check_king(position, color):
    """
    Check valid moves for the king.

    Parameters:
    - position (tuple): Current position of the king.
    - color (str): Color of the king ('white' or 'black').

    Returns:
    - list: List of valid moves for the king.
    """
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# checking queen valid moves
def check_queen(position, color):
    """
    Check valid moves for the queen.

    Parameters:
    - position (tuple): Current position of the queen.
    - color (str): Color of the queen ('white' or 'black').

    Returns:
    - list: List of valid moves for the queen.
    """
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# checking bishop moves
def check_bishop(position, color):
    """
    Check valid moves for the bishop.

    Parameters:
    - position (tuple): Current position of the bishop.
    - color (str): Color of the bishop ('white' or 'black').

    Returns:
    - list: List of valid moves for the bishop.
    """
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# checking rook moves
def check_rook(position, color):
    """
    Check valid moves for the rook.

    Parameters:
    - position (tuple): Current position of the rook.
    - color (str): Color of the rook ('white' or 'black').

    Returns:
    - list: List of valid moves for the rook.
    """

    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# checking  valid pawn moves
def check_pawn(position, color):
    """
    Check valid moves for the pawn.

    Parameters:
    - position (tuple): Current position of the pawn.
    - color (str): Color of the pawn ('white' or 'black').

    Returns:
    - list: List of valid moves for the pawn.
    """
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# checking valid knight moves
def check_knight(position, color):
    """
    Check valid moves for the knight.

    Parameters:
    - position (tuple): Current position of the knight.
    - color (str): Color of the knight ('white' or 'black').

    Returns:
    - list: List of valid moves for the knight.
    """
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# checking for valid moves for just selected piece
def check_valid_moves():
    """
    Check valid moves for the currently selected piece.

    Returns:
    - list: List of valid moves for the selected piece.
    """
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    """
    Draw valid move indicators on the screen.

    Parameters:
    - moves (list): List of valid moves to be highlighted on the board.
    """

    if turn_step < 2:
        color = 'black'
    else:
        color = 'black' 
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)  #sizes of dots


        


# draw a flashing square around king if in check
def draw_check():
    """
    Draw a flashing square around the king if in check.
    """

    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    """
    Draw the game over screen with the winner and instructions to restart.
    """
    pygame.draw.rect(screen, 'light gray', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('light yellow')
    draw_board()
    draw_pieces()
    
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
# event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()