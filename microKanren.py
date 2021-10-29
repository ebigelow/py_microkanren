from dataclasses import dataclass
from typing import Callable, List, Tuple, Union

@dataclass
class Variable:
    value: int

Term = Union[str, bool, int, Variable, List['Term']]  # ADT

@dataclass
class Substitution:
    pairs: List[Tuple[Variable, Term]]

@dataclass
class State:
    sub: Substitution
    counter: int

# ADTs in python; only used for hinting, not instantiated
ListStream = List[State]                    # [State]
ImmatureStream = Callable[[], 'Stream']     # () -> Stream
Stream = Union[ListStream, ImmatureStream]  # ListStream | Immature

Goal = Callable[[State], Stream]            # State -> Stream

def walk(u: Term, s: Substitution) -> Term:
    # Recursively search for a variable `u`'s value in the substitution `s`.
    if isinstance(u, Variable):
        v, t = next(((v, t) for v, t in s.pairs if (u == v)), [0, 0])
        if v:
            return walk(t, s)
    return u

def ext_s(v: Variable, t: Term, s: Substitution) -> Substitution:
    # Extend substitution with a new binding
    return Substitution([(v, t)] + s.pairs)

def eqeq(u: Term, v: Term) -> Goal:
    # Return a goal that succeeds if the two terms unify in the received state
    def g(sc: State) -> Stream:
        s = unify(u, v, sc.sub)
        return unit(State(s, sc.counter)) if s is not None else mzero()
    return g

def mzero() -> Stream:
    return []

def unit(sc: State) -> Stream:
    return [sc]

def unify(u: Term, v: Term, s: Substitution) -> Substitution:
    # Extend a substitution with the walked pair (u, v)
    u = walk(u, s)
    v = walk(v, s)

    if isinstance(u, Variable) and (u == v):
        return s
    elif isinstance(u, Variable):
        return ext_s(u, v, s)
    elif isinstance(v, Variable):
        return ext_s(v, u, s)
    elif isinstance(u, list) and isinstance(v, list) and (u and v):
        s_ = unify(u[0], v[0], s)
        return unify(u[1:], v[1:], s_) if s_ else None
    else:
        return s if ((u == v) and s) else None

def call_fresh(f: Callable[[Variable], Goal]) -> Goal:
    # Wrap `f` in a Goal (State -> Stream) function that injects fresh variables
    def g(sc: State) -> Stream:          # Substitute first function arg with fresh var
        f_var = f(Variable(sc.counter))  # e.g. in `f = lambda a: ..`, replace `a` with new Variable
        return f_var(State(sc.sub, sc.counter + 1))  # call `f(var)(new_state)`, increment counter
    return g

def disj(g1: Goal, g2: Goal) -> Goal:
    def g(sc: State) -> Stream:
        return mplus(g1(sc), g2(sc))
    return g

def conj(g1: Goal, g2: Goal) -> Goal:
    def g(sc: State) -> Stream:
        return bind(g1(sc), g2)
    return g

# Lisp list processing primitives
def cons(a, b):   # (cons 'a 'b) == '(a . b)   (cons 'a '(b)) == '(a b)
    return ([a] + b if isinstance(b, list) else [a] + [b])

def cdr(ls):      # (cdr '(a . b)) == 'b       (cdr '(a b)) == '(b)
    return ls[1] if len(ls) == 2 and not isinstance(ls[1], State) else ls[1:]

def mplus(S1: Stream, S2: Stream) -> Stream:
    # Append two streams together
    if not S1:
        return S2
    elif callable(S1):
        return lambda: mplus(S2, S1())
    else:
        S_ = mplus(cdr(S1), S2)
        return cons(S1[0], S_)

def bind(S: Stream, g: Goal) -> Stream:
    # Map g(s) to each state s in S
    if not S:
        return mzero()
    elif callable(S):
        return lambda: bind(S(), g)
    else:
        S_ = bind(cdr(S), g)
        return mplus(g(S[0]), S_)
