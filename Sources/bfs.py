import os

import support_function as spf
import time
from copy import deepcopy
'''
//========================//
//           BFS          //
//        ALGORITHM       //
//     IMPLEMENTATION     //
//========================//
'''
def BFS_search(board, list_check_point):
    start_time = time.time()
    ''' BFS SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win first")
        return [board]
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)
    ''' INITIALIZE 2 LISTS USED FOR BFS SEARCH '''
    list_state = [start_state]
    list_visit = [start_state]
    ''' LOOP THROUGH VISITED LIST '''
    while len(list_visit) != 0:
        ''' GET NOW STATE TO SEARCH '''
        now_state = list_visit.pop(0)

        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)

        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos,now_state.check_points,list_check_point)
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board,new_checkpoint = spf.move(now_state.board, next_pos, cur_pos, deepcopy(now_state.check_points))
            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state,new_checkpoint):
                continue
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, new_checkpoint):
                continue
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, new_checkpoint):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, new_checkpoint)
            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, new_checkpoint):
                print("Found win")
                end_time = time.time()
                print(len(list_state))
                return (new_state.get_line(), len(list_state),round(end_time - start_time,3))
            
            ''' APPEND NEW STATE TO VISITED LIST AND TRAVERSED LIST '''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []