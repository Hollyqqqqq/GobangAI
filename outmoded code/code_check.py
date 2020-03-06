#!/usr/bin/env python3
"""
check the security and functionability of uploaded code
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback
import sys
import os
import numpy as np

# from timeout_decorator import timeout

FORBIDDEN_LIST = ['import os', 'exec']


class CodeCheck():
    def __init__(self, script_file_path, chessboard_size):
        self.time_out = 5
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.errormsg = 'Error'
        self.errorcase = 0
        # sys.stdout = open(os.devnull, 'w')
        # sys.stderr = open(os.devnull, 'w')
        # print(self.chessboard)

    # Call this function and get True or False, self.errormsg has the massage
    def check_code(self):
        # check if contains forbidden library
        if self.__check_forbidden_import() == False:
            return False

        # check initialization
        try:
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False

        # check simple condition
        # if not self.__check_simple_chessboard():
        #     self.errormsg = "Can not pass usability test."
        #     return False

        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False

        return True

    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r', encoding='UTF-8') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True

    def __check_go(self, chessboard):
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
        try:
            self.agent.go(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            return False
        return True

    def __check_result(self, chessboard, result):
        if not self.__check_go(chessboard):
            return False
        # print(self.agent.candidate_list)
        print(self.agent.candidate_list[-1])
        if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
            return False
        return True

    def __check_simple_chessboard(self):
        # empty chessboard
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            return False

        # only one empty position remain
        chessboard = np.ones((self.chessboard_size, self.chessboard_size))
        chessboard[:, ::2] = -1
        for i in range(0, self.chessboard_size, 4):
            chessboard[i] = -chessboard[i]
        x, y = np.random.choice(self.chessboard_size, 2)
        chessboard[x, y] = 0

        if not self.__check_result(chessboard, [[x, y]]):
            return False

        return True

    def __check_advance_chessboard(self):
        #                       0   1   2   3   4   5   6   7   8   9   0   1   2   3   4
        chessboard = np.array([[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#0
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#1
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#2
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#3
                               [0,  0,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  0,  0,  0],#4
                               [0,  0,  0,  0,  0,  0, -1, -1, -1,  1,  0,  0,  0,  0,  0],#5
                               [0,  0,  0,  0,  0,  0,  1,  1, -1,  0,  0,  0,  0,  0,  0],#6
                               [0,  0,  0,  0,  0,  0,  1, -1, -1, -1, -1,  0,  0,  0,  0],#7
                               [0,  0,  0,  0,  0,  0,  1,  0, -1,  0,  0,  0,  0,  0,  0],#8
                               [0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0],#9
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#0
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#1
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#2
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],#3
                               [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]])#4
        if not self.__check_result(chessboard, [[7, 11]]):
            print(-2)
            self.errorcase = 1
            return False
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[ 8, 8] =-1
        chessboard[7, 7] =1
        chessboard[7, 8] =-1
        chessboard[6, 8] =1
        chessboard[8, 6] =-1
        chessboard[8, 9] =1
        chessboard[8, 7] =-1
        chessboard[6, 9] =1
        chessboard[8, 5] =-1
        chessboard[8, 4] =1
        chessboard[7, 9] =-1
        chessboard[6, 10] =1
        chessboard[6, 7] =-1
        chessboard[5, 8] =1
        chessboard[ 7, 10] =-1
        chessboard[7, 11] =1
        chessboard[5, 9] =-1
        chessboard[6, 11] =1
        chessboard[ 6, 12] =-1
        chessboard[9, 11] =1
        chessboard[ 8, 11] =-1
        chessboard[ 8, 12] =1
        chessboard[ 7, 13] =-1
        chessboard[ 5, 11] =1
        chessboard[ 9, 13] =-1
        chessboard[ 8, 13] =1
        chessboard[7, 12] =-1
        chessboard[4, 11] =1
        chessboard[3, 11] =-1
        chessboard[4, 12] =1
        chessboard[ 9, 10] =-1
        chessboard[ 10, 9] =1
        chessboard[ 6, 13] =-1
        print(chessboard)
        if not self.__check_result(chessboard, [[5, 14]]):
            print(-1)
            self.errorcase = 1
            return False



        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[7, 7] = -1
        chessboard[6, 6] = 1
        chessboard[8, 6] = -1
        chessboard[6, 8] = 1
        chessboard[7, 5] = -1
        chessboard[6, 7] = 1
        chessboard[6, 5] = -1
        chessboard[6, 9] = 1
        chessboard[6, 10] = -1
        chessboard[7, 8] = 1
        chessboard[9, 5] = -1
        chessboard[8, 5] = 1
        chessboard[5, 8] = -1
        chessboard[5, 6] = 1
        chessboard[4, 5] = -1
        chessboard[9, 6] = 1
        chessboard[8, 7] = -1
        chessboard[8, 9] = 1
        chessboard[9, 10] = -1
        chessboard[7, 9] = 1
        chessboard[5, 9] = -1
        chessboard[8, 10] = 1
        chessboard[5, 7] = -1
        chessboard[9, 9] = 1
        chessboard[10, 9] = -1
        chessboard[8, 11] = 1
        chessboard[7, 6] = -1
        if not self.__check_result(chessboard, [[9, 8]]):
            print(0)
            self.errorcase = 1
            return False

        return True


        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2] = 1
        # chessboard[3, 3] = 1
        # chessboard[4, 4] = 1
        # chessboard[5, 6] = 1
        # chessboard[5, 8] = 1
        # chessboard[1:3, 11] = -1
        # chessboard[3, 9:11] = -1
        # chessboard[6, 13] = -1
        # if not self.__check_result(chessboard, [[5, 5]]):
        #     print(1)
        #     self.errorcase = 1
        #     return False
        #
        # #
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2:4] = 1
        # chessboard[4, 1:3] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12] = -1
        # if not self.__check_result(chessboard, [[1, 9]]):
        #     print(2)
        #     self.errorcase = 2
        #     return False
        #
        # #
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2] = 1
        # chessboard[2, 4] = 1
        # chessboard[3, 2:4] = 1
        # chessboard[5, 2] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12:14] = -1
        # if not self.__check_result(chessboard, [[4, 2]]):
        #     print(3)
        #     self.errorcase = 3
        #     return False
        #
        # #
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2:5, 2] = 1
        # chessboard[6, 3:5] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12:14] = -1
        # if not self.__check_result(chessboard, [[5, 2]]):
        #     print(4)
        #     self.errorcase = 4
        #     return False
        #
        # #
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[1, 3] = 1
        # chessboard[2, 2] = 1
        # chessboard[2, 5] = 1
        # chessboard[3:5, 3] = 1
        # chessboard[1, 11:13] = -1
        # chessboard[2, 11:13] = -1
        # chessboard[5, 13] = -1
        # if not self.__check_result(chessboard, [[2, 3]]):
        #     print(5)
        #     self.errorcase = 5
        #     return False
        # return True
