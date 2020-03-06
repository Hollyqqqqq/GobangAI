import numpy as np

# # chessboard = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
# #                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
# #                        [0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# chessboard = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#                        [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
#
#
# def point_value_4_dir(chessboard, each, color):
#     chess_type = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
#     score_all = 0
#     x = each[0]
#     y = each[1]
#     # 设置四个方向
#     direction = [[1, 0], [0, 1], [1, 1], [-1, 1]]
#     for i in range(0, 4):
#         line = []
#         line.append(color)
#         k = 1
#         while k < 5 and (x + k * direction[i][0] < 15) and (y + k * direction[i][1] < 15) and \
#                 chessboard[x + k * direction[i][0]][y + k * direction[i][1]] != -1 * color:
#             line.append(chessboard[x + k * direction[i][0], y + k * direction[i][1]])
#             k += 1
#
#         k = -1
#         while k > -5 and (x + k * direction[i][0] >= 0) and (y + k * direction[i][1] >= 0) and \
#                 chessboard[x + k * direction[i][0]][y + k * direction[i][1]] != -1 * color:
#             line.insert(0, chessboard[x + k * direction[i][0], y + k * direction[i][1]])
#             k -= 1
#
#         point_score = 0
#         line_len = len(line)
#         if line_len < 5:
#             point_score += 0
#         else:
#             # 预处理棋子数
#             counts = []
#             counts.insert(0, 1 if line[0] == color else 0)
#             for i in range(1, line_len):
#                 if line[i] == color:
#                     counts.append(counts[i - 1] + 1)
#                 else:
#                     counts.append(counts[i - 1])
#
#             # 统计棋子数
#             dict = {}
#             for i in range(0, line_len):
#                 if line[i] == color:
#                     for j in range(4, -1, -1):
#                         if i + j < line_len:
#                             if line[i + j] == color:
#                                 dict[(i, i + j)] = counts[i + j] - counts[i] + 1  # key是始末位置，value是count
#                                 break
#                     # j = 4
#                     # while j >= 0 and ((i+j < line_len) and line[i+j] != color):
#                     #     j -=1
#             # 寻找棋子数最大
#             dict = sorted(dict.items(), key=lambda d: d[1], reverse=True)  # 这时候dict已经是list类型了
#             max_count = dict[0][1]
#             i = 0
#
#             hasrun4 = False
#             run4idx = 0
#             while i < len(dict) and dict[i][1] == max_count:
#                 # 执行judge
#                 s_index = dict[i][0][0]
#                 e_index = dict[i][0][1]
#                 jump = e_index - s_index + 1 - max_count
#                 if jump == 0 and s_index - 1 >= 0 and e_index + 1 < line_len:
#                     chess_type[0][max_count - 1] += 1
#                     #point_score += live[max_count - 1] * color
#                 elif jump == 1 and s_index - 1 >= 0 and e_index + 1 < line_len:
#                     # 双冲四单独判断
#                     if max_count == 4:
#                         if not hasrun4:
#                             chess_type[1][max_count - 1] += 1
#                             run4idx = s_index
#                             hasrun4 = True
#                             # point_score += run[max_count - 1] * color
#                         else:
#                             if e_index - run4idx - (counts[e_index] - counts[run4idx]) < 2:
#                                 break
#                             else:
#                                 chess_type[1][max_count - 1] += 1
#                                 # point_score += run[max_count - 1] * color
#                     else:
#                         chess_type[1][max_count - 1] += 1
#                     #point_score += run[max_count - 1] * color
#                 elif jump >= 2 or s_index - 1 < 0 or e_index + 1 >= line_len:
#                     chess_type[2][max_count - 1] += 1
#                     #point_score += sleep[max_count - 1] * color
#                 else:
#                     point_score += 0
#                 i += 1
#     # score_all += self.point_value_1_dir(line, color)
#     return chess_type
#
#
# # chess_t = point_value_4_dir(chessboard, [4, 7], 1)
# #
# # print(chess_t[0])
# # print(chess_t[1])
# # print(chess_t[2])
# # print()
# #
# # chess_t = point_value_4_dir(chessboard, [5, 6], 1)
# # print(chess_t[0])
# # print(chess_t[1])
# # print(chess_t[2])
# for each in chessboard:
#     point_value_4_dir(chessboard, each, 1)
# import time
#
# chess_type_me = [[1, 0, 0, 0, 2], [0, 0, 3, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 1, 0]]# live, run, sleep, KO
# chess_type_temp = [[2, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 2, 0, 0, 0]]
# start = time.clock()
# total = []
# for i in range(0, 4):
#     total.append(np.sum([chess_type_me[i],chess_type_temp[i]], axis=0))
# end = time.clock()
# print(end - start)
# print(total)
# start = time.clock()
# chess_type_me = [[chess_type_me[0][i] + chess_type_temp[0][i] for i in range(0,5)],
#                              [chess_type_me[1][i] + chess_type_temp[1][i] for i in range(0,5)],
#                              [chess_type_me[2][i] + chess_type_temp[2][i] for i in range(0,5)],
#                              [chess_type_me[3][i] + chess_type_temp[3][i] for i in range(0,5)]]
# end = time.clock()
# print(end - start)
# print(chess_type_me)
import math
print(math.ceil(-1.0/3))
print(math.floor(-1.0/3))

