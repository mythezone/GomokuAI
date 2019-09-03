import numpy as np 
import random
import time
from player import AI

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
# random.seed(0)

class chess:
    def __init__(self,board_size):
        self.board_size=board_size
        self.board=np.zeros((board_size,board_size))
        self.black_list=list()
        self.white_list=list()
        self.win=0
        

    def go(self,ind,color):
        assert self.board[ind[0]][ind[1]]==COLOR_NONE
        self.board[ind[0]][ind[1]]=color
        if color==COLOR_BLACK:
            self.black_list.append(ind)
        else:
            self.white_list.append(ind)

        win=self.check_win(color)
        if win==COLOR_BLACK:
            print("Black player win!!")
            self.show()
        elif win==COLOR_WHITE:
            print("White Player win!!")
            self.show()
        else:
            return 

    def show(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j]==COLOR_BLACK:
                    print('b',end=' ')
                elif self.board[i][j]==COLOR_WHITE:
                    print('w',end=' ')
                else:
                    print(' ',end=' ')
            print('\n',end='')

    def check_win(self,color):
        if color==COLOR_BLACK:
            for ind in self.black_list:
                x=self.check_directs(color,ind)
                if x==5:
                    return self.win
        else:
            for ind in self.white_list:
                x=self.check_directs(color,ind)
                if x==5:
                    return self.win
        return self.win

    def check_direct(self,color,ind,direction,num):
        tmp=(ind[0]+direction[0],ind[1]+direction[1])
        if tmp[0]<0 or tmp[0]>14:
            return num
        if tmp[1]<0 or tmp[1]>14:
            return num
        if self.board[tmp[0]][tmp[1]]==color:
            if num==4:
                self.win=color
                return 5
            else:
                return self.check_direct(color,tmp,direction,num+1)
        else:
            return num

    def check_directs(self,color,ind):
        directions=[(0,1),(1,-1),(1,0),(1,1)]
        max_x=1
        for d in directions:
            x=self.check_direct(color,ind,d,1)
            if x==5:
                return 5
            if x>max_x:
                max_x=x
        return max_x

if __name__=='__main__':
    c=chess(15)
    w=AI(15,COLOR_WHITE,1000)
    b=AI(15,COLOR_BLACK,1000)
    for i in range(100):
        print("-------------------------------")
        b.go(c.board)
        tmp_b=b.candidate_list[-1]
        c.go(tmp_b,COLOR_BLACK)
        if c.win!=0:
            break
        w.go(c.board)
        tmp_w=w.candidate_list[-1]
        c.go(tmp_w,COLOR_WHITE)
        if c.win!=0:
            break
        c.show()
    #c.show()
    print("wait to save...")
    np.save('./board.npy',c.board,allow_pickle=True)



