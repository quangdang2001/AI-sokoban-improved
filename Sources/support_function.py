from copy import deepcopy

import numpy as np
from scipy.optimize import linear_sum_assignment

TIME_OUT = 1800
'''
//========================//
//        SUPPORTING      //
//        FUNCTIONS       //
//========================//
'''
'''
DATA CONTAINER TO STORE THE STATE FOR EACH STEP
'''


class state:
    def __init__(self, board, state_parent, list_check_point):
        '''storage current board and state parent of this state'''
        self.board = board
        self.state_parent = state_parent
        self.g = 0
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)

    ''' RECURSIVE FUNCTION TO BACKTRACK TO THE FIRST FIRST IF THE CURRENT STATE IS GOAL '''

    def get_line(self):
        '''use loop to find list board from start to this state'''
        if self.state_parent is None:
            return [self.board, self.check_points]
        return (self.state_parent).get_line() + [self.board, self.check_points]

    ''' COMPUTE HEURISTIC FUNCTION USED FOR A* ALGORITHM '''
    def is_similar_style(self,box,checkpoint_style):
        if box == '$' + str(checkpoint_style):
            return True
        return False

    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            temp = []
            for box in list_boxes:
                for check_point in self.check_points:
                    if self.is_similar_style(self.board[box[0]][box[1]],check_point[3]):
                        temp.append(abs(box[0] - check_point[0]) + abs(box[1] - check_point[1]))
                    else:
                        temp.append(np.inf)
            # print(temp)
            arr = np.array(temp)
            cost = arr.reshape(len(list_boxes), len(self.check_points))

            try:
                row_ind, cow_ind = linear_sum_assignment(cost)
                self.heuristic = cost[row_ind, cow_ind].sum()
            except:
                self.heuristic=np.inf

            if (self.state_parent != None):
                self.g = self.state_parent.g + 1
        return self.heuristic

    ''' OPERATORS OVERLOADING THAT ALLOW STATES TO BE STORED IN PRIORITY QUEUE '''

    def __gt__(self, other):
        if self.compute_heuristic() + self.g > other.compute_heuristic() + other.g:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.compute_heuristic() + self.g < other.compute_heuristic() + other.g:
            return True
        else:
            return False


''' CHECK WHETHER THE BOARD IS GOAL OR NOT '''

# Kiem tra xem vi tri cua hop co la checkpoint va co dung loai hay khong
def is_postion_checkpoint(box, list_checkpoints,board):
    check = False
    for checkpoint in list_checkpoints:
        if box[0] == checkpoint[0] and box[1] == checkpoint[1] and board[box[0]][box[1]] == '$' + str(checkpoint[3]):
            check = True
    if check:
        return True
    return False


def check_win(board, list_check_point):
    result = find_boxes_position(board)
    for b in result:
        if not is_postion_checkpoint(b, list_check_point,board):
            return False
    return True


''' ASSIGN THE MATRIX '''


def assign_matrix(board):
    '''return board as same as input board'''
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]


''' FIND THE PLAYER'S CURRENT POSITION IN A BOARD '''


def find_position_player(board):
    '''return position of player in board'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x, y)
    return (-1, -1)  # error board


''' COMPARE 2 BOARDS '''


def compare_matrix(board_A, board_B, A_checkpoint, B_checkpoint):
    '''return true if board A is as same as board B'''
    for i in range(len(A_checkpoint)):
        if A_checkpoint[i][0] != B_checkpoint[i][0]:
            return False
        if A_checkpoint[i][1] != B_checkpoint[i][1]:
            return False
        if A_checkpoint[i][2] != B_checkpoint[i][2]:
            return False

    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True


''' CHECK WHETHER THE BOARD ALREADY EXISTED IN THE TRAVERSED LIST'''


def is_board_exist(board, list_state, checkpoint):
    '''return true if has same board in list'''
    for state in list_state:
        if compare_matrix(state.board, board, state.check_points, checkpoint):
            return True
    return False


''' CHECK WHETHER A SINGLE BOX IS ON A CHECKPOINT '''


def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False


''' CHECK WHETHER A SIGNLE BOX IS STUCK IN THE CORNER '''


def check_in_corner(board, x, y, list_check_point):
    '''return true if board[x][y] in corner'''
    if board[x - 1][y - 1] == '#':
        if board[x - 1][y] == '#' and board[x][y - 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x + 1][y - 1] == '#':
        if board[x + 1][y] == '#' and board[x][y - 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x - 1][y + 1] == '#':
        if board[x - 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x + 1][y + 1] == '#':
        if board[x + 1][y] == '#' and board[x][y + 1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    return False


''' FIND ALL BOXES' POSITIONS '''


def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if '$' in board[i][j]:
                result.append((i, j))
    return result


''' CHECK WHETHER A SINGLE BOX CAN BE MOVED IN AT LEAST 1 DIRECITON'''


def is_box_can_be_moved(board, box_position):
    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or '%' in board[left_move[0]][left_move[1]] or board[left_move[0]][
        left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and '$' not in board[right_move[0]][
        right_move[1]]:
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or '%' in board[right_move[0]][right_move[1]] or
        board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and \
            '$' not in board[left_move[0]][left_move[1]]:
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or '%' in board[up_move[0]][up_move[1]] or board[up_move[0]][
        up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and '$' not in board[down_move[0]][
        down_move[1]]:
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or '%' in board[down_move[0]][down_move[1]] or board[down_move[0]][
        down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and '$' not in board[up_move[0]][up_move[1]]:
        return True
    return False


''' CHECK WHEHTER ALL BOXES ARE STUCK '''


def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result


''' CHECK WHETHER AT LEAST ONE BOX IS STUCK IN THE CORNER'''


def is_board_can_not_win(board, list_check_point):
    '''return true if box in corner of wall -> can't win'''
    for x in range(len(board)):
        for y in range(len(board[0])):
            if '$' in board[x][y]:
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False


''' GET THE NEXT POSSIBLE MOVE '''


# Check if available < max - 1 then return false
def is_can_push_box(x, y, checkpoint1, checkpoint2):
    for i in range(len(checkpoint1)):
        if checkpoint1[i][0] == x and checkpoint1[i][1] == y:
            if checkpoint1[i][2] < checkpoint2[i][2] - 1:
                return False
    return True


def is_can_append_box(x, y, checkpoint1):
    for i in range(len(checkpoint1)):
        if checkpoint1[i][0] == x and checkpoint1[i][1] == y:
            if checkpoint1[i][2] > 0:
                return True
    return False


# Kiem tra xem checkpoint da co hop hay chua, neu chua co the di, neu co phai cung loai moi duoc di
def is_can_push_box_to_checkpoint(box, x, y, list_checkpoint, list_checkpoint_original,broad):
    for i in range(len(list_checkpoint)):
        # Kiem tra co phai la vi tri checkpoint
        if list_checkpoint[i][0] == x and list_checkpoint[i][1] == y:
            # Kiem tra cung loai hay khong
            if box != '$' + str(list_checkpoint[i][3]):
                # Kiem tra xem vi tri checkpoint da co hop hay chua
                if list_checkpoint[i][2] == list_checkpoint_original[i][2]:
                    return True
            else:
                # Dieu kien cung loai, neu khong co hop hoac co hop cung loai trong checkpoint thi co the di
                if '%' in broad[x][y] or broad[x][y] == box:
                    return True
    return False


def get_next_pos(board, cur_pos, list_checkpoint, list_checkpoint_original):
    '''return list of positions that player can move to from current position'''
    x, y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or '%' in value:
            list_can_move.append((x - 1, y))
        elif '$' in value and 0 <= x - 2 < len(board):
            if is_can_push_box(x - 1, y, list_checkpoint, list_checkpoint_original):
                next_pos_box = board[x - 2][y]
                if next_pos_box != '#':
                    if next_pos_box == ' ':
                        list_can_move.append((x - 1, y))
                    elif '%' in next_pos_box:
                        if is_can_push_box_to_checkpoint(value, x - 2, y, list_checkpoint, list_checkpoint_original,board):
                            list_can_move.append((x - 1, y))
                    elif '$' in next_pos_box:
                        if is_can_append_box(x - 2, y, list_checkpoint):
                            if is_can_push_box_to_checkpoint(value, x - 2, y, list_checkpoint,
                                                             list_checkpoint_original,board):
                                list_can_move.append((x - 1, y))

    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or '%' in value:
            list_can_move.append((x + 1, y))
        elif '$' in value and 0 <= x + 2 < len(board):
            if is_can_push_box(x + 1, y, list_checkpoint, list_checkpoint_original):
                next_pos_box = board[x + 2][y]
                if next_pos_box != '#':
                    if next_pos_box == ' ':
                        list_can_move.append((x + 1, y))
                    elif '%' in next_pos_box:
                        if is_can_push_box_to_checkpoint(value, x + 2, y, list_checkpoint, list_checkpoint_original,board):
                            list_can_move.append((x + 1, y))
                    elif '$' in next_pos_box:
                        if is_can_append_box(x + 2, y, list_checkpoint):
                            if is_can_push_box_to_checkpoint(value, x + 2, y, list_checkpoint,
                                                             list_checkpoint_original,board):
                                list_can_move.append((x + 1, y))

    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or '%' in value:
            list_can_move.append((x, y - 1))
        elif '$' in value and 0 <= y - 2 < len(board[0]):
            if is_can_push_box(x, y - 1, list_checkpoint, list_checkpoint_original):
                next_pos_box = board[x][y - 2]
                if next_pos_box != '#':
                    if next_pos_box == ' ':
                        list_can_move.append((x, y - 1))
                    elif '%' in next_pos_box:
                        if is_can_push_box_to_checkpoint(value, x, y - 2, list_checkpoint, list_checkpoint_original,board):
                            list_can_move.append((x, y - 1))
                    elif '$' in next_pos_box:
                        if is_can_append_box(x, y - 2, list_checkpoint):
                            if is_can_push_box_to_checkpoint(value, x, y - 2, list_checkpoint,
                                                             list_checkpoint_original,board):
                                list_can_move.append((x, y - 1))

    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or '%' in value:
            list_can_move.append((x, y + 1))
        elif '$' in value and 0 <= y + 2 < len(board[0]):
            if is_can_push_box(x, y + 1, list_checkpoint, list_checkpoint_original):
                next_pos_box = board[x][y + 2]
                if next_pos_box != '#':
                    if next_pos_box == ' ':
                        list_can_move.append((x, y + 1))
                    elif '%' in next_pos_box:
                        if is_can_push_box_to_checkpoint(value, x, y + 2, list_checkpoint, list_checkpoint_original,board):
                            list_can_move.append((x, y + 1))
                    elif '$' in next_pos_box:
                        if is_can_append_box(x, y + 2, list_checkpoint):
                            if is_can_push_box_to_checkpoint(value, x, y + 2, list_checkpoint,
                                                             list_checkpoint_original,board):
                                list_can_move.append((x, y + 1))

    return list_can_move


''' MOVE THE BOARD IN CERTAIN DIRECTIONS '''


def move(board, next_pos, cur_pos, list_check_point):
    '''return a new board after move'''
    # MAKE NEW BOARD AS SAME AS CURRENT BOARD
    new_board = assign_matrix(board)
    # FIND NEXT POSITION IF MOVE TO BOX

    if '$' in new_board[next_pos[0]][next_pos[1]]:
        # Neu vi tri hien tai cua hop la checkpoint thi sau khi day di cho trong + 1
        for p in list_check_point:
            if p[0] == next_pos[0] and p[1] == next_pos[1]:
                p[2] += 1
        x = 2 * next_pos[0] - cur_pos[0]
        y = 2 * next_pos[1] - cur_pos[1]
        for p in list_check_point:
            if p[0] == x and p[1] == y:
                p[2] -= 1
        new_board[x][y] = new_board[next_pos[0]][next_pos[1]]
    # MOVE PLAYER TO NEW POSITION
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # CHECK IF AT CHECK POINT'S POSITION DON'T HAVE ANYTHING THEN UPDATE % LIKE CHECK POINT
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%' + str(p[3])
    return new_board, list_check_point

# ''' FIND ALL CHECKPOINTS ON THE BOARD '''
# def find_list_check_point(board):
#     '''return list check point form the board
#         if don't have any check point, return empty list
#         it will check num of box, if num of box < num of check point
#             return list [(-1,-1)]'''
#     list_check_point = []
#     num_of_box = 0
#     ''' CHECK THE ENTIRE BOARD TO FIND CHECK POINT AND NUM OF BOX'''
#     for x in range(len(board)):
#         for y in range(len(board[0])):
#             if board[x][y] in '$':
#                 num_of_box += 1
#             elif board[x][y] in '%':
#                 list_check_point.append((x,y))
#     ''' CHECK IF NUMBER OF BOX < NUM OF CHECK POINT'''
#     if num_of_box < len(list_check_point):
#         return [(-1,-1)]
#     return list_check_point
