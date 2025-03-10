class TD0:
    '''
    The reinforcing learning algorithm, which contains:
    1.all_Q: #storage all the action values of visited state-action pairs. Index is hash_a() number
    2.visited: #storage the visited time for each pairs during the trail. It is used to caculate the step-size for each pairs.
    3.policy : #storage the greedy policy. Index is state hash() number
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
        action = 50 #initialize greedy action is 50% of captial allocated into risky asset
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
        First generate the initial state, get its action, and increase its visited.
        Then loop untill terminal state:
            update greedy policy,
            
            get new state and its action, and the reward,
            backup,
            
            update the state infomation.
        Return summation of all change of Q(old_pair) after hole episode.
        '''
        change = 0 #storage summation of all change of Q(s,a) after one episode of TD0 update.
        
        ### episode starting state, time=0, wealth=100
        old_pair = State_Action()
        ### get action for old state using epsilon greedy method
        old_pair.action = self.get_action(old_pair.hash())
        ### update the visited value for state-action pair
        self.visited[old_pair.hash_a()] = 1 + self.visited.get(old_pair.hash_a(),0)
        
        while not old_pair.is_end(self.player.T) :    
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
            
            ### update the old_state, and visited times
            old_pair = new_pair
            self.visited[old_pair.hash_a()] = 1 + self.visited.get(old_pair.hash_a(),0)
        
        return change #Return summation of all change of Q(old_pair) after hole episode.
