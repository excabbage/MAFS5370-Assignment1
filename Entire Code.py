import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class State_Action:
    '''
    define state-action pair class, wich contains
    1.time
    2.wealth: For simplification, I will round the wealth so the wealth state is integer.
    3.action: Use integer 0 - 100 to representation 0%-100% respectively.
    4.hash function: map the state to an unique integer
    5.hash_a function: map the state-action pair to an unique integer
    6.is_end function: judge whether state reach the given terminal time
    '''
    
    time:int 
    wealth:int 
    action:int
    
    
    def __init__(self, time:int = 0, wealth:int = 100, action:int = 50):
        #initial is time zero, and wealth be 100 represents 100% of capital. Action is 50% of capital allocated into risky asset.
        self.time = time
        self.wealth = wealth
        self.action = action

    def hash(self) -> int :
        '''
        As t is between 0 and 10,
        so we map the state into number:
            hash = wealth * 11 + time.
        and we can recover it by
            time = hash % 11,
            wealth = (hash - time)/11
        '''
        return self.wealth * 11 + self.time
    
    def hash_a(self) -> int :
        '''
        As action is between 0 and 100, 
        so we make use of hash function and map the state-action pair into number:
            hash_a = hash * 101 + action.
        and we can recover it by
            action = hash_a % 101,
        '''
        return self.hash() * 101 + self.action
    
    def is_end(self, T:int) -> bool :
         #parameter T is the terminal time assigned outside the State_Action class. I will assign it in the following environment class.
         if self.time < T :
             return False
         else :
             return True
    
class environment:
    '''
    define the behaviour of riskfree asset and risky asset. Define the result of our allocation action. class contains
    1.a,b,p: the parameters of binomial distribution Y of risky asset return.
    2.r: riskfree interest rate.
    3.T: The terminal time of each episode.
    4.Y function: Distribution of risky asset return, in this case the distribution is binomial
    5.next_state function: To get the next_state with given state-action pair
    '''
    
    a:float 
    b:float
    p:float
    r:float
    T:int
    
    def __init__(self, a:float = 0.06, b:float = 0.04, p:float = 0.6,
                 r:float = 0.05,
                 T:int = 10):
        '''
        For some reason, I initial the parameters' values and solve only this case optimal strategy.
        1.riskfree interest rate = 0.05 = 5%
        2.distribution of risky asset return: Y_t = 0.06, prob=0.6, and 0.04, prob=0.4.
        3.Time period is fixed as 10
        '''
        self.a = a
        self.b = b
        self.p = p
        self.r = r
        self.T = T
    
    def Y(self) -> float :
        #Y is binomial distribution, with probability p to equal a, probability 1-p to equal b
        x = np.random.uniform(0,1)
        if x <= self.p :
            return self.a
        else :
            return self.b  
        
    def next_state(self, current_state_action:State_Action ) -> State_Action(int,int) :
        '''
        Given the State-action class as parameter,
        1.judge whether time is terminal,
        2.get the random result of the risky asset return,
        3.caculate the next wealth,
        4.return the next state using class form.
        '''
        #extract the state-action information from input class parameter
        t = current_state_action.time
        w = current_state_action.wealth
        action = current_state_action.action
        
        #1.judge whether time is terminal. If it is terminal, do nothing just return the current state. 
        if current_state_action.is_end(self.T):
            return current_state_action
            
        #2.get the random result of the risky asset return
        risky = self.Y()

        #3.caculate the next wealth
        next_w = action/100 * (1+risky) * w + (100-action)/100 * (1+self.r) * w 
        next_w = round(next_w,0) #For simplication, I constraint wealth as integer
        
        #4.return the next state using class form.
        return State_Action(t+1,next_w)

class TD0:
    '''
    The reinforcing learning algorithm, which contains:
    1.all_Q: #dynamically storage all the action values of visited state-action pairs. Index is hash_a() number
    2.visited: #dynamically storage the visited time for each pairs during the trail. It is used to caculate the step-size for each pairs.
    3.policy : #dynamically storage the greedy policy. Index is state hash() number
    4.player: the class environment(), telling TD0 algorithm the environment.
    5.epsilon: the parameter of epsilon greedy policy
    6.gamma: the paramter of discount return Gt = Rt+1 + gamma * Rt+2 + gamma^2 * Rt+3 + ....
    7.polic_update function: use all_Q to update the greedy policy pi(St) = argmax Q(St,a)
    8.get_action fucntion: use epsilon greedy policy to get action
    9.backup function: TD0 back up
    10.episode function: Do a trail, use TD0 method to update Q(s,a) and greedy policy, return the total change of Q
    '''
    all_Q = dict() 
    visited = dict() 
    policy = dict() 
    player = environment()
    epsilon = 0.5
    gamma = 0.99
          
    def policy_update(self, state_hash:int):
        '''
        Given the input state_hash integer, the function use self.all_Q to update the greedy action in the self.policy
        '''
        action = self.policy.get( state_hash , 50) #If there is no exist policy, initialize greedy action is 50% of captial allocated into risky asset
        Qvalue = self.all_Q.get( state_hash*101 + action , 0)# initialize action value. If the state-action pairs haven't been visited, the Qvalue is 0.
        for action_tmp in range(0,101): #get the greedy action
            Qvalue_tmp = self.all_Q.get( state_hash*101 + action_tmp , 0) #If the state-action pairs haven't been visited, the Qvalue——tmp is 0.
            if Qvalue < Qvalue_tmp:
                action = action_tmp
                Qvalue = Qvalue_tmp
        self.policy[ state_hash ] = action #update the greedy policy in the self.policy. There is no return of this function.
    
    def get_action(self, state_hash:int) -> int:
        '''
        Given the input state_hash integer, use epsilon greedy method to get action.
        return this action.
        '''
        if np.random.uniform(0,1) < self.epsilon : #with probability epsilon, randomly choose action in 0%-100%.
            action = np.random.uniform(0,100)
            action = round(action,0) #I set action be integer.
        else : #with probability 1-epsilon, choose greedy action from self.policy
            action = self.policy.get( state_hash , 50)#If the state haven't been visited, the initial action is 50.
        return action
    
    def backup(self, old_pair:int, new_pair:int, R:int) -> float:
        '''
        old_pair, new_pair are state-action pair hash_a number, which are used as index of self.all_Q.
        Use single step TD method to backup value function Q(s,a).
        Step-size is average step-size: 1/k, which comes from self.visited.
        Update the value Q(old_pair) in self.all_Q,
        return the absolute change of Q(old_pair) after updating.
        '''
        alpha = ( 1 / self.visited.get(old_pair,1) ) #step-size. Initial value is 1
        change = alpha * (R + self.gamma * self.all_Q.get(new_pair,0) - self.all_Q.get(old_pair,0))
        self.all_Q[old_pair] = self.all_Q.get(old_pair,0) + change #update the Q value in self.all_Q
        return np.abs(change)
    
    def episode(self) -> float:
        '''
        First generate the initial state, get its action.
        Then loop untill terminal state:
            update visited of old_pair
            update greedy policy,
            get new state and the reward,
            Q-learning method backup,
            use epsilon greedy policy to get new state's action
            update the state infomation.
        Return summation of all change of Q(old_pair) after hole episode.
        '''
        change = 0 #storage summation of all change of Q(s,a) after one episode of TD0 update.
        
        ### episode starting state, time=0, wealth=100
        old_pair = State_Action()
        ### get action for old state using epsilon greedy method
        old_pair.action = self.get_action(old_pair.hash())
        
        while not old_pair.is_end(self.player.T) :    
            ### update the visited value for state-action pair
            self.visited[old_pair.hash_a()] = 1 + self.visited.get(old_pair.hash_a(),0)
            
            ### use self.all_Q to update the greedy policy for old state
            self.policy_update(old_pair.hash())
            
            #### get the next state
            new_pair = self.player.next_state(old_pair)
            
            ### I use Q-learning method, so here I get greedy action for new state first.
            new_pair.action = self.policy.get( new_pair.hash() , 50)
            
            ### get reward. In this case, the reward is zero untill end of episode. At the end, the reward is Utility function of wealth
            if new_pair.is_end(self.player.T):
                R = (1 - math.exp(-new_pair.wealth/100))*100 #Utility function of wealth
            else :
                R = 0

            ### back up using Q-learning method, the input are two hash numbers. And stroage the change of Q value.
            change += self.backup(old_pair.hash_a(), new_pair.hash_a() ,R)

            ### After Q-learning backup, I now get the actual action of new state, using epsilon greedy method.
            new_pair.action = self.get_action(new_pair.hash())
            
            ### update the old_state
            old_pair = new_pair
        
        return change #Return summation of all change of Q(old_pair) after hole episode.


#######   assignment1 ###########
test = TD0()

for i in range(0,1000000):
    change = test.episode()
#    if change < 1e-5:
#        break

a = [[],[],[],[],[],[],[],[],[],[]] #storage the action. There are ten arrays respect to ten time periods
w = [[],[],[],[],[],[],[],[],[],[]] #storage the wealth. There are ten arrays respect to ten time periods
for key in test.policy:
    time = int(key%11)
    a[time]=np.append(a[time],test.policy[key])
    w[time]=np.append(w[time],(key-key%11)/11)
    #sort
    a[time] = a[time][np.argsort(w[time])]
    w[time] = np.sort(w[time])
# view the result of policy
for n in range(0,10):
    plt.plot(w[n],a[n],'o-',label='policy at time %d' % n)
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim([0,101])
plt.legend(loc=[1.05,0])

Q = [np.empty((len(w[0]),101)),np.empty((len(w[1]),101)),np.empty((len(w[2]),101)),
     np.empty((len(w[3]),101)),np.empty((len(w[4]),101)),np.empty((len(w[5]),101)),
     np.empty((len(w[6]),101)),np.empty((len(w[7]),101)),np.empty((len(w[8]),101)),
     np.empty((len(w[9]),101))] #storage the Q. There are ten arrays respect to ten time periods
for key in test.all_Q:
    time = int((key%1111-key%101)/101)
    for index in range(0,len(w[time])) :
        if w[time][index] == (key-key%1111)/1111 :
            break
    Q[time][index][int(key%101)] = test.all_Q[key]
for time in range(0,10) :
    a[time],w[time] = np.meshgrid(range(0,101),w[time])
# view the result of Q
for n in range(0,10):
    ax = plt.subplot(111,projection='3d')
    ax.scatter(w[n],a[n],Q[n])
    ax.set_zlim([0,100])
    ax.set_xlabel('wealth')
    ax.set_ylabel('action')
    ax.set_zlim([73,83])
    ax.set_zlabel('Q label')
    ax.view_init(elev=5,azim=30)
    
