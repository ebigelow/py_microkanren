from microKanren import *
from microKanren_test_programs import *


test_check('second_set t1', 
	actual=call_fresh(lambda q: eqeq(q, 5))(empty_state)[0],
	expected=State(Substitution([(Variable(0), 5)]), 1)
)

test_check('second_set t2', 
	actual=call_fresh(lambda q: eqeq(q, 5))(empty_state)[1:],
	expected=[]
)

test_check('second_set t3', 
	actual=a_and_b(empty_state)[0],
	expected=State(Substitution([
		(Variable(1), 5), 
		(Variable(0), 7)
	]), 2)
)

test_check('second_set t3, take', 
	actual=take(a_and_b(empty_state), 1),
	expected=[State(Substitution([
		(Variable(1), 5), 
		(Variable(0), 7)
	]), 2)]
)


test_check('second_set t4', 
	actual=a_and_b(empty_state)[1],
	expected=State(Substitution([
		(Variable(1), 6), 
		(Variable(0), 7)
	]), 2)
)

test_check('second_set t5', 
	actual=a_and_b(empty_state)[2:],
	expected=[]
)

test_check('who cares',
	actual=take(call_fresh(lambda q: fives(q))(empty_state), 0),
	expected=[]
)

test_check('take 2 a-and-b stream', 
	actual=take(a_and_b(empty_state), 2),
	expected=[
		State(Substitution([
			(Variable(1), 5), 
			(Variable(0), 7)
		]), 2),
		State(Substitution([
			(Variable(1), 6), 
			(Variable(0), 7)
		]), 2)
	]
)

test_check('take-all a-and-b stream', 
	actual=take_all(a_and_b(empty_state)),
	expected=[
		State(Substitution([
			(Variable(1), 5), 
			(Variable(0), 7)
		]), 2),
		State(Substitution([
			(Variable(1), 6), 
			(Variable(0), 7)
		]), 2)
	]
)

test_check('appendo', 
	actual=take(call_appendo(empty_state), 2),
	expected=[
		State(Substitution([
			(Variable(0), [Variable(1), Variable(2), Variable(3)]), 
			(Variable(2), Variable(3)), 
			(Variable(1), [])
		]), 4),
		State(Substitution([
			(Variable(0), [Variable(1), Variable(2), Variable(3)]), 
			(Variable(2), Variable(6)), 
			(Variable(5), []), 
			(Variable(3), [Variable(4), Variable(6)]), 
			(Variable(1), [Variable(4), Variable(5)])
		]), 7)
	]
)

test_check('appendo2', 
	actual=take(call_appendo2(empty_state), 2),
	expected=[
		State(Substitution([
			(Variable(0), [Variable(1), Variable(2), Variable(3)]), 
			(Variable(2), Variable(3)), 
			(Variable(1), [])
		]), 4),
		State(Substitution([
			(Variable(0), [Variable(1), Variable(2), Variable(3)]), 
			(Variable(3), [Variable(4), Variable(6)]), 
			(Variable(2), Variable(6)), 
			(Variable(5), []),
			(Variable(1), [Variable(4), Variable(5)])
		]), 7)
	]
)

# TODO: test fails  - `appendo(['a'], ['b'], ['a', 'b'])(empty_state)` returns []
test_check('ground appendo', 
	actual=take(ground_appendo(empty_state), 1),
	expected=State(Substitution([
		(Variable(2), ['b']), 
		(Variable(1), []), 
		(Variable(0), 'a')
	]), 3)
)

# TODO: test fails
test_check('ground appendo2', 
	actual=take(ground_appendo2(empty_state), 1),
	expected=State(Substitution([
		(Variable(2), ['b']), 
		(Variable(1), []), 
		(Variable(0), 'a')
	]), 3)
)

# Note: `reify-1st` tests omitted because most miniKanren wrappers aren't implemented
test_check('many non-ans', 
	actual=take(many_non_ans(empty_state), 1),
	expected=[State(Substitution([(Variable(0), 3)]), 1)]
)
