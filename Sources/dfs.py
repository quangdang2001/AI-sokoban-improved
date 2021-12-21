import support_function as spf
import time
from copy import deepcopy

start_time = 0
result = ()
list_checkpoint_original = []


def DFS_util(now_state, visited_state):
    global result
    ''' thêm now_state vào danh sách đã duyệt'''
    visited_state.add(now_state)
    ''' lấy vị trí hiện tại của player'''
    cur_pos = spf.find_position_player(now_state.board)
    ''' lấy ra list các vị trí player có thể di chuyển '''
    list_can_move = spf.get_next_pos(now_state.board, cur_pos, now_state.check_points, list_checkpoint_original)
    ''' tạo các trạng thái mới từ list_can_move '''
    for next_pos in list_can_move:
        if result:
            break
        new_board, new_checkpoint = spf.move(now_state.board, next_pos, cur_pos, deepcopy(now_state.check_points))
        ''' nếu board đã tồn tại thì bỏ qua '''
        if spf.is_board_exist(new_board, visited_state, new_checkpoint):
            continue
        ''' nếu có hộp nằm trong góc thì bỏ qua '''
        if spf.is_board_can_not_win(new_board, new_checkpoint):
            continue
        ''' nếu tất cả các hộp bị kẹt thì bỏ qua '''
        if spf.is_all_boxes_stuck(new_board, new_checkpoint):
            continue

        ''' tạo state mới '''
        new_state = spf.state(new_board, now_state, new_checkpoint)
        ''' kiểm tra goal '''
        if spf.check_win(new_board, new_checkpoint):
            print("Found win")
            end_time = time.time()
            print(len(visited_state))
            result = new_state.get_line(), len(visited_state), round(end_time - start_time, 3)
            return

        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            result = []

        DFS_util(new_state, visited_state)


def DFS_search(board, list_check_point):
    global list_checkpoint_original
    global start_time
    global result
    result = ()
    list_checkpoint_original = list_check_point

    start_time = time.time()
    ''' kiểm tra board ban đầu'''
    if spf.check_win(board, list_check_point):
        print("Found win first")
        return [board]

    start_state = spf.state(board, None, spf.check_checkpoint_init(board,list_check_point))
    ''' khai báo danh sách đã duyệt'''
    visited = set()
    DFS_util(start_state, visited)
    return result
