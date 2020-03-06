import numpy as np
import math
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

#活三和冲三的分数要相同，冲四和眠四的分数要相同
# 必胜棋型：连五，活四，双冲四，冲四活三，双活三 （双冲四有可能是假的）

# live = [0, 150, 2000, 40000000, 50000000]
# run = [0, 100, 2000, 2500, 50000000]
# sleep = [0, 20, 200, 3000, 50000000]
KO = [100000, 100000, 100000, 100000, 100000]
score = [[0, 150, 2500, 40000000, 50000000], # live
         [0, 100, 2200, 2500, 50000000], # run
         [0, 20, 200, 2500, 50000000], # sleep
         [10000000, 20000000, 30000000, 40000000, 50000000]]# KO

class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):  # type(chessboard) = np.array
        self.candidate_list.clear()
        # =====================================================

        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        if len(idx) == 0:
            new_pos = [7,7]
            assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
            self.candidate_list.append(new_pos)
        elif len(idx) > 100:
            empty = self.find_empty(chessboard)
            max_score = -1
            for each in empty:
                chess_type1 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0]]  # live, run, sleep, KO
                chess_type2 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0]]  # live, run, sleep, KO
                syn_score_me = self.point_value_4_dir(chessboard, each, self.color, chess_type1)
                syn_score_op = self.point_value_4_dir(chessboard, each, -1 * self.color, chess_type2) * 0.8
                syn_score = syn_score_me + (-1) * syn_score_op
                if abs(syn_score) > max_score:
                    max_score = abs(syn_score)
                    assert chessboard[each[0], each[1]] == COLOR_NONE
                    self.candidate_list.append(each)
        else:
            best_action = self.min_max_decision(chessboard, 4)
            assert chessboard[best_action[0], best_action[1]] == COLOR_NONE
            self.candidate_list.append(best_action)

    def min_max_decision(self, chessboard, depth):
        color = self.color
        inf = float("inf")
        #取前几个位置
        count_len = 4
        #将空位置进行预先排序
        sorted_empty = self.sort_empty(chessboard, color)
        # sorted_empty = [[(3,5),1],[(2,7),1]]

        def max_value(empty, chessboard, old_chess, curr_d, alpha, beta):
            if curr_d == depth:
                #计算state的分数,,不能这样计算
                v = self.total_eval(chessboard, old_chess)
                return v
            v = -inf
            for a in empty[:count_len]:
                # old_chess = np.copy(chessboard)
                chessboard[a[0][0],a[0][1]] = color
                #找空位置还可以优化, 在最后一层要return的时候可以不用算new_empty
                if curr_d + 1 < depth:
                    new_empty = self.sort_empty(chessboard, -1*color)
                else:
                    new_empty = empty
                    v = max(v, min_value(new_empty, chessboard, old_chess, curr_d+1, alpha, beta))
                chessboard[a[0][0],a[0][1]] = COLOR_NONE
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(empty, chessboard, old_chess, curr_d, alpha, beta):
            if curr_d == depth:
                v = self.total_eval(chessboard, old_chess)
                return v
            v = inf
            for b in empty[:count_len]:
                # old_chess = np.copy(chessboard)
                chessboard[b[0][0],b[0][1]] = -1*color
                if curr_d + 1 < depth:
                    new_empty = self.sort_empty(chessboard, color)
                else:
                    new_empty = empty
                    v = min(v, max_value(new_empty, chessboard, old_chess, curr_d+1, alpha, beta))
                chessboard[b[0][0], b[0][1]] = COLOR_NONE
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        best_score = -inf
        beta = inf
        best_action = None
        old_chess = np.copy(chessboard)
        # print(sorted_empty)
        for a in sorted_empty[:count_len]:
            # old_chess = np.copy(chessboard)
            chessboard[a[0][0], a[0][1]] = self.color
            new_empty = self.sort_empty(chessboard, -1*self.color)
            v = min_value(new_empty, chessboard, old_chess, 1, best_score, beta)
            chessboard[a[0][0], a[0][1]] = 0
            # print(a)
            # print(v)
            if v > best_score:
                best_score = v
                best_action = a[0]
        return best_action

    def total_eval(self, chessboard, old_chess): # 后续增加一个old chess
        chess_type_me = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # live, run, sleep, KO
        chess_type_op = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # live, run, sleep, KO
        update_pos = []
        #得到只有更新点的整个棋盘
        for j in range(0, 15):
            update_pos.append([chessboard[j][i] - old_chess[j][i]for i in range(0, 15)])
        #提取出更新点
        update_pos = np.array(update_pos)
        update_points = np.where(update_pos != COLOR_NONE)
        update_points = list(zip(update_points[0], update_points[1]))
        # 将更新点会影响到的点全部加进effect_points里面，准备计算增量
        effect_points = []
        for each in update_points:
            x = each[0]
            y = each[1]
            direction = [[1, 0], [0, 1], [1, 1], [-1, 1]]
            for i in range(0, 4):
                k = 1
                while k < 5 and (x + k * direction[i][0] >= 0) and (x + k * direction[i][0] < 15) \
                    and (y + k * direction[i][1] >= 0) and (y + k * direction[i][1] < 15):
                    if old_chess[x + k * direction[i][0]][y + k * direction[i][1]] != COLOR_NONE:
                        effect_points.append((x + k * direction[i][0], y + k * direction[i][1]))
                    k += 1

                k = -1
                while k > -5 and (x + k * direction[i][0] >= 0) and (x + k * direction[i][0] < 15) \
                    and (y + k * direction[i][1] >= 0) and (y + k * direction[i][1] < 15):
                    if old_chess[x + k * direction[i][0]][y + k * direction[i][1]] != COLOR_NONE:
                        effect_points.append((x + k * direction[i][0], y + k * direction[i][1]))
                    k -= 1

        # 受影响的点去重
        effect_points = list(set(effect_points))
        # print("effect:", effect_points)
        # 开始计算增量
        # for each in effect_points:
        #     if old_chess[each[0]][each[1]] == self.color:
        #         chess_type_temp = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        #         self.point_value_4_dir(old_chess, each, self.color, chess_type_temp)
        #         chess_type_me = [[chess_type_me[0][i] - chess_type_temp[0][i] for i in range(0, 5)],
        #                          [chess_type_me[1][i] - chess_type_temp[1][i] for i in range(0, 5)],
        #                          [chess_type_me[2][i] - chess_type_temp[2][i] for i in range(0, 5)],
        #                          [chess_type_me[3][i] - chess_type_temp[3][i] for i in range(0, 5)]]
        #     else:
        #         chess_type_temp = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        #         self.point_value_4_dir(old_chess, each, -1*self.color, chess_type_temp)
        #         chess_type_op = [[chess_type_op[0][i] - chess_type_temp[0][i] for i in range(0, 5)],
        #                          [chess_type_op[1][i] - chess_type_temp[1][i] for i in range(0, 5)],
        #                          [chess_type_op[2][i] - chess_type_temp[2][i] for i in range(0, 5)],
        #                          [chess_type_op[3][i] - chess_type_temp[3][i] for i in range(0, 5)]]
        for each in update_points:
            effect_points.append(each)
        for each in effect_points:
            if chessboard[each[0]][each[1]] == self.color:
                chess_type_temp = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
                self.point_value_4_dir(chessboard, each, self.color, chess_type_temp)
                chess_type_me = [[chess_type_me[0][i] + chess_type_temp[0][i] for i in range(0, 5)],
                                 [chess_type_me[1][i] + chess_type_temp[1][i] for i in range(0, 5)],
                                 [chess_type_me[2][i] + chess_type_temp[2][i] for i in range(0, 5)],
                                 [chess_type_me[3][i] + chess_type_temp[3][i] for i in range(0, 5)]]
            else:
                chess_type_temp = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
                self.point_value_4_dir(chessboard, each, -1*self.color, chess_type_temp)
                chess_type_op = [[chess_type_op[0][i] + chess_type_temp[0][i] for i in range(0, 5)],
                                 [chess_type_op[1][i] + chess_type_temp[1][i] for i in range(0, 5)],
                                 [chess_type_op[2][i] + chess_type_temp[2][i] for i in range(0, 5)],
                                 [chess_type_op[3][i] + chess_type_temp[3][i] for i in range(0, 5)]]
        # print("old_chess:", old_chess)
        # print("chess:", chessboard)
        state_score_me = 0
        state_score_op = 0
        for i in range(0, 4):
            for j in range(0, 5): #整数向上取整，负数向下取整
                state_score_me += math.ceil(chess_type_me[i][j]/(j+1)) * score[i][j] if chess_type_me[i][j] > 0 else math.floor(chess_type_me[i][j]/(j+1)) * score[i][j]
                state_score_op += math.ceil(chess_type_op[i][j]/(j+1)) * score[i][j] if chess_type_op[i][j] > 0 else math.floor(chess_type_op[i][j]/(j+1)) * score[i][j]
        # state_score_me *= 1.1
        state_score = state_score_me - state_score_op
        # print("type_me:", chess_type_me)
        # print("score_me:", state_score_me)
        # print("type_op:", chess_type_op)
        # print("score_op:", state_score_op)
        # print("score_total:", state_score)
        # print()
        return state_score

    def point_value_4_dir(self, chessboard, each, color, chess_type):
        # chess_type = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]#live, run, sleep, KO
        score_all = 0
        x = each[0]
        y = each[1]
        # 设置四个方向
        direction = [[1, 0], [0, 1], [1, 1], [-1, 1]]
        for i in range(0, 4):
            line = []
            line.append(color)
            k = 1
            while k < 5 and (x + k * direction[i][0] >= 0) and (x + k * direction[i][0] < 15) \
                    and (y + k * direction[i][1] >= 0) and (y + k * direction[i][1] < 15) and \
                    chessboard[x + k * direction[i][0]][y + k * direction[i][1]] != -1 * color:
                line.append(chessboard[x + k * direction[i][0], y + k * direction[i][1]])
                k += 1

            k = -1
            while k > -5 and (x + k * direction[i][0] >= 0) and (x + k * direction[i][0] < 15)\
                    and (y + k * direction[i][1] >= 0) and (y + k * direction[i][1] < 15) and \
                    chessboard[x + k * direction[i][0]][y + k * direction[i][1]] != -1 * color:
                line.insert(0, chessboard[x + k * direction[i][0], y + k * direction[i][1]])
                k -= 1
            score_all += self.point_value_1_dir(line, color, chess_type)

        # 必胜棋型判断
        if chess_type[0][4] > 0:  # 连五
            score_all += KO[4] if color != self.color else KO[4] * 1.1
        elif chess_type[0][3] > 0:  # 活四
            score_all += KO[3] if color != self.color else KO[3] * 1.1
        elif chess_type[1][3] + chess_type[2][3] > 1:  # 双冲四
            chess_type[3][2] += 1
            score_all += KO[2] if color != self.color else KO[2] * 1.1
            if chess_type[1][3] > 1:
                chess_type[1][3] -= 2
            elif chess_type[1][3] > 0:
                chess_type[1][3] -= 1
                chess_type[2][3] -= 1
            else:
                chess_type[2][3] -= 2
        elif (chess_type[1][3] + chess_type[2][3] > 0) and (chess_type[0][2] + chess_type[1][2] > 0):  # 冲四活三
            chess_type[3][1] += 1
            score_all += KO[1] if color != self.color else KO[1] * 1.1
            if chess_type[1][3] > 0:
                chess_type[1][3] -= 1
            else:
                chess_type[2][3] -= 1
            if chess_type[0][2] > 0:
                chess_type[0][2] -= 1
            else:
                chess_type[1][2] -= 1
        elif chess_type[0][2] + chess_type[1][2] > 1:  # 双三
            chess_type[3][0] += 1
            score_all += KO[0] if color != self.color else KO[0] * 1.1
            if chess_type[0][2] > 1:
                chess_type[0][2] -= 2
            elif chess_type[0][2] > 0:
                chess_type[0][2] -= 1
                chess_type[1][2] -= 1
            else:
                chess_type[1][2] -= 2
        return score_all

    def point_value_1_dir(self, line, color, chess_type):
        point_score = 0
        line_len = len(line)
        if line_len < 5:
            point_score += 0
        else:
            # 预处理棋子数
            counts = []
            counts.insert(0, 1 if line[0] == color else 0)
            for i in range(1, line_len):
                if line[i] == color:
                    counts.append(counts[i - 1] + 1)
                else:
                    counts.append(counts[i - 1])

            # 统计棋子数
            dict = {}
            for i in range(0, line_len):
                if line[i] == color:
                    for j in range(4, -1, -1):
                        if i+j < line_len:
                            if line[i+j] == color:
                                dict[(i, i + j)] = counts[i + j] - counts[i] + 1  # key是始末位置，value是count
                                break
            # 寻找棋子数最大
            dict = sorted(dict.items(), key = lambda d: d[1], reverse = True) # 这时候dict已经是list类型了
            max_count = dict[0][1]
            i = 0
            if max_count > 1:
                hasrun4 = False
                run4idx = 0
                while i < len(dict) and dict[i][1] == max_count:
                    #执行judge
                    s_index = dict[i][0][0]
                    e_index = dict[i][0][1]
                    jump = e_index - s_index + 1 - max_count
                    if jump == 0 and s_index-1 >= 0 and e_index + 1 < line_len:
                        # 低级活三单独判断
                        if max_count == 3:
                            if line_len > 5:
                                chess_type[0][max_count - 1] += 1
                                point_score += score[0][max_count - 1] * color
                            else:
                                chess_type[2][max_count - 1] += 1
                                point_score += score[2][max_count - 1] * color
                        else:
                            chess_type[0][max_count - 1] += 1
                            point_score += score[0][max_count - 1] * color
                        # chess_type[0][max_count-1] += 1
                        # point_score += score[0][max_count-1]*color
                    elif jump == 1 and s_index-1 >= 0 and e_index + 1 < line_len:

                        # 双冲四单独判断
                        if max_count == 4:
                            if not hasrun4:
                                chess_type[1][max_count - 1] += 1
                                run4idx = s_index
                                hasrun4 = True
                                point_score += score[1][max_count - 1] * color
                            else:
                                if e_index - run4idx - (counts[e_index] - counts[run4idx]) < 2:
                                    break
                                else:
                                    chess_type[1][max_count - 1] += 1
                                    point_score += score[1][max_count - 1] * color
                        else:
                            chess_type[1][max_count - 1] += 1
                            point_score += score[1][max_count-1]*color

                    elif jump >= 2 or s_index-1 < 0 or e_index + 1 >= line_len:
                        chess_type[2][max_count - 1] += 1
                        point_score += score[2][max_count-1]*color
                    else:
                        point_score += 0
                    i += 1
        return point_score

    def find_empty(self, chessboard):
        # 找到已下棋的位置范围
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        max_x, max_y, min_x, min_y = -1, -1, 15, 15
        for i in range(0, len(idx)):
            x = idx[i][0]
            y = idx[i][1]
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y

        # 往外扩展
        extend = 2
        ex_min_x = min_x - extend if min_x - extend >= 0 else 0
        ex_max_x = max_x + extend if max_x + extend < 15 else 14
        ex_min_y = min_y - extend if min_y - extend >= 0 else 0
        ex_max_y = max_y + extend if max_y + extend < 15 else 14

        # 找出可以考虑的空位置，准备遍历
        empty = np.where(chessboard[ex_min_x:ex_max_x + 1, ex_min_y:ex_max_y + 1] == COLOR_NONE)
        return list(zip(empty[0] + ex_min_x, empty[1] + ex_min_y))

    def sort_empty(self, chessboard, color):
        empty = self.find_empty(chessboard)
        score_empty = {}
        for each in empty:
            chess_type1 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # live, run, sleep, KO
            chess_type2 = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # live, run, sleep, KO
            syn_score_me = self.point_value_4_dir(chessboard, each, color, chess_type1)*1.2
            syn_score_op = self.point_value_4_dir(chessboard, each, -1 *color, chess_type2)
            syn_score = syn_score_me + (-1)*syn_score_op
            score_empty[each] = abs(syn_score)
        sorted_empty = sorted(score_empty.items(), key=lambda d: d[1], reverse=True)
        return sorted_empty
