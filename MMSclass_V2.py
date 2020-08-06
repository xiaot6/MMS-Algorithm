import numpy as np
import numpy.random as random
import random



class MMS:
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
        self.Allo = {}
        for i in range(agentNumber_):
            self.Allo[i] = []


    def normalize(self): #normalize
        for i in range(self.n):
            sum = 0.
            for j in range(self.m):
                sum += self.values[i][j]
            for j in range(self.m):
                self.values[i][j] = self.values[i][j] * (self.current_n) / sum

    def sortMMS_de(self): # sort in decreasing order
        self.values.sort(axis = 1)
        for i in range(self.n):
            self.values[i] = self.values[i][::-1]

    def sortMMS_in(self): # sort in increasing order
        self.values.sort(axis = 1)

def identical_ordinary_alpha_MMS(MMS,alpha): ## alpha-MMS allocation similar to bagfilling
    # toreturn = {} # to create a two-dimensional list which to store allocation results.
    i = MMS.n
    # while i > 0: #2d list start with empty.
    #     tmp = []
    #     toreturn.append(tmp)
    #     i -= 1
    MMS.normalize();
    MMS.sortMMS_de();
    prevbag = [] # this bag always has one least item than bag.
    bag = []
    bagvalue = 0.
    prebagvalue = 0.
    while MMS.current_n > 0 and MMS.current_m > 0: # if there is still agent/item in the system unassigned;
        for j in range(MMS.m): #loop of item
            if (j not in MMS.FilledItem) and (j not in bag):
                bag.append(j) #bag will put the items that haven't assigned
                for i in range(MMS.n): #loop of agent
                    if i not in MMS.Filledagent:
                        for x in bag:
                            bagvalue += MMS.values[i][x]
                        for y in prevbag:
                            prebagvalue += MMS.values[i][y]
                        if bagvalue > alpha and prebagvalue <= alpha and len(prevbag) != 0: # get upper the limit and put the
                            MMS.Allo[i] += prevbag;
                            MMS.current_n -= 1
                            MMS.current_m -= len(prevbag)
                            MMS.Filledagent.append(i)
                            for item in prevbag:
                                MMS.FilledItem.append(item)
                                MMS.values[i][item] = 0.
                            prevbag = []
                            bag = []
                            prebagvalue = 0.
                            bagvalue = 0.
                            MMS.normalize()
                            break
                        else:
                            bagvalue = 0.
                            prebagvalue = 0.
                            prevbag = []
                            for z in bag:
                                prevbag.append(z)
            if (len(MMS.FilledItem + bag) == MMS.m) and (len(bag) != 0):
                for i in range(MMS.n): #loop of agent
                    if i not in MMS.Filledagent:
                        MMS.Allo[i] += bag;
                        # print(i, prevbag)
                        MMS.current_n -= 1
                        MMS.current_m -= len(prevbag)
                        MMS.Filledagent.append(i)
                        for item in prevbag:
                            MMS.FilledItem.append(item)
                            MMS.values[i][item] = 0.
                        # s ='MMS.FilledItem'
                        # print(s,MMS.FilledItem)
                        prevbag = []
                        bag = []
                        prebagvalue = 0.
                        bagvalue = 0.
                        MMS.normalize()
                        return MMS.Allo
    return MMS.Allo


if __name__ == '__main__':
    example= MMS(5,40)
    x = identical_ordinary_alpha_MMS(example, 11./9.)
    print(x)
    print('hello world')
