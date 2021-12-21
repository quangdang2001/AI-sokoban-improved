import numpy as np
import os
import pygame

import bfs
import astar
import dfs

''' TIME OUT FOR ALL ALGORITHM : 30 MIN ~ 1800 SECONDS '''
TIME_OUT = 1800
''' GET THE TESTCASES AND CHECKPOINTS PATH FOLDERS '''
path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'

''' TRAVERSE TESTCASE FILES AND RETURN A SET OF BOARD '''


def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}\{file}"
            board = get_board(file_path)

            # print(file)
            list_boards.append(board)

    return list_boards


''' TRAVERSE CHECKPOINT FILES AND RETURN A SET OF CHECKPOINT '''


def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}\{file}"
            check_point = get_pair(file_path)

            list_check_point.append(check_point)

    return list_check_point


''' FORMAT THE INPUT TESTCASE TXT FILE '''


def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b1':
            row[i] = '$1'
        elif row[i] == 'b2':
            row[i] = '$2'
        elif row[i] == 'b3':
            row[i] = '$3'
        elif row[i] == 'c':
            row[i] = '%'
        elif row[i] == '.':
            row[i] = '#'


''' FORMAT THE INPUT CHECKPOINT TXT FILE '''


def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result


''' READ A SINGLE TESTCASE TXT FILE '''


def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result


''' READ A SINGLE CHECKPOINT TXT FILE '''


def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result


'''
KHỞI TẠO MAP VÀ CÁC CHECKPOINT
'''


# THAY ĐỔI KÝ HIỆU CHECKPOINT THEO LOẠI
def change_maps_by_checkpoints(maps, check_points):
    for i in range(len(maps)):
        for check_point in check_points[i]:
            if maps[i][check_point[0]][check_point[1]] == '%':
                maps[i][check_point[0]][check_point[1]] = '%' + str(check_point[3])
    return maps


check_points = get_check_points()
maps = change_maps_by_checkpoints(get_boards(), check_points)
print(maps)
'''
    KHỞI TẠO PYGAME
'''
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((760, 760))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (125, 102, 8)
GREEN = (35, 155, 86)
'''
GET SOME ASSETS
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
player = pygame.transform.scale(player, (50, 50))
wall = pygame.image.load(os.getcwd() + '\\wall.png')
wall = pygame.transform.scale(wall, (50, 50))
box1 = pygame.image.load(os.getcwd() + '\\box1.png')
box1 = pygame.transform.scale(box1, (50, 50))

box2 = pygame.image.load(os.getcwd() + '\\box2.png')
box2 = pygame.transform.scale(box2, (50, 50))

box3 = pygame.image.load(os.getcwd() + '\\box3.png')
box3 = pygame.transform.scale(box3, (50, 50))

point = pygame.image.load(os.getcwd() + '\\goal.png')
point = pygame.transform.scale(point, (50, 50))

space = pygame.image.load(os.getcwd() + '\\space.png')
space = pygame.transform.scale(space, (50, 50))

arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
arrow_up = pygame.image.load(os.getcwd() + '\\arrow_up.png')

'''
RENDER THE MAP
'''


def renderMap(board, check_point, current_state=None, count_state=None, time=None):
    if current_state != None:
        titleSize = pygame.font.SysFont('Open Sans', 20, bold=True)
        titleText = titleSize.render(f"Step: {current_state}", True, WHITE)
        screen.blit(titleText, (600, 370))

    if count_state != None:
        titleSize = pygame.font.SysFont('Open Sans', 20, bold=True)
        titleText = titleSize.render(f"State: {count_state}", True, WHITE)
        screen.blit(titleText, (600, 400))

    if time != None:
        titleSize = pygame.font.SysFont('Open Sans', 20, bold=True)
        titleText = titleSize.render(f"Time: {time}s", True, WHITE)
        screen.blit(titleText, (600, 430))

    width = len(board[0])
    height = len(board)
    indent = (760 - width * 50) / 2.0
    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * 50 + indent, i * 50 + 150))
            if board[i][j] == '#':
                screen.blit(wall, (j * 50 + indent, i * 50 + 150))
            if '%' in board[i][j]:
                screen.blit(point, (j * 50 + indent, i * 50 + 150))
            if board[i][j] == '$1':
                screen.blit(box1, (j * 50 + indent, i * 50 + 150))
            if board[i][j] == '$2':
                screen.blit(box2, (j * 50 + indent, i * 50 + 150))
            if board[i][j] == '$3':
                screen.blit(box3, (j * 50 + indent, i * 50 + 150))
            if board[i][j] == '@':
                screen.blit(player, (j * 50 + indent, i * 50 + 150))
    # HIỂN THỊ SỐ LƯỢNG CÒN TRỐNG TRONG CHECKPOINT THEO LOẠI
    for i in check_point:
        titleSize = pygame.font.SysFont('Open Sans', 40, bold=True)
        if i[3] == 1:
            titleText = titleSize.render(f"{i[2]}", True, YELLOW)
        elif i[3] == 2:
            titleText = titleSize.render(f"{i[2]}", True, GREEN)
        elif i[3] == 3:
            titleText = titleSize.render(f"{i[2]}", True, RED)
        screen.blit(titleText, (i[1] * 50 + indent + 10, i[0] * 50 + 145))


'''
KHỞI TẠO MỘT SỐ BIẾN
'''
# Map level
mapNumber = 0
# Algorithm
algorithm = "Breadth First Search"
list_algorithm = ["Breadth First Search", "A Star Search", "Depth First Search"]
sceneState = "init"
index_algorithm = 0
''' SOKOBAN FUNCTION '''


def sokoban():
    running = True
    global sceneState
    global algorithm
    global list_board
    global mapNumber
    global index_algorithm
    stateLenght = 0
    currentState = 0
    found = True
    countState = 0
    count_step = 0
    time = 0
    while running:
        screen.fill(BLACK)
        if sceneState == "init":
            # Choose map and display
            initGame(maps[mapNumber])

        if sceneState == "executing":
            count_step = 0
            # Choose map
            list_check_point = check_points[mapNumber]
            # Choose between BFS or A*
            if algorithm == "Breadth First Search":
                print("BFS")
                list_board = bfs.BFS_search(maps[mapNumber], list_check_point)
            elif algorithm == "Depth First Search":
                print("DFS")
                list_board = dfs.DFS_search(maps[mapNumber], list_check_point)
            elif algorithm == "A Star Search":
                print("AStar")
                list_board = astar.AStart_Search(maps[mapNumber], list_check_point)

            if len(list_board) > 0:
                sceneState = "playing"
                countState = list_board[1]
                stateLenght = len(list_board[0])
                time = list_board[2]
                currentState = 0
            else:
                sceneState = "end"
                found = False
        if sceneState == "loading":
            loadingGame()
            sceneState = "executing"

        if sceneState == "end":
            if found:
                foundGame(list_board[0][stateLenght - 2], list_board[0][stateLenght - 1], count_step, countState, time)
            else:
                notfoundGame()

        if sceneState == "playing":
            clock.tick(3)
            renderMap(list_board[0][currentState], list_board[0][currentState + 1], count_step, countState, time)
            count_step += 1
            currentState = currentState + 2
            if currentState == stateLenght:
                sceneState = "end"
                found = True

        # Check event when you press key board
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Press arrow key board to change level map
                if event.key == pygame.K_RIGHT and sceneState == "init":
                    if mapNumber < len(maps) - 1:
                        mapNumber = mapNumber + 1
                if event.key == pygame.K_LEFT and sceneState == "init":
                    if mapNumber > 0:
                        mapNumber = mapNumber - 1
                # Press ENTER key board to select level map and algorithm
                if event.key == pygame.K_RETURN:
                    if sceneState == "init":
                        sceneState = "loading"
                    if sceneState == "end":
                        sceneState = "init"
                # Press SPACE key board to switch algorithm
                if event.key == pygame.K_UP and sceneState == "init":
                    index_algorithm += 1
                    if index_algorithm > 2:
                        index_algorithm = 0
                    algorithm = list_algorithm[index_algorithm]

        pygame.display.flip()
    pygame.quit()


''' DISPLAY MAIN SCENE '''


# HIỂN THỊ MÀN HÌNH CHỌN MAP VÀ LEVEL
def initGame(map):
    titleSize = pygame.font.SysFont('Open Sans', 60, bold=True)
    titleText = titleSize.render('Improved Sokoban', True, WHITE)
    titleRect = titleText.get_rect(center=(380, 40))
    screen.blit(titleText, titleRect)

    mapSize = pygame.font.SysFont('Open Sans', 30, bold=True)
    mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
    mapRect = mapText.get_rect(center=(380, 100))
    screen.blit(mapText, mapRect)

    screen.blit(arrow_left, (304, 90))
    screen.blit(arrow_right, (428, 90))
    screen.blit(arrow_up, (380, 600))
    algorithmSize = pygame.font.SysFont('Open Sans', 30, bold=True)
    algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
    algorithmRect = algorithmText.get_rect(center=(380, 650))
    screen.blit(algorithmText, algorithmRect)

    renderMap(map, check_points[mapNumber])


''' LOADING '''


def loadingGame():
    fontLoading_1 = pygame.font.SysFont('Open Sans', 40, bold=True)
    text_1 = fontLoading_1.render('LOADINGGG!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(380, 200))
    screen.blit(text_1, text_rect_1)

    fontLoading_2 = pygame.font.SysFont('Open Sans', 40, bold=True)
    text_2 = fontLoading_2.render('...', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(380, 230))
    screen.blit(text_2, text_rect_2)


''' GIẢI THÀNH CÔNG'''


def foundGame(map, stateLength, currentState, countState, time):
    screen.fill(BLACK)

    font_1 = pygame.font.SysFont('Open Sans', 30, bold=True)
    text_1 = font_1.render('COMPLETE!!!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(380, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.SysFont('Open Sans', 20, bold=True)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(380, 600))
    screen.blit(text_2, text_rect_2)

    renderMap(map, stateLength, currentState - 1, countState, time)


''' KHÔNG TÌM THẤY KẾT QUẢ'''


def notfoundGame():
    screen.fill(BLACK)

    font_1 = pygame.font.SysFont('Open Sans', 40, bold=True)
    text_1 = font_1.render('NOT FOUND!!!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(380, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.SysFont('Open Sans', 20, bold=True)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(380, 600))
    screen.blit(text_2, text_rect_2)


def main():
    sokoban()


if __name__ == "__main__":
    main()
