#This is a module to contain classes and functions that define what
#Tokens are, and turn user input into them; and the exceptions relating
#to these classes and functions

from type_modeling import *


#exception thrown when the user enters unidentified characters
#form: stmnt offsets accepted as *why arguments (as of now)
class Unrecognized_Input(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a statement has no terminating semicolon
#form: None objects accepted as *why arguments (as of now)
class No_Semicolon(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a char token remains unclosed
#form: None objects accepted as *why arguments (as of now)
class Unclosed_Char(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a string token remains unclosed
#not used at all as of now
"""
class Unclosed_String(Exception):
    def __init__(self, *why):
        self.why = why
"""


#represents a general token, with a type name and an object value
class Token:
    def __init__(self, name, value):
        self.name = name
        self.item = value


#following functions turn user input into statements

#reads c++ statements (cin style, not newline based)
#will stop reading once it detects a line with a semicolon
def stmnt_read():
    text = ""
    while 1:
        line = input()
        if line == RESET:
            return RESET
        text += line
        if line.find(SEMICOLON) != -1:
            return text

#takes what is read by stmnt_read and
#splits it into individual statements
#to append to stmnt_list
def stmnt_list_app(stmnts):
    split_stmnts = stmnts.split(SEMICOLON)
    offset = 0
    flag = 1 if split_stmnts[-1] == "" else 0
    while offset < len(split_stmnts) - flag:
        if (offset == len(split_stmnts) - 1 and
            split_stmnts[-1] != ""):
            stmnt_list.append(split_stmnts[offset])
            return
        else:    
            stmnt_list.append(split_stmnts[offset] + SEMICOLON)
        offset += 1


#following functions used to find patterns in user input

#tries to find a word in a string
#words are only considered found if they are not part of a larger word
#called by tokenize_type and tokenize_bool
def find_word(string, substring):
    if len(substring) <= len(string):
        if string[0:len(substring)] == substring:
            if len(string) == len(substring):
                return True
            elif (LETTERS.find(string[len(substring)]) == -1 and
                  INTS.find(string[len(substring)]) == -1):
                return True
    return False
        
#tries to find an symbol in a string
#SYMBOLS are considered separated by spaces
#called by tokenize_symbol
def find_symbol(string, symbol):
    if len(symbol) <= len(string):
        if string[0:len(symbol)] == symbol:
            return True
    return False


#following functions turn statements into Tokens

#function to manage all the sub-tokenizing functions
def tokenize_stmnt(stmnt):
    stmnt_offset[0] = 0
    while stmnt_offset[0] < len(stmnt):
        #calls all token detection/appending functions
        #then increases the offset based on appended token length
        offset_original = stmnt_offset[0]
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_type(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_adj(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_int(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_double(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_bool(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_idtfr(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_char(stmnt[stmnt_offset[0]:])
        #strings not tokenized - only primitives types as of now
        #if stmnt_offset[0] < len(stmnt):
            #stmnt_offset[0] += tokenize_string(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_symbol(stmnt[stmnt_offset[0]:])
        if stmnt_offset[0] < len(stmnt):
            stmnt_offset[0] += tokenize_space(stmnt[stmnt_offset[0]])
        if stmnt_offset[0] < len(stmnt):
            if tokenize_semicolon(stmnt[stmnt_offset[0]]):
                return
        #no token recognized, throws an exception
        if offset_original == stmnt_offset[0]:
            raise Unrecognized_Input(stmnt_offset[0])
    #while loop exits without a SEMICOLON having been found
    raise No_Semicolon(None)

#checks for a type identifier and acts accordingly
def tokenize_type(substmnt):
    for i in TYPES.values():
        if find_word(substmnt, i):
            token_list.append(Token(NAMES["type_token"], i))
            return len(i)
    return 0

#checks for a type identifier and acts accordingly
def tokenize_adj(substmnt):
    for i in SIGNS.values():
        if find_word(substmnt, i):
            token_list.append(Token(NAMES["adjetive_token"], i))
            return len(i)
    return 0

#checks for a int token and acts accordingly
def tokenize_int(substmnt):
    offsets_advanced = 0
    int_ = ""
    for i in substmnt:
        if INTS.find(i) != -1:
            int_ += i
            offsets_advanced += 1
        else:
            if i == PERIOD:
                offsets_advanced = 0
                return offsets_advanced
            else:
                break
    if len(int_) > 0:
        token_list.append(Token(NAMES["int_token"], C_Int(int(int_))))
    return offsets_advanced

#checks for a double token and acts accordingly
def tokenize_double(substmnt):
    offsets_advanced = 0
    double = ""
    flag = False;
    for i in substmnt:
        if INTS.find(i) != -1:
            double += i
            offsets_advanced += 1
        elif i == PERIOD:
            if flag:
                break
            else:
                flag = True
                double += i
                offsets_advanced += 1
        else:
            break
    if len(double) > 1:
        token_list.append(Token(NAMES["double_token"], C_Double(float(double))))
    else:
        offsets_advanced = 0
    return offsets_advanced

#checks for a name token and acts accordingly
def tokenize_idtfr(substmnt):
    offsets_advanced = 0
    name = ""
    flag = False
    for i in substmnt:
        if LETTERS.find(i) != -1:
            flag = True
            name += i
            offsets_advanced += 1
        elif flag and INTS.find(i) != -1:
            name += i
            offsets_advanced += 1
        else:
            break
    if len(name) > 0:
        token_list.append(Token(NAMES["identifier_token"], name))
    return offsets_advanced

#checks for a bool token and acts accordingly
def tokenize_bool(substmnt):
    for i in BOOLS.values():
        if find_word(substmnt, i):
            bool_ = eval(i[0].upper() + i[1:])
            token_list.append(Token(NAMES["bool_token"], C_Bool(bool_)))
            return len(i)
    return 0

#checks for a char token and acts accordingly
def tokenize_char(substmnt):
    if len(substmnt) >= 3:
        if substmnt[0] == SINGLE_QUOTE:
            char = substmnt[0:3]
            if substmnt[2] == SINGLE_QUOTE:
                token_list.append(Token(NAMES["char_token"],
                                  C_Char(char.replace(SINGLE_QUOTE, ""))))
                return 3
            else:
                raise Unclosed_Char(None)
    return 0

#checks for a string token and acts accordingly
#NOT USED AS OF PRESENT
"""
def tokenize_string(substmnt):
    offsets_advanced = 0
    string = ""
    flag = False
    for i in substmnt:
        if i == DOUBLE_QUOTE:
            if flag:
                string += i
                offsets_advanced += 1
                token_list.append(Token(NAMES["string_token"],
                                  string.replace(DOUBLE_QUOTE, "")))
                return offsets_advanced
            else:
                string += i
                offsets_advanced += 1
                flag = True
                continue
        if flag:
            string += i
            offsets_advanced += 1
        else:
            break
    if flag:
        raise Unclosed_String(string.replace(DOUBLE_QUOTE, ""))
    return offsets_advanced
"""

#checks for a symbol token and acts accordingly
def tokenize_symbol(substmnt):
    for i in SYMBOLS.values():
        if find_symbol(substmnt, i):
            token_list.append(Token(NAMES["symbol_token"], i))
            return len(i)
    return 0

#checks for a SPACE token and acts accordingly
def tokenize_space(char):
    return 1 if char == SPACE else 0 

#checks for a SEMICOLON token and acts accordingly
def tokenize_semicolon(char):
    if char == SEMICOLON:
        token_list.append(Token(NAMES["symbol_token"], SEMICOLON))
        return 1
    return 0


#function to print out the contents of token_list in a readable fashion
def token_print(start, end):
    for i in range(start, end):
        item = token_list[i].item
        if issubclass(type(item), C_Type):
            if type(item) == C_Char:
                print("'" + item.output() + "'", end = " ")
            else:
                print(item.output(), end = " ")
        else:
            print(item, end = " ")


    
