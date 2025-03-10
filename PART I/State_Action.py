import numpy as np
import math

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
        
    def Y_test(self) -> float :
        #Y_test is normal distribution, used in the integral testing.
        x = np.random.normal(0.06,1)
        return x      
        
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
        #risky = self.Y_test() #used in the integral testing

        #3.caculate the next wealth
        next_w = action/100 * (1+risky) * w + (100-action)/100 * (1+self.r) * w 
        next_w = round(next_w,0) #For simplication, I constraint wealth as integer
        
        #4.return the next state using class form.
        return State_Action(t+1,next_w)
    
