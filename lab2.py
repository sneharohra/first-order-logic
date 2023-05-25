import os
import re
import copy

global loop_break
loop_break = 0
final_ans = []

class Term():
    __slots__ = ('name', 'type', 'args')

    def __init__(self, name = 'None', type = 'None'):
        self.name = name
        self.type = type
        self.args = []

    def __str__(self,rec_call = 0):
        result = '\n\t\tTerm: '
        if rec_call == 1:
            result = ""
        return result+'Name: '+str(self.name)+', Type: '+str(self.type)+', Args: '+str([Term.__str__(i,1) for i in self.args])

    def __eq__(self, other):
        if not isinstance(other, Term):
            return NotImplemented
        if self.type == other.type == 'variable':
            return True
        if (self.type == 'constant' and other.type == 'variable') or (self.type == 'variable' and other.type == 'constant'):
            return True
        if self.type == other.type and self.name == other.name and self.type != 'function':
            return True
        if (self.type == 'variable' and other.type == 'function') or (other.type == 'variable' and self.type == 'function'):
            return True
        if self.type == other.type == 'function':
            if len(self.args) != len(other.args):
                return False
            i = 0
            while i < len(self.args) and self.args[i] == other.args[i]:
                i += 1
            if i == len(self.args):
                return True
        return False



class Predicate():
    __slots__ = ('name', 'flag',  'args')

    def __init__(self, name = 'None', flag=1):
        self.name = name
        self.args = []
        self.flag = flag

    def __str__(self):
        result = '\nPredicate:\n\tName: '+self.name+', Flag: '+str(self.flag) + '\n\tArgs:'
        for i in self.args:
            result += str(Term.__str__(i))
        return result

    def predicate_check(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented

        if len(self.args) != len(other.args):
            return False
        if self.name == other.name and self.flag == -1*(other.flag):
            i=0
            while i < len(self.args) and self.args[i] == other.args[i]:
                i+=1
            if i == len(self.args):
                self.args = []
                other.args = []
                return True
        return False



class Clause():
    __slots__ = ('predicate_list')

    def __init__(self):
        self.predicate_list = []

    def __str__(self):
        result = "\nClause:"
        for i in self.predicate_list:
            result += " " + Predicate.__str__(i)
        return result

    def clause_check(self, other):
        if not isinstance(other, Clause):
            return NotImplemented

        global loop_break
        for i in self.predicate_list:
            for j in other.predicate_list:
                if Predicate.predicate_check(i,j) is True:
                    self.predicate_list.remove(i)
                    other.predicate_list.remove(j)
                    if self.predicate_list == [] and other.predicate_list == []:
                        final_ans.append("no")
                        loop_break = 1
                        return
                    if self.predicate_list != [] and other.predicate_list != []:
                        self.predicate_list += other.predicate_list
                        other.predicate_list = []
                        return 0
                    return



class KB():
    __slots__ = ('clause_list')

    def __init__(self):
        self.clause_list = []

    def __str__(self):
        result = "KB:\n"
        for i in self.clause_list:
            result += " " + Clause.__str__(i)
        return result


def create_knowledgebase(predicates, variables, constants, functions, clauses):
    kb = KB()
    for z in clauses:
        c = Clause()
        for cl in z:
            var_inside_function = 0
            for f in functions:
                if f != '' and f in cl:
                    var_inside_function = len(re.findall(f+'\((.*?)\)',cl)[0].split(','))
                    fun = Term()
            p = Predicate()
            words = re.findall('\w+', cl)
            if cl[0] == '!':
                p.flag = -1
            for w in words:
                t = Term()
                if w in variables:
                    t.name = w
                    t.type = 'variable'
                    if var_inside_function > 0:
                        fun.args.append(t)
                        var_inside_function -= 1
                        continue
                    p.args.append(t)
                    continue
                if w in constants:
                    t.name = w
                    t.type = 'constant'
                    if var_inside_function > 0:
                        fun.args.append(t)
                        var_inside_function -= 1
                        continue
                    p.args.append(t)
                    continue
                if w in predicates:
                    p.name = w
                    c.predicate_list.append(p)
                    continue
                if w in functions:
                    fun.name = w
                    fun.type = 'function'
                    p.args.append(fun)

        kb.clause_list.append(c)
    return kb

def is_empty(kb):
    for k in kb.clause_list:
        if k.predicate_list != []:
            return "yes"
    return 'no'

def get_data(file):
    abs_path = os.path.abspath(file)
    s1 = 'Predicates: (.*)'
    s2 = 'Variables: (.*)'
    s3 = 'Constants: (.*)'
    s4 = 'Functions: (.*)'
    s5 = 'Clauses.*\n((.|\n)*)'
    with open(abs_path, 'r') as f:
        lines = f.read()
    try:
        predicates = re.findall(s1, lines)[0].strip().split(' ')
    except:
        predicates = []

    try:
        variables = re.findall(s2, lines)[0].strip().split(' ')
    except:
        variables = []

    try:
        constants = re.findall(s3, lines)[0].strip().split(' ')
    except:
        constants = []
    try:
        functions = re.findall(s4, lines)[0].strip().split(' ')
    except:
        functions = []

    clauses = []
    clauses_lines = re.findall(s5, lines)[0][0].strip().split('\n')
    for c in clauses_lines:
        x = c.strip().split(' ')
        clauses.append(x)

    return predicates, variables, constants, functions, clauses


def main():
    f = input("Enter the file name: ")
    try:
        predicates, variables, constants, functions, clauses = get_data(f)
    except:
        print("File not found in the current directory. If it is inside a directory make sure to enter the complete path to the file.")
        exit(1)

    og_kb = create_knowledgebase(predicates, variables, constants, functions, clauses)

    for bigi in range(len(og_kb.clause_list)):
        knowledgebase = copy.deepcopy(og_kb)
        if bigi > 0:
            for zz in range(bigi):
                knowledgebase.clause_list.append(knowledgebase.clause_list.pop(0))
        not_match = set()
        for i in range(0,len(knowledgebase.clause_list)):
            if knowledgebase.clause_list[i].predicate_list == []:
                continue
            j = 0
            while j < len(knowledgebase.clause_list):
                if i == j or (i,j) in not_match or (j,i) in not_match:
                    j+=1
                    continue
                if knowledgebase.clause_list[j].predicate_list == []:
                    j+=1
                    continue
                idk = Clause.clause_check(knowledgebase.clause_list[i],knowledgebase.clause_list[j])
                if idk == 0:
                    not_match.add((i,j))
                    j = 0
                    continue
                if loop_break == 1:
                    break
                j+=1
            if loop_break == 1:
                break
        if loop_break == 1:
            continue
        final_ans.append(is_empty(knowledgebase))
    if "no" in final_ans:
        print("no")
    else:
        print("yes")


main()