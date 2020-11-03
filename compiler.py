#################################################
####    GEORGIOS DIMOPOULOS     #################   
####    A.M. 2964               #################
####    username: cse52964      #################
####    NIKOLAS LAMPROS         #################
####    A.M. 2922               #################
####    username: cse42922      #################
#################################################

import sys

#################################################
###########   LEKTIKOS ANALYTHS   ###############
#################################################
        

def lex():
    
    global state 
    global file_pointer
    global line
    
    # flags
    OK = -1
    EOF = -2
    error = -3
    
    # initialization
    word = ""
    letters = [] 
    W = []

    # go to the last readen word 
    f.seek(file_pointer)
    
    # start 
    state = 0
    
    while(state != OK and state != EOF and state != error):
       
        char = f.read(1)
        if (char == "\n"):
            line += 1
        
        if (not char and state != 6):
              if (state == 1):
                    state = OK
                    word = "".join(letters)
                    W += [word] + [1]
              elif (state == 2):
                    state = OK
                    word = "".join(letters)
                    if word in standard_words: # check if the word is a standard word
                        W += [word] + [100]    
                    else:
                        W += [word] + [2] 

              else:
                    state = EOF

        #STATE 0 
        if (state == 0):
            if(char == "\t" or char == " " or char == "\n" or char == "\r"):    
                state = 0
            elif(char.isdigit()):
                state = 1
            elif(char.isalpha()):
                state = 2
            elif(char == "<"):
                state = 3
            elif(char == ">"):
                state = 4
            elif(char == ":"):
                state = 5
            elif(char == "/"):
                state = 6
            elif(char == ""):
                state = EOF
            else:
                state = OK
                
                letters.append(char)
                word = "".join(letters)  
                
                if (char == "+"):
                    W += [word] + [3]
                elif (char == "-"):
                      W += [word] + [4]   
                elif (char == '*'):
                    W += [word] + [5]   
                elif (char == '='):
                    W += [word] + [6]
                elif (char == ';'):
                  W += [word] + [7]
                elif (char == ','):
                    W += [word] + [8]
                elif (char == '('):
                      W += [word] + [9]
                elif (char == ')'):
                      W += [word] + [10]
                elif (char == '['):
                      W += [word] + [11]
                elif (char == ']'):
                      W += [word] + [12]
                else:
                      state=error
                      print("ERROR: invalid symbol")
                      print("Line:",line)
                      exit(1)
                    
                    
        #   STATE 1 ---> CHAR IS A DIGIT    
        if (state == 1):          
            if (char.isdigit()):
                state = 1
                letters.append(char)
            else:
                word = "".join(letters)              
                if (int(word) > -32767 and int(word) < 32767):
                    state = OK
                    W += [word] + [1]    
                else:
                    state = error
                    print("ERROR: number must be between [-32767,32767]")
                    print("Line:",line)
                    exit(1)
                f.seek(f.tell()-1)  # return at the start of the next word
                if(char == "\n"):
                        line -= 1
                
                
        #   STATE 2 ---> CHAR IS A LETTER         
        if (state == 2):             
            if (char.isalpha() or char.isdigit()):
                state = 2               
                if (len(letters) < 30):
                    letters.append(char)   
                    
            else:
                    state = OK
                    word = "".join(letters)
                    if word in standard_words:  # check if the word is a standard word
                        W += [word] + [100]
                    else:
                        W += [word] + [2]
        
                    f.seek(f.tell()-1) 
                    if(char == "\n"):
                        line -= 1
                
                
        #STATE 3 ---> GIVEN SYMBOL "<"      
        if (state == 3):
            state = OK
            char = f.read(1)
            if (char == ">"):
                letters = "<>"
                word = "".join(letters) 
                W += [word] +[13]
            elif (char == "="):
                letters = "<="
                word = "".join(letters)   
                W += [word] + [14]
            else:
                letters = "<"
                word = "".join(letters)
                W += [word] + [15]
                f.seek(f.tell()-1)
                if(char == "\n"):
                        line -= 1
                
            
        #STATE 4 ---> GIVEN SYMBOL ">"        
        if (state == 4):
            state = OK
            char = f.read(1)
            if(char == "="):
                letters = ">="
                word = "".join(letters)
                W += [word] + [16]
            else:
                letters = ">"
                word = "".join(letters)
                W += [word] + [17]
                f.seek(f.tell()-1)
                if(char == "\n"):
                        line -= 1
                
            
        #STATE 5 ---> GIVEN SYMBOL ":"      
        if (state == 5):
            state = OK
            char = f.read(1)
            if (char == "="):
                letters = ":="
                word = "".join(letters)
                W += [word] + [18]
            else:
                letters = ":"
                word = "".join(letters)
                W += [letters] + [19]
                f.seek(f.tell()-1)
                if(char == "\n"):
                        line -= 1   
            
               
        #STATE 6 ---> 1 LINE COMMENTS
        if (state == 6):
            char = f.read(1)
            if (char == "/"):
                while(char != "\n"):
                    char = f.read(1)
                state = 0
            
            elif(char == "*"):
                state = 7
            else:
                state = OK
                W += ["/"] + [20]
                f.seek(f.tell()-1)
                if(char == "\n"):
                        line -= 1


        #STATE 7 ---> COMMENTS
        if (state == 7):
            char = f.read(1)
            if (char == "/"):
                char = f.read(1)
                if (char == "*" or char == "/"):
                    state = error
                    print("ERROR: nested comments aren't allowed")
                    print("Line:",line)
                    exit(1)
                else:
                    state = 7
                    
            elif (char == "*"):
                char = f.read(1)
                if (char == "/"):
                    state = 0
                else:
                    state = 7
                    
            elif (char == ""):
                state = error
                print("ERROR: unclosed comments")
                print("Line:",line)
                exit(1)
            else:
                state = 7
                              
            
        #STATE EOF         
        if (state == EOF):
            W += ["EOF"] + [-2]
            
            
        #STATE ERROR 
        if (state == error):
            W += ["error"] + [-1]

     
    file_pointer = f.tell()
    #f.close()
    
    #return the word and it's "value"
    return W[0], W[1]

############################################################################
########## SYNTAKTIKOS ANALYTIKHS & ENDIAMESOS KWDIKAS #####################
############################################################################

global listOfQuads 
listOfQuads = []
QUAD_ID = 1 

def nextQuad():
    global QUAD_ID
    return QUAD_ID

def genQuad(op, x, y, z):
    global QUAD_ID
    global listOfQuads
    newQuad = []
    
    newQuad.append(nextQuad())         
    newQuad.append(op)
    newQuad.append(x)
    newQuad.append(y)
    newQuad.append(z)
    QUAD_ID +=1 
    listOfQuads.append(newQuad) 

    return newQuad


T_i = 1
listOfTempVars = []

def newTemp():
    global T_i
    global listOfTempVars
    
    list = ['T_']
    list.append(str(T_i))
    tempVar="".join(list)
    T_i +=1
    
    listOfTempVars.append(tempVar)
    
    return tempVar

def emptyList():
    listOfLabels = []   
    return listOfLabels

def makeList(x):
    
    new_list = [x]
    return new_list

def merge(list1, list2):
    merged = []
    merged += list1+list2

    return merged

def backPatch(list, z):
    global listOfQuads
    
    for i in range(len(list)):
        for j in range(len(listOfQuads)):
            if(list[i]==listOfQuads[j][0] and listOfQuads[j][4]=='_'):
                listOfQuads[j][4] = z
    return


def syntaktikosAnalyths(gN):

    global token
    global temporary
    global check
    check =0
    token =lex()

    def program():
        global token
        if(token[0]=='program'):
            token=lex()
            if(token[1]!=2):
                print("ERROR: Program name was expected, line:",line)
                exit(1)
            else:  
                name = token[0]
                token=lex()
                block(name,1)
                if(token[0]=='endprogram'):
                    token=lex()
                else:
                    print("ERROR: the keyword 'endprogram' was expected, line:",line)
                    exit(1)
        
        else:
            print("ERROR: the keyword 'program' was expected, line:",line)
            exit(1)
        return

    def block(name,ProgramBlock):
        global token
        declarations()
        subprograms()
        genQuad("begin_block",name,"_","_")
        statements()
        if (ProgramBlock==1):
            genQuad("halt","_","_","_")
        genQuad("end_block",name,"_","_")
        return

    def declarations():
        global token

        while(token[0]=='declare'):
            token=lex()
            varlist()
            if(token[0]==';'):
                token=lex()
            else:
                print("ERROR: ';' was expected, line:",line)
                exit(1)
        return


    def varlist():
        global token

        if(token[1]==2):
            gN.write(token[0])
            token=lex()
            while(token[0]==','):
                gN.write(token[0])
                token=lex()
                if(token[1]==2):
                    gN.write(token[0])
                    token=lex()
                else:
                    print("ERROR: var name was expected, line:",line)
                    exit(1)
        return

    def subprograms():
        global token
        while(token[0]=='function'):
            subprogram()
        return

    def subprogram():
        global token
        if(token[0]=='function'):
            token=lex()
            if(token[1]==2):
                name=token[0]
                token=lex()
                funcbody(name,1)
                if(token[0]=='endfunction'):
                    token=lex()
                else:
                    print("ERROR: the keyword 'endfunction' was expected, line:",line)
                    exit(1)
            else:
                print("ERROR: subprogram name was expected, line:",line)
                exit(1)
        else:
            print("ERROR: the keyword 'function' was expected, line: ",line)
            exit(1)
        return


    def funcbody(name,flag):
        global token
        formalpars()
        block(name,5) 
        return

    def formalpars():
        global token
        if(token[0]=='('):
            token=lex()
            formalparlist()
            if(token[0]==')'):
                token=lex()
            else:
                print("ERROR: ')' was expected, line:",line)
                exit(1)
        else:
            print("ERROR: '(' was expected, line:",line)
            exit(1)


    def formalparlist():
        global token

        formalparitem()

        while(token[0]==','):
            token=lex()
            formalparitem()
        return    

    def formalparitem():
        global token

        if(token[0]=='in'):
            token=lex()
            if(token[1]==2):
                token=lex()
            else:
                print("ERROR: in name was expected, line:",line)
                exit(1)

        elif(token[0]=='inout'):
            token=lex()
            if(token[1]==2):
                token=lex()
                return
            else:
                print("ERROR: inout name was expected, line:",line)
                exit(1)

        elif(token[0]=='inandout'):
            token=lex()
            if(token[1]==2):
                token=lex()
                return
            else:
                print("ERROR: inandout name was expected, line:",line)
                exit(1)
        else:
            print("ERROR: expected write correct keyword!")
            exit(1)
        return

    def statements():
        global token

        statement()
        while(token[0]==';'):
            token=lex()
            statement()
        return

    def statement():
        global token

        if(token[1]==2):
            assignment_stat()
        elif(token[0]=='if'):
            if_stat()
        elif(token[0]=='while'):
            while_stat()
        elif(token[0]=='dowhile'):
            do_while_stat()
        elif(token[0]=='loop'):
            loop_stat()
        elif(token[0]=='exit'):
            exit_stat()
        elif(token[0]=='forcase'):
            forcase_stat()
        elif(token[0]=='incase'):
            incase_stat()
        elif(token[0]=='return'):
            return_stat()
        elif(token[0]=='input'):
            input_stat()
        elif(token[0]=='print'):
            print_stat()
        return

    def assignment_stat():
        global token
        global temporary
        global check
        ID=token[0]
        token=lex()
        if(token[0]==':='):
            token=lex() 
            temporary=token[0]
            EPlace=expression()
            if(check==1): 
                genQuad(':=', temporary, '_', ID)
                check=0
            else:
                genQuad(':=', EPlace, '_', ID)
        else:
            print("ERROR: expected ':=', line:",line)
            exit(1)
        return

    def if_stat():
        global token
        token=lex()
        if(token[0]=='('):
            token=lex()
            bool_list = condition()
            if(token[0]==')'):
                token=lex()
            else:
                print("ERROR: ')' was expected, line:",line)
                exit(1)
            if(token[0]=='then'):
                token=lex()
                backPatch(bool_list[0],nextQuad())
                statements()
                List=makeList(nextQuad())
                genQuad('jump','_','_','_')
                backPatch(bool_list[1],nextQuad())
                elsepart()
                backPatch(List, nextQuad())
                if(token[0]=='endif'):
                    token=lex()
                else:
                    print("ERROR: the keyword 'endif' was expected, line:",line)
                    exit(1)
            else:
                print("ERROR: the keyword 'then' was expected, line:",line)
                exit(1)
        else:
            print("ERROR: '(' was expected, line:",line)
            exit(1)
        return bool_list[0],bool_list[1]

    def elsepart():
        global token
        
        if(token[0]=='else'):
            token=lex()
            statements()


    def while_stat():
        global token
        token=lex()
        if(token[0]=='('):
            token=lex()
            quad=nextQuad()
            bool_list=condition()
            if(token[0]==')'):
                backPatch(bool_list[0], nextQuad())
                token=lex()
                statements()
                genQuad('jump', '_', '_', quad)
                backPatch(bool_list[1], nextQuad())
                if(token[0]=='endwhile'):
                    token=lex()
                else:
                    print("ERROR: the keyword 'endwhile' was expected, line:",line)
                    exit(1)
            else:
                print("ERROR: ')' was expected, line:",line)
                exit(1)
        else:
            print("ERROR: '(' was expected, line:",line)
            exit(1)
        
        WTrue=bool_list[0]
        WFalse=bool_list[1]
        return WTrue,WFalse


    def do_while_stat():
        global token
        sQuad=nextQuad()
        token=lex()
        statements()
        if(token[0]=='enddowhile'):
            token=lex()
            if(token[0]=='('):
                token=lex()
                bool_list=condition()
                backPatch(bool_list[0], sQuad)
                backPatch(bool_list[1], nextQuad())
                if(token[0]==')'):
                    token=lex()
                else:
                    print("ERROR: ')' was expected, line:",line)
                    exit(1)
            else:
                print("ERROR: '(' was expected, line:",line)
                exit(1)
        else:
            print("ERROR: the keyword 'enddowhile' was expected, line:",line)
            exit(1)
        return bool_list[0],bool_list[1]

    def loop_stat():
        global token

        token=lex()
        lQuad=nextQuad()
        statements()
        genQuad("jump","_","_",lQuad)
        if(token[0]=='endloop'):
            token=lex()
        else:
            print("ERROR: the keyword 'endloop' was expected, line:",line)
            exit(1)

    def exit_stat():
        global token
        token=lex()

    def incase_stat():
        global token
        token=lex()
        temp=newTemp()
        iQuad=nextQuad()
        genQuad(':=', 1, '_', temp)
        while(token[0]=='when'):
            token=lex()
            if(token[0]=='('):
                token=lex()
                bool_list=condition()
                if(token[0]==')'):
                    token=lex()
                else:
                    print("ERROR ')' was expected line:",line)
                    exit(1)
            else:
                print("ERROR '(' was expected line:",line)
                exit(1)
            if(token[0]==':'):
                token=lex()
                backPatch(bool_list[0], nextQuad())
                genQuad(':=', 0, '_', temp)
                statements()
                backPatch(bool_list[1], nextQuad())
            else:
                print("ERROR: ':' was expected, line:",line)
                exit(1)
        if(token[0]=='endincase'):
            token=lex()
            genQuad(':=', temp, 0, iQuad)
        else:
            print("ERROR: the keyword 'endincase' was expected, line:",line)
            exit(1)
    
    def return_stat():
        global token
        token=lex()
        EPlace=expression()
        genQuad('retv', EPlace, '_', '_')
    
    def print_stat():
        global token
        token=lex()
        EPlace=expression()
        genQuad('out', EPlace, '_', '_')

    def input_stat():
        global token
        token=lex()
        if(token[1]==2):
            token=lex()
            EPlace=token[0]
            genQuad('input', EPlace, '_','_')
        else:
            print("ERROR: name input was expected, line:",line)
            exit(1)

    def actualpars(name,flag):
        
        global token
        global temporary

        if(token[0]=='('):
            token=lex()
            actualparlist()
            if(token[0]==')'):
                token=lex()
                if(flag==1):
                    temp=newTemp()
                    genQuad('par', temp, 'RET', '_')
                    genQuad('call', name, '_', '_')
                    temporary=temp
                else:
                    genQuad('call', name, '_', '_')
            else:
                print("ERROR: ')' was expected, line:",line)
                exit(1)
        else:
            print("ERROR: '(' was expected, line:",line)
            exit(1)
    
    def actualparlist():
        global token
        actualparitem()
        while(token[0]==','):
            token=lex()
            actualparitem()
        return

    def actualparitem():
        global token
        if(token[0]=='in'):
            token=lex()
            EPlace=expression()
            genQuad('par', EPlace, 'CV', '_')
        elif(token[0]=='inout'):
            token=lex()
            if(token[1]==2):
                genQuad('par', token[0], 'REF', '_')
                token=lex()
            else:
                print("ERROR: name inout was expected, line:",line)
                exit(1)
        elif(token[0]=='inandout'):
            token=lex()
            if(token[1]==2):
                genQuad('par', token[0], 'REF', '_')
                token=lex()
            else:
                print("ERROR: name inandout was expected, line:",line)
                exit(1)

    def condition():
        global token
        bool_list=boolterm()
        trueList=bool_list[0]
        falseList=bool_list[1]
        while(token[0]=='or'):
            token=lex()
            backPatch(falseList, nextQuad())
            bool_list=boolterm()
            trueList= merge(trueList, bool_list[0])
            falseList=bool_list[1]
        return trueList,falseList

    def boolterm():
        global token
        btTrue=[]
        btFalse=[]
        bt=boolfactor()
        btTrue=bt[0]
        btFalse=bt[1]
        while(token[0]=='and'):
            token=lex()
            backPatch(btTrue,nextQuad())
            bt1=boolfactor()
            btFalse=merge(btFalse,bt1[1])
            btTrue=bt1[0]
        return  btTrue,btFalse

    def boolfactor():
        global token
        trueList=[]
        falseList=[]
        relop=''
        EPlace, EPlace1='',''

        if(token[0]=='not'):
            token=lex()
            if(token[0]=='['):
                token=lex()
                bool_list=condition()             
                if(token[0]==']'):
                    token=lex()
                    trueList=bool_list[1]
                    falseList=bool_list[0]
                else:
                    print("ERROR: ']' was expected, line:",line)
                    exit(1)
            else:
                print("ERROR: '[' was expected, line:",line)
                exit(1)
        elif(token[0]=='['):
            token=lex()
            bool_list=condition()
            if(token[0]==']'):
                token=lex()
                trueList=bool_list[0] #check the arrays
                falseList=bool_list[1]
            else:
                print("ERROR: ']' was expected, line:",line)
                exit(1)
        else:
            EPlace=expression()
            relop=relation_oper()
            EPlace1=expression()

            trueList=makeList(nextQuad())
            genQuad(relop, EPlace, EPlace1, '_')
            falseList=makeList(nextQuad())
            genQuad('jump', '_', '_', '_')
        
        return trueList,falseList
    def expression():
        global token
        optional_sign()
        TPlace=term()
        while(token[0]=='+' or token[0]=='-'):
            op=add_oper()
            T1Place=term()
            temp=newTemp()
            genQuad(op,TPlace, T1Place, temp)
            TPlace=temp
        EPlace=TPlace
        return EPlace

    def term():
        global token
        FPlace=factor()
        while(token[0]=='*' or token[0]=='/'):
            op=mul_oper()
            F1Place=factor()
            temp=newTemp()
            genQuad(op, FPlace, F1Place, temp)
            FPlace=temp
        EPlace=FPlace
        return EPlace
    
    def factor():
        global token
        if(token[1]==1):
            name=token[0]
            token=lex() 

        elif(token[0]=='('):
            token=lex()
            EPlace=expression()
            if(token[0]==')'):
                name=EPlace
                token=lex()
            else:
                print("ERROR: ')' was expected, line:")
                exit(1)

        elif(token[1]==2):
            name=token[0]
            token=lex()
            idtail(name)
        else:
            print("ERROR: the name factor was expected, line:")
            exit(1)
        return name

    def idtail(name):
        global token
        if(token[0]=='('):
            check=1
            actualpars(name,1)
    
    def relation_oper():
        global token
        if(token[0]=='='):
            george = token[0]
            token=lex()
        elif(token[0]=='<='):
            george=token[0]
            token=lex()
        elif(token[0]=='<='):
            george=token[0]
            token=lex()
        elif(token[0]=='>='):
            george=token[0]
            token=lex()
        elif(token[0]=='>'):
            george=token[0]
            token=lex()
        elif(token[0]=='<'):
            george=token[0]
            token=lex()
        elif(token[0]=='<>'):
            george=token[0]
            token=lex()
        return george
    
    def add_oper():
        global token
        if(token[0]=='+'):
            opp=token[0]
            token=lex()
        elif(token[0]=='-'):
            opp=token[0]
            token=lex()
        return opp
    
    def mul_oper():
        global token
        if(token[0]=='*'):
            opp=token[0]
            token=lex()
        elif(token[0]=='/'):
            opp=token[0]
            token=lex()
        return opp

    def optional_sign():
        global token
        if(token[0]=='+' or token[0]=='-'):
            nikos=add_oper()
            return
    
    def forcase_stat():
        global token
        token=lex()
        fQuad=nextQuad()
        while(token[0]=='when'):
            token=lex()
            if(token[0]=='('):
                token=lex()
                bool_list=condition()
                if(token[0]==')'):
                    token=lex()
                    if(token[0]==':'):
                        token=lex()
                        backPatch(bool_list[0], nextQuad())
                        statements()
                        genQuad('jump', '_','_',fQuad)
                        backPatch(bool_list[1], nextQuad())
                    else:
                        print("ERROR: ')' was expected line:",line)
                        exit(1)
                else:
                    print("ERROR: ')' was expected line:",line)
                    exit(1)

            else:
                print("ERROR: ')' was expected, line:")
                exit(1)
        else:
            print("ERROR the keyword 'when' was expected line:",line)
            exit(1)
        if(token[0]=='default:'):
            token=lex()
            f1Quad=nextQuad()
            statements()
            if(token[0]=='enddefault'):
                token=lex()
            else:
                print("ERROR the keyword 'enddefault' was expected line:",line)
                exit(1)
        else:
            print("ERROR the keyword 'default' was expected line:",line)
            exit(1)
        if(token[0]=='endforcase'):
            token=lex()
        else:
            print("ERROR the keyword 'endforcase' was expected line:",line)
            exit(1)
 

    
    program()
    print("----------OK----------")
    return

# Write quads in the file
def write_quads(write_intFile, i):
        write_intFile.write(str(listOfQuads[i][0])+":\t")
        write_intFile.write(str(listOfQuads[i][1])+"\t")
        write_intFile.write(str(listOfQuads[i][2])+"\t")
        write_intFile.write(str(listOfQuads[i][3])+"\t")
        write_intFile.write(str(listOfQuads[i][4])+"\n")

# Write the C code in a file
# Write the Assembly code in a file
def write_files(write_intFile,write_cFile,finalFile):
    global listOfTempVars

    if(len(listOfTempVars)!=0):
        write_cFile.write(",")

    for k in range(len(listOfTempVars)):
        write_cFile.write(listOfTempVars[k])
        if(k+1!=len(listOfTempVars)):
            write_cFile.write(",")
        else:
            write_cFile.write(";\n\t")

    for l in range(len(listOfQuads)):
        write_quads(write_intFile, l)
        if(listOfQuads[l][1] == 'begin_block'):
            write_cFile.write('L_'+str(l)+":"'\n\t')
        elif(str(listOfQuads[l][1]) == '<'):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+"<"+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('blt,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == '<>'):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+"<>"+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('bne,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == '<='):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+"<="+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('ble,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == '>'):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+">"+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('bgt,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == '>='):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+">="+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('bge,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == '='):
            write_cFile.write("L_"+str(l)+": "+"if ("+str(listOfQuads[l][2])+"=="+str(listOfQuads[l][3])+") goto L_"+str(listOfQuads[l][4])+";\n\t")
            finalFile.write('beq,$t1,$t2,'+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == ':='):
            write_cFile.write("L_"+str(l)+": "+ str(listOfQuads[l][4])+"="+str(listOfQuads[l][2])+";\n\t")
        elif(listOfQuads[l][1] == '+'):
            write_cFile.write("L_"+str(l)+": "+ str(listOfQuads[l][4])+"="+str(listOfQuads[l][2])+"+"+str(listOfQuads[l][3])+";\n\t")
            finalFile.write('add,$t1,$t1,$t2'+'\n')
        elif(listOfQuads[l][1] == '-'):
            write_cFile.write("L_"+str(l)+": "+ str(listOfQuads[l][4])+"="+str(listOfQuads[l][2])+"-"+str(listOfQuads[l][3])+";\n\t")
            finalFile.write('sub,$t1,$t1,$t2'+'\n')
        elif(listOfQuads[l][1] == '*'):
            write_cFile.write("L_"+str(l)+": "+ str(listOfQuads[l][4])+"="+str(listOfQuads[l][2])+"*"+str(listOfQuads[l][3])+";\n\t")
            finalFile.write('mul,$t1,$t1,$t2'+'\n')
        elif(listOfQuads[l][1] == '/'):
            write_cFile.write("L_"+str(l)+": "+ str(listOfQuads[l][4])+"="+str(listOfQuads[l][2])+"/"+str(listOfQuads[l][3])+";\n\t")
            finalFile.write('div,$t1,$t1,$t2'+'\n')
        elif(listOfQuads[l][1] == 'jump'):
            write_cFile.write("L_"+str(l)+": "+"goto L_"+str(listOfQuads[l][4])+ ";\n\t")
            finalFile.write('j'+' '+str(listOfQuads[l][4])+'\n')
        elif(listOfQuads[l][1] == 'out'):
            write_cFile.write("L_"+str(l)+": "+"printf(\""+str(listOfQuads[l][2])+"= %d\", "+str(listOfQuads[l][2])+");\n\t")
            finalFile.write('li $v0,1'+'\n')
            finalFile.write('li $a0,'+listOfQuads[l][4]+'\n')
            finalFile.write('starlet'+'\n')
        elif(listOfQuads[l][1] == 'halt'):
            write_cFile.write("L_"+str(l)+": {}\n\t")
        if(listOfQuads[l][1] == 'end_block'):
            write_cFile.write('L_'+str(l)+":"'\n\t')

    write_cFile.write("\n}")




# main of the program
file_pointer = 0 
line = 1
standard_words = ["program", "endprogram", "declare", "if", "then", "else", "endif", "do", "while", "endwhile",
                        "loop", "endloop", "exit", "forcase", "endforcase", "incase", "endincase", "when", "default", "enddefault",
                        "function", "endfunction", "return", "in", "inout", "inandout", "and", "or", "not", "input", "print", 
                        "dowhile", "enddowhile"]

# check if user entered a starlet file as an argument
if(len(sys.argv) <= 1):
    print('ERROR: You must enter a starlet file')
    exit(1)

# open the entered starlet file
f = open(sys.argv[1],'r') 

# open files 
file1=open('file1.int','w')
file2=open('file2.c','w')
file3=open('final.asm','w')
file2.write("int main()\n{\n\tint  ")

syntaktikosAnalyths(file2)
write_files(file1,file2,file3)

# close files
file1.close()
file2.close()
file3.close()
f.close()


