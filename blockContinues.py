import sys

def main(argv):
    global line
    global input
    global word_buffer
    global tokenType
    global tokenString
    global charType
    global char_buffer
    global next_quad_number
    global quad_list
    global temp_counter

    temp_counter = 0
    quad_list = []
    next_quad_number = 0
    charType = ''
    tokenType = ''
    tokenString = ''
    word_buffer = ''
    char_buffer = ''
    line = 1
    #file = list(sys.argv)
    #inputFile = file[1]

    if(len(argv) == 0 ):
        input = open("cimple.ci", "r")
    else:
        input = open(argv[0], "r")
    program()
###################################### INTERMEDIATE CODE #########################################

# returns the number of the next quad
def nextquad():
    global next_quad_number
    next_quad_number += 1
    return next_quad_number

# generates the new quand
def genquad(op, x, y, z):

    new_quad = [next_quad_number , op , x , y , z]
    #quad_list.append(new_quad)
    return new_quad


# creates and returns a new temporary variable
# the temporary changes are of the form T_1, T_2, T_3 ...
def newtemp():

    temp_counter += 1 # na thhmithw otan kleinei ena block na to mhdenizw
    new_temp = 'T_%s' % temp_counter
    return new_temp


# creates a blank list of labels
def emptylist():
    new_quad = [next_quad_number , "_" , "_" , "_" , "_"]
    #quad_list.append(new_quad)
    return new_quad

# creates a list of labels containing only x
def makelist(x):
    new_quad = [next_quad_number , "_" , x , "_" , "_"]

# creates a list of labels from the merge of list 1 and list 2
#def merge(list 1 , list 2 )

# the list consists of indices in quads whose last end is not is completed
# The backpatch visits these quads one by one and completes them with the z tag
#def backpatch(list,z):


###################################### GRAMMAR ANALYSIS #########################################
def program():
    global tokenType
    lex()
    if(tokenString == "program"):
        lex()
        if(tokenType == "idtk"):
            block()
        else:
            print("Syntax Error line: " + str(line) + "\nProgram name expected")
            exit()
    else:
        print ("Syntax Error line: " + str(line)+ "\nThe keyword ' program' expected")
        exit()

def block():
    lex()
    declarations()
    subprograms()
    lex()
    while(1):
        statements()
        if(tokenString == "}"):
            lex()


def declarations():

    while(tokenString == "declare"):
        while(1):
            lex()
            if(tokenType == "idtk"):
                if(tokenString not in varlist):
                    varlist.append(tokenString)
                else:
                    print("ERROR line: " + str(line) + "\nYou can't declare the same id multiple times" + tokenString)
                    exit()
            else:
                print("Syntax Error in line: " + str(line) + "\nExpected ID not "+tokenType +" ( "+tokenString + " )")
                exit()
            lex()
            if(tokenType == "commatk"):
                continue
            if(tokenType == "semicolontk"):
                lex()
                break
            else:
                print("Syntax Error in line: " + str(line) + "\nWrong syntax of declaration")
                exit()
        continue

def subprograms():

    while(tokenString == "function" or tokenString == "procedure"):
        lex()
        if(tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID not "+tokenType +" ( "+tokenString + " ) after function/procedure")
            exit()
        lex()
        if(tokenType != "ParenthesesOpentk"):
            print("Syntax Error in line: " + str(line) + "\nExpected to open Parentheses")
            exit()
        formalparlist()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected to close Parentheses")
            exit()
        block()


# 1 or more statements
def statements():

#    genquad("begin_block",name,"_","_")
    if(tokenType == "BracesOpentk"):
        lex()
        while(1):
            statem = tokenString
            statement()
            if(tokenType == "BracesClosetk"):
                lex()
                if(tokenType != "semicolontk"):
                    print("Syntax Error in line: " + str(line) + "\nStatement "+statem+" must finish with semicolon not "+ tokenString)
                    exit()
                break
            else:
                continue
    else:
        statem = tokenString
        statement()




#one statement
def statement():

    print( "-------------------------------------------------------------------\nSTATEMENT : " + tokenString +"\n")
    if(tokenString == 'if'):
        ifStat()
    if(tokenString == "while"):
        whileStat()
    elif(tokenString == "switchcase"):
        switchcaseStat()
    elif(tokenString == "forcase"):
        forcaseStat()
    elif(tokenString == "incase"):
        incaseStat()
    elif(tokenString == "call"):
        callStat()
    elif(tokenString == "return"):
        returnStat()
    elif(tokenString == "input"):
        inputStat()
    elif(tokenString == "print"):
        printStat()
    elif(tokenType == "idtk"):
        assignStat()
    else:
        pass
def incaseStat():
    print("mphka INCASE me: " + tokenString)
    lex()
    c = 0
    while(tokenString == "case"):
        c+=1
        lex()
        if(tokenType == "ParenthesesOpentk"):
            lex()
            condition()
            if(tokenType == "ParenthesesClosetk"):
                lex()
                statements()
                if(check_statement_to_finish_with_semicolon() == 0):
                    print("Syntax Error in line: " + str(line) +  "\nStatement incase must finish with semicolon not "+ tokenString)
                    exit()
            else:
                print("Syntax Error in line: " + str(line) + "\nExpected ')' to close the expression in IncaseStat() not "+tokenString)
                exit()
        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '(' after ID in IncaseStat() not "+tokenString)
            exit()

    print(str(c) + " cases for incase")
    print("vgainw apo incase me " + tokenString)


def forcaseStat():
    print("mphka forcase me "+tokenString)
    lex()
    c = 0
    while(tokenString == "case"):
        c +=1
        lex()
        if(tokenType == "ParenthesesOpentk"):
            lex()
            condition()
            if(tokenType != "ParenthesesClosetk"):
                print("Syntax Error in line: " + str(line) + "\nExpected ')'' to close the expression in forcaseStat() not "+tokenString)
                exit()
            else:
                lex()
                statements()
                if(check_statement_to_finish_with_semicolon() == 0):
                    print("Syntax Error in line: " + str(line) +  "\nStatement forcase must finish with semicolon not "+ tokenString)
                    exit()
        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '('' to open case not "+tokenString)
            exit()
    print(str(c) + " cases for forcecase")
    if(tokenString != "default"):
        print("Syntax Error in line: " + str(line) + "\nYou must have 'default' case at forcase")
        exit()
    lex()
    statements()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) +  "\nStatement forcase must finish with semicolon not "+ tokenString)
        exit()

def switchcaseStat():
    print("mphka switch me "+tokenString)
    lex()
    c = 0
    while(tokenString == "case"):
        c += 1
        lex()
        if(tokenType == "ParenthesesOpentk"):
            lex()
            condition()
            if(tokenType != "ParenthesesClosetk"):
                print("Syntax Error in line: " + str(line) + "\nExpected ')'' to close the expression in switchcaseStat() not "+tokenString)
                exit()
            else:
                lex()
                statements()
                if(check_statement_to_finish_with_semicolon() == 0):
                    print("Syntax Error in line: " + str(line) +  "\nStatement switchcase must finish with semicolon not "+ tokenString)
                    exit()
        else:
            print("Syntax Error in line: " + str(line) + "\nExpected '('' to open case not "+tokenString)
            exit()
    print(str(c) + " cases for switchcase")
    if(tokenString != "default"):
        print("Syntax Error in line: " + str(line) + "\nYou must have 'default' case at switchcase")
        exit()
    lex()
    statements()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement switchcase must finish with semicolon not "+ tokenString)
        exit()

# while statement
def whileStat():
    print("mphka while me "+tokenString)
    lex()
    if(tokenType == "ParenthesesOpentk"):
        lex()
        condition()
        lex()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ')'' to close the expression in WhileStat() not "+tokenString)
            exit()
        else:
            lex()
            statements()
    else:
        print("Syntax Error in line: " + str(line) + "\nExpected '('' after ID in whileStat() not "+tokenString)
        exit()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement while must finish with semicolon not "+ tokenString)
        exit()


# assigment statement
def assignStat():
    print("mphka assigment me "+tokenString)
    lex()
    if(tokenType != "assignmenttk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of assigment")
        exit()
    lex()
    expression()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement assignment must finish with semicolon not "+ tokenString)
        exit()


# if statement
def ifStat():
    print("mphka if me: " + tokenString)
    lex()
    if(tokenType == "ParenthesesOpentk"):
        lex()
        condition()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ')'' to close the expression in IfStat() not "+tokenString)
            exit()
        lex()
        statements()
        if(check_statement_to_finish_with_semicolon() == 0):
            print("Syntax Error in line: " + str(line) + "\nStatement if must fiish with semicolon not "+ tokenString)
            exit()
        elsepart()
    else:
        print("Syntax Error in line: " + str(line) + "\nExpected '('' after ID in IfStat() not "+tokenString)
        exit()

    print("vgainw apo if me: " + tokenString)

def elsepart():
    print("mpainw elsepart me: " + tokenString)
    if(tokenString == "else"):
        lex()
        statements()
        if(check_statement_to_finish_with_semicolon() == 0):
            print("Syntax Error in line: " + str(line) + "\nStatement else must fiish with semicolon not "+ tokenString)
            exit()

    else:
        pass
    print("vgainw apo elsepart me: " + tokenString)   #maria


# call statement
def callStat():
    print("mphka call stat me : " + tokenString)
    lex()
    if(tokenType != "idtk"):
        print("Syntax Error in line: " + str(line) + "\nExpected ID not "+tokenType +" ( "+tokenString + " ) after 'call' statement")
        exit()
    lex()
    if(tokenType == "ParenthesesOpentk"):
        actualparlist()
    else:
        print("Syntax Error in line: " + str(line) + "\nExpected '('' after to start actualparlist in call() not "+tokenString)
        exit()

# input statement
def inputStat():
    lex()
    if(tokenType == "ParenthesesOpentk"):
        lex()
        if(tokenType != "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected keyword inside 'input'")
            exit()
        lex()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ') to close the expression 'input(ID)'")
            exit()
    else:
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of input(ID)")
        exit()
    lex()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement input must finish with semicolon not "+ tokenString)
        exit()

# print statement
def printStat():
    lex()
    if(tokenType != "ParenthesesOpentk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of print()")
        exit()
    lex()
    expression()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement print must finish with semicolon not "+ tokenString)
        exit()

# return statement
def returnStat():
    lex()
    if(tokenType != "ParenthesesOpentk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of return() - Does not open")
        exit()
    lex()
    expression()
    if(check_statement_to_finish_with_semicolon() == 0):
        print("Syntax Error in line: " + str(line) + "\nStatement return must finish with semicolon not "+ tokenString)
        exit()




def check_statement_to_finish_with_semicolon():

    if(tokenType != "semicolontk"):
        return 0
    else:
        lex()
        return 1

def formalparlist():

    lex()
    if(formalparitem() == 1):
        lex()
        while(tokenType == "commatk"):
            formalparitem()
    else:
        pass

def formalparitem():
    if(tokenString == "inout" or tokenString == "in"):
        lex()
        if(tokenType!= "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID after 'inout')'")
            exit()
        else:

            return 1
    else:
        return 0


def actualparlist():
    print("mphka actualparlist me "+tokenString)
    lex()
    while(actualparitem() == 1):
        if(tokenType == "ParenthesesClosetk"):
            break
        lex()
        while(tokenType == "commatk"):
            lex()
            continue
    print("vaginw actualparlist me "+tokenString)

def actualparitem():
    print("mphka actualparitem me "+tokenString)
    if(tokenString == "in"):
        lex()
        expression()
        return 1
    elif(tokenString == "inout"):
        lex()
        if(tokenType!= "idtk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ID after 'inout')'")
            exit()
        else:
            return 1
    else:
        return 0

def condition():
    print("mphka condition me "+tokenString)
    boolterm()
    if(tokenType == "ParenthesesClosetk"):
        return
    lex()
    while(tokenString == "or"):
        lex()
        boolterm()
        lex()

def boolterm():
    print("mphka boolterm me "+tokenString)
    boolfactor()
    while(tokenString == "and"):
        boolfactor()

def boolfactor():
    print("mphka boolfactor me "+tokenString)
    if(tokenString == "not"):
        lex()
        if(tokenType != "bracketOpentk"):
            print("Syntax Error in line: " + str(line) + "\nExpected '[' before condition")
            exit()
        lex()
        condition()
        if(tokenType != "bracketClosetk"):
            print("Syntax Error in line: " + str(line) + "\nExpected ']' before closing")
            exit()
    elif(tokenType == "bracketOpentk"):
        condition()
        if(tokenType != "bracketClosetk"):
                print("Syntax Error in line: " + str(line) + "\nExpected ']' before closing")
                exit()
    else:
        expression()
        REL_OP()
        expression()


def expression():
    print("\nmphka expresion me "+tokenString + "\n")
    optional_sign()
    term()
    if(tokenType == "ParenthesesClosetk"):
        print("\nvgainw expresion1 me "+tokenString + "\n")
        lex()
        if(tokenType == "BracesOpentk"):
            input.seek(input.tell()-5,0)
            lex()
            return
    if(tokenType == "semicolontk"):
        print("\nvgainw expresion2 me "+tokenString + "\n")
        return
    if(tokenType == "idtk"):
        print("\nvgainw expresion3 me "+tokenString + "\n")
        return
    if(ADD_OP() == 1):
        while(ADD_OP() == 1):
            print(tokenString)
            lex()
            term()
            if(tokenType == "ParenthesesClosetk"):
                break
            lex()
    if(tokenString in single_tokens_list):
        print("\nvgainw expresion4 me "+tokenString + "\n")
        return
    if(tokenType != "ParenthesesClosetk"):
        print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
        exit()
    print("\nvgainw expresion me "+tokenString + "\n")

def term():
    print("mphka term me "+tokenString)
    factor()
    while(MUL_OP() == 1 or ADD_OP() == 1): #h grammatikh leei mono gia MUL alla den exei nohma
        print(tokenString)
        lex()
        factor()


def factor():
    print("mphka factor me "+tokenString)
    if(tokenType == "numbertk"):  #INTEGER
        lex()
    elif(tokenType == "idtk"):
        idtail()
    else: #EXPRESSION
        if(tokenType != "ParenthesesOpentk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
            exit()
        expression()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of expresion")
            exit()
def idtail():
    print("mphka idtail me "+tokenString)
    if(tokenString in varlist):
        lex()
        return
    lex()
    if(tokenType == "ParenthesesOpentk"):
        actualparlist()
        if(tokenType != "ParenthesesClosetk"):
            print("Syntax Error in line: " + str(line) + "\nWrong syntax of actualparlist, does not close")
            exit()
    else:
        pass
# symbols + and - (are optional)
def optional_sign():
    if(ADD_OP() == 1):
        lex()
    else:
        pass
        #PREPEI OPWSDHPOTE 1/3
def ADD_OP():
    if(tokenString == "+" or tokenString == "-"):
        return 1
    return 0
def MUL_OP():
    if(tokenString == "*" or tokenString == "/"):
        return 1
    return 0

def REL_OP():

    if(tokenString == "=" ):
        lex()
    elif(tokenType == "lesstk"):
        lex()
        print(tokenString)
        if(tokenType == "greatertk" or tokenString == "="):
            lex()
    elif(tokenType == "greatertk"):
        lex()
        if(tokenString == "="):
            lex()
    else:
        print("Syntax Error in line: " + str(line) + "\nYou must have REL_OP between expressions in boolfactor() not "+tokenType)
        exit()

###################################### LEXICAL ANALYSIS #########################################

def newSymbol():
    global char
    global line

    char = input.read(1)
    if(char == '\n'):
        line +=1

def lex():
    global char
    global charType
    global word_buffer
    global tokenString
    global state
    global line

    state = 0
    while(True):

        if(add_char_to_buffer() == 1):
            break
        #print("state: "+str(state) +  " type: "+ str(charType) +" "+ word_buffer )
        state = auto[state][charType]
        if(state == -1):
            potential_num()
            check_state()
            break
        elif(state == -2):
            potential_ID_or_Keyword()
            check_state()
            break
        check_state()

def check_if_EOF_after_dot():
    newSymbol()
    while(char== "\n" or char == "\t" or char ==" "):
        newSymbol()
    if not char:
        print("COMPILE SUCCESSFUL COMPLETE!" )
        exit(1)
    else:
        print("ERROR line: "+str(line) + "\nProgram must finish with '.'")
        exit()

def check_if_programm_ends_with_dot():
    if(char_buffer == '.'):
        print("COMPILE SUCCESSFUL COMPLETE!" )

        exit(1)
    else:
        print("ERROR line: "+str(line) + "\nProgram must finish with '.'")
        exit()
def add_char_to_buffer():
    global char
    global word_buffer
    global comment_state
    global state
    global charType
    global tokenType
    global tokenString
    global char_buffer

    if(char_buffer in single_tokens_list):
        charType = find_char_type(char_buffer)
        tokenString = char_buffer
        char_buffer = ''
        return 1
    newSymbol()
    charType = find_char_type(char);
    #print("char : "+ char+ " string: "+ tokenString + " type: " + str(tokenType))
    if(charType == 13):
        cross_comment()
    if(charType == 12):
        check_if_EOF_after_dot()
    if not char:
        check_if_programm_ends_with_dot()
    if(charType == -1):
        print("ERROR line:" + str(line) + "\nChar:" + char + " is not belongs to alphabet")
        exit()
    if(word_buffer == ":" and char!= "="):
        print("ERROR line: " + str(line) + "\nCharacter '=' must exist after character ':' ")
        exit()
    elif(word_buffer == ':' and char == '='):
        word_buffer += char # dhladh o word_buffer periexei to :=
        tokenType = "assignmenttk"
        state = 5
        check_state()
        return 1
    elif(charType == 0 or charType == 1 or charType == 5 ): #krataw ston word_buffer mono arithmous,strings kai ton xarakthra :
        word_buffer += char
    if(charType != 18):
            char_buffer = char
    return 0

def check_state():

    global state
    global tokenString
    global word_buffer

    if(state == 6): #error
        print("ERROR line: " + str(line) +"\nBecause of: " + word_buffer)
        exit()
    elif(state == 5): #OK
        tokenString = word_buffer
        word_buffer = ''

def cross_comment():

    global line
    global charType
    global char
    global tokenType

    comment_line = line
    newSymbol()
    while(char != "#"):
        if not char:
            print("ERROR line :"+str(comment_line)+"\nWrong syntax of comment")
            exit()
        newSymbol()
        charType = find_char_type(char);

def potential_num():
    global state
    global tokenType

    if not (word_buffer.isnumeric()):
        print("ERROR line :" + str(line) + "\nKeyword cant start with number : ( " +word_buffer+" )" )
        exit()
    if(int(word_buffer) > -4294967295 or int(word_buffer) < 4294967295 ):
        tokenType = "numbertk"
        state = 5
    else:
        print("ERROR line: " + str(line) + "\nNumber is not between -(2^32-1) and (2^32-1)")
        exit()

def potential_ID_or_Keyword():
    global tokenType
    global state

    if(word_buffer in ID_words):
        tokenType = "keywordtk"
        state = 5
    elif(len(word_buffer) < 30):
        tokenType= "idtk"
        state = 5
    else:
        print("ERROR line: " + str(line) + "\nThe length of the string is more than 30")
        exit()

def find_char_type(c):

    global tokenType

    if(c.isalpha()):
        tokenType = ""
        return 0
    elif(c.isdigit()):
        tokenType = ""
        return 1
    elif(c == '+' or c =='-' or c == '*' or c == '/'):
        tokenType = "arithmetictk"
        return 2
    elif(c == ';'):
        tokenType  = "semicolontk"
        return 3
    elif(c == ','):
        tokenType = "commatk"
        return 4
    elif(c == ':'):
        return 5
        tokenType = ""
    elif(c == '['):
        tokenType = "bracketOpentk"
        return 6
    elif(c == ']'):
        tokenType = "bracketClosetk"
        return 7
    elif(c == '{'):
        tokenType = "BracesOpentk"
        return 8
    elif(c == '}'):
        tokenType = "BracesClosetk"
        return 9
    elif(c == '('):
        tokenType = "ParenthesesOpentk"
        return 10
    elif(c == ')'):
        tokenType = "ParenthesesClosetk"
        return 11
    elif(c == '.'):
        tokenType = "dottk"
        return 12
    elif(c == '#'):
        tokenType ="commenttk"
        return 13
    elif(c == '<'):
        tokenType = "lesstk"
        return 14
    elif(c == '>'):
        tokenType = "greatertk"
        return 15
    elif(c == '='):
        tokenType = ""
        return 16
    elif(not c):
        tokenType = ""
        return 17
    elif(c == " " or c == '\n' or c == '\t'):
        tokenType = "whiteSpacetk"
        return 18
    else:
        tokenType = ""
        return -1 #char is not in alphabet
#start = 0
#rem = 1
#asgn = 2
#dig = 3
#idk = 4
#OK =  5
#ERROR = 6
#smaller =  7
#larger =  8
#-1 pn
#-2 pik
# 0 grammata 1 arithmoi 2+-*/ 3; 4,  5: 6[ 7] 8{ 9 10 ( 11) 12. 13 # 14< 15> 16 = 17 EOF 18 tab space \n
ID_words= ["program","if","switchcase","not","function","input","declare",
            "else","forcase","and","procedure","print","while","incase","or",
            "call","case", "default","return","in","inout"]
single_tokens_list = [",",";","+","-","*","/",")","(","[","]","{","}",">","<","="]
auto = [
[4,3,5,5,5,2,5,5,5,5,5,5,5,0,7,8,5,5,5],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,6,1],
[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,6,6],
[-1,3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[4,4,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
[4,3,0,0,0,2,0,0,0,0,0,0,5,0,0,0,0,0,5],
[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
[5,5,5,5,5,5,5,5,5,5,5,5,5,6,5,5,5,5,5],
[5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,5,5,5,5],
]
varlist = []


if __name__ == "__main__":
    main(sys.argv[1:])
