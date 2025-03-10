#### Unit Test
'''
Test State_Action:
1.test initial funcion: If print(test.time,test.wealth,test.action), result should be 0,100,50 repsectively
2.test hash function: The hash value should be wealth * 11 + time = 1100
3.test hash_a function: The hash_a value should be 1100 * 101 + action = 111150
4.test is_end function: Test using Terminal time as 4,10,0 respectively, result should be False,False,True repsectively. Because the initial time value is 0
5.change time and wealth value: Change the time=8, wealth=-40, action=10, If print(test.time,test.wealth,test.action), result should be 8,-40,10 repsectively
6.test hash function again: The hash value should be wealth * 11 + time = -432
7.test hash_a function again: The hash_a value should be -432 * 101 + action = -43622
8.test is_end function again: Test using Terminal time as 4,10,0 respectively, result should be True,False,True repsectively.
9.test initial funcion with assign parameter: initial the parameter as time=4,wealth=25. If print(test.time,test.wealth,test.action), result should be 4,25,50 repsectively
10.test hash function again: The hash value should be wealth * 11 + time = 279
11.test hash_a function again: The hash_a value should be 279 * 101 + action = 28229
12.test is_end function again: Test using Terminal time as 4,10,0 respectively, result should be True,False,True repsectively.
'''
#1:result should be 0,100,50 repsectively
test = State_Action()
print(test.time,test.wealth,test.action)

#2:result should be 1100
print(test.hash())

#3:result should be 111150
print(test.hash_a())

#4:result should be False,False,True repsectively
print(test.is_end(4),test.is_end(10),test.is_end(0))

#5:result should be 8,-40,10 repsectively
test.time=8
test.wealth=-40
test.action=10
print(test.time,test.wealth,test.action)

#6:result should be -432
print(test.hash())

#7:result should be -43622
print(test.hash_a())

#8:result should be True,False,True repsectively
print(test.is_end(4),test.is_end(10),test.is_end(0))

#9:result should be 4,25,50 repsectively
test = State_Action(4,25)
print(test.time,test.wealth,test.action)

#10:result should be 279
print(test.hash())

#11:result should be 28229
print(test.hash_a())

#12:result should be True,False,True repsectively
print(test.is_end(4),test.is_end(10),test.is_end(0))

'''
Test environment
1.test initial funcion: If print(test.a,test.b,test.p,test.r,test.T), result should be 0.06,0.04,0.6,0.05,10 repsectively
2.test Y function: If run Y function 1000 timss and storage in the 'result' variable, 'reslut' shoulg consist of roughly 600 times of value 0.06, roughly 400 times of value 0.04. And there is no other value.
3.test next_state function: If run next_state function 1000 times with imput parameter State_Action(4,250). The result should be 60% probability of State_Action(5,264), 40% probability of State_Action(5,261).

'''

#1:result should be 0.06,0.04,0.6,0.05,10 repsectively
test = environment()
print(test.a,test.b,test.p,test.r,test.T)

#2:reslut shoulg consist of roughly 600 times of value 0.06, roughly 400 times of value 0.04. And there is no other value.
import pandas as pd
result = np.zeros(1000)
for i in range(0,1000):
  result[i] = test.Y()
pd.value_counts(result)

#3:The result should be 60% probability of State_Action(5,264)--hash value is 2909, hash_a value is 293859
#40% probability of State_Action(5,261)--hahs value is 2876, hash_a value is 290526
result_t = np.zeros(1000)
result_wealth = np.zeros(1000)
result_hash = np.zeros(1000)
result_hash_a = np.zeros(1000)
for i in range(0,1000):
  result = test.next_state(State_Action(4,250))
  result_t[i] = result.time
  result_wealth[i] = result.wealth
  result_hash[i] = result.hash()
  result_hash_a[i] = result.hash_a()
pd.value_counts(result_t)
pd.value_counts(result_wealth)
pd.value_counts(result_hash)
pd.value_counts(result_hash_a)


####Integration Testing
'''

'''
test=State_Action(1,200)
#Its value should be time=1, wealth=200, visited=0, value=0
test.action = 20
#Its value should be action=20
test1 =play()
test2 = test1.next_state(test)
#test2 is a hash value, wich value should be 209002000 or 212002000.

