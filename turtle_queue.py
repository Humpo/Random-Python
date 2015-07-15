class QueueBoard(object):
    def __init__(self, num_queues, size):
        '''Grabs vars and makes the 'queue board' '''
        self.entities = 0
        self.entitiesProcessed = 0
        self.queues = num_queues
        self.size = size
        self.board = [['.' for j in range(self.size)] for i in range(self.queues)]
        #self.entity = entity
    
    def getEntities(self):
        '''grabs all entities on the board'''
        all_entities = []
        for queue_row in self.board:
            all_entities += list(filter(lambda i: isinstance(i,entity), queue_row))
        return all_entities
        
    def get(self, queue_num, position):
        '''gets whatever is on the board'''
        if 0 <= queue_num < self.queues and 0 <= position < self.size:
            return self.board[queue_num][position]

    def switch(self, pos_a, pos_b):
        '''swaps 2 board elements'''
        self.board[pos_a[0]][pos_a[1]],self.board[pos_b[0]][pos_b[1]] = self.board[pos_b[0]][pos_b[1]],self.board[pos_a[0]][pos_a[1]]
        
    def getEntityDecisions(self):
        '''Used to analyzing and excecuting decisions'''
        return list(map(lambda i: i.decision(), self.getEntities()))

    def excecuteEntityDecisions(self):
        '''excecutes backwards through a list for each entity'''
        for queue_row in range(len(self.board)-1,-1,-1):#loop through backwards queues
            for queue_col in range(len(self.board[queue_row])-1,-1,-1):#loop through backwards positions
                ent = self.get(queue_row, queue_col)
                if isinstance(ent, entity):
                    #ent.printStatus()
                    if ent.fuel <= 0:#if feul empty change symbol name to declare "EMPTY" 
                        ent.name = '#'
                    elif ent.isBeingResolved():
                        if ent.isResolved():
                            self.board[queue_row][queue_col] = '.'
                            self.entities -= 1
                            self.entitiesProcessed += 1
                    elif not ent.hasMoved:
                        decision = ent.decision()
                        if decision == "left":
                            if self.get(ent.y+1, ent.x) == '.':
                                if ent.moveLeft():
                                    self.switch((queue_row,queue_col),(queue_row+1,queue_col))
                        elif decision == "right":
                            if self.get(ent.y-1, ent.x) == '.':
                                if ent.moveRight():
                                    self.switch((queue_row,queue_col),(queue_row-1,queue_col))
                        elif decision == "up":
                            if self.get(ent.y, ent.x-1) == '.':
                                if ent.moveUp():
                                    self.switch((queue_row,queue_col),(queue_row,queue_col-1))
                        elif decision == "down":
                            if self.get(ent.y, ent.x+1) == '.':
                                if ent.moveDown():
                                    self.switch((queue_row,queue_col),(queue_row,queue_col+1))

        #resets movement
        for queue_row in range(len(self.board)):
            for queue_col in range(len(self.board[queue_row])):
                ent = self.get(queue_row, queue_col)
                if isinstance(ent, entity):
                    ent.moved()
                    
    def addEntity(self, queue_num=0, position=0, name="", wait=1, fuel=1000):
        '''adds an entity if empty'''
        if not isinstance(self.board[queue_num][position],entity):
            if name == "":inp_name = string.ascii_lowercase[(self.entities+self.entitiesProcessed)%len(string.ascii_lowercase)]
            else:inp_name = name
            self.board[queue_num][position] = entity(self,
                                                     queue_num,
                                                     position,
                                                     inp_name,
                                                     wait,
                                                     fuel)
            self.entities += 1
            return True
        return False

    def printBoard(self):
        '''prints the board with the name as it's icon'''
        for queue_row in self.board:
            print list(map(lambda queue_col:queue_col.name if isinstance(queue_col,entity) else queue_col, queue_row))
        return True

class entity(object):
    def __init__(self, board, y, x, name, wait, fuel):
        self.y = y
        self.x = x
        self.name = name
        self.wait = wait
        self.board = board
        self.hasMoved = False
        self.stall = False
        self.fuel = fuel

    def printStatus(self):
        print "Name: "+self.name
        print "Location: "+str((self.y,self.x))
        print "Fuel: "+str(self.fuel)
        print "Decision: "+self.decision()
        print "Wait: "+str(self.wait)+'\n'
        
    def moved(self):
        self.hasMoved = not self.hasMoved
        
    def isResolved(self):
        ''''Queue is resolved if '''
        if self.x==self.board.size - 1 and self.wait <= 0:
            return True
        return False

    def isBeingResolved(self):
        '''returns bool if being resolved in last position in any lane'''
        if self.x==self.board.size - 1:
            self.wait -= 1
            return True
        return False
    
    def decision(self):
        '''simple greedy algorithm for switching queues'''
        if self.isResolved():return "None"
        elif self.canGoDown():return "down"
        elif self.canGoLeft():return "left"
        elif self.canGoRight():return "right"
        return "None"
    def decisionSplit(self):
        if self.isResolved():return "None"
        elif self.canGoDown():return "down"
        elif self.x % 2 == 0:return "left"
        elif self.canGoRight():return "right"
        return "None"
    
    '''methods to check position'''
    def canGoLeft(self):
        if self.board.get(self.y+1, self.x) == '.':return True
        return False
    def canGoRight(self):
        if self.board.get(self.y-1, self.x) == '.':return True
        return False
    def canGoUp(self):
        if self.board.get(self.y, self.x-1) == '.':return True
        return False
    def canGoDown(self):
        if self.board.get(self.y, self.x+1) == '.':return True
        return False
    
    '''move methods'''
    def moveLeft(self):#increments pos, subtracts fuel, and sets state to moved
        if self.canGoLeft():
            if self.fuel > 0:self.y+=1;self.fuel-=1;self.moved()
            return True
        return False
    def moveRight(self):
        if self.canGoRight():
            if self.fuel > 0:self.y-=1;self.fuel-=1;self.moved()
            return True
        return False
    def moveUp(self):
        if self.canGoUp():
            if self.fuel > 0:self.x-=1;self.fuel-=1;self.moved()
            return True
        return False
    def moveDown(self):
        if self.canGoDown():
            if self.fuel > 0:self.x+=1;self.fuel-=1;self.moved()
            return True
        return False
    
if __name__ == "__main__":
    #This program is used to model the queue likebehavior of turtlebots when
    #depositing material to a location
    #This is unlike a normal queue because gaps can form in a line, and other real
    #life attributes stop a real queue from forming
    from random import choice
    import string
    
    turtle_queue = QueueBoard(3, 10)

    #adding entities
    def turtle_scenario_normal(queue, counter):
        if counter == 0:#initial settings
            for i in range(queue.queues):
                for j in range(2):
                    queue.addEntity(i,j)
        if counter == 5 or counter == 10:#turn 5&10 stalled turtles will be added
            queue.addEntity(choice(range(queue.queues)),0,fuel=queue.size - choice(range(3,6)))

        #all other turns 2 turtles are added
        if counter % 2 == 0 or counter % 3 == 0:
            queue.addEntity(choice(range(queue.queues)),0)

    def turtle_scenario_merge(queue, counter):
        if counter == 0:#initial settings
            for i in range(queue.queues):
                for j in range(2):
                    queue.addEntity(i,j)
                    
            #stall turtles act as a wall forcing turtles to merge
            queue.addEntity(0,queue.size-1,fuel=0)
            queue.addEntity(0,queue.size-2,fuel=0)
            queue.addEntity(queue.queues-1,queue.size-1,fuel=0)
            queue.addEntity(queue.queues-1,queue.size-2,fuel=0)

        #all other turns 2 turtles are added
        if counter % 2 == 0 or counter % 3 == 0:
            queue.addEntity(choice(range(queue.queues)),0)

    counter = 0
    while counter != 100:
        turtle_scenario_normal(turtle_queue, counter)
        #turtle_scenario_merge(turtle_queue, counter)
        #turtle_queue.printBoard()
        #raw_input()
        print "Turn: "+str(counter)
        print "Processed: "+str(turtle_queue.entitiesProcessed)
        turtle_queue.excecuteEntityDecisions()
        turtle_queue.printBoard()
        counter+=1
        raw_input()
