import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

random.seed(0)
#
# types = {"be5": [[0, 1, 1, 1, 1, 1]],
#          "live4": [[0, 1, 1, 1, 1, 0]],
#          "run4": [[-1, 1, 1, 1, 1, 0],
#                   [1, 1, 1, 0, 1],
#                   [1, 1, 0, 1, 1]],
#          "live3": [[0, 0, 1, 1, 1, 0]],
#          "live3_d": [[-1, 0, 1, 1, 1, 0],
#                    [0, 1, 1, 0, 1, 0]],
#          "sleep3": [[-1, 1, 1, 1, 0, 0],
#                     [-1, 1, 1, 0, 1, 0],
#                     [-1, 1, 0, 1, 1, 0],
#                     [1, 0, 1, 0, 1],
#                     [1, 1, 0, 0, 1]],
#          "live2": [[0, 1, 1, 0, 0],
#                    [0, 1, 0, 1, 0],
#                    [0, 1, 0, 0, 1, 0]],
#          "sleep2": [[-1, 1, 1, 0, 0, 0],
#                     [-1, 1, 0, 1, 0, 0],
#                     [-1, 1, 0, 0, 1, 0],
#                     [1, 0, 0, 0, 1]],
#          "live1": [[0, 1, 0, 0, 0],
#                    [0, 0, 1, 0, 0]],
#          "sleep1": [[-1, 1, 0, 0, 0, 0]]}

#活三和冲三的分数要相同，冲四和眠四的分数要相同
# 必胜棋型：连五，活四，双冲四，冲四活三，双活三 （双冲四有可能是假的，双活三也可能是假的）
# live = [100, 5000, 30000, 150000, 1000000]
# run = [50, 3000, 30000, 50000, 1000000]
# sleep = [20, 2000, 8000, 50000, 1000000]

live = [10, 150, 2000, 40000000, 50000000]
run = [10, 100, 2000, 10000, 50000000]
sleep = [2, 20, 800, 10000, 50000000]

# live = [100, 1000, 10000, 100000, 1000000]
# run = [100, 1000, 10000, 50000, 1000000]
# sleep = [10, 500, 3000, 50000, 1000000]


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):  # type(chessboard) = np.array
        self.candidate_list.clear()
        # =====================================================
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))

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
            # print(ex_min_x)
            # print(ex_min_y)
            # print(ex_max_x)
            # print(ex_max_y)
            empty = np.where(chessboard[ex_min_x:ex_max_x+1, ex_min_y:ex_max_y+1] == COLOR_NONE)
            # empty = np.where(chessboard == COLOR_NONE)
            empty = list(zip(empty[0]+ex_min_x, empty[1]+ex_min_y))

            #empty = [(1,9), (3,2)]

            # 用字典 cal_done储存已经算完的点
            cal_done = {}
            cal_max_score = -1
            # for each in empty:
            #     syn_score_me = self.point_value_4_dir(chessboard, each, self.color)
            #     if abs(syn_score_me) > cal_max_score:
            #         cal_max_score = abs(syn_score_me)
            #         new_pos = each
            #         assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
            #         self.candidate_list.append(new_pos)
            # for each in empty:
            #     syn_score_op = self.point_value_4_dir(chessboard, each, -1 * self.color)
            #     if abs(syn_score_op) > cal_max_score:
            #         cal_max_score = abs(syn_score_op)
            #         new_pos = each
            #         assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
            #         self.candidate_list.append(new_pos)
            for each in empty:
                syn_score_me = self.point_value_4_dir(chessboard, each, self.color)
                syn_score_op = self.point_value_4_dir(chessboard, each, -1 * self.color)
                syn_score = syn_score_me + (-1)*syn_score_op
                if abs(syn_score) > cal_max_score:
                    cal_max_score = abs(syn_score)
                    new_pos = each
                    assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
                    self.candidate_list.append(new_pos)

    # def dfs(self, chessboard, empty, color, depth):
    #     # 设置四个方向
    #     direction = [[1, 0], [0, 1], [-1, -1], [-1, 1]]
    #     for each in empty:
    #         x = each[0]
    #         y = each[1]
    #         for i in range(0, 4):
    #             line = []
    #             line.append(chessboard[x, y])
    #             for k in range(1, 5):
    #                 if chessboard[x + k * direction[i], y + k * direction[i]] == color:

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

        #必胜棋型判断
        if chess_type[0][4] > 0: # 连五
            score_all = live[4] if color != self.color else live[4]+1000000
        elif chess_type[0][3] > 0: # 活四
            score_all = live[3] if color != self.color else live[3]+1000000
        elif chess_type[1][3] + chess_type[2][3] > 1: # 双冲四
            score_all = 30000000 if color != self.color else 31000000
        elif (chess_type[1][3] + chess_type[2][3] > 0) and (chess_type[0][2] + chess_type[1][2] > 0): #冲四活三
            score_all = 20000000 if color != self.color else 21000000
        elif chess_type[0][2] + chess_type[1][2] > 1: # 双三
            score_all = 10000000 if color != self.color else 11000000
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
                    # j = 4
                    # while j >= 0 and ((i+j < line_len) and line[i+j] != color):
                    #     j -=1
                    # dict[(i, i+j)] = counts[i+j] - counts[i] #key是始末位置，value是count
            # 寻找棋子数最大
            dict = sorted(dict.items(), key = lambda d: d[1], reverse = True) # 这时候dict已经是list类型了
            max_count = dict[0][1]
            i = 0

            while i < len(dict) and dict[i][1] == max_count:
                #执行judge
                s_index = dict[i][0][0]
                e_index = dict[i][0][1]
                jump = e_index - s_index + 1 - max_count
                if jump == 0 and s_index-1 >= 0 and e_index + 1 < line_len:
                    chess_type[0][max_count-1] += 1
                    point_score += live[max_count-1]*color
                elif jump == 1 and s_index-1 >= 0 and e_index + 1 < line_len:
                    chess_type[1][max_count - 1] += 1
                    point_score += run[max_count-1]*color
                elif jump >= 2 or s_index-1 < 0 or e_index + 1 >= line_len:
                    chess_type[2][max_count - 1] += 1
                    point_score += sleep[max_count-1]*color
                else:
                    point_score += 0
                i += 1
        return point_score

    # def type_verify(self, line, color):
    #     line_type = []
    #     check_len = 6
    #     line_len = len(line)
    #     counts = []
    #     counts[0] = 1 if line[0] == color else 0
    #     for i in range(1, line_len + 1):
    #         if line[i] == color:
    #             counts[i] = counts[i - 1] + 1
    #         else:
    #             counts[i] = counts[i - 1]
    #
    #     i = check_len - 1
    #     while i < line_len: #没有考虑到长连
    #         count = counts[i] - counts[i - (check_len - 1)]
    #         if count == 5: #也不一定是成5：0110111只能算冲4
    #             line_type.append("be5")
    #             return line_type
    #         elif count == 4:
    #             for c4 in types["live4"]:
    #                 if line == c4:
    #                     line_type.append("live4")
    #                     break
    #             for c4 in types["run4"]:
    #                 if line == c4 or line[::-1] == c4:
    #                     line_type.append("run4")
    #         elif count == 3:
    #             for c3 in types["live3"]:
    #                 if line[:5] == c3 or line[1:] == c3 or line == c3 or line[::-1] == c3:
    #                     line_type.append("live3")
    #             for c3 in types["live3_d"]:
    #                 if line == c3 or line[::-1] == c3:
    #                     line_type.append("live3_d")
    #             for c3 in types["sleep3"]:
    #                 if line == c3 or line[::-1] == c3 or line[:5] == c3 or line[1:] == c3:
    #                     line_type.append("sleep3")
    #         elif count == 2:
    #             for c2 in types["live2"]:
    #                 if line == c2 or line[:5] == c2 or line[1:] == c2 or line[:5] == c2[::-1] or line[1:0] == c2[::-1]:
    #                     line_type.append("live2")
    #             for c2 in types["sleep2"]:
    #                 if line == c2 or line[::-1] == c2:
    #                     line_type.append("sleep2")
    #         elif count == 1:
    #             for c1 in types["live1"]:
    #                 if line[:5] == c1 or line[1:] == c1 or line[:5] == c1[::-1] or line[1:] == c1[::-1]:
    #                     line_type.append("live1")
    #             for c1 in types["sleep1"]:
    #                 if line == c1 or line[::-1] == c1:
    #                     line_type.append("sleep1")
    #         else:
    #             line_type.append("useless")
    #         i += 1
    #     return line_type