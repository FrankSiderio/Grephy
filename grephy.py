import os
import sys

def match(re, s): return run(prepare(re), s)

def run(states, s):
    for c in s:
        states = set.union(*[state(c) for state in states])
    return accepting_state in states

def accepting_state(c): return set()
def expecting_state(char, k): return lambda c: k(set()) if c == char else set()

def state_node(state): return lambda seen: set([state])
def alt_node(k1, k2):  return lambda seen: k1(seen) | k2(seen)
def loop_node(k, make_k):
    def loop(seen):
        if loop in seen: return set()
        seen.add(loop)
        return k(seen) | looping(seen)
    looping = make_k(loop)
    return loop

def prepare(re):
    ts = list(re)

    def parse_expr(precedence, k):
        rhs = parse_factor(k)
        while ts:
            if ts[-1] == '(': break
            prec = 2 if ts[-1] == '|' else 4
            if prec < precedence: break
            if chomp('|'):
                rhs = alt_node(parse_expr(prec + 1, k), rhs)
            else:
                rhs = parse_expr(prec + 1, rhs)
        return rhs

    def parse_factor(k):
        if not ts or ts[-1] in '|(':
            return k
        elif chomp(')'):
            e = parse_expr(0, k)
            assert chomp('(')
            return e
        elif chomp('*'):
            return loop_node(k, lambda loop: parse_expr(6, loop))
        else:
            return state_node(expecting_state(ts.pop(), k))

    def chomp(token):
        matches = (ts and ts[-1] == token)
        if matches: ts.pop()
        return matches

    k = parse_expr(0, state_node(accepting_state))
    assert not ts
    return k(set())

inputFile = str(sys.argv[1])
regexFile = str(sys.argv[2])

# Check if file exists
if(os.path.isfile(inputFile) and os.path.isfile(regexFile)):
    print("Found files!")
    if(os.stat(inputFile).st_size == 0 and os.stat(regexFile).st_size == 0):
        print("Files are empty")
    inputFile = open(inputFile)
    regexFile = open(regexFile)

    with regexFile as f:
        regex = f.readline()

    with inputFile as f:
        input = f.readlines()

    for i in input:
        print (i + str(match(regex, i)))
        print "\n"

    # print match(regex, input)
else:
    print("File not found. Try again")
