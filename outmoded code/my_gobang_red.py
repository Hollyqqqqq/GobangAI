import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

#活三和冲三的分数要相同，冲四和眠四的分数要相同
# 必胜棋型：连五，活四，双冲四，冲四活三，双活三 （双冲四有可能是假的）

# live = [0, 100, 1000, 2000000, 10000000]
# run = [0, 100, 1000, 5000, 10000000]
# sleep = [0, 20, 50, 5000, 10000000]
# KO = [500000, 800000, 1000000, 2000000, 10000000]

# live = [5, 150, 2000, 40000000, 50000000]
# run = [0, 100, 2000, 10000, 50000000]
# sleep = [0, 20, 800, 10000, 50000000]
# KO = [10000000, 20000000, 30000000, 40000000, 50000000]

# live = [0, 800, 2200, 40000000, 50000000]
# run = [0, 100, 2200, 2000, 50000000]
# sleep = [0, 20, 150, 2500, 50000000]

live = [0, 150, 2000, 40000000, 50000000]
run = [0, 100, 2000, 2500, 50000000]
sleep = [0, 20, 200, 3000, 50000000]

# curr best
# live = [0, 800, 2000, 40000000, 50000000]
# run = [0, 100, 1500, 10000, 50000000]
# sleep = [0, 20, 150, 10000, 50000000]
# KO = [10000000, 20000000, 30000000, 40000000, 50000000]
KO = [100000, 100000, 100000, 100000, 100000]


# live = [10, 150, 2000, 40000000, 50000000]
# run = [10, 100, 2000, 10000, 50000000]
# sleep = [2, 20, 800, 10000, 50000000]
# KO = [10000000, 20000000, 30000000, 40000000, 50000000]

# live = [10, 150, 10000, 40000000, 50000000]
# run = [10, 100, 10000, 10000, 50000000]
# sleep = [2, 20, 800, 10000, 50000000]


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):  # type(chessboard) = np.array
        self.candidate_list.clear()
        # =====================================================

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
        ex_min_x = min_x - extend if min_x - extend >=0 else 0
        ex_max_x = max_x + extend if max_x + extend < 15 else 14
        ex_min_y = min_y - extend if min_y - extend >=0 else 0
        ex_max_y = max_y + extend if max_y + extend < 15 else 14

        idx = np.where(chessboard != COLOR_NONE)
        if len(idx[0]) == 0 and len(idx[1]) == 0:
            new_pos = [7,7]
            assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
            self.candidate_list.append(new_pos)
        else:
            # 找出可以考虑的空位置，准备遍历
            empty = np.where(chessboard[ex_min_x:ex_max_x+1, ex_min_y:ex_max_y+1] == COLOR_NONE)
            empty = list(zip(empty[0]+ex_min_x, empty[1]+ex_min_y))

            # empty = [(9, 3), (13, 7)]

            cal_max_score = -1
            score_pos = [[], [], []]
            me_max = 0
            op_max = 0
            me_index = 0
            op_index = 0
            for each in empty:
                syn_score_me = abs(self.point_value_4_dir(chessboard, each, self.color))
                # syn_score_op = abs(self.point_value_4_dir(chessboard, each, -1 * self.color))*0.9 if self.color == 1 \
                #     else abs(self.point_value_4_dir(chessboard, each, -1 * self.color))
                syn_score_op = abs(self.point_value_4_dir(chessboard, each, -1 * self.color)) * 0.8
                # syn_score = syn_score_me + (-1)*syn_score_op
                # if abs(syn_score) > cal_max_score:
                #     cal_max_score = abs(syn_score)
                #     new_pos = each
                #     assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
                #     self.candidate_list.append(new_pos)
                score_pos[0].append(syn_score_me)
                score_pos[1].append(syn_score_op)
                score_pos[2].append(each)
                print(each)
                print(syn_score_me)
                print(syn_score_op)

                if syn_score_me > me_max:
                    me_max = syn_score_me
                    me_index = len(score_pos[0])-1
                elif syn_score_me == me_max:
                    if score_pos[1][len(score_pos[0])-1] > score_pos[1][me_index]:
                        me_index = len(score_pos[0]) - 1
                if syn_score_op > op_max:
                    op_max = syn_score_op
                    op_index = len(score_pos[0])-1
                elif syn_score_op == op_max:
                    if score_pos[0][len(score_pos[0])-1] > score_pos[0][op_index]:
                        op_index = len(score_pos[0]) - 1

                # if syn_score_me > me_max + live[1]: # 相差分数大于活二的分数
                #     me_max = syn_score_me
                #     me_index = len(score_pos[0])-1
                # elif syn_score_me > me_max: # 相差分数小于活二的分数
                #     if score_pos[1][len(score_pos[0])-1] > score_pos[1][me_index] + live[1]:
                #         me_index = len(score_pos[0]) - 1
                # else: # 取综合得分最高的
                #     if syn_score_op + syn_score_me > score_pos[0][me_index] + score_pos[1][me_index]:
                #         me_max = syn_score_me
                #         me_index = len(score_pos[0]) - 1
                # if syn_score_op > op_max + live[1]: # 相差分数大于活二的分数
                #     op_max = syn_score_op
                #     op_index = len(score_pos[0])-1
                # elif syn_score_op > op_max: # 相差分数小于活二的分数
                #     if score_pos[1][len(score_pos[0])-1] > score_pos[1][op_index] + live[1]:
                #         op_index = len(score_pos[0]) - 1
                # else: # 取综合得分最高的
                #     if syn_score_op + syn_score_me > score_pos[0][op_index] + score_pos[1][op_index]:
                #         op_max = syn_score_op
                #         op_index = len(score_pos[0]) - 1
                # if abs(syn_score_me - me_max) <= me_max*0.000005: # 如果相差不多的话, 取综合评分高的
                #     if syn_score_me + syn_score_op > score_pos[0][me_index] + score_pos[1][me_index]:
                #         me_max = syn_score_me
                #         me_index = len(score_pos[0]) - 1
                # elif syn_score_me > me_max:
                #     me_max = syn_score_me
                #     me_index = len(score_pos[0]) - 1
                # if abs(syn_score_op - op_max) <= op_max*0.000005: # 如果相差不多的话, 取综合评分高的
                #     if syn_score_op + syn_score_me > score_pos[0][op_index] + score_pos[1][op_index]:
                #         op_max = syn_score_op
                #         op_index = len(score_pos[0]) - 1
                # elif syn_score_op > op_max:
                #     op_max = syn_score_op
                #     op_index = len(score_pos[0]) - 1
                # print("wo d zui da = ", me_max)
                # print(me_index)
                # print("ta d zui da = ", op_max)
                # print(op_index)
                # print()
                if me_max >= op_max:
                    new_pos = score_pos[2][me_index]
                else:
                    new_pos = score_pos[2][op_index]

                assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
                self.candidate_list.append(new_pos)

    def point_value_4_dir(self, chessboard, each, color):
        chess_type = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
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
            # print(score_all)

        #必胜棋型判断
        if chess_type[0][4] > 0: # 连五
            score_all += KO[4] if color != self.color else KO[4]*1.1
        elif chess_type[0][3] > 0: # 活四
            score_all += KO[3] if color != self.color else KO[3]*1.1
        elif chess_type[1][3] + chess_type[2][3] > 1: # 双冲四
            score_all += KO[2] if color != self.color else KO[2]*1.1
        elif (chess_type[1][3] + chess_type[2][3] > 0) and (chess_type[0][2] + chess_type[1][2] > 0): #冲四活三
            score_all += KO[1] if color != self.color else KO[1]*1.1
        elif chess_type[0][2] + chess_type[1][2] > 1: # 双三
            score_all += KO[0] if color != self.color else KO[0]*1.1
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
                            point_score += live[max_count - 1] * color
                        else:
                            chess_type[2][max_count - 1] += 1
                            point_score += sleep[max_count - 1] * color
                    else:
                        chess_type[0][max_count-1] += 1
                        point_score += live[max_count-1]*color
                    # chess_type[0][max_count - 1] += 1
                    # point_score += live[max_count-1]*color
                elif jump == 1 and s_index-1 >= 0 and e_index + 1 < line_len:
                    # 双冲四单独判断
                    if max_count == 4:
                        if not hasrun4:
                            chess_type[1][max_count - 1] += 1
                            run4idx = s_index
                            hasrun4 = True
                            point_score += run[max_count - 1] * color
                        else:
                            if e_index - run4idx - (counts[e_index] - counts[run4idx]) < 2:
                                break
                            else:
                                chess_type[1][max_count - 1] += 1
                                point_score += run[max_count - 1] * color

                    else:
                        chess_type[1][max_count - 1] += 1
                        point_score += run[max_count-1]*color
                elif jump >= 2 or s_index-1 < 0 or e_index + 1 >= line_len:
                    chess_type[2][max_count - 1] += 1
                    point_score += sleep[max_count-1]*color
                else:
                    point_score += 0
                i += 1
        return point_score