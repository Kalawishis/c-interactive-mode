#This is a module to contain functions to manage the all the other modules,
#guide the user, and recover from exceptions

from evaluation import *


#the function that manages everything
def compute(arg = ""):
    stmnt_list.clear()
    reset()
    #if arg:
        #stmnt_list_app(arg)
    #else:
    #below up to for loop will be indented if above code
    #is uncommented
    print("Enter your statement(s):")
    text = stmnt_read()
    if text == RESET:
        super_reset()
        print("Everything has reset.")
        return
    stmnt_list_app(text)
    for i in stmnt_list:
        current_stmnt[0] += 1
        reset()
        try:
            tokenize_stmnt(i)
        #exceptions found in tokenization (some are not used yet)
        #except Invalid_Operator as e:
        except Unrecognized_Input as e:
            manage_unrecognized_input(e)
            continue
        except No_Semicolon as e:
            manage_no_semicolon(e)
            continue
        except Unclosed_Char as e:
            manage_unclosed_char(e)
            continue
        #except Unclosed_String as e:
        try:
            if declaration():
                continue
            if definition():
                continue
            if reassignment():
                continue
            expression(False)
        #exceptions found in type_modeling (some are not used yet)
        #except Invalid_Operator as e:
        #except Cannot_Convert as e:
        except Divided_By_0 as e:
            manage_divided_by_0(e)
            continue
        #exceptions found in evaluation
        except Bad_Syntax as e:
            manage_bad_syntax(e)
            continue
        except Unclosed_Parentheses as e:
            manage_unclosed_parentheses(e)
            continue
        except Already_Declared as e:
            manage_already_declared(e)
            continue
        except Not_Declared as e:
            manage_not_declared(e)
            continue
        except Not_Initialized as e:
            manage_not_initialized(e)
        except Bad_Adjetive as e:
            manage_bad_adjetive(e)
            continue
    current_stmnt[0] = -1   
    #print("Computation ended!")


#following functions manage exceptions for compute
#names are pretty self explanatory

def manage_unrecognized_input(e):
    stmnt = stmnt_list[current_stmnt[0]]
    print("error reading statement:", stmnt)
    print(stmnt[:e.why[0]],
          '[',
          stmnt[e.why[0]],
          ']',
          stmnt[e.why[0] + 1:])
    print("bracketed is unrecognized input")

def manage_no_semicolon(e):
    stmnt = stmnt_list[current_stmnt[0]]
    print("error reading statement:", stmnt)
    print("no concluding semicolon")

def manage_unclosed_char(e):
    stmnt = stmnt_list[current_stmnt[0]]
    print("error reading statement:", stmnt)
    print(stmnt[:stmnt_offset[0]],
          '[',
          stmnt[stmnt_offset[0]:stmnt_offset[0] + 2],
          ']',
          stmnt[stmnt_offset[0] + 2:])
    print("bracketed is unclosed char")

def manage_divided_by_0(e):
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    token_print(0, e.why[0])
    print('[', end = " ")
    token_print(e.why[0], e.why[1])
    print(']', end = " ")
    token_print(e.why[1], len(token_list))
    print("\nbracketed evaluates to zero - cannot divide or modulo by zero")

def manage_bad_syntax(e):
    reason = token_list[e.why[0]].item.output() if \
                     type(token_list[e.why[0]].item).__bases__[0] == C_Type else \
                     token_list[e.why[0]].item
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    token_print(0, e.why[0])
    print('[', reason, ']', end = " ")
    token_print(e.why[0] + 1, len(token_list))
    print("\nbracketed is improper syntax, and should be moved, removed, or replaced")

def manage_unclosed_parentheses(e):
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    print("forgot a right parenthesis or two somewhere")

def manage_already_declared(e):
    reason = e.why[0].item
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    print(reason, "is already declared or defined")

def manage_not_declared(e):
    reason = e.why[0].item
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    print(reason, "has not been declared")

def manage_not_initialized(e):
    reason = e.why[0].item
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    print(reason, "has not been initialized")

def manage_bad_adjetive(e):
    adj = e.why[0].item
    typnm = e.why[1].item
    stmnt = stmnt_list[current_stmnt[0]]
    print("error in statement:", stmnt)
    print(typnm + 's', "cannot be", adj)


#function to reset everything (like when an exception is called)
def reset():
    token_list.clear()
    token_offset[0] = 0
    saved_offsets.clear()
    stmnt_offset[0] = 0
    print()

#function to reset ABSOLUTELY everything (when user enters "reset")
def super_reset():
    reset()
    var_dict.clear()


#user directions
print("""
         Welcome to the Python C++ Model!
         
         This is a program to help beginners of C++.
         
         Simply type in a C++ statement,
         and this program will evaluate it for you.
         
         Ex. "3 + 5;" will return 8, "int a = 4;"
         will define an int of value 4.

         Currently supported:
             expressions
             declarations
             definitions
             reassignments: =, +=, -=, postfix ++ and --
             operators: +, -, *, /, %
             comparators: <, >, <=, >=, ==, !=
             parentheses
             ints
             doubles
             chars
             bools
             adjectives: signed, unsigned
         Currently unsupported:
             everything else
             (note: this Interactive Mode currently cannot comprehend
             a reassignment returning a value, which means that
             =, +=, -=, ++ and -- cannot be used in an expression yet)

         The exceptions should be able to identify any errors you made
         more clearly than an average compiler.
         
         If you want to reset everything, simply type "reset" by itself
         and nothing else.
         
         Have fun and explore. 
      """)

while True:
    compute()

