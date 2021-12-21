from copy import deepcopy

import support_function as spf
import time
from queue import PriorityQueue


def AStart_Search(board, list_check_point):
    start_time = time.time()

    ''' nếu board ban đầu là goal thì trả về '''
    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]
    ''' khởi tạo state ban đầu '''
    start_state = spf.state(board, None, spf.check_checkpoint_init(board, list_check_point))
    list_state = [start_state]
    ''' khởi tạo hàng đợi ưu tiên '''
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    ''' lặp qua hàng đợi '''
    while not heuristic_queue.empty():
        '''lấy giá state có f cost nhỏ nhất trong hàng đợi'''
        now_state = heuristic_queue.get()

        ''' lấy vị trí hiện tại của player'''
        cur_pos = spf.find_position_player(now_state.board)

        ''' lấy danh sách vị trí mà player có thể di chuyển '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos, now_state.check_points, list_check_point)
        ''' tạo các state mới từ list can move '''
        for next_pos in list_can_move:
            ''' tạo board và checkpoint mới '''
            new_board, new_checkpoint = spf.move(now_state.board, next_pos, cur_pos, deepcopy(now_state.check_points))
            ''' kiểm tra đã tồn tại chưa '''
            if spf.is_board_exist(new_board, list_state, new_checkpoint):
                continue
            ''' kiểm tra có hộp nào trong nằm góc '''
            if spf.is_board_can_not_win(new_board, new_checkpoint):
                continue
            ''' kiểm tra tất cả các hộp có bị kẹt '''
            if spf.is_all_boxes_stuck(new_board, new_checkpoint):
                continue

            ''' tạo state mới '''
            new_state = spf.state(new_board, now_state, new_checkpoint)
            ''' kiểm tra goal '''
            if spf.check_win(new_board, new_checkpoint):
                print("Found win")
                print("Cost: ", now_state.g + 1)
                end_time = time.time()
                print(len(list_state))
                return new_state.get_line(), len(list_state), round(end_time - start_time, 3)

            ''' thêm trạng thái vào list đã duyệt và hàng đợi '''
            list_state.append(new_state)
            heuristic_queue.put(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []
