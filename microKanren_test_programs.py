from microKanren import *

# MiniKanren wrappers
empty_state = State(Substitution([]), 0)

def pull(S: Stream) -> ListStream:
	return pull(S()) if callable(S) else S

def take(S: Stream, n: int) -> ListStream:
	# Use take(S,n) instead of S[:n] if S might be an ImmatureStream
	if n == 0:
		return []

	S_ = pull(S)  # convert Stream -> ListStream
	if not S_:
		return []
	return cons(S_[0], take(cdr(S_), n-1))

def take_all(S: Stream) -> ListStream:
	S_ = pull(S)
	if not S_:
		return []
	return cons(S_[0], take_all(cdr(S_)))


# Tests -----------------------------------------------------------------------

def test_check(title, actual, expected):
	print(f'Testing: {title}')
	if actual != expected:
		print(f'\t{title} Failed.\n\t\tExpected={expected}\n\t\tActual={actual}')

# type: Goal
a_and_b = conj(
	call_fresh(lambda a: eqeq(a, 7)),
	call_fresh(lambda b:
		disj(
			eqeq(b, 5),
			eqeq(b, 6),
		)))

# type: Goal
fives = lambda x: disj(
	eqeq(x, 5),
	lambda ac: lambda: fives(x)(ac)
)


# type: Goal
relo = (
	lambda x:
	call_fresh(lambda x1:
	call_fresh(lambda x2:
	conj(
		eqeq(x, cons(x1, x2)),
		disj(
			eqeq(x1, x2),
			lambda sc: lambda: relo(x)(sc)
		)
	)))
)

# type: Goal
many_non_ans = call_fresh(lambda x:
	disj(
		relo([5, 6]),
		eqeq(x, 3)
	))

# type: Goal
appendo = lambda l, s, out: disj(
	conj(
		eqeq([], l),
		eqeq(s, out)
	),
	call_fresh(lambda a:
	call_fresh(lambda d:
	conj(
		eqeq(cons(a, d), l),
		call_fresh(lambda res:
			conj(
				eqeq(cons(a, res), out),
				lambda sc: lambda: appendo(d, s, res)(sc)  # Goal(State) -> Stream
				# lambda sc: lambda: <Stream>
				# lambda sc: <ImmatureStream>
			))
	)))
)

# type: Goal
appendo2 = lambda l, s, out: disj(
	conj(
		eqeq([], l),
		eqeq(s, out)
	),
	call_fresh(lambda a:
	call_fresh(lambda d:
	conj(
		eqeq(cons(a, d), l),
		call_fresh(lambda res:
			conj(
				lambda sc: lambda: appendo(d, s, res)(sc),
				eqeq(cons(a, res), out)  
			))
	)))
)

# type: Goal
call_appendo = (
	call_fresh(lambda q:
	call_fresh(lambda l:
	call_fresh(lambda s:
	call_fresh(lambda out:
	conj(
		appendo(l, s, out),
		eqeq([l, s, out], q)
	)))))
)

# type: Goal
call_appendo2 = (
	call_fresh(lambda q:
	call_fresh(lambda l:
	call_fresh(lambda s:
	call_fresh(lambda out:
	conj(
		appendo2(l, s, out),
		eqeq([l, s, out], q)
	)))))
)

# type: Goal
call_appendo3 = (
	call_fresh(lambda q:
	call_fresh(lambda l:
	call_fresh(lambda s:
	call_fresh(lambda out:
	conj(
		eqeq([l, s, out], q),   
		appendo(l, s, out)
	)))))
)

# type: Stream
ground_appendo = appendo(['a'], ['b'], ['a', 'b'])

# type: Stream
ground_appendo2 = appendo2(['a'], ['b'], ['a', 'b'])
