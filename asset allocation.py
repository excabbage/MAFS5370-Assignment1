import numpy as np
import math
import matplotlib.pyplot as plt

class State_Action:
    '''
    define state-action pair class, wich contains
    1.time
    2.wealth: For simplification, the wealth state is integer.
    3.action: Use integer 0 - 100 to representation 0%-100%
    4.hash function: map the state to an unique integer
    5.hash_a function: map the state-action pair to an unique integer
    6.is_end function: judge whether state reach the given terminal time
    '''
    
    time:int 
    wealth:int 
    action:int
    
    #initial is time zero, and wealth be 100 represents 100% of capital. Action is 0% of risky.
    def __init__(self, time:int = 0, wealth:int = 100):
        self.time = time
        self.wealth = wealth
        self.action = 0


    def hash(self) -> int :
        '''
        As t is between 0 and 10,
        so we map the state-action pair into number:
            hash = wealth * 11 + time.
        and we can recover it by
            time = hash % 11,
            wealth = (hash - time)/11
        '''
        return self.wealth * 11 + self.time
    
    def hash_a(self) -> int :
        '''
        As action take value in 0-100, 
        so we make use of hash function
            hash_a = hash * 101 + action.
        and we can recover it by
            action = hash_a % 101,
        '''
        if self.wealth >= 0 :
            return self.wealth * 1000000 + self.time * 1000 + self.action
        else :
            return self.wealth * 1000000 - self.time * 1000 - self.action
    
    def is_end(self, T:int) -> bool : #parameter T is the terminal time
         if self.time < T :
             return False
         else :
             return True
    
class play:
    '''
    define the action process, wich contains
    1.a,b,p: the parameters of binomial distribution Y.
    2.r: riskless rate
    3.T: The terminal time
    4.Y function: Distribution of risky asset, in this case the distribution is binomial
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
        
#    def Y_test(self) -> float :
#        #Y_test is normal distribution, use to test the integral test.
#        x = np.random.normal(0.06,1)
#        return x      
        
    def next_state(self, current_state_action:State_Action ) -> State_Action(int,int) :
        '''
        Given the State and the action, first judge whether time is terminal.
        Than get the random result of the risky asset return.
        Finally, caculate the next wealth, and return the next state's hash value.
        '''
        t = current_state_action.time
        w = current_state_action.wealth
        action = current_state_action.action
        
        if current_state_action.is_end(self.T): #Judge whether current time is terminal
            return current_state_action
        
        risky = self.Y() #the next time, risky asset's return
        #risky = self.Y_test() #Use in integral test
        next_w = action/100 * (1+risky) * w + (100-action)/100 * (1+self.r) * w #the next state wealth
        next_w = round(next_w,0) #For simplication, we make wealth be integer
        #return the hash value of next state.
        return State_Action(t+1,next_w)
    
'''
Integration Testing: test State_Action and play class working well.
test=State_Action(1,200)
#Its value should be time=1, wealth=200, visited=0, value=0
test.action = 20
#Its value should be action=20
test1 =play()
test2 = test1.next_state(test)
#test2 is a hash value, wich value should be 209002000 or 212002000.
'''

class TD0:
    '''
    The reinforcing learning algorithm, which contains:
    1.all_Q: #storage all the action values of visited state-action pairs. Index is hash_a() number
    2.visited: #storage the visited time for each pairs during the trail. It is used to get the step-size 1/k. Index is hash_a() number.
    3.policy : #storage the greedy policy. Index is state hash() number
    4.player: the class play(), telling TD0 algorithm how to run the action process.
    5.epsilon: the parameter of epsilon greedy policy
    6.gamma: the paramter of discount return Gt = Rt+1 + gamma * Rt+2 + gamma^2 * Rt+3 + ....
    7.polic_update function: to get greedy policy
    8.get_action fucntion: use epsilon greedy policy to get action
    9.backup function: TD0 back up
    10.episode function: Do a trail, use TD0 method to update Q(s,a) and greedy policy, return the total change of Q
    '''
    
    all_Q = dict() 
    visited = dict() 
    policy = dict() 
    player = play()
    epsilon = 0.1
    gamma = 1
          
    def policy_update(self, state_hash:int):
        '''
        Given the input state_hash integer, the function update the greedy action in the self.policy
        '''
        action = 0 #initialize greedy action is 0% of risky
        value = self.all_Q.get( state_hash + action , 0)# if we have visited this state-action, initialize value as its value, else as 0.
        for a in range(1,101): #get the greedy action
            value_a = self.all_Q.get( state_hash + a , 0)
            if value < value_a:
                action = a
                value = value_a
        self.policy[ state_hash ] = action
    
    def get_action(self, state_hash:int) -> int:
        '''
        Given the input state_hash integer, use epsilon greedy method to get action.
        '''
        if np.random.uniform(0,1) < self.epsilon : #with probability epsilon, randomly choose action in 0%-100%.
            action = np.random.uniform(0,100)
            action = round(action,0)
        else : #with probability 1-epsilon, choose greedy action from self.policy
            action = self.policy.get( state_hash , 0)
        return action
    
    def backup(self, old_pair:int, new_pair:int, R:int) -> float:
        '''
        old_pair, new_pair are state-action pair hash number, which is index of self.all_Q.
        Use TD0 method to backup value function Q(s,a). Step-size is average step-size: 1/k.
        Return the difference of Q(old_pair) after updating.
        '''
        change = (1/self.visited[old_pair]) * (R + self.gamma * self.all_Q.get(new_pair,0) - self.all_Q.get(old_pair,0))
        self.all_Q[old_pair] = self.all_Q.get(old_pair,0) + change
        return np.abs(change)
    
    def episode(self) -> float:
        '''
        First generate the initial state, get its action, and increase its visited.
        Then loop untill terminal state:
            update greedy policy,
            get new state and its action, and the reward,
            backup,
            update the state infomation.
        '''
        change = 0 # the total change of Q(s,a) after one episode of TD0 update.
        
        ### episode starting state
        old_pair = State_Action()
        ### get action for old state using epsilon greedy method###
        old_pair.action = self.get_action(old_pair.hash())
        ### update the visited value #####
        self.visited[old_pair.hash_a()] = 1 + self.visited.get(old_pair.hash_a(),0)
        
        while not old_pair.is_end(self.player.T) :    
            ### update the greedy policy for old state ####
            self.policy_update(old_pair.hash())
            
            #### get the next state #####
            new_pair = self.player.next_state(old_pair)
            
            ### get action for new state using epsilon greedy method###
            new_pair.action = self.get_action(new_pair.hash())
            
            ### get reward. In this case, the reward is zero untill end of episode.
            if new_pair.is_end(self.player.T):
                R = (1 - math.exp(-new_pair.wealth/100))*100 #Utility function
            else :
                R = 0

            ### back up using TD(0) , the input are two hash numbers ####
            change += self.backup(old_pair.hash_a(), new_pair.hash_a() ,R)
            
            ### update the old_state ###
            old_pair = new_pair
            self.visited[old_pair.hash_a()] = 1 + self.visited.get(old_pair.hash_a(),0)
        
        return change

'''
Integration Testing: test the TD0 working well.
I use normal distribution of risky return to test the output policy.
As referred in text book 'Fouundatoins of Reinforcement Learning with Applications in Finance', 
the policy is independent to wealth:
    xt = (mu - r)/( sigma^2 * 100 * (1+r)^(T-t-1) ) 
which are all closed to 0
From the test we can see the median of the xt with respect to wealth are close to zero, and 3/4 quantile are about 10%
'''
            
#######   assignment1 ###########
test = TD0()
for i in range(0,1000000):
    change = test.episode()
    if np.abs(change) < 1e-5 and np.abs(change) > 0:
        break
    
p = test.policy
x0 = []
w0 = []
for key in p:
    if np.abs(key)%1000000 == 0000 :
        x0=np.append(x0,p[key])
        w0=np.append(w0,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w0,x0,'o')

x1 = []
w1 = []
for key in p:
    if np.abs(key)%1000000 == 1000 :
        x1=np.append(x1,p[key])
        w1=np.append(w1,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w1,x1,'o')

x2 = []
w2 = []
for key in p:
    if np.abs(key)%1000000 == 2000 :
        x2=np.append(x2,p[key])
        w2=np.append(w2,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w2,x2,'o')

x3 = []
w3 = []
for key in p:
    if np.abs(key)%1000000 == 3000 :
        x3=np.append(x3,p[key])
        w3=np.append(w3,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w3,x3,'o')

x4 = []
w4 = []
for key in p:
    if np.abs(key)%1000000 == 4000 :
        x4=np.append(x4,p[key])
        w4=np.append(w4,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w4,x4,'o')

x5 = []
w5 = []
for key in p:
    if np.abs(key)%1000000 == 5000 :
        x5=np.append(x5,p[key])
        w5=np.append(w5,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w5,x5,'o')

x6 = []
w6 = []
for key in p:
    if np.abs(key)%1000000 == 6000 :
        x6=np.append(x6,p[key])
        w6=np.append(w6,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w6,x6,'o')

x7 = []
w7 = []
for key in p:
    if np.abs(key)%1000000 == 7000 :
        x7=np.append(x7,p[key])
        w7=np.append(w7,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w7,x7,'o')

x8 = []
w8 = []
for key in p:
    if np.abs(key)%1000000 == 8000 :
        x8=np.append(x8,p[key])
        w8=np.append(w8,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w8,x8,'o')

x9 = []
w9 = []
for key in p:
    if np.abs(key)%1000000 == 9000 :
        x9=np.append(x9,p[key])
        w9=np.append(w9,np.sign(key)*(np.abs(key)-np.abs(key)%1000000)/1000000)
plt.plot(w9,x9,'o')
