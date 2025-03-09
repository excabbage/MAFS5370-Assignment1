# MAFS5370-Assignment1
Group member: Li,Zhiyan

Abstract: The case is discrete-Time asset allocation between one rikfree asset and one risky asset. There are $T=10$ time perids and risky asset has single-time return as $Y_t$= $a$, prob= $p$, and $b$, prob= $(1-p)$. I use time $t$ and wealth $W_t$ to be the state $s_t=\\{t,W_t\\}$, and propotion of risky asset allocation to be action $a(s_t)$. To simplify the case, I discretize the wealth and action. For some reason, I fix the parameters' values, set initial wealth $W_0=100$, $p=0.6$, $a=0.06$, $b=0.04$ ,riskfree interest rate $r=0.05$. I use TD(0) Q-learning method to find the Q function and optimal strategy in this special case.

## 1 Discrete-Time asset allocation is MDP
### 1.1 The defination of reward
The reward is the Utility of Consumption of Money extracted from allocation. In this case, one don't extract any money until the end of time, and extract all the money at the end,

$$R_t=0 \quad, t \in [1,9]$$
$$R_t=U(W_t)=100(1-e^{-\frac{W_t}{100}}) \quad,t=10$$

where $U(W_t)$ is Utility function.


### 1.2 Proof it is MDP
Because the reward $R_t$ is definite given $s_t$, so 

$$P(s_{t+1},R_{t+1}|F_t)=P(s_{t+1}|F_t)$$

By defination of $s_t$, it equals to

$$=P(t+1,W_{t+1}|F_t)=P(W_{t+1}|F_t)$$

And $W_{t+1}$ is obtained from the return of riskfree asset and risky asset, it equals to

$$=P(W_t * (1+(1-A_t )*r+A_t * Y_t )|F_t )$$

Use identical function $\mathbb{1}$ to change probability into expectatoin, it equals to

$$=E[\mathbb{1}_{W_t * (1+(1-A_t )*r+A_t * Y_t )} |F_t ]$$

Because it is a constant under all the past condition, so one can take expectation under condition $s_t ,A_t $. Then apply tower property, it equals to

$$=E[ E[ \mathbb{1}_{W_t * (1+(1-A_t )*r+A_t * Y_t )} |F_t ] |s_t,A_t  ]$$

$$=E[ E[ \mathbb{1}_{W_t * (1+(1-A_t )*r+A_t * Y_t )} |s_t,A_t ] |F_t ]$$

Admit that $\{ Y_t \}$ is i.i.d., so the inside expectation is determined without randomness, one can remove the outside expectation

$$=E[\mathbb{1}_{W_t * (1+(1-A_t )*r+A_t * Y_t )} |s_t,A_t ]$$

Backward similarly, it equals to

$$=P(s_{t+1},R_{t+1}|s_t,A_t)$$

## 2 Part I: Define the environment model
To simplify the case, I discretize the wealth and action. $W_t$ is roud into integer. Action is integer between 0 and 100. (i.e. $a_t=24$ means 24% of wealth allocated into riksy asset at time t.)

Define the hash function. It maps the state-- time and wealth-- into integer one-to-one by

$$hash(t,W_t) = W_t * 11 + t \quad, t\in [0,10]$$

Define the hash_a function. It maps the state action pairs into integer one-to-one by

$$hash_a(t,W_t,a_t) = hash(t,W_t) * 101 + a_t \quad,a_t \in [0,100]$$

Then I specify the riskfree interest rate, $r=0.05$. And distribution of risky asset return is $Y_t=0.06$, prob= $0.6$, and $0.04$, prob= $0.4$. The reward of each action is 

$$R_t=0 \quad, t \in [1,9]$$
$$R_t=U(W_t)=100(1-e^{-\frac{W_t}{100}}) \quad,t=10$$

where $U(W_t)$ is Utility function.

## 3 Part II: Define TD(0) method
Initialize $A_t = 50, \forall s_t$, and $Q(S_t,A_t) = 0, \forall S_t,A_t$.

Repeat(for each episode):

-Initialize $S_t=\\{ t=0,W_t=100\\} $

--Repeat (for each step of episode):

--Choose $A_t$ from $S_t$ using epsilon-greedy policy, I set epsilon be 0.2.

--Take action $A_t$, observe reward $R_{t+1}$ and new state $S_{t+1}$

--back up the action value Q, where $\alpha = 0.9$ and $\gamma = 0.9$

$$Q^{new}(S_t,A_t) = Q^{old}(S_t,A_t) + \alpha * (R_{t+1} +\gamma *\max\limits_{a}Q^{old}(S_{t+1},a) - Q^{old}(S_t,A_t))$$

--update the State: $S_t=S_{t+1}$

-until $S_t$ is terminal
