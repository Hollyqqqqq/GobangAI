# 测试一下

import numpy as np
import random
from enum import Enum
from collections import Counter
from operator import itemgetter
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
# random.seed(0)

class Type(Enum):
    FIVE = 10
    OPEN_FOUR = 9
    FOUR = 8
    OPEN_THREE = 7
    THREE = 5
    OPEN_TWO = 3
    TWO = 2


class Pattern:
    def __init__(self, c_type, pattern, rating, sym):
        self.c_type = c_type
        self.pattern = pattern
        self.rating = rating
        self.sym = sym

# don't change the class name
class AI(object):
    p1 = Pattern(Type.FIVE, "XXXXX", 1000000, 1)  # 5 continuous
    p2 = Pattern(Type.OPEN_FOUR, ".XXXX.", 20000, 1)  # 4 continuous
    p3 = Pattern(Type.FOUR, "OXXXX.", 500, 0)  # 4 continuous
    p4 = Pattern(Type.FOUR, "XX.XX",  498, 1)  # 2 continuous
    p5 = Pattern(Type.FOUR, "XXX.X",  499, 0)  # 3 continuous
    p6 = Pattern(Type.OPEN_THREE, ".XXX.",  100, 1)  # 3 continuous
    p7 = Pattern(Type.OPEN_THREE, ".XX.X.", 100, 0)  # 2 continuous
    p8 = Pattern(Type.THREE, "OXXX..",  5, 0)  # 3 continuous
    p9 = Pattern(Type.THREE, "XX..X",   5, 0)  # 2 continuous
    p10 = Pattern(Type.THREE, "OXX.X.", 5, 0)  # 2 continuous
    p11 = Pattern(Type.THREE, "OX.XX.", 5, 0)  # 2 continuous
    p12 = Pattern(Type.THREE, "X.X.X",  5, 1)  # 1 continuous
    p13 = Pattern(Type.THREE, "O.XXX.O", 5, 1)
    p14 = Pattern(Type.OPEN_TWO, "..XX..", 10, 1)
    p15 = Pattern(Type.OPEN_TWO, ".X.X.",  9, 1)
    # p16 = Pattern(Type.OPEN_TWO, "X..X",   3, 1)
    # p17 = Pattern(Type.TWO, "...XXO", 2, 0)
    # p18 = Pattern(Type.TWO, "X...X",  2, 1)
    # p19 = Pattern(Type.TWO, "..X.XO", 2, 0)
    # p20 = Pattern(Type.TWO, ".X..XO", 2, 0)
    boardCount = 0
    eval_time = 0
    steps = 0
    infinity = float("inf")
    # print("asdfjlkas;dlfjasl;kdf")

    pattern_list = [[p1],
                    [p2],
                    [p3, p4, p5],
                    [p6, p7],
                    [p8, p9, p10, p11, p12, p13],
                    [p14, p15]
                    #,[p17, p18, p19, p20]
                    ]

# ------parameter area--------------
    extend_len = 2
    theta = p1.rating * 1.05
    max_depth = [4, 2]
    max_point = [12, 10, 8, 4]

    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_list as your decision.
        self.candidate_list = []
        if self.color == COLOR_WHITE:
            self.steps = -1
        else:
            self.steps = -2

    @staticmethod
    def extract_judge_line(chessboard, x, y, k):
        result = []
        s_tmp = []
        # horizontal line
        for i in range(-4, 5):
            if not i:
                s_tmp.append("X")
                continue

            t = x + i
            if 0 <= t < 15:
                if chessboard[t][y] == k:
                    s_tmp.append("X")
                elif chessboard[t][y] == - k:
                    if i > 0:
                        s_tmp.append("O")
                        break
                    else:
                        s_tmp = ["O"]
                else:
                    s_tmp.append(".")
            if t == 15 or t == -1:
                s_tmp += "O"
        result.append(''.join(s_tmp))
        s_tmp = []
        for i in range(-4, 5):
            if not i:
                s_tmp.append("X")
                continue

            t = y + i
            if 0 <= t < 15:
                if chessboard[x][t] == k:
                    s_tmp.append("X")
                elif chessboard[x][t] == - k:
                    if i > 0:
                        s_tmp.append("O")
                        break
                    else:
                        s_tmp = ["O"]
                else:
                    s_tmp.append(".")
            if t == 15 or t == -1:
                s_tmp.append("O")
        result.append(''.join(s_tmp))
        s_tmp = []
        for i in range(-4, 5):
            if not i:
                s_tmp.append("X")
                continue

            t1 = i + x
            t2 = y + i
            if 0 <= t1 < 15 and 0 <= t2 < 15:
                if chessboard[t1][t2] == k:
                    s_tmp.append("X")
                elif chessboard[t1][t2] == - k:
                    if i > 0:
                        s_tmp.append("O")
                        break
                    else:
                        s_tmp = ["O"]
                else:
                    s_tmp.append(".")
            if t1 == 15 or t2 == 15 or t1 == -1 or t2 == -1:
                s_tmp.append("O")
        result.append(''.join(s_tmp))
        s_tmp = []
        for i in range(-4, 5):
            if not i:
                s_tmp.append("X")
                continue

            t1 = i + x
            t2 = y - i
            if 0 <= t1 < 15 and 0 <= t2 < 15:
                if chessboard[t1][t2] == k:
                    s_tmp.append("X")
                elif chessboard[t1][t2] == - k:
                    if i > 0:
                        s_tmp.append("O")
                        break
                    else:
                        s_tmp = ["O"]
                else:
                    s_tmp.append(".")
            if t1 == 15 or t2 == 15 or t1 == -1 or t2 == -1:
                s_tmp.append("O")
        result.append(''.join(s_tmp))
        # filter(lambda p: len(p) > 4, result)
        # if x == 0 and y == 0:
        #     print(result)
        return result

    def get_valuable_blank(self, chessboard):
        idx_chess = np.where(chessboard != 0)
        x_range_min = min(idx_chess[0]) - self.extend_len
        x_range_max = max(idx_chess[0]) + self.extend_len
        y_range_min = min(idx_chess[1]) - self.extend_len
        y_range_max = max(idx_chess[1]) + self.extend_len
        x_range = [x_range_min if x_range_min > 0 else 0, x_range_max if x_range_max < 14 else 14]
        y_range = [y_range_min if y_range_min > 0 else 0, y_range_max if y_range_max < 14 else 14]
        # print(x_range, y_range)
        return x_range, y_range

    def sort_point(self, chessboard, color, depth):
        d = {}
        x_range, y_range = self.get_valuable_blank(chessboard)
        for i in range(x_range[0], x_range[1] + 1):
            for j in range(y_range[0], y_range[1] + 1):
                if chessboard[i, j] == 0:
                    # print(str((i, j)) + str(self.eval_stat_res(self.eval_value(chessboard, i, j, color))) + " "
                    # + str(self.eval_stat_res(self.eval_value(chessboard, i, j, -color))))
                    d.update({(i, j): self.eval_stat_res(self.eval_value(chessboard, i, j, color)) * 1.05 + self.eval_stat_res(
                        self.eval_value(chessboard, i, j, -color))})
        point_sorted = [x for x in sorted(d.items(), key=itemgetter(1), reverse=True)][:self.max_point[depth]]
        return point_sorted

    def alphabeta_search(self, chessboard, depth_index):
        def max_val(chessboard, alpha, beta, depth, color):
            if depth == self.max_depth[depth_index]:
                return self.eval_board(chessboard)
            v = - self.infinity
            keys_sorted = self.sort_point(chessboard, color, depth)
            # print(depth * '   ' + "+==" + str(keys_sorted) + " " + str(color))
            # point_sorted = [x[0] for x in keys_sorted]
            for pair in keys_sorted:
                point = pair[0]
                chessboard[point[0], point[1]] = color
                if pair[1] >= self.theta:
                    if color == self.color:
                        chessboard[point[0], point[1]] = 0
                        return pair[1]
                    else:
                        chessboard[point[0], point[1]] = 0
                        return - pair[1]
                else:
                    v = max(v, min_val(chessboard, alpha, beta, depth + 1, -color))
                    if v >= beta:
                        chessboard[point[0], point[1]] = 0
                        return v
                    alpha = max(alpha, v)
                    chessboard[point[0], point[1]] = 0
            return v

        def min_val(chessboard, alpha, beta, depth, color):
            if depth == self.max_depth[depth_index]:
                return self.eval_board(chessboard)
            v = self.infinity
            keys_sorted = self.sort_point(chessboard, color, depth)
            # print(depth * '   ' + "+==" + str(keys_sorted) + " " + str(color))
            # point_sorted = [x[0] for x in keys_sorted]
            for pair in keys_sorted:
                point = pair[0]
                chessboard[point[0], point[1]] = color
                if pair[1] >= self.theta:
                    if color == self.color:
                        chessboard[point[0], point[1]] = 0
                        return pair[1]
                    else:
                        chessboard[point[0], point[1]] = 0
                        return - pair[1]
                else:
                    v = min(v, max_val(chessboard, alpha, beta, depth + 1, -color))
                    if v <= alpha:
                        chessboard[point[0], point[1]] = 0
                        return v
                    beta = min(beta, v)
                    chessboard[point[0], point[1]] = 0
            return v
        depth = 0
        best_score = -self.infinity
        beta = self.infinity
        best_action = None
        keys_sorted = self.sort_point(chessboard, self.color, 0)
        # print(depth * '   ' + "+==" + str(keys_sorted) + " " + str(self.color))
        # point_sorted = [x[0] for x in keys_sorted]
        # print(depth, keys_sorted)
        for pair in keys_sorted:
            point = pair[0]
            chessboard[point[0], point[1]] = self.color
            # print(chessboard)
            if pair[1] >= self.theta:
                v = pair[1]
            else:
                v = min_val(chessboard, best_score, beta, depth + 1, -self.color)
            # print(point, v)
            if v > best_score:
                best_score = v
                best_action = point
            chessboard[point[0], point[1]] = 0
        print(best_action)
        return best_action

    def match_pattern(self, string, rev):
        result = []
        for pg in self.pattern_list:
            for p in pg:
                if not (p.sym and rev):
                    flag = True
                    start = 0
                    while flag:
                        a = string.find(p.pattern, start)
                        if a == -1:
                            flag = False
                        else:
                            result.append(p)
                            start = a + 1
        return result

    def eval_stat_res(self, stat):
        val = 0
        # print(p1.c_type)
        # for k in stat.keys():
        #     print(k.c_type)
        if self.p1 in stat:
            return self.p1.rating

        if (((self.p3 in stat) or (self.p4 in stat) or (self.p5 in stat)) and ((self.p6 in stat) or (self.p7 in stat))) \
                or (stat.get(self.p3, 0) + stat.get(self.p4, 0) + stat.get(self.p5, 0) >= 2):
            # print(p2 in stat)
            val += 6000

        if stat.get(self.p6, 0) + stat .get(self.p7, 0) >= 2:
            val += 4800

        # if k == self.color:
        #     val += 20

        val += sum((k.rating * v for k, v in stat.items()))
        return val

    def eval_value(self, chessboard, x, y, k):
        surround = self.extract_judge_line(chessboard, x, y, k)
        surround_rev = [x[::-1] for x in surround]
        stat = []
        for t in surround:
            stat.extend(self.match_pattern(t, 0))
        for t in surround_rev: # 对于对称的pattern就没必要反向再比一次，设置为一
            stat.extend(self.match_pattern(t, 1))
        stat = dict(Counter(stat))
        return stat

    @staticmethod
    def extract_chessboard(chessboard, color):
        result = []
        # extract horizontal line
        tmp_result = []
        for i in chessboard:
            tmp_str = []
            for j in i:
                if j == color:
                    tmp_str.append("X")
                elif j == -color:
                    tmp_str.append("O")
                else:
                    tmp_str.append(".")
            tmp_result.append(''.join(tmp_str))
        result.append(tmp_result)

        # extract vertical line
        tmp_result = []
        [rows, cols] = chessboard.shape
        for i in range(cols):
            tmp_str = []
            for j in range(rows):
                if chessboard[j, i] == color:
                    tmp_str.append("X")
                elif chessboard[j, i] == - color:
                    tmp_str.append("O")
                else:
                    tmp_str.append(".")
            tmp_result.append(''.join(tmp_str))
        result.append(tmp_result)

        # extract / line
        tmp_result = []
        for index_sum in range(4, 25):
            tmp_str = []
            i_low = 0 if index_sum <= 14 else index_sum - 14
            i_high = index_sum if index_sum < 14 else 14
            for i in range(i_low, i_high + 1):
                # print(i_high, i, index_sum - i)
                if chessboard[i, index_sum - i] == color:
                    tmp_str.append("X")
                elif chessboard[i, index_sum - i] == -color:
                    tmp_str.append("O")
                else:
                    tmp_str.append(".")
            tmp_result.append(''.join(tmp_str))
        result.append(tmp_result)

        # extract \ line
        tmp_result = []
        i_start, j_start = 0, 10
        while i_start <= 10:
            i, j = i_start, j_start
            tmp_str = []
            while i < 15 and j < 15:
                if chessboard[i, j] == color:
                    tmp_str.append("X")
                elif chessboard[i, j] == -color:
                    tmp_str.append("O")
                else:
                    tmp_str.append(".")
                i += 1
                j += 1
            tmp_result.append(''.join(tmp_str))
            if j_start != 0:
                j_start -= 1
            else:
                i_start += 1
        result.append(tmp_result)
        return result

    # 先做一个全局的评估先，不管那么多
    def eval_board(self, chessboard):
        s_time = time.time()
        result_mine = self.extract_chessboard(chessboard, self.color)
        # print(result_mine)
        result_mine_rev = [x[::-1] for i in result_mine for x in i]
        stat = []
        stat_opponent = []
        for direct in result_mine:
            # print(direct)
            for i in direct:
                # print(i)
                stat.extend(self.match_pattern(i, 0))
                i1 = i.replace('O', '1')
                i1 = i1.replace('X', 'O')
                i1 = i1.replace('1', 'X')
                stat_opponent.extend(self.match_pattern(i1, 0))
                # print(i1, [x.pattern for x in stat_opponent])
        for i in result_mine_rev:
                stat.extend(self.match_pattern(i, 1))
                i1 = i.replace('O', '1')
                i1 = i1.replace('X', 'O')
                i1 = i1.replace('1', 'X')
                stat_opponent.extend(self.match_pattern(i1, 1))
        stat = dict(Counter(stat))
        stat_opponent = dict(Counter(stat_opponent))
        val = self.eval_stat_res(stat)
        val_opponent = self.eval_stat_res(stat_opponent)
        self.boardCount += 1
        e_time = time.time()
        # print("val = %d" % val)
        # print("val_opponent = %d" % val_opponent)
        self.eval_time += (e_time - s_time)
        return val - val_opponent

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.steps += 2
        s_time = time.time()
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        idx_chess = np.where(chessboard != 0)
        # idx_blank = np
        # print(self.eval_board(chessboard))
        count =idx_chess[0].size
        if count == 0:
            new_pos = tuple([7, 7])
            self.candidate_list.append(new_pos)
        else:
            # print(chessboard)
            # print(self.sort_point(chessboard, self.color))
            key_sorted = [x[0] for x in self.sort_point(chessboard, self.color, 0)]
            self.candidate_list.extend(key_sorted[::-1])
            if count < 90:
                self.candidate_list.append(self.alphabeta_search(chessboard, 0))
            # if count == self.steps:
            #     if 60 < count < 90:
            #         self.candidate_list.append(self.alphabeta_search(chessboard, 1))
            #     else:
            #         self.candidate_list.append(self.alphabeta_search(chessboard, 0))
            print(self.boardCount)
            print(self.eval_time)
        e_time = time.time()
        print("go_time = %f" % (e_time - s_time))
