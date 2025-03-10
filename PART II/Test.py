####Unit Testing
'''
Test TD0 class:
1.test policy_update function: Because policy and all_Q storage the data dynamically, I test 4 situation. 
    There is neither policy data nor all_Q data of state: time=1, wealth=100, for all action.
    There is policy data of state: time=2, wealth=100, no all_Q data of pairs: time=2, wealth=100, for all action.
    There is no policy data of state: time=4, wealth=100, there is all_Q data of pairs: time=4, wealth=100, action=30.
    There is both policy data and all_Q data of state: time=6, wealth=100, action=50 or 80.
  running policy_update functiion for this four situation,
  The results of print(test.policy) should be 1101:50, 1102:25, 1104:30, 1106:80
2.test get_action function: Using the above test data, I test 2 situation: Whether there is policy data of input state.
    There is no policy data of state: time=10, wealth=100.
    There is policy data of state: time=6, wealth=100.
  running get_action functiion for this two situation,
  The result of first situation should be 50.5% probability of 50, 0.5% probability of 0~100 except 50.
  The result of second situation should be 50.5% probability of 80, 0.5% probability of 0~100 except 80.
3.test backup function:
4.test episode function:
'''
#1:The results of print(test.policy) should be 1101:50, 1102:25, 1104:30, 1106:80
test = TD0()
test.policy[100*11+2] = 25
test.policy[100*11+6] = 75
test.all_Q[100*1111+4*101+30] = 20
test.all_Q[100*1111+6*101+80] = 30
test.all_Q[100*1111+6*101+50] = 0
test.policy_update(100*11+1)
test.policy_update(100*11+2)
test.policy_update(100*11+4)
test.policy_update(100*11+6)
print(test.policy)

#2:
result = np.zeros(1000)
for i in range(0,1000): # run 1000 times to approximate the probability.
  result[i] = test.get_action(100*11+10) # first situation
plt.hist(result) #The result of first situation should be 50.5% probability of 50, 0.5% probability of 0~100 except 50.
for i in range(0,1000):
  result[i] = test.get_action(100*11+6) # second situation
plt.hist(result) #The result of second situation should be 50.5% probability of 80, 0.5% probability of 0~100 except 80.

#3:



####Integration Testing:
'''
test the TD0 working well.
I use normal distribution of risky return to test the output policy.
As referred in text book 'Fouundatoins of Reinforcement Learning with Applications in Finance', 
the policy is independent to wealth:
    xt = (mu - r)/( sigma^2 * 100 * (1+r)^(T-t-1) ) 
which are all closed to 0
From the test we can see the median of the xt with respect to wealth are close to zero, and 3/4 quantile are about 10%
'''
            
