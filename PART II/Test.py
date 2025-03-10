####Unit Testing
'''

'''








'''
Integration Testing: test the TD0 working well.
I use normal distribution of risky return to test the output policy.
As referred in text book 'Fouundatoins of Reinforcement Learning with Applications in Finance', 
the policy is independent to wealth:
    xt = (mu - r)/( sigma^2 * 100 * (1+r)^(T-t-1) ) 
which are all closed to 0
From the test we can see the median of the xt with respect to wealth are close to zero, and 3/4 quantile are about 10%
'''
            
