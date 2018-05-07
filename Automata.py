from os import popen

class Automata:
    # Class to represent an Automata

    def __init__(self, language = set(['0', '1'])):
        self.states = set()
        self.startState = None
        self.finalStates = []
        self.transitions = dict()
        self.language = language

    @staticmethod
    def epsilon():
        return ":e:"

    def setstartState(self, state):
        self.startState = state
        self.states.add(state)

    def addFinalStates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalStates:
                self.finalStates.append(s)

    def addTransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}

    def addTransitionDict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addTransition(fromstate, state, tostates[state])

    def getTransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def getEClose(self, findstate):
        allstates = set()
        states = set([findstate])
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def display(self):
        print "states:", self.states
        print "start state: ", self.startState
        print "final states:", self.finalStates
        print "transitions:"
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print "  ",fromstate, "->", state, "on '"+char+"'",
            print

    def getPrintText(self):
        text = "language: {" + ", ".join(self.language) + "}\n"
        text += "states: {" + ", ".join(map(str,self.states)) + "}\n"
        text += "start state: " + str(self.startState) + "\n"
        text += "final states: {" + ", ".join(map(str,self.finalStates)) + "}\n"
        text += "transitions:\n"
        linecount = 5
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    text += "    " + str(fromstate) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount +=1
        return [text, linecount]

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartState(translations[self.startState])
        rebuild.addFinalStates(translations[self.finalStates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartState(pos[self.startState])
        for s in self.finalStates:
            rebuild.addFinalStates(pos[s])
        return rebuild

    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startState
            for state in self.states:
                if state in self.finalStates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"

        return dotFile

    # Creates the dot file
    def createDotFile(self, filePath):
        file = open("graphs/" + filePath + ".dot", "w+")
        file.write(self.getDotFile())
        file.close()

    def inLanguage(self, input):
        inLanguage = False

        for i in input:
            if i in self.language:
                inLanguage = True
            else:
                inLanguage = False
                break

        return inLanguage

    def match(self, input):
        currentState = self.startState
        matches = False

        if(not self.inLanguage(input)):
            matches = False
        else:
            # For each character in the input
            for i in input:
                # For each transition
                for fromstate, tostates in self.transitions.items():
                    for state in tostates:
                        for char in tostates[state]:
                            # If the current state is the first state in the transition
                            if(fromstate == currentState):
                                # If the character in the transition is the same as the character in the input
                                if(char == i):
                                    currentState = state

            # If the current state is the same as the final state then the input passes
            for finalState in self.finalStates:
                if(currentState == finalState):
                    matches = True

        if(matches):
            print input
            matches = False

class BuildAutomata:
    # Class for building e-nfa basic structures

    @staticmethod
    def basicStructure(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setstartState(state1)
        basic.addFinalStates(state2)
        basic.addTransition(1, 2, inp)
        return basic

    @staticmethod
    def plusStructure(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartState(state1)
        plus.addFinalStates(state2)
        plus.addTransition(plus.startState, a.startState, Automata.epsilon())
        plus.addTransition(plus.startState, b.startState, Automata.epsilon())
        plus.addTransition(a.finalStates[0], plus.finalStates[0], Automata.epsilon())
        plus.addTransition(b.finalStates[0], plus.finalStates[0], Automata.epsilon())
        plus.addTransitionDict(a.transitions)
        plus.addTransitionDict(b.transitions)
        return plus

    @staticmethod
    def dotStructure(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.setstartState(state1)
        dot.addFinalStates(state2)
        dot.addTransition(a.finalStates[0], b.startState, Automata.epsilon())
        dot.addTransitionDict(a.transitions)
        dot.addTransitionDict(b.transitions)
        return dot

    @staticmethod
    def starStructure(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartState(state1)
        star.addFinalStates(state2)
        star.addTransition(star.startState, a.startState, Automata.epsilon())
        star.addTransition(star.startState, star.finalStates[0], Automata.epsilon())
        star.addTransition(a.finalStates[0], star.finalStates[0], Automata.epsilon())
        star.addTransition(a.finalStates[0], a.startState, Automata.epsilon())
        star.addTransitionDict(a.transitions)
        return star



def drawGraph(automata, file):
    f = popen(r"dot -Tpng -o %s.png" % file, 'w')
    try:
        f.write(automata.getDotFile())
    except:
        raise BaseException("Error creating graph")
    finally:
        f.close()
