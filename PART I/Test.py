### Unit Test






##Integration Testing: test State_Action and play class working well.
test=State_Action(1,200)
#Its value should be time=1, wealth=200, visited=0, value=0
test.action = 20
#Its value should be action=20
test1 =play()
test2 = test1.next_state(test)
#test2 is a hash value, wich value should be 209002000 or 212002000.

