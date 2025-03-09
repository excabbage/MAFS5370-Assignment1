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
        As t is not greater than 99,
        so we map the state-action pair into number:
            hash = wealth , time , 000.
        '''
        if self.wealth >= 0 :
            return self.wealth * 1000000 + self.time * 1000
        else :
            return self.wealth * 1000000 - self.time * 1000
    
    def hash_a(self) -> int :
        '''
        As action take value in 0-100, not greater than 999,
        so
            action_hash = wealth , time , action = hash + action.
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
