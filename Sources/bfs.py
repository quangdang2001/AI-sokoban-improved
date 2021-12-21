import os

import support_function as spf
import time
from copy import deepcopy

def BFS_search(board, list_check_point):
    start_time = time.time()

    ''' nếu board ban đầu là goal thì trả về '''
    if spf.check_win(board,list_check_point):
        print("Found win first")
        return [board]
    ''' khởi tạo trạng thái ban đầu '''
    start_state = spf.state(board, None, spf.check_checkpoint_init(board,list_check_point))

    ''' khởi tạo 2 list cho thuật toán bfs'''
    # visited_state danh sách các trạng thái đã đc xét
    visited_state = [start_state]
    # queue_state danh sách các trạng thái đang đợi để xét
    queue_state = [start_state]

    ''' lặp queue_state '''
    while len(queue_state) != 0:
        ''' lấy trạng thái đầu tiên trong hàng đợi '''
        now_state = queue_state.pop(0)

        ''' lấy vị trí hiện tại của player '''
        cur_pos = spf.find_position_player(now_state.board)

        ''' lấy ra list các vị trí player có thể di chuyển '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos,now_state.check_points,list_check_point)
        ''' tạo các trạng thái mới từ list_can_move '''
        for next_pos in list_can_move:
            ''' tạo board mới và checkpoint của nó '''
            new_board,new_checkpoint = spf.move(now_state.board, next_pos, cur_pos, deepcopy(now_state.check_points))
            ''' nếu board đã tồn tại thì bỏ qua '''
            if spf.is_board_exist(new_board, visited_state,new_checkpoint):
                continue
            ''' nếu có hộp nằm trong góc thì bỏ qua '''
            if spf.is_board_can_not_win(new_board, new_checkpoint):
                continue
            ''' nếu tất cả các hộp bị kẹt thì bỏ qua '''
            if spf.is_all_boxes_stuck(new_board, new_checkpoint):
                continue

            ''' tạo một trạng thái mới '''
            new_state = spf.state(new_board, now_state, new_checkpoint)
            ''' kiểm tra đã đạt goal '''
            if spf.check_win(new_board, new_checkpoint):
                print("Found win")
                end_time = time.time()
                print(len(visited_state))
                return new_state.get_line(), len(visited_state), round(end_time - start_time, 3)
            
            ''' thêm trạng thái mới vào 2 list '''
            visited_state.append(new_state)
            queue_state.append(new_state)


            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []