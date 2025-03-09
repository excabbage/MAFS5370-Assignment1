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
        return self.hash() * 101 + self.action
    
    def is_end(self, T:int) -> bool : #parameter T is the terminal time
         if self.time < T :
             return False
         else :
             return True
