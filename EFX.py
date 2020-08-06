import numpy as np
import numpy.random as random
import copy
import queue

class EFX:
    '''
    algorithm 1 and 2 for paper https://arxiv.org/abs/1907.04596
    A little charity Grarantees ALmost Envy-Freeness
    '''
    def __init__(self, agentNumber_, itemNumber_, values_ = None):
        self.n = agentNumber_;
        self.m = itemNumber_;
        self.current_n = agentNumber_; # will decrease during allication
        self.current_m = itemNumber_;
        if values_ == None: # if not take the values, we will randomly generate the values.
            self.values = np.zeros((agentNumber_,itemNumber_))
            for i in range(agentNumber_):
                for j in range(itemNumber_):
                    self.values[i][j] = float(random.randint(0,100))
        else: # else take the values from constructor
            self.values = values_
        self.Filledagent = [] # a list to store the index of those agent who has assigned
        self.FilledItem = []# a list to store the index of those assigned items
        self.P  = []
        for i in range(itemNumber_):
            self.P.append(i)
        self.Allo = {}
        for i in range(agentNumber_):
            self.Allo[i] = []
        self.Matrix = []
        self.dictReach = {}
        for i in range(agentNumber_):
            self.dictReach[i] = []
        self.source = []

    # def copy(self):


    def getValue(self,agent,owner = -1):
        '''
        agent and owner should be int, which is their id Number.
        This function is to get the sum of agent's value for one owner's items,
        The agent can be the same or different as the owner
        '''
        if owner == -1:
            owner = agent
        sum = 0;
        if len(self.Allo[owner]) == 0:
            return 0
        for i in self.Allo[owner]:
            sum += self.values[agent,i]
        return sum

    def getValue_without(self,agent,owner,item2ignore):
        '''
        this is to get the value of agent's valuation of owner's items if owner
        do not have the item 2 item2ignore
        '''
        if len(self.Allo[owner]) == 0:
            return 0
        sum = 0
        for i in self.Allo[owner]:
            if i != item2ignore:
                sum += self.values[agent,i]
        return sum

    def getValue_P(self,agent):
        '''
        to get the value of  P(the charity part) form agent's view
        '''
        sum = 0
        for i in self.P:
            sum += self.values[agent,i]
        return sum

    def AssignItem(self, agent, item):
        '''
        Assign item to agent
        if betweenagents == True: assign the item from one agent to another agnent
                P do not change
        if betweenagents == False: P will decrease
        '''
        self.Allo[agent].append(item)
        if item in self.P:
            self.P.remove(item)

    def DeleteItem(self, agent, item, bwtagents = False):
        '''
        to delete one item agent to this agent
        '''
        if item not in self.Allo[agent]:
            print("No item to delete")
            return
        self.Allo[agent].remove(item)
        if bwtagents == False:
            self.P.append(item)

    def ifEnvy(self, agent_i, agent_j):
        '''
        this function is to see if agent_i envy agent_j
        return a boolean
        '''
        if (self.getValue(agent_i, agent_j) > self.getValue(agent_i)):
            return True
        return False

    def ifEFX(self, agent_i, agent_j):
        '''
        return a boolean
        agent_i may envy agent_j,
        however this envy would vanish
        as soon as any good is removed from Xj
        return true: when no more evey exist after any removal
        return false: when envy still exist after any removal
        (differnt from self.ifEnvy
        '''
        if agent_i == agent_j:
            return True
        if self.ifEnvy(agent_i, agent_j) == False:
            return True
        agent_i_selfvalue = self.getValue(agent_i)
        for i in self.Allo[agent_j]:
            if agent_i_selfvalue < self.getValue_without(agent_i,agent_j,i):
                return False
        return True

    def ifEFX_system(self):
        '''
        "ifCondition1"
        to check if the whole allocation are EFX
        (frist condition on page2 https://arxiv.org/abs/1907.04596)
        '''
        for i in range(self.n):
            for j in range(self.n):
                if self.ifEFX(i,j) == False:
                    return False
        return True


    def ifCondition2(self):
        '''
        to check if vi(Xi) >= vi(P) for all agents i
        (second condition on page2 https://arxiv.org/abs/1907.04596)
        '''
        for i in range(self.n):
            if self.getValue(i) < self.getValue_P(i):
                return False
        return True

    def ifCondition3(self):
        '''
        to check if |p| < n
        (Third condition on page2 https://arxiv.org/abs/1907.04596)
        '''
        if len(self.P) < self.n:
            return True
        else:
            return False

    def ifAllcondition(self):
        '''to check if satisfy all three conditons on
        page2 https://arxiv.org/abs/1907.04596
        '''
        return self.ifEFX_system() and self.ifCondition3() and self.ifCondition2()


    def IfStillEFX(self, agent, item):
        '''
        to see if we assin the item in P to agent here,
        would the system still be a EFX system.
        return a boolean
        helper function of "UpdateRule_0"
        '''
        back_Allo = copy.deepcopy(self.Allo)
        backup_P = copy.deepcopy(self.P)
        self.AssignItem(agent,item) # assign not bwt agents
        if self.ifEFX_system() == True:
            self.Allo = copy.deepcopy(back_Allo)
            self.P = copy.deepcopy(backup_P)
            return True
        else:
            self.Allo = copy.deepcopy(back_Allo)
            self.P = copy.deepcopy(backup_P)
            return False

    def UpdateRule_0(self):
        '''
        (Algorithm 2, function 0 on page8 https://arxiv.org/abs/1907.04596)
        if an item in P to assign to agent i, the system is still EFX,
        then assign
        '''
        print(self.P)
        for i in range(self.n): #agent i
            for j in self.P: #item j
                if self.IfStillEFX(i,j) == True:
                    self.AssignItem(i,j)
                    # break

    def ifUpdateRule_0(self):
        '''
        if UpdateRule_0.applicable： True
        '''
        for i in range(self.n): #agent i
            for j in self.P: #item j
                if self.IfStillEFX(i,j) == True:
                    return True

    def getKx(self, agent_i):
        '''
        helper function of UpdataRule_1
        to find what is the smallest size of of package in P that vi(Z) > vi(Xi)
        '''
        if self.getValue_P(agent_i)<= self.getValue(agent_i):
            print("getKx if not working")
            return None
        vp = [] # a list to store the values of agent_i to P
        for x in self.P:
            vp.append(self.values[agent_i,x])
        tmpvalue = 0.
        Z = [] # the bag to return, include the index of items
        while tmpvalue <= self.getValue(agent_i):
            currentmax = vp.index(max(vp))
            Z.append(self.P[currentmax])
            tmpvalue += max(vp)
            vp[currentmax] = -1
        return Z

    def UpdataRule_1(self):
        '''
        (Algorithm 2, function 1 on page8 https://arxiv.org/abs/1907.04596)
        if vi(P) > vi(Xi)
        let Z be the smallest size of of package in P that vi(Z) > vi(Xi)
        Then change Xi = Z
        '''
        for agent_i in range(self.n):
            if self.getValue_P(agent_i)> self.getValue(agent_i):
                back_Allo = copy.deepcopy(self.Allo)
                backup_P = copy.deepcopy(self.P)
                Z = self.getKx(agent_i)
                for i in range(len(self.Allo[agent_i])):
                    self.P.append(self.Allo[agent_i][i])
                self.Allo[agent_i] = Z
                for i in range(len(Z)):
                    self.P.remove(Z[i])
                if self.ifEFX_system() == False:
                    self.Allo = copy.deepcopy(back_Allo)
                    self.P = copy.deepcopy(backup_P)
                else:
                    return


    def ifUpdataRule_1(self):
        '''
        if UpdateRule_1.applicable： True
        '''
        for agent_i in range(self.n):
            if self.getValue_P(agent_i)> self.getValue(agent_i):
                return True


    def BuildReachableMatrix(self):
        '''
        self.Matrix: build a n*n matrix where is i in row envy j in column, [i,j]would be true:
        self.dictReach: a dictionary form to store the matrix
        self.source: to know which agent is one of reachable source
        '''
        visited = []
        for i in range(self.n):
            self.Matrix.append([])
            visited.append([])
        for i in range(self.n):
            for j in range(self.n):
                self.Matrix[i].append(False)
                visited[i].append(False)
        for i in range(self.n):
            for j in range(self.n):
                if self.ifEnvy(i,j):
                    self.Matrix[i][j] = True
                    self.dictReach[i].append(j)
                    if j not in self.source:
                        self.source.append(j)



    def isReachable(self,agent_i,agent_j):
        '''
        if isReachable form agent_i to agent_j
        '''
        self.BuildReachableMatrix()
        # Create a queue for BFS
        queue=[]
        # Mark the source node as visited and enqueue it
        visited = []
        for i in range(self.n):
            visited[i].append(False)
        queue.append(agent_i)
        visited[agent_i] = True
        while queue:#q is not empty
            #Dequeue a vertex from queue
            n = queue.pop(0)
            # If this adjacent node is the destination node,
            # then return true
            if self.Matrix[n,agent_j] == True:
                 return True
            #  Else, continue to do BFS
            for i in self.dictReach[n]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        return False

    def findmostenvy(self):
        '''
        find the most envious agent
        '''
        min = self.m
        mostenvy = -1 #most envy agent
        for i in range(self.n):
            if self.getKx(i) != None:
                if len(self.getKx(i)) < min:
                    min = len(self.getKx(i))
                    mostenvy = i
        return mostenvy

    def IfUpdataRule_2(self):
        '''
        (Algorithm 2, function 2 on page8 https://arxiv.org/abs/1907.04596)
        '''
        Pn = len(self.P)
        Sn = len(self.source)
        if Pn < 1:
            return False
        if Sn < 1:
            return False
        if self.n <= 1:
            return False
        if self.findmostenvy in self.source:
            return True
        return False
    def UpdataRule_2(self):
        '''
        (Algorithm 2, function 2 on page8 https://arxiv.org/abs/1907.04596)
        '''
        Pn = len(self.P)
        Sn = len(self.source)
        if Pn < 1:
            return False
        if Sn < 1:
            return False
        if self.n <= 1:
            return False
        L = min(Pn,Sn,self.n)
        if self.findmostenvy in self.source:
            Z = self.getKx(self.findmostenvy)
            if self.P[self.findmostenvy] not in self.P[L-1:]:
                self.P =self.Allo[self.findmostenvy].remove(Z) + self.P[L-1:] + self.P[self.findmostenvy]
            else:
                self.P =self.Allo[self.findmostenvy].remove(Z) + self.P[L-1:]
            self.Allo[self.findmostenvy] = Z

    def algorithm1(self):
        '''
        algorithm 1
        '''
        while self.ifUpdateRule_0() or self.ifUpdataRule_1() or self.IfUpdataRule_2():
            if self.ifUpdateRule_0():
                self.UpdateRule_0()
            if self.ifUpdataRule_1():
                self.UpdataRule_1()
            if self.IfUpdataRule_2():
                self.UpdataRule_2()







if __name__ == '__main__':
    example= EFX(5,10)
    print(example.Allo)
    # print(example.Allo)
    example.algorithm1()
    # example.UpdataRule_1()
    # example.UpdataRule_2()
    # example.BuildReachableMatrix()
    # print(example.Matrix)
    # print(example.source)
    print(example.Allo)
    print(example.ifAllcondition())
    print("hello world")
