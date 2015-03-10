#!/usr/bin/python
def compress(instructions):
    count=0
    comp_list = []
    while count < len(instructions):
        begin = instructions[count]
        comp_list.append(begin)
        count2 = 1
        while count+count2 < len(instructions):
            finish = instructions[count+count2]
            if begin == finish:None
            elif begin!=finish:
                if count2>2:comp_list.append(count2)
                elif count2==1:None
                elif count2==2:comp_list.append(begin)
                break
            count2 = count2+1
        count = count+count2
    if count2>2:
        comp_list.append(count2)
    if count2==1:
        None
    if count2==2:
        comp_list.append(begin)
    return (comp_list)
def path(inpdict):
    slocx,slocy=inpdict[2],inpdict[3]
    elocx,elocy=inpdict[4],inpdict[5]
    
    #manual search for endpoint
    '''i,j=0,0
    for i in range(inpdict[0]):
        j=0
        for j in range(inpdict[1]):
            if board[i][j]=='[$]':
                elocx,elocy=i,j
            j+=1
        i+=1'''
    i=0
    instructions = []
    while i<((inpdict[0]+inpdict[1])-2):
        if elocx>slocx:
            instructions.append("D")
            slocx+=1
        if elocx<slocx:
            instructions.append("U")
            slocx-=1
        if elocy>slocy:
            instructions.append("R")
            slocy+=1
        if elocy<slocy:
            instructions.append("L")
            slocy-=1
        inpdict[2],inpdict[3]=slocx,slocy
        inpdict[4],inpdict[5]=elocx,elocy
        sleep(0.08)
        boardcreate(inpdict)
        '''
        if slocx==elocx and slocy==elocy:
            print ("Found it!\n\nThis is the path I followed:")
            #print (compress(instructions))
            print (instructions)
            break
        '''
        if slocx==elocx and slocy==elocy:
            elocx=randrange(0,inpdict[0])
            elocy=randrange(0,inpdict[1])
            flag=False
            while True:
                a=input("quit? (y/n)")
                if a=='y':
                    flag=True
                    break
                elif a=='n':
                    flag=False
                    break
            if flag==True:
                break
            i=-1
        i+=1
def check(case, value,dim):
    errorprin={
        0:"VALID",
        1:"*Positive",
        2:"Out of m range",
        3:"Out of n range"
    }
    if case=='x':
        if dim>value>=0:return (errorprin[0], True)
        else:return(errorprin[2], False)
    elif case=='y':
        if dim>value>=0:return (errorprin[0], True)
        else:return(errorprin[3], False)
    elif case=='dim':
        if value>0:return (errorprin[0], True)
        else:return(errorprin[1], False)
def inp():
    '''
    This function grabs the appropriate input
    '''
    prindict={
    0:"m value: ",        #mprint
    1:"n value: ",        #nprint
    2:"Start m value: ",  #start x print
    3:"Start n value: ",  #start y print
    4:"End m value: ",    #end x print
    5:"End n value: ",    #end y print
    }
    inpdict={}
    checkVar=True
    errorout='VALID'
    i=0
    while i<=3:
        try:
            inpdict.update({i:int(input(prindict[i]))})
            if i==0 or i==1:errorout, checkVar=check('dim',inpdict[i], None)
            if i==2:errorout, checkVar=check('x',inpdict[i], inpdict[0])
            if i==3:errorout, checkVar=check('y',inpdict[i], inpdict[1])
            print (errorout)
            if checkVar==True:i+=1
        except ValueError:print ("*INTEGER")
    #random shit
    inpdict[4]=randrange(0,inpdict[0])
    inpdict[5]=randrange(0,inpdict[1])
    return (inpdict)
def boardcreate(inpdict):
    '''
    This function clears the screen and makes a new board with the pieces in the appropriate positions
    '''
    system('cls')
    board=[]
    x,y,count = 0,0,0
    for y in range(inpdict[0]):
        for x in range(inpdict[1]):
            if inpdict[2]==y and inpdict[3]==x:board.append('[*]')
            elif inpdict[4]==y and inpdict[5]==x:board.append('[^]')
            else:board.append('[0]')
    print ("---------------------------")
    for i in board:
        if count<inpdict[1]-1:
            print (i, end='')
            count+=1
        else:
            print (i)
            count=0
    print ("---------------------------")
    print ("[*]"+'('+str(inpdict[2])+', '+str(inpdict[3])+')')
    print ("[^]"+'('+str(inpdict[4])+', '+str(inpdict[5])+')')
    print ("Dimensions: "+'('+str(inpdict[0])+', '+str(inpdict[1])+')')
    print('\n')
if __name__=="__main__":
    '''
    This program starts at a position in a field and moves a marker "*" to the indicated
    position
    '''
    from os import system
    from time import sleep
    from random import randrange
    print ("Give me mxn grid and a start location and i'll find all the blocks")
    inpdict = inp()
    board = boardcreate(inpdict)
    instructions = path(inpdict)
