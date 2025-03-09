# MAFS5370-Assignment1
TD(0) Solve Discrete-Time Asset Allocation

Group member: Li,Zhiyan

Abstract: The Discrete-Time asset allocation between one rikfree asset and one risky asset. There are $T=10$ time perids and risky asset has single-time return as $Y_t$= $a$, prob= $p$, and $b$, prob= $(1-p)$. I use time $t$ and wealth $W_t$ to be the state $s(t,W_t)$, and propotion of risky asset allocation to be action $a(s(t,W_t))$. To simplify the case, I discretize the wealth and action. And set initial wealth $W_0=100$, $p=0.6$, $a=0.06$, $b=0.04$ ,riskfree interest rate $r=0.05$. I use TD(0) sarsa method to find the optimal Q function and strategy.
