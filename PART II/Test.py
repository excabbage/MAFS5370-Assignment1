####Unit Testing
'''
Test TD0 class:
1.test policy_update function: Because policy and all_Q storage the data dynamically, I test 4 situation. 
    There is neither policy data nor all_Q data of state: time=1, wealth=100, for all action. Result should be initial policy value=50
    There is policy data of state: time=2, wealth=100, no all_Q data of pairs: time=2, wealth=100, for all action. Result should be exist policy value.
    There is no policy data of state: time=4, wealth=100, there is all_Q data of pairs: time=4, wealth=100, action=30. Result should be 30 as I have only visited it.
    There is both policy data and all_Q data of state: time=6, wealth=100, action=40 or 80. Result should be the action with highest Q value.
  Running policy_update function on this four situation,
  The results of print(test.policy) should be 1101:50, 1102:25, 1104:30, 1106:80
2.test get_action function: Using the above test data, I test 2 situation: Whether there is policy data of input state.
    There is no policy data of state: time=10, wealth=100.
    There is policy data of state: time=6, wealth=100.
  Running get_action function on this two situation, and epsilon = 0.5.
  The result of first situation should be 50.5% probability of 50, 0.5% probability of 0~100 except 50.
  The result of second situation should be 50.5% probability of 80, 0.5% probability of 0~100 except 80.
3.test backup function: Using the above test data,
    If backup( 100*1111+4*101+30 , 100*1111+6*101+80 , 0 ), The value of all_Q[100*1111+4*101+30] will change from 20 into 29.7, which is 20 + 1*[0 + 0.99*30 - 20]
    If backup( 100*1111+4*101+30 , 100*1111+6*101+40 , 10 ), The value of all_Q[100*1111+4*101+30] will change from 20 into 10, which is 20 + 1*[10 + 0.99*0 - 20]
4.test episode function: If I run episode functio once, the length of all_Q, policy, should be 10 as we dynamically storage the visited nodes. And only last all_Q is non zero.
'''
#1:The results of print(test.policy) should be 1101:50, 1102:25, 1104:30, 1106:80
test = TD0()
test.policy[100*11+2] = 25
test.policy[100*11+6] = 75
test.all_Q[100*1111+4*101+30] = 20
test.all_Q[100*1111+6*101+80] = 30
test.all_Q[100*1111+6*101+40] = 0
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
change = test.backup( 100*1111+4*101+30 , 100*1111+6*101+80 , 0 ) # first situation
print(change, test.all_Q[100*1111+4*101+30]) #result should be 9.7, 29.7
test.all_Q[100*1111+4*101+30] = 20 # reset
change = test.backup( 100*1111+4*101+30 , 100*1111+6*101+40 , 10 ) # second situation
print(change, test.all_Q[100*1111+4*101+30]) #result should be 10, 10

#4: 
test1 = TD0()
test1.episode()
print(len(test1.all_Q),len(test1.policy)) #result should be 10, 10
print(test1.all_Q) # And only last all_Q is non zero.


####Integration Testing:
'''
test the TD0 working well.
I use a special case to test: the risky asset return is always higher than riskfree interest rate.
Obviously, there is an arbitrage opportunity, and thus optimal stratagy is 100% of capital allocated into risky asset.
I will set risky asset return Y= 0.08, prob= 0.6, and 0.06, prob= 0.4. Run the episode function until 1000000 times or until the summation of change of Q is less than 1e-5.
'''
test = TD0()
test.player.a=0.08
test.player.b=0.06
for i in range(0,1000000):
    change = test.episode()
    if change < 1e-5 :
        break
p = test.policy #get the policy
# view the result of policy at time 0
x0 = []
w0 = []
for key in p:
    if key%11 == 0 :
        x0=np.append(x0,p[key])
        w0=np.append(w0,(key-key%11)/11)
plt.plot(w0,x0,'o')
plt.title('Policy at time 0')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 1
x1 = []
w1 = []
for key in p:
    if key%11 == 1 :
        x1=np.append(x1,p[key])
        w1=np.append(w1,(key-key%11)/11)
plt.plot(w1,x1,'o')
plt.title('Policy at time 1')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 2
x2 = []
w2 = []
for key in p:
    if key%11 == 2 :
        x2=np.append(x2,p[key])
        w2=np.append(w2,(key-key%11)/11)
plt.plot(w2,x2,'o')
plt.title('Policy at time 2')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 3
x3 = []
w3 = []
for key in p:
    if key%11 == 3 :
        x3=np.append(x3,p[key])
        w3=np.append(w3,(key-key%11)/11)
plt.plot(w3,x3,'o')
plt.title('Policy at time 3')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 4
x4 = []
w4 = []
for key in p:
    if key%11 == 4 :
        x4=np.append(x4,p[key])
        w4=np.append(w4,(key-key%11)/11)
plt.plot(w4,x4,'o')
plt.title('Policy at time 4')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 5
x5 = []
w5 = []
for key in p:
    if key%11 == 5 :
        x5=np.append(x5,p[key])
        w5=np.append(w5,(key-key%11)/11)
plt.plot(w5,x5,'o')
plt.title('Policy at time 5')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 6
x6 = []
w6 = []
for key in p:
    if key%11 == 6 :
        x6=np.append(x6,p[key])
        w6=np.append(w6,(key-key%11)/11)
plt.plot(w6,x6,'o')
plt.title('Policy at time 6')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 7
x7 = []
w7 = []
for key in p:
    if key%11 == 7 :
        x7=np.append(x7,p[key])
        w7=np.append(w7,(key-key%11)/11)
plt.plot(w7,x7,'o')
plt.title('Policy at time 7')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 8
x8 = []
w8 = []
for key in p:
    if key%11 == 8 :
        x8=np.append(x8,p[key])
        w8=np.append(w8,(key-key%11)/11)
plt.plot(w8,x8,'o')
plt.title('Policy at time 8')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
# view the result of policy at time 9
x9 = []
w9 = []
for key in p:
    if key%11 == 9 :
        x9=np.append(x9,p[key])
        w9=np.append(w9,(key-key%11)/11)
plt.plot(w9,x9,'o')
plt.title('Policy at time 9')
plt.xlabel('wealth')
plt.ylabel('action %')
plt.ylim((0,101))
