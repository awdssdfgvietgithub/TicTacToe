import pygame
import sys
import time
import tqdm

import tictactoe_5x5_apdungthuattoan_minimax as ttt

pygame.init()
size = width, height = 1300, 700

# Colors
black = (0, 0, 0)
gold = (255, 215, 0)

screen = pygame.display.set_mode(size)

smallFont = pygame.font.SysFont("Verdana", 30)
smallFont.set_underline(True)
mediumFont = pygame.font.SysFont("Verdana", 30)
largeFont = pygame.font.SysFont("Verdana", 40)
moveFont = pygame.font.SysFont("Verdana", 60)

class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, gold)
 
    def render(self, display):
        self.text = self.font.render('Fps: ' + str(round(self.clock.get_fps(),2)), True, gold)
        display.blit(self.text, (0, 0))
 
fps = FPS()

user = None
board = ttt.initial_state()
ai_turn = False

while True:
    fps.render(screen)
    pygame.display.update()
    fps.clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Ve tieu de
        title = largeFont.render("Trò chơi Tic-Tac-Toe", True, gold)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 70)
        screen.blit(title, titleRect)

        label = mediumFont.render("(5x5)", True, gold)
        labelRect = label.get_rect()
        labelRect.center = ((width / 2), 120)
        screen.blit(label, labelRect)

        body = mediumFont.render("Chọn cờ:", True, gold)
        bodyRect = body.get_rect()
        bodyRect.center = ((width / 2), 175)
        screen.blit(body, bodyRect)
        
        # Ve 2 nut chon nhan vat
        playXButton = pygame.Rect((width / 3), (height / 2), width / 7, 50)
        playX = smallFont.render("X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, gold, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(2 * (width / 4), (height / 2), width / 7, 50)
        playO = smallFont.render("O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, gold, playOButton)
        screen.blit(playO, playORect)

        # Kiem tra chon co
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:
        # Ve ban co
        tile_size = 80
        tile_origin = (width / 2 - (2.5 * tile_size),
                       height / 2 - (2.5 * tile_size))
        tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, gold, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, gold)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Ve tieu de
        if game_over:   
            winner = ttt.winner(board)
            if winner is None:
                title = f"Kết thúc: Hòa."
            else:
                title = f"Kết thúc: {winner} thắng."
        elif user == player:
            title = f"Người chơi {user}"
        else:
            title = f"Đợi xíu, đang nghĩ..."
        title = largeFont.render(title, True, gold)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 45)
        screen.blit(title, titleRect)

        # Kiem tra move AI
        if user != player and not game_over:
            if ai_turn:
                time.sleep(1)
                move = ttt.minimax(board, 2)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Kiem tra move nguoi choi
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(5):
                for j in range(5):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Chơi lại", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, gold, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
