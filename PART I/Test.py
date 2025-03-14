#### Unit Test
'''
Test State_Action:
1.test initial function: If print(test.time,test.wealth,test.action), result should be 0,100,50 respectively
2.test hash function: The hash value should be wealth * 11 + time = 1100
3.test hash_a function: The hash_a value should be 1100 * 101 + action = 111150
4.test is_end function: Test using Terminal time as 4,10,0 respectively, result should be False,False,True respectively. Because the initial time value is 0
5.change time and wealth value: Change the time=8, wealth=-40, action=10, If print(test.time,test.wealth,test.action), result should be 8,-40,10 v
6.test hash function again: The hash value should be wealth * 11 + time = -432
7.test hash_a function again: The hash_a value should be -432 * 101 + action = -43622
8.test is_end function again: Test using Terminal time as 4,10,0 respectively, result should be True,False,True respectively.
9.test initial funcion with assign parameter: initial the parameter as time=4,wealth=25. If print(test.time,test.wealth,test.action), result should be 4,25,50 respectively
10.test hash function again: The hash value should be wealth * 11 + time = 279
11.test hash_a function again: The hash_a value should be 279 * 101 + action = 28229
12.test is_end function again: Test using Terminal time as 4,10,0 respectively, result should be True,False,True.
'''
#1:result should be 0,100,50 respectively
test = State_Action()
print(test.time,test.wealth,test.action)

#2:result should be 1100
print(test.hash())

#3:result should be 111150
print(test.hash_a())

#4:result should be False,False,True respectively
print(test.is_end(4),test.is_end(10),test.is_end(0))

#5:result should be 8,-40,10 respectively
test.time=8
test.wealth=-40
test.action=10
print(test.time,test.wealth,test.action)

#6:result should be -432
print(test.hash())

#7:result should be -43622
print(test.hash_a())

#8:result should be True,False,True respectively
print(test.is_end(4),test.is_end(10),test.is_end(0))

#9:result should be 4,25,50 respectively
test = State_Action(4,25)
print(test.time,test.wealth,test.action)

#10:result should be 279
print(test.hash())

#11:result should be 28229
print(test.hash_a())

#12:result should be True,False,True respectively
print(test.is_end(4),test.is_end(10),test.is_end(0))


'''
Test environment
1.test initial function: If print(test.a,test.b,test.p,test.r,test.T), result should be 0.06,0.04,0.6,0.05,10 respectively
2.test Y function: If run Y function 1000 timss and storage in the 'result' variable, 'reslut' shoulg consist of roughly 600 times of value 0.06, roughly 400 times of value 0.04. And there is no other value.
3.test next_state function: If run next_state function 1000 times with imput parameter State_Action(4,250). The result should be 60% probability of State_Action(5,264), 40% probability of State_Action(5,261).
'''
#1:result should be 0.06,0.04,0.6,0.05,10 respectively
test = environment()
print(test.a,test.b,test.p,test.r,test.T)

#2:result should consist of roughly 600 times of value 0.06, roughly 400 times of value 0.04. And there is no other value.
import pandas as pd
result = np.zeros(1000)
for i in range(0,1000):
  result[i] = test.Y()
pd.Series(result).value_counts()

#3:The result should be 60% probability of State_Action(5,264)--hash value is 2909, hash_a value is 293859
#40% probability of State_Action(5,261)--hahs value is 2876, hash_a value is 290526
result_t = np.zeros(1000) #storage the result of time
result_wealth = np.zeros(1000) #storage the result of wealth
result_hash = np.zeros(1000) #storage the result of hash value
result_hash_a = np.zeros(1000) #storage the result of hash_a value
for i in range(0,1000):
  result = test.next_state(State_Action(4,250))
  result_t[i] = result.time
  result_wealth[i] = result.wealth
  result_hash[i] = result.hash()
  result_hash_a[i] = result.hash_a()
pd.Series(result_t).value_counts()
pd.Series(result_wealth).value_counts()
pd.Series(result_hash).value_counts()
pd.Series(result_hash_a).value_counts()


####Integration Testing
'''
Above two classes have only one interaction--next_state function in the environment class
I will use State_Action(4,200,80) as a starting node1. Use next_state to generate new node2 from node1, and storage it in the same adress.
Then set the action of node2 be 40, again use next_state to generate new node3 from node2.
Ideally node2 should be 60% of State_Action(5,212), 40% of State_Action(5,208). 
I focus on the node3, which should be 36% of State_Action(6,223), 24% of State_Action(6,222), 24% of State_Action(6,219), 16% of State_Action(6,218)
'''
test2 =environment()
result_t = np.zeros(1000) #storage the result of node3 time
result_wealth = np.zeros(1000) #storage the result of node3 wealth
for i in range(0,1000):
  test1 = State_Action(4,200,80) #Starting node1
  test1 = test2.next_state(test1) #get node2
  test1.action = 40 #set node2 action be 40
  result = test2.next_state(test1) #get node3
  result_t[i] = result.time
  result_wealth[i] = result.wealth
pd.value_counts(result_t)
pd.value_counts(result_wealth)
