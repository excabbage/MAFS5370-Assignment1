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
