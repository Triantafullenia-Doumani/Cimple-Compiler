# MARIA TSIGKOU 4191
# TRIANTAFYLLIW DOUMANI 4052

import sys

SINGLE_TOKENS_LIST = [",", ";", "+", "-", "*", "/", ")", "(", "[", "]", "{", "}", ">", "<", "="]
VARLIST = []
AUTO = [
    [4, 3, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 0, 7, 8, 5, 5, 5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 6, 1],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6],
    [-1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
    [4, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 5, 5, 5, 5],
]


class Entities:

    arguments = []
    def __init__(self, name, value, parMode, offset, type, startQuad, framelength):
        self.name = name
        self.type = type
        self.offset = offset
        self.startQuad = startQuad
        self.framelength = framelength
        self.value = value
        self.parMode = parMode



class Scope:

    entity = []
    offset = 12
    def __init__(self, nestingLevel):
        self.nestingLevel = nestingLevel


class Arguments:

    def __init__(self, parMode, varType):
        self.parMode = parMode
        self.varType = varType


class Buffers:

    def __init__(self, string_buffer, counter, temp, filename, state):
        self.word_buffer = string_buffer
        self.charType = string_buffer
        self.char_buffer = string_buffer
        self.assigment_buffer = string_buffer
        self.temp_counter = counter
        self.T1_place = temp
        self.input_file_name = filename
        self.state = state


class Quads:
    def __init__(self):
        self.quad_list = []
        self.quad_list_for_c = []


class Flag:
    def __init__(self, flag):
        self.sub = flag
        self.program_includes_fun_or_prod = flag


def main(argv):
    global BUFFERS
    global QUADS
    global FLAG
    global input
    global tokenType
    global tokenString
    global line
    global scopes
    global level


    tokenType = ""
    tokenString = ""
    scopes = []
    line = 1
    level = 0
    BUFFERS = Buffers("", 0, "T_0", argv[0], 0)
    QUADS = Quads()
    FLAG = Flag(0)
    input = open(argv[0], "r")

    program()


###################################### INTERMEDIATE CODE #########################################

def create_int_file():
    int_file_name = BUFFERS.input_file_name.replace(".ci", ".int")
    int_file = open(int_file_name, "w")

    for quad in QUADS.quad_list:
        int_file.write(str(quad) + "\n")

    int_file.close()


def create_c_file():
    c_file_name = BUFFERS.input_file_name.replace(".ci", ".c")
    c_file = open(c_file_name, "w")
    c_file.write("#include <stdio.h> \n")
    c_file.write("\nvoid main() \n{\n")
    c_file.write("int ")

    var_len = len(VARLIST)
    for var in range(var_len - 1):
        c_file.write(str(VARLIST[var]) + ",")
    if len(VARLIST) > 1:
        c_file.write(str(VARLIST[-1]) + "; \n")
    for line in QUADS.quad_list_for_c:
        c_file.write(str(line))
    c_file.write("}")
    c_file.close()


# returns the number of the next quad
def nextquad():
    return len(QUADS.quad_list)


# generates the new quand
def genquad(op, x, y, z):
    label = nextquad()
    new_quad = [label, op, x, y, z]
    QUADS.quad_list.append(new_quad)
    return new_quad


# creates and returns a new temporary variable
# the temporary changes are of the form T_1, T_2, T_3 ...
def newtemp():
       # def __init__(self, name, value, parMode, offset, type, startQuad, framelength):

    global temp_counter
    new_temp = 'T_%s' % BUFFERS.temp_counter
    addNewTempVar(new_temp)
    BUFFERS.temp_counter += 1
    return new_temp


# creates a blank list of labels
def emptylist():
    new_quad = ["_", "_", "_", "_", "_"]
    return new_quad


# creates a list of labels containing only x
def makelist(x):
    new_quad = [x, "_", "_", "_", "_"]
    return new_quad


# creates a list of labels from the merge of list 1 and list 2
def merge(list1, list2):
    new_list = list1 + list2
    return new_list


# the list consists of indices in quads whose last end is not is completed
# The backpatch visits these quads one by one and completes them with the z tag
def backpatch(pointers_list, z):
    for i in pointers_list:
        for q in range(1, len(QUADS.quad_list)):
            if (QUADS.quad_list[q][0] == i):
                QUADS.quad_list[q][4] = z


def backpatch_c(z):
    for x in range(len(QUADS.quad_list_for_c)):
        string = str(QUADS.quad_list_for_c[x])
        QUADS.quad_list_for_c[x] = string.replace("null", str(z))

def addNewScope():
    level = len(scopes) #maria
    scopes.append(Scope(level))

def addNewVar(name):
    ent = Entities(name,None,None,scopes[-1].offset, "Var",None,None)
    scopes[-1].entity.append(ent)
    scopes[-1].offset += 4
    #obj = scopes[-1]
    #print(obj.entity[-1].name," ",obj.entity[-1].type, " ",obj.entity[-1].offset)

   
def addNewTempVar(name):
    ent = Entities(name,None,None,scopes[-1].offset,"tempVar",None,None)
    scopes[-1].entity.append(ent)
    scopes[-1].offset += 4
    #obj = scopes[-1]
    #print(obj.entity[-1].name," ",obj.entity[-1].type, " ",obj.entity[-1].offset)
    
   
def addNewPar(name,parMode):
    ent = Entities(name,None,parMode,scopes[-1].offset, "Par",None,None)
    scopes[-1].entity.append(ent)
    scopes[-1].offset += 4
    #obj = scopes[-1]
    #print(obj.entity[-1].name," ",obj.entity[-1].type, " ",obj.entity[-1].offset," ",obj.entity[-1].parMode)
   
def addNewFunction(name):
   
    ent = Entities(name,None,None,None,"Function",None,None)
    scopes[-1].entity.append(ent)

def addArgument(parMode):

    scopes[-2].entity[-1].arguments.append(parMode)
    obj = scopes[-2]
    print(obj.entity[-1].name," ",obj.entity[-1].type, " ",obj.entity[-1].offset," ",obj.entity[-1].parMode)

def removeScope():
    global level
    print("Scope : " , level,"\n")
    obj = scopes[-1]
    for ent in obj.entity:
        if(ent.type == "Var"):
               print(ent.name," ",ent.type, " ",ent.offset)
        elif(ent.type == "tempVar"):
               print(ent.name," ",ent.type, " ",ent.offset)
        elif(ent.type == "Par"):
               print(ent.name," ",ent.type, " ",ent.offset," ",ent.parMode)
        elif(ent.type == "Function" or ent.type == "procedure"):
           print(ent.name," ",ent.type, " ",ent.startQuad)

    print("\n")
    scopes.pop(level - 1)
    level = level - 1

###################################### GRAMMAR ANALYSIS #########################################
def program():
    global tokenType
    global program_name
    lex()
    if (tokenString == "program"):
        lex()
        addNewScope()
        if (tokenType == "idtk"):
            program_name = tokenString
            block()
        else:
            print("Syntax Error line: " + str(line) + "\nProgram name expected")
            exit()
    else:
        print("Syntax Error line: " + str(line) + "\nThe keyword ' program' expected")
        exit()


def block():
    lex()
    declarations()
    subprograms()
    statements()


def declarations():
    if (tokenType == "BracesOpentk"):
        lex()
    while (tokenString == "declare"):
        while (1):
            lex()
            if (tokenType == "idtk"):
                if (tokenString not in VARLIST):
                    VARLIST.append(tokenString)
                    addNewVar(tokenString)
                else:
                    print("ERROR line: " + str(line) + "\nYou can't declare the same id multiple times" + tokenString)
                    exit()
            else:
                print("Syntax Error in line: " + str(
                    line) + "\nExpected ID not " + tokenType + " ( " + tokenString + " )")
                exit()
            lex()
            if (tokenType == "commatk"):
                continue
            if (tokenType == "semicolontk"):
                lex()
                break
            else:
                print("Syntax Error in line: " + str(line) + "\nWrong syntax of declaration")
                exit()
        continue


def subprograms():
    global BUFFERS

    if (tokenType == "BracesOpentk" and FLAG.sub == 0):
        genquad("begin_block", program_name, "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ":\n"
        QUADS.quad_list_for_c.append(line_c)
        FLAG.sub = 1
    elif (tokenType == "BracesOpentk"):
        lex()
    while (tokenString == "function" or tokenString == "procedure"):
        FLAG.program_includes_fun_or_prod = 1
        FLAG.sub = 1
        lex()
        if (tokenType != "idtk"):
            print("Syntax Error in line: " + str(
                line) + "\nExpected ID not " + tokenType + " ( " + tokenString + " ) after function/procedure")
            exit()
        function_name = tokenString
        addNewFunction(function_name)       #maria
        
        addNewScope()
        genquad("begin_block", function_name, "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1)
        QUADS.quad_list_for_c.append(line_c)
        lex()
        if (tokenType != "ParenthesesOpentk"):
            print("Syntax Error in line: " + str(line) + "\nExpected to open Parentheses")
            exit()
        formalparlist()
        scopes[-2].entity[-1].startQuad = len(QUADS.quad_list)  #maria
        block()
        removeScope()  
        genquad("end_block", function_name, "_", "_")
        FLAG.sub = 0
    if (tokenType == "BracesOpentk" and FLAG.sub == 0):
        genquad("begin_block", program_name, "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ":\n"
        QUADS.quad_list_for_c.append(line_c)
        FLAG.sub = 1


# 1 or more statements
def statements():
    if (tokenType == "BracesOpentk"):
        lex()
    while (1):
        if (tokenType == "BracesOpentk"):
            lex()
            while (1):
                statem = tokenString
                statement()
                if (tokenType == "BracesClosetk"):
                    lex()
                    if (tokenType != "semicolontk"):
                        print("Syntax Error in line: " + str(
                            line) + "\nStatement " + statem + " must finish with semicolon not " + tokenString)
                        exit()
                    break
                else:
                    continue
        else:
            statem = tokenString
            if statement():
                #    if(tokenType == "semicolontk"):
                #        print("Syntax Error in line: " + str(line) + " Duplicate semicolon \n")
                #        exit()
                break
        if (tokenString == "}"):
            lex()
            return


# one statement
def statement():
    if (tokenString == 'if'):
        ifStat()
    if (tokenString == "while"):
        whileStat()
    elif (tokenString == "switchcase"):
        switchcaseStat()
    elif (tokenString == "forcase"):
        forcaseStat()
    elif (tokenString == "incase"):
        incaseStat()
    elif (tokenString == "call"):
        callStat()
    elif (tokenString == "return"):
        returnStat()
    elif (tokenString == "input"):
        inputStat()
    elif (tokenString == "print"):
        printStat()
    elif (tokenType == "idtk"):
        assignStat()
    else:
        return 1


def incaseStat():
    lex()
    w = newtemp()
    iquad = nextquad()
    # genquad(":=","1","_",w)
    # active_case_flag = 1
    while (tokenString == "case"):
        lex()
        if (tokenType == "ParenthesesOpentk"):
            lex()
            C_place = condition()
            backpatch_c(nextquad() + 1)
            genquad("jump", "_", "_", "_")
            line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null ; // ( jump,_,_,null )\n"
            QUADS.quad_list_for_c.append(line_c)
            if (tokenType == "ParenthesesClosetk"):
                lex()
                backpatch(C_place[1], nextquad())
                #    genquad(":=","0","_",w)
                statements()
                # line_c = "L_"+str(len(QUADS.quad_list) -1)+": if "+str(w)+" == 0 goto L_"+str(iquad)+" // ( jump,_,_,"+str(iquad)+")\n"
                # QUADS.quad_list_for_c.append(line_c)
                backpatch(C_place[0], nextquad())
                backpatch_c(nextquad())


            else:
                print("Syntax Error in line: " + str(
                    line) + "\nExpected ')' to close the expression in IncaseStat() not " + tokenString)
                exit()
        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '(' after ID in IncaseStat() not " + tokenString)
            exit()

    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement incase must finish with semicolon not " + tokenString)
        exit()
    genquad("=", w, "0", iquad)
    line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": if " + str(w) + " == 0 goto L_" + str(
        iquad) + ";  // ( jump,_,_," + str(iquad) + ") \n"
    QUADS.quad_list_for_c.append(line_c)


def forcaseStat():
    lex()
    fquad = nextquad()
    while (tokenString == "case"):
        lex()
        if (tokenType == "ParenthesesOpentk"):
            lex()
            C_place = condition()
            backpatch_c(nextquad() + 1)
            genquad("jump", "_", "_", "_")
            line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null ; // ( jump,_,_,null )\n"
            QUADS.quad_list_for_c.append(line_c)
            if (tokenType != "ParenthesesClosetk"):
                print("Syntax Error in line: " + str(
                    line) + "\nExpected ')'' to close the expression in forcaseStat() not " + tokenString)
                exit()
            else:
                lex()
                backpatch(C_place[1], nextquad())
                statements()
                genquad("jump", "_", "_", fquad)
                line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_" + str(fquad) + " ; // ( jump,_,_," + str(
                    fquad) + ")\n"
                QUADS.quad_list_for_c.append(line_c)
                backpatch(C_place[0], nextquad())
                backpatch_c(nextquad())

        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '('' to open case not " + tokenString)
            exit()
    if (tokenString != "default"):
        print("Syntax Error in line: " + str(line) + "\nYou must have 'default' case at forcase")
        exit()
    lex()
    statements()
    if (check_statement_to_finish_with_semicolon() == 0):
        print(
            "Syntax Error in line: " + str(line) + "\nStatement forcase must finish with semicolon not " + tokenString)
        exit()


def switchcaseStat():
    lex()
    exit_list = emptylist()
    pointers_list = []
    while (tokenString == "case"):
        lex()
        if (tokenType == "ParenthesesOpentk"):
            lex()
            C_place = condition()
            backpatch_c(nextquad() + 1)
            genquad("jump", "_", "_", "_")
            line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null ; // ( jump,_,_,null )\n"
            QUADS.quad_list_for_c.append(line_c)
            if (tokenType != "ParenthesesClosetk"):
                print("Syntax Error in line: " + str(
                    line) + "\nExpected ')'' to close the expression in switchcaseStat() not " + tokenString)
                exit()
            else:
                lex()
                backpatch(C_place[1], nextquad())
                statements()
                e = makelist(nextquad())
                genquad("jump", "_", "_", "_")
                line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null //( jump,_,_, null)\n"
                QUADS.quad_list_for_c.append(line_c)
                exit_list = merge(exit_list, e)
                backpatch(C_place[0], nextquad())
            #    backpatch_c(nextquad())

        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '('' to open case not " + tokenString)
            exit()
    if (tokenString != "default"):
        print("Syntax Error in line: " + str(line) + "\nYou must have 'default' case at switchcase")
        exit()
    lex()
    statement()
    backpatch(exit_list, nextquad())
    backpatch_c(nextquad())


# while statement
def whileStat():
    lex()
    pointers_list = []
    bquad = nextquad()
    if (tokenType == "ParenthesesOpentk"):
        lex()
        C_place = condition()
        backpatch_c(nextquad() + 1)
        genquad("jump", "_", "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null ; // ( jump,_,_,null )\n"
        QUADS.quad_list_for_c.append(line_c)
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(
                line) + "\nExpected ')'' to close the expression in WhileStat() not " + tokenString)
            exit()
        else:
            lex()
            print(C_place[1] + "ddd")
            backpatch(C_place[1], nextquad())
            statements()
            backpatch_c(nextquad() + 1)
    else:
        print("Syntax Error in line: " + str(line) + "\nExpected '('' after ID in whileStat() not " + tokenString)
        exit()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement while must finish with semicolon not " + tokenString)
        exit()
    genquad("jump", "_", "_", bquad)
    backpatch(C_place[0], nextquad())
    line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_" + str(bquad) + " ; // ( jump,_,_," + str(bquad) + ")\n"
    QUADS.quad_list_for_c.append(line_c)


# assignment statement
def assignStat():
    ID = tokenString
    lex()
    if (tokenType != "assignmenttk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of assignment")
        exit()
    lex()
    E_place = expression()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(
            line) + "\nStatement assignment must finish with semicolon not " + tokenString)
        exit()
    genquad(":=", ID, "_", E_place)
    line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": " + str(ID) + " = " + str(E_place) + " ; // (:= ," + str(
        ID) + ",_," + str(E_place) + ")\n"
    QUADS.quad_list_for_c.append(line_c)


# if statement
def ifStat():
    lex()
    if (tokenType == "ParenthesesOpentk"):
        lex()
        C_place = condition()
        backpatch_c(nextquad() + 1)
        genquad("jump", "_", "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": goto L_null ; // ( jump,_,_,null )\n"
        QUADS.quad_list_for_c.append(line_c)
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(
                line) + "\nExpected ')'' to close the expression in IfStat() not " + tokenString)
            exit()
        lex()
        backpatch(C_place[1], nextquad())
        statements()
        backpatch(C_place[0], nextquad())
        backpatch_c(nextquad())
        #    ifList = makelist(nextquad())
        elsepart()
        # backpatch(ifList,nextquad())

    else:
        print("Syntax Error in line: " + str(line) + "\nExpected '('' after ID in IfStat() not " + tokenString)
        exit()


def elsepart():
    if (tokenString == "else"):
        lex()
        statements()
    else:
        pass


# call statement
def callStat():
    lex()
    if (tokenType != "idtk"):
        print("Syntax Error in line: " + str(
            line) + "\nExpected ID not " + tokenType + " ( " + tokenString + " ) after 'call' statement")
        exit()
    called_function_name = tokenString
    lex()
    if (tokenType == "ParenthesesOpentk"):
        actualparlist()
    else:
        print("Syntax Error in line: " + str(
            line) + "\nExpected '('' after to start actualparlist in call() not " + tokenString)
        exit()
    lex()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement else must fiish with semicolon not " + tokenString)
        exit()
    genquad("call", "", "_", called_function_name)


# input statement
def inputStat():
    lex()
    if (tokenType == "ParenthesesOpentk"):
        lex()
        if (tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected keyword inside 'input'")
            exit()
        ID_place = tokenString
        genquad("inp", ID_place, "_", "_")
        input = ': scanf("%f", &' + str(ID_place) + ")"
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + input + " ;// ( inp," + str(ID_place) + "_,_,)\n"
        QUADS.quad_list_for_c.append(line_c)

        lex()
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ') to close the expression 'input(ID)'")
            exit()
    else:
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of input(ID)")
        exit()
    lex()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement input must finish with semicolon not " + tokenString)
        exit()


# print statement
def printStat():
    lex()
    if (tokenType != "ParenthesesOpentk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of print()")
        exit()
    lex()
    E_place = expression()

    genquad("out", E_place, "_", "_")
    line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": printf(" + str(E_place) + "); // ( out," + str(
        E_place) + "_,_,)\n"
    QUADS.quad_list_for_c.append(line_c)

    lex()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement print must finish with semicolon not " + tokenString)
        exit()


# return statement
def returnStat():
    lex()
    if (tokenType != "ParenthesesOpentk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of return() - Does not open")
        exit()
    lex()
    E_place = expression()
    lex()
    if (check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement return must finish with semicolon not " + tokenString)
        exit()

    genquad("retv", E_place, "_", "_")
    line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": return " + str(E_place) + "; // ( retv," + str(
        E_place) + "_,_,)\n"
    QUADS.quad_list_for_c.append(line_c)


def check_statement_to_finish_with_semicolon():
    if (tokenType != "semicolontk"):
        return 0
    else:
        lex()
        return 1


def formalparlist():
    lex()
    while (formalparitem() == 1):
        if (tokenType == "commatk"):
            lex()
            continue
        elif (tokenType == "ParenthesesClosetk"):
            lex()
            break
        else:
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of formalparlist )'")
            exit()


def formalparitem():
    if (tokenString == "in"):


        lex()
        if (tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID after 'inout' or 'in' )'")
            exit()
        else:
            genquad("par", tokenString, "CV", "_")
            lex()
            return 1
    elif (tokenString == "inout"):

        lex()
        if (tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID after 'inout' or 'in' )'")
            exit()
        else:
            genquad("par", tokenString, "REF", "_")
            lex()
            return 1
    else:
        return 0


def actualparlist():
    lex()
    while (actualparitem() == 1):

        if (tokenType == "ParenthesesClosetk"):
            break
        lex()
        while (tokenType == "commatk"):
            lex()
            continue


def actualparitem():
    if (tokenString == "in"):
        argument = tokenString
        lex()
        E_place = expression()
        addNewPar(E_place,"cv")
        addArgument(argument)
        genquad("par", E_place, "CV", "_")
        return 1
    elif (tokenString == "inout"):
        argument = tokenString
        lex()
        if (tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID after 'inout')'")
            exit()
        else:
            genquad("par", tokenString, "REF", "_")
            lex()
            addNewPar(tokenString,"ref")
            addArgument(argument)
            return 1
    else:
        return 0


def condition():
    BT_place = boolterm()
    C_place = BT_place

    if (tokenType == "ParenthesesClosetk"):
        # backpatch_c(nextquad()+ 1)
        #    genquad("jump", "_", "_", "_")
        #    line_c = "L_"+str(len(QUADS.quad_list) - 1)+": goto L_null ; // ( jump,_,_,null )\n"
        #    QUADS.quad_list_for_c.append(line_c)
        return C_place
    lex()
    while (tokenString == "or"):
        lex()
        backpatch(C_place[0], nextquad())
        BT_place = boolterm()
        C_place[0] = BT_place[0]
        C_place[1] = merge(C_place[1], BT_place[1])
        lex()
    return C_place


def boolterm():
    BF_place = boolfactor()
    BT_place = BF_place
    while (tokenString == "and"):
        backpatch(BT_place[1], nextquad())
        BF_place = boolfactor()
        BT_place[1] = BF_place[1]
        BT_place[0] = merge(BT_place[0], BF_place[0])
    return BT_place


def boolfactor():
    BF_place = [[], []]  # lista apoteloumenh apo 2 listes ( h prwth gia false h deuterh gia true)
    if (tokenString == "not"):
        lex()
        if (tokenType != "bracketOpentk"):
            print("Syntax Error in line: " + str(line) + "\nExpected '[' before condition")
            exit()
        lex()
        C_place = condition()
        if (tokenType != "bracketClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ']' before closing")
            exit()
        BF_place[1] = C_place[0]
        BF_place[0] = C_place[1]
        return BF_place
    elif (tokenType == "bracketOpentk"):
        C_place = condition()
        if (tokenType != "bracketClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ']' before closing")
            exit()
        return C_place
    else:
        E1_place = expression()
        RO_place = REL_OP()
        E2_place = expression()

        BF_place[1] = makelist(nextquad())
        genquad(RO_place, E1_place, E2_place, "_")
        BF_place[0] = makelist(nextquad())
        # genquad("jump", "_", "_", "_")
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": if (" + str(E1_place) + " " + str(RO_place) + " " + str(
            E2_place) + ") goto L_null // (" + str(RO_place) + "," + str(E1_place) + "," + str(E2_place) + ",null )\n"
        QUADS.quad_list_for_c.append(line_c)
        return BF_place


def expression():
    OS_place = optional_sign()
    T1_place = term()
    while (1):
        if (tokenType == "semicolontk"):
            break
        if (tokenType == "idtk"):
            break
        if (ADD_OP() == 1):
            while (ADD_OP() == 1):
                op = tokenString
                lex()
                T2_place = term()
                w = newtemp()
                genquad(op, T1_place, T2_place, w)
                line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": " + str(w) + " = " + str(T1_place) + " " + str(
                    op) + " " + str(T2_place) + "; //(" + str(op) + "," + str(T1_place) + "," + str(T2_place) + str(
                    w) + ")\n"
                QUADS.quad_list_for_c.append(line_c)
                T1_place = w

                if (tokenType == "ParenthesesClosetk"):
                    break
                lex()
        if (tokenString in SINGLE_TOKENS_LIST):
            break
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
            exit()
    return T1_place


def term():
    F1_place = factor()
    while (MUL_OP() == 1 or ADD_OP() == 1):
        op = tokenString
        lex()
        F2_place = factor()
        w = newtemp()
        genquad(op, F1_place, F2_place, w)
        line_c = "L_" + str(len(QUADS.quad_list) - 1) + ": " + str(w) + " = " + str(F1_place) + " " + str(
            op) + " " + str(F2_place) + "; // (" + str(op) + "," + str(F1_place) + ",_," + str(F2_place) + "," + str(
            w) + ")\n"
        QUADS.quad_list_for_c.append(line_c)
        F1_place = w
    return F1_place


def factor():
    if (tokenType == "numbertk"):
        T = tokenString
        lex()
        return T
    elif (tokenType == "idtk"):
        ID_place = idtail()
        return ID_place
    else:  # EXPRESSION
        if (tokenType != "ParenthesesOpentk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
            exit()
        E_place = expression()
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
            exit()
        return E_place


def idtail():
    global w

    if (tokenString in VARLIST):
        T = tokenString
        lex()
        return T
    else:
        var = tokenString
    called_function_name = tokenString
    lex()
    if (tokenType == "ParenthesesOpentk"):
        actualparlist()
        w = newtemp()
        genquad("par", w, "RET", "_")
        genquad("call", "_", "_", called_function_name)
        if (tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of actualparlist, does not close")
            exit()
        lex()
        return w
    # else:
    #    print("Error in line: " + str(line) + "\nVariable is not defined : "+ var)
    #    exit()

    return var


# symbols + and - (are optional)
def optional_sign():
    if (ADD_OP() == 1):
        lex()
    else:
        pass


def ADD_OP():
    if (tokenString == "+" or tokenString == "-"):
        return 1
    return 0


def MUL_OP():
    if (tokenString == "*" or tokenString == "/"):
        return 1
    return 0


def REL_OP():
    if (tokenString == "="):
        relop_buffer = tokenString
        lex()
        return relop_buffer
    elif (tokenType == "lesstk"):
        relop_buffer = tokenString
        lex()
        if (tokenType == "greatertk" or tokenString == "="):
            relop_buffer += tokenString
            lex()
        return relop_buffer
    elif (tokenType == "greatertk"):
        relop_buffer = tokenString
        lex()
        if (tokenString == "="):
            relop_buffer += tokenString
            lex()
        return relop_buffer
    else:
        print("Syntax Error in line: " + str(
            line) + "\nYou must have REL_OP between expressions in boolfactor() not " + tokenType)
        exit()


###################################### LEXICAL ANALYSIS #########################################

def newSymbol():
    global char
    global line

    char = input.read(1)
    if (char == '\n'):
        line += 1


def lex():
    global char
    global tokenString
    global line

    while (True):

        if (add_char_to_buffer() == 1):
            break
        BUFFERS.state = AUTO[BUFFERS.state][BUFFERS.charType]
        if (BUFFERS.state == -1):
            potential_num()
            check_state()
            break
        elif (BUFFERS.state == -2):
            potential_ID_or_Keyword()
            check_state()
            break
        check_state()


def check_if_EOF_after_dot():
    newSymbol()
    while (char == "\n" or char == "\t" or char == " "):
        newSymbol()
    if not char:
        print("COMPILE SUCCESSFUL COMPLETE!\n")
        genquad("halt", "_", "_", "_")
        genquad("end_block", program_name, "_", "_")
        if FLAG.program_includes_fun_or_prod == 0:
            line_c = "L_" + str(len(QUADS.quad_list) - 1) + ":\n"
            QUADS.quad_list_for_c.append(line_c)
            create_c_file()
        create_int_file()
        input.close()
        exit(1)
    else:
        print("ERROR line: " + str(line) + "\nProgram must finish with '.'")
        exit()


def check_if_programm_ends_with_dot():
    if (BUFFERS.char_buffer == '.'):
        print("COMPILE SUCCESSFUL COMPLETE!\n")
        genquad("halt", "_", "_", "_")
        genquad("end_block", program_name, "_", "_")
        if FLAG.program_includes_fun_or_prod == 0:
            line_c = "L_" + str(len(QUADS.quad_list) - 1 + ": \n")
            QUADS.quad_list_for_c.append(line_c)
            create_c_file()
        input.close()
        create_int_file()   
        exit(1)
    else:
        print("ERROR line: " + str(line) + "\nProgram must finish with '.'")
        exit()


def add_char_to_buffer():
    global char
    global comment_state
    global tokenType
    global tokenString

    if (BUFFERS.char_buffer in SINGLE_TOKENS_LIST):
        BUFFERS.charType = find_char_type(BUFFERS.char_buffer)
        tokenString = BUFFERS.char_buffer
        BUFFERS.char_buffer = ''
        return 1
    if (BUFFERS.assigment_buffer == ":="):
        tokenType = "assignmenttk"
        tokenString = ":="
        BUFFERS.assigment_buffer = ""
        return 1
    newSymbol()
    BUFFERS.charType = find_char_type(char);
    if (BUFFERS.charType == 13):
        cross_comment()
    if (BUFFERS.charType == 12):
        check_if_EOF_after_dot()
    if not char:
        check_if_programm_ends_with_dot()
    if (BUFFERS.charType == -1):
        print("ERROR line:" + str(line) + "\nChar:" + char + " is not belongs to alphabet")
        exit()
    if (BUFFERS.assigment_buffer == ":" and char != "="):
        print("ERROR line: " + str(line) + "\nCharacter '=' must exist after character ':' ")
        exit()
    elif (BUFFERS.assigment_buffer == ':' and char == '='):
        BUFFERS.assigment_buffer += char
        BUFFERS.state = 5
        check_state()
        return 0
    elif (BUFFERS.charType == 0 or BUFFERS.charType == 1):
        BUFFERS.word_buffer += char  # word_buffer only stores numbers , strings and ':'
    elif (BUFFERS.charType == 5):
        BUFFERS.assigment_buffer = ":"
    if (BUFFERS.charType != 18):
        BUFFERS.char_buffer = char
    return 0


def check_state():
    global BUFFERS
    global tokenString

    if (BUFFERS.state == 6):  # error
        print("ERROR line: " + str(line) + "\nBecause of: " + BUFFERS.word_buffer)
        exit()
    elif (BUFFERS.state == 5):  # OK
        tokenString = BUFFERS.word_buffer
        BUFFERS.word_buffer = ''


def cross_comment():
    global line
    global charType
    global char
    global tokenType

    comment_line = line
    newSymbol()
    while (char != "#"):
        if not char:
            print("ERROR line :" + str(comment_line) + "\nWrong syntax of comment")
            exit()
        newSymbol()
        BUFFERS.charType = find_char_type(char);


def potential_num():
    global BUFFERS
    global tokenType

    if not (BUFFERS.word_buffer.isnumeric()):
        print("ERROR line :" + str(line) + "\nKeyword cant start with number : ( " + word_buffer + " )")
        exit()
    if (int(BUFFERS.word_buffer) > -4294967295 or int(BUFFERS.word_buffer) < 4294967295):
        tokenType = "numbertk"
        BUFFERS.state = 5
    else:
        print("ERROR line: " + str(line) + "\nNumber is not between -(2^32-1) and (2^32-1)")
        exit()


def potential_ID_or_Keyword():
    global tokenType
    global BUFFERS

    if (BUFFERS.word_buffer in ID_words):
        tokenType = "keywordtk"
        BUFFERS.state = 5
    elif (len(BUFFERS.word_buffer) < 30):
        tokenType = "idtk"
        BUFFERS.state = 5
    else:
        print("ERROR line: " + str(line) + "\nThe length of the string is more than 30")
        exit()


def find_char_type(c):
    global tokenType

    if (c.isalpha()):
        tokenType = ""
        return 0
    elif (c.isdigit()):
        tokenType = ""
        return 1
    elif (c == '+' or c == '-' or c == '*' or c == '/'):
        tokenType = "arithmetictk"
        return 2
    elif (c == ';'):
        tokenType = "semicolontk"
        return 3
    elif (c == ','):
        tokenType = "commatk"
        return 4
    elif (c == ':'):
        return 5
        tokenType = ""
    elif (c == '['):
        tokenType = "bracketOpentk"
        return 6
    elif (c == ']'):
        tokenType = "bracketClosetk"
        return 7
    elif (c == '{'):
        tokenType = "BracesOpentk"
        return 8
    elif (c == '}'):
        tokenType = "BracesClosetk"
        return 9
    elif (c == '('):
        tokenType = "ParenthesesOpentk"
        return 10
    elif (c == ')'):
        tokenType = "ParenthesesClosetk"
        return 11
    elif (c == '.'):
        tokenType = "dottk"
        return 12
    elif (c == '#'):
        tokenType = "commenttk"
        return 13
    elif (c == '<'):
        tokenType = "lesstk"
        return 14
    elif (c == '>'):
        tokenType = "greatertk"
        return 15
    elif (c == '='):
        tokenType = ""
        return 16
    elif (not c):
        tokenType = ""
        return 17
    elif (c == " " or c == '\n' or c == '\t'):
        tokenType = "whiteSpacetk"
        return 18
    else:
        tokenType = ""
        return -1  # char is not in alphabet


ID_words = ["program", "if", "switchcase", "not", "function", "input", "declare",
            "else", "forcase", "and", "procedure", "print", "while", "incase", "or",
            "call", "case", "default", "return", "in", "inout"]

if __name__ == "__main__":
    main(sys.argv[1:])

# STRUCTURE OF AUTO ARRAY

# LETTERS - NUMBERS - (+-*/) - ; - , - : - [ - ] - { - } - ( - ) - . -  # - < - > - = - EOF - (white spaces)
# start = 0
# rem = 1
# asgn = 2
# dig = 3
# idk = 4
# OK =  5
# ERROR = 6
# smaller =  7
# larger =  8
# -1 pn
# -2 pik
