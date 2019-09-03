import numpy as np
import random
import time
import re

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
#random.seed(0)
#don't change the class name
class AI(object):
#chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []


   # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        #==================================================================
        #Write your algorithm here
        #Here is the simplest sample:Random decision

        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))

        # black=np.where(chessboard == COLOR_BLACK)
        # black_idx=list(zip(black[0],black[1]))
        # white=np.where(chessboard==COLOR_WHITE)
        # white_idx=list(zip(white[0],white[1]))
        if self.color==COLOR_BLACK:
            color='b'
        else:
            color='w'
        ps=patterns(chessboard,color)
        self.candidate_list.append(ps.cand)

        # pos_idx = random.randint(0, len(idx)-1)
        # new_pos = idx[pos_idx]
        # #==============Find new pos========================================
        # # Make sure that the position of your decision in chess board is empty. 
        # #If not, return error.
        # assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE
        # #Add your decision into candidate_list, Records the chess board
        # self.candidate_list.append(new_pos)

class atom:
    def __init__(self,ind):
        self.x=ind[0]
        self.y=ind[1]
        self.direct=15

directs=[(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1)] # 9点开始顺时针
def get_next(ind,direct):
    drct=directs[direct]
    return (ind[0]+drct[0],ind[1]+drct[1])

def get_nexts(ind,direct,num):

    if num==1:
        return get_next(ind,direct)
    elif num==-1:
        return get_next(ind,get_oppo_direct(direct))
    elif num==0:
        return ind
    else:
        k=1
        if num<0:
            k=-1
        return get_nexts(get_next(ind,direct),direct,num-k)

def get_nexts_arr(ind,direct,arr):
    res=list()
    for i in arr:
        res.append(get_nexts(ind,direct,i))
    return res

def get_oppo_direct(direct):
    return (direct+4)%8

def check_pos(ind,board,color):
    size=len(board)
    if ind[0]<0 or ind[0]>=size:
        return False
    if ind[1]<0 or ind[1]>=size:
        return False
    if board[ind[0]][ind[1]]==color:
        return True
    else:
        return False

def check_next(ind,direct,board,color):
    ind=get_next(ind,direct)
    return check_pos(ind,board,color)

def check_nexts(ind,direct,num,board,color):
    if num==1:
        return check_next(ind,direct,board,color)
    elif num==-1:
        return check_next(ind,get_oppo_direct(direct),board,color)
    else:
        k=1
        if num<0:
            k=-1
        return check_nexts(ind,direct,num-k,board,color)

def check_nexts_arr(ind,direct,arr,board,color):
    res=list()
    for i in arr:
        res.append(check_nexts(ind,direct,i,board,color))
    return res

def check_default(ind,direct,board,color,revise=False):
    if revise==False:
        arr=[1,2,3,4]
    else:
        arr=[-1,-2,-3,-4]
    return check_nexts_arr(ind,direct,arr,board,color)

class form:
    def __init__(self,ind,num,direct,form_type):
        self.ind=ind
        self.num=num
        self.direct=direct
        self.form_type=form_type
        self.cand=list([0]*6)

    def get_candi(self):
        if self.num==5:
            return list()
        elif self.num==4:
            # 这里代码冗余，等待算法改进后添加合适的待选值
            if self.form_type == 4:
                res_tmp=get_nexts_arr(self.ind,self.direct,[-1,self.form_type])
            elif self.form_type == 3:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type])
            elif self.form_type == 2:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type])
            elif self.form_type == 1:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type])
            self.cand[4]=res_tmp

        elif self.num==3:
            if self.form_type == 3:
                res_tmp=get_nexts_arr(self.ind,self.direct,[-1,self.form_type])
            elif self.form_type == 2:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type,-1,4])
            elif self.form_type == 1:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type,-1,4])
            self.cand[3]=res_tmp

        elif self.num==2:
            if self.form_type == 2:
                res_tmp=get_nexts_arr(self.ind,self.direct,[-1,self.form_type])
            elif self.form_type == 1:
                res_tmp=get_nexts_arr(self.ind,self.direct,[self.form_type,-1,4])
            self.cand[2]=res_tmp

        elif self.num==1:
            res_tmp=list()
            for i in range(8):
                res_tmp.append(get_next(self.ind,i))
            self.cand[1]=res_tmp

class situation:
    def __init__(self,board,color):
        self.board=board
        self.cand=list([0]*6)
        self.none=self.get_none()
        self.my=self.get_color(color)
        self.oppo=self.get_color(-color)
        self.color=color
        self.my_forms=list()
        self.oppo_forms=list()

    def get_none(self):
        idx = np.where(self.board == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        return idx

    def get_color(self,color):
        c=np.where(self.board == color)
        c_ind=list(zip(c[0],c[1]))
        return c_ind

    def get_form(self,ind,color):
        res_form=list()
        directs=list()
        for i in range(4):
            if sum(check_default(ind,i,self.board,color,revise=True))==0:
                directs.append(i+4)

        for i in directs:
            tmp=check_default(ind,i,self.board,color)
            num=sum(tmp)+1
            tmp_type=0
            for j in range(4):
                if tmp[j]==True:
                    tmp_type=tmp_type*10+j
            new_form=form(ind,num,i,tmp_type)
            res_form.append(new_form)
        return res_form

    def get_oppo_forms(self):
        pass

    def get_forms(self,me=True):
        if me==True:
            atoms=self.my
            color=self.color
        else:
            atoms=self.oppo
            color=-self.color
        tmp_forms=list()
        for ind in atoms:
            x=self.get_form(ind,color)
            tmp_forms+=x
        
        # 按照form种类的大小排序
        tmp_forms=sorted(tmp_forms,key=lambda x:x.form_type)
        return tmp_forms

sembol=['b','n','w','x']
def get_atom(board,ind):
    try:
        x=board[ind[0]][ind[1]]
    except:
        x=2
    return sembol[int(x+1)]
    

class pattern:
    def __init__(self,ind,direct,st):
        self.ind=ind
        self.direct=direct
        self.st=st
        self.info=(ind,direct)
        self.size=len(st)

    def get_cand(self):
        pass

class patterns:
    def __init__(self,board,color):
        self.size=len(board)
        self.board=board
        self.collection=self.get_patterns()
        self.maps=self.get_maps()
        self.info_maps=self.get_info_maps()
        self.attention_b=list([
            'nbbbb','bnbbb','bbnbb','bbbnb','bbbbn',
            'nwwww','wnwww','wwnww','wwwnw','wwwwn',
            'nbbbn','bnbbn','nbnbb','nbbnb','bbnbn',
            'nwwwn','nwnww','wnwwn','wwnwn','nwwnw',
            'nbbn','bnbn','nbnb',
            'nwwn','nwnwn','nwnw',
            'nbn','nb','bn',
            'nwn','nw','wn'
            
        ])
        self.attention_w=list([
            'nwwww','wnwww','wwnww','wwwnw','wwwwn',
            'nbbbb','bnbbb','bbnbb','bbbnb','bbbbn',
            
            'nwwwn','nwnww','wnwwn','wwnwn','nwwnw',
            'nbbbn','bnbbn','nbnbb','nbbnb','bbnbn',
            
            'nwwn','nwnwn','nwnw',
            'nbbn','bnbn','nbnb',
            
            'nwn','nw','wn',
            'nbn','nb','bn'
            
            
        ])
        
        if color=='b':
            self.cand=self.get_candi('b')
        else:
            self.cand=self.get_candi('w')

    def get_patter(self,ind,direct):
        res=get_atom(self.board,ind)
        for i in range(self.size-1):
            res+=get_atom(self.board,get_nexts(ind,direct,i+1))
        return res
        
    def get_patterns(self):
        res=list()
        for i in range(self.size):
            tmp1=self.get_patter((0,i),6)
            res.append(pattern((0,i),6,tmp1))

            tmp1=self.get_patter((i,0),4)
            res.append(pattern((i,0),4,tmp1))

            tmp1=self.get_patter((0,i),5)
            res.append(pattern((0,i),5,tmp1))

            tmp1=self.get_patter((i,0),3)
            res.append(pattern((i,0),3,tmp1))

            tmp1=self.get_patter((i,0),5)
            res.append(pattern((i,0),5,tmp1))

            tmp1=self.get_patter((self.size-1,i),3)
            res.append(pattern((self.size-1,i),3,tmp1))
        return res

    def get_maps(self):
        res=''
        for i in self.collection:
            res+=i.st+'\n'
        return res

    def get_info_maps(self):
        res=list()
        for i in self.collection:
            res.append(i.info)
        return res

    def get_pos(self,row,idx):
        ind=self.info_maps[row][0]
        direct=self.info_maps[row][1]
        return get_nexts(ind,direct,idx)

    def get_candi(self,color='b'):
        if color=='b':
            tmp=self.attention_b
        else:
            tmp=self.attention_w
        
        for s in tmp:
            x=re.compile(s)
            offset=0
            offsets=list()
            for i in range(len(s)):
                if s[i]=='n':
                    offsets.append(i)
            
            f=x.search(self.maps)
            if f!=None:
                pos=list()
                for i in offsets:
                    pos.append(f.start()+i)
                break

        try:
            select=np.random.randint(0,len(pos))
            tmp_pos=pos[select]
            row=tmp_pos//(self.size+1)
            offset=tmp_pos%(self.size+1)
        except:
            print("The init",end=':')
            row=self.size//2
            offset=self.size//2
            return (row,offset)
        return self.get_pos(row,offset)
                
    def show(self):
        for i in self.collection:
            print(i.st)

if __name__=="__main__":
    board=np.load('board.npy')
    ps=patterns(board,'b')
    print(ps.maps)
    for i in ps.info_maps:
        print(i)












        
            
                

        
        







