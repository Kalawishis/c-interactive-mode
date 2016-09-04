#This is a module to contain the functions that read in tokens and act
#according to the c++ syntax, and the exceptions relating to these functions

from tokenization import *


#exception thrown when the tokens are in a nonsensical order
#form: token_list offsets accepted as *why arguments (as of now)
class Bad_Syntax(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when parentheses are not closed
#form: None objects accepted as *why arguments (as of now)
class Unclosed_Parentheses(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a user tries to declare or define
#the same variable twice
#form: identifier tokens accepted as *why arguments (as of now)
class Already_Declared(Exception):
    def __init__(self, *why):
        self.why = why

#excpetion thrown when a user tries to use a variable that
#has not been declared or defined
#form: identifier tokens accepted as *why arguments (as of now)
class Not_Declared(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a user tries to use a variable that
#has not been initialized
#form: identifier tokens accepted as *why arguments (as of now)
class Not_Initialized(Exception):
    def __init__(self, *why):
        self.why = why

#exception for when a user tries to put incompatible adjetives and types together
#form: adjetive and typename tokens accepted as *why arguments (as of now)
class Bad_Adjetive(Exception):
    def __init__(self, *why):
        self.why = why


#C_Int representation of -1 and 1, named since magic constants are bad
#not in reference since reference doesn't have the type_modeling classes
C_NEG1 = C_Int(-1)
C1 = C_Int(1)


#following functions deal with evaluating expressions
#each function manages the ones below it, in accordance with grammar.txt

#deals with checking for a semicolon, the end of an expression
#can throw Bad_Syntax exception
def expression(increment):
    token_offset[0] += increment
    left = superterm(False)
    if not token_list[token_offset[0]].item is SEMICOLON:
        raise Bad_Syntax(token_offset[0])
    expression_print(left)
    return left

#print the details of a successful expression
def expression_print(output):
    print(stmnt_list[current_stmnt[0]],
          "expression result is",
          output.output())

#manage ==, !=, >, <, >=, <= operators
def superterm(increment):
    token_offset[0] += increment
    left = term(False)
    while True:
        if token_list[token_offset[0]].item is SYMBOLS["eql_check"]:
            left = left == term(True)
        elif token_list[token_offset[0]].item is SYMBOLS["uneql_check"]:
            left = left != term(True)
        elif token_list[token_offset[0]].item is SYMBOLS["grt_than"]:
            left = left > term(True)
        elif token_list[token_offset[0]].item is SYMBOLS["less_than"]:
            left = left < term(True)
        elif token_list[token_offset[0]].item is SYMBOLS["grt_or_eql"]:
            left = left >= term(True)
        elif token_list[token_offset[0]].item is SYMBOLS["less_or_eql"]:
            left = left <= term(True)
        else:
            break
    return left

#manage +, - operators
def term(increment):
    token_offset[0] += increment
    left = primary(False)
    while True:
        if token_list[token_offset[0]].item is SYMBOLS["add"]:
            left = left + primary(True)
        elif token_list[token_offset[0]].item is SYMBOLS["subtract"]:
            left = left - primary(True)
        else:
            break
    return left

#manage *, /, % operators 
def primary(increment):
    token_offset[0] += increment
    left = element(False)
    while True:
        if token_list[token_offset[0]].item is SYMBOLS["times"]:
            left = left * element(True)
        elif token_list[token_offset[0]].item is SYMBOLS["divide"]:
            saved_offsets.append(token_offset[0] + 1)
            right = element(True)
            saved_offsets.append(token_offset[0])
            left = left / right
            del saved_offsets[- 2:]
        elif token_list[token_offset[0]].item is SYMBOLS["modulo"]:
            saved_offsets.append(token_offset[0] + 1)
            right = element(True)
            saved_offsets.append(token_offset[0])
            left = left % right
            del saved_offsets[- 2:]
        else:
            break
    return left

#manage the transfer of tokens into operable objects
#can throw Bad_Syntax, Unclosed_Parentheses,
#Not_Intitialized, Not_Declared exceptions
def element(increment):
    token_offset[0] += increment
    token = token_list[token_offset[0]]
    left = 0
    if token.item is SYMBOLS["add"]:
        left = element(True)
    elif token.item is SYMBOLS["subtract"]:
        left = element(True) * C_NEG1
    #prefix incrementation and deincrementation to be implemented
    #elif token.item is SYMBOLS["increment"]:
        #left = element(True) + C1
    #elif token.item is SYMBOLS["deincrement"]:
        #left = element(True) - C1
    elif token.item is SYMBOLS["left_par"]:
        left = superterm(True)
        token = token_list[token_offset[0]]
        if not token.item is SYMBOLS["right_par"]:
            raise Unclosed_Parentheses(None)
        token_offset[0] += 1
    elif token.name is NAMES["identifier_token"]:
        try:
            left = var_dict[token.item].item
            if left.init is False:
                raise Not_Initialized(token)
        except KeyError:
            raise Not_Declared(token)
        else:
            token_offset[0] += 1
    elif token.name in TYPES.values():
        left = token.item
        token_offset[0] += 1
    elif token.name is SEMICOLON:
        pass
    else:
        raise Bad_Syntax(token_offset[0])
    return left


#following functions deal with declarations, definitions, reassignments

#checks for a declaration and acts accordingly
#can raise Bad_Adjetive exception
def declaration():
    temp = token_offset[0]
    adj = adjetive()
    if adj is False:
        adj = Token(NAMES["adjetive_token"], SIGNS["signed"])
        manual = False
    else:
        manual = True
    typnm = typename()
    idtfr = identifier()
    if (not typnm is False and
        not idtfr is False and
        token_list[token_offset[0]].item is SEMICOLON):
        if (typnm.item is TYPES["bool_token"] or \
            typnm.item is TYPES["double_token"]) and \
            manual:
            raise Bad_Adjetive(adj, typnm)
        declare_var(adj, typnm, idtfr)
        declare_print(adj, typnm, idtfr, manual)
        return True
    token_offset[0] = temp
    return False

#declares a variable (can raise Already_Declared exception)
def declare_var(adj, typnm, idtfr):
    if var_dict.get(idtfr.item):
        raise Already_Declared(idtfr)
    else:
        if typnm.item is NAMES["int_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["int_token"], C_Int(0, sign = adj.item, init = False))
        if typnm.item is NAMES["double_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["double_token"], C_Double(0, sign = adj.item, init = False))
        if typnm.item is NAMES["bool_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["bool_token"], C_Bool(0, sign = adj.item, init = False))
        if typnm.item is NAMES["char_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["char_token"], C_Char(0, sign = adj.item, init = False))

#prints the details of a successful declaration
def declare_print(adj, typnm, idtfr, manual):
    if typnm.item is TYPES["bool_token"]:
        print(idtfr.item,
              "declared as a",
              typnm.item)
    else:
        print(idtfr.item,
              "declared as a",
              adj.item,
              typnm.item)
    if not manual and not typnm.item is TYPES["bool_token"]:
        print("(" +
              idtfr.item,
              "is",
              adj.item,
              "by default)")

#checks for a definition and acts accordingly
#can raise Bad_Adjetive exception
def definition():
    temp = token_offset[0]
    adj = adjetive()
    if adj is False:
        adj = Token(NAMES["adjetive_token"], SIGNS["signed"])
        manual = False
    else:
        manual = True
    typnm = typename()
    idtfr = identifier()
    if (not typnm is False and
        idtfr is False):
        raise Bad_Syntax(token_offset[0])
    if (not typnm is False and
        not idtfr is False and
        token_list[token_offset[0]].item is SYMBOLS["eql"]):
        if (typnm.item is TYPES["bool_token"] or \
            typnm.item is TYPES["double_token"]) and \
            manual:
            raise Bad_Adjetive(adj, typnm)
        token_offset[0] += 1
        output = expression(False)
        define_var(adj, typnm, idtfr, output)
        new_output = var_dict[idtfr.item].item.output()
        define_print(adj, typnm, idtfr, output, new_output, manual)
        return True
    token_offset[0] = temp
    return False

#defines a variable (can raise Already_Declared exception)
def define_var(adj, typnm, idtfr, output):
    if var_dict.get(idtfr.item):
        raise Already_Declared(idtfr)
    else:
        if typnm.item is NAMES["int_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["int_token"], C_Int(output, sign = adj.item))
        if typnm.item is NAMES["double_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["double_token"], C_Double(output, sign = adj.item))
        if typnm.item is NAMES["bool_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["bool_token"], C_Bool(output, sign = adj.item))
        if typnm.item is NAMES["char_token"]:
            var_dict[idtfr.item] = \
            Token(TYPES["char_token"], C_Char(output, sign = adj.item))    

#prints the details of a successful definition
def define_print(adj, typnm, idtfr, output, new_output, manual):
    if typnm.item is TYPES["bool_token"]:
        print(idtfr.item,
              "defined as a",
              typnm.item,
              "assigned to the value",
              output.output())
    else:
        print(idtfr.item,
              "defined as a",
              adj.item,
              typnm.item,
              "assigned to the value",
              new_output)
    if not manual and not typnm.item is TYPES["bool_token"]:
        print("(" +
              idtfr.item,
              "is",
              adj.item,
              "by default)")

#checks for a reassignment and acts accordingly
#can raise Not_Declared, Not_Initialized exception
def reassignment():
    temp = token_offset[0]
    idtfr = identifier()
    current_item = token_list[token_offset[0]].item
    if not idtfr is False:
        if not var_dict.get(idtfr.item):
            raise Not_Declared(idtfr)
        var_val = var_dict.get(idtfr.item).item
        if current_item is SYMBOLS["eql"]:
            token_offset[0] += 1
            output = expression(False)
            reassign_var(idtfr, output)
            return var_val
        elif current_item is SYMBOLS["add_eql"]:
            if var_val.init is False:
                raise Not_Initialized(idtfr)
            token_offset[0] += 1
            output = var_val + expression(False)
            reassign_var(idtfr, output)
            return var_val
        elif current_item is SYMBOLS["subtract_eql"]:
            if var_val.init is False:
                raise Not_Initialized(idtfr)
            token_offset[0] += 1
            output = var_val - expression(False)
            reassign_var(idtfr, output)
            return var_val
        elif current_item is SYMBOLS["increment"]:
            if var_val.init is False:
                raise Not_Initialized(idtfr)
            token_offset[0] += 1
            if not token_list[token_offset[0]].item is SEMICOLON:
                raise Bad_Syntax(token_offset[0])
            output = var_val + C1
            reassign_var(idtfr, output)
            return var_val
        elif current_item is SYMBOLS["deincrement"]:
            if var_val.init is False:
                raise Not_Initialized(idtfr)
            token_offset[0] += 1
            if not token_list[token_offset[0]].item is SEMICOLON:
                raise Bad_Syntax(token_offset[0])
            output = var_val - C1
            reassign_var(idtfr, output)
            return var_val
    token_offset[0] = temp
    return False

#reassigns a variable to a new value (handles =, +=, -=, ++, --)
#can raise Not_Initialized exception
def reassign_var(idtfr, output):
    idtfr_adj = var_dict[idtfr.item].item.sign
    var_type = var_dict[idtfr.item].name
    if var_type is NAMES["int_token"]:
        var_dict[idtfr.item] = \
        Token(TYPES["int_token"], C_Int(output, sign = idtfr_adj))
    if var_type is NAMES["double_token"]:
        var_dict[idtfr.item] = \
        Token(TYPES["double_token"], C_Double(output, sign = idtfr_adj))
    if var_type is NAMES["bool_token"]:
        var_dict[idtfr.item] = \
        Token(TYPES["bool_token"], C_Bool(output, sign = idtfr_adj))
    if var_type is NAMES["char_token"]:
        var_dict[idtfr.item] = \
        Token(TYPES["char_token"], C_Char(output, sign = idtfr_adj))
    new_output = var_dict[idtfr.item].item.output()
    reassign_print(idtfr, var_dict[idtfr.item])

#prints the details of a successful reassignment
def reassign_print(idtfr, new_value):
    print(idtfr.item,
          "reassigned to value",
          new_value.item.output())
        

#following functions used to identify adjetive, typename, identifier
    
#checks if current token is an adjetive token
def adjetive():
    temp = token_list[token_offset[0]]
    if temp.name is NAMES["adjetive_token"]:
        token_offset[0] += 1
        return temp
    return False

#checks if current token is a typename token
def typename():
    temp = token_list[token_offset[0]]
    if temp.name is NAMES["type_token"]:
        token_offset[0] += 1
        return temp
    return False

#checks if current token is an identifier token
def identifier():
    temp = token_list[token_offset[0]]
    if temp.name is NAMES["identifier_token"]:
        token_offset[0] += 1
        return temp
    return False
