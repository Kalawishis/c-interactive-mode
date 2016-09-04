#This is a module to contain values that are neither classes nor functions
#these values can be consts or mutables, and are referenced by the the
#functions and classes in the other modules (thus the names)

import collections


#following are OrderedDicts that are read-only
#OrderedDicts for both name and key access (goes for all OrderedDict's)

#indicating signage (to check if a C_Type is signed or unsigned)
SIGNS = collections.OrderedDict()
SIGNS["signed"] = "signed"
SIGNS["unsigned"] = "unsigned"

#represent items of symbol Tokens
SYMBOLS = collections.OrderedDict()
SYMBOLS["subtract_eql"] = "-="
SYMBOLS["add_eql"] = "+="
SYMBOLS["increment"] = "++"
SYMBOLS["deincrement"] = "--"
SYMBOLS["left_par"] = "("
SYMBOLS["right_par"] = ")"
SYMBOLS["uneql_check"] = "!="
SYMBOLS["grt_or_eql"] = ">="
SYMBOLS["less_or_eql"] = "<="
SYMBOLS["eql_check"] = "=="
SYMBOLS["add"] = "+"									
SYMBOLS["subtract"] = "-"
SYMBOLS["times"] = "*"
SYMBOLS["divide"] = "/"
SYMBOLS["modulo"] = "%"
SYMBOLS["grt_than"] = ">"
SYMBOLS["less_than"] = "<"
SYMBOLS["eql"] = "="

#represent all names a Token can be given
NAMES = collections.OrderedDict()
NAMES["type_token"] = "type"
NAMES["adjetive_token"] = "adjetive"
NAMES["identifier_token"] = "identifier"
NAMES["int_token"] = "int"
NAMES["double_token"] = "double"
NAMES["bool_token"] = "bool"
NAMES["char_token"] = "char"
NAMES["string_token"] = "string"
NAMES["symbol_token"] = "symbol"

#represent the items of type Tokens
#subset of NAMES, since NAMES cannot be sliced
TYPES = collections.OrderedDict()
TYPES["int_token"] = "int"
TYPES["double_token"] = "double"
TYPES["bool_token"] = "bool"
TYPES["string_token"] = "string"
TYPES["char_token"] = "char"

#represent items of bool Tokens
BOOLS = collections.OrderedDict()
BOOLS["bool_true"] = "true"
BOOLS["bool_false"] = "false"


#follwing are read only strings to be referenced when
#analyzing user input

#to be referenced when checking for an int or string in user input
INTS = "0123456789";

#to be referenced when checking for an string or identifier in user input
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"

#special symbol, one recognized but passed over (no space Token)
SPACE = " "

#represent the special item of a symbol Token
SEMICOLON = ";"

#to be referenced when checking for an int or double in user input
PERIOD = "."

#to be referenced when checking for a string in user input
DOUBLE_QUOTE = '"'

#to be referenced when checking for an char in user input
SINGLE_QUOTE = "'"

#string entered when user wants to clear all the data
RESET = "reset"


#following are read_write collections for varied reference

#list of statments appended by stmnt_list_app
stmnt_list = []

#offset of stmnt_list showing statement currently being worked on
#used by function without a statement passed in to access the current statement
#a list because ints in python can be immutable
#(this goes for all lists of the form "l = [x]")
current_stmnt = [-1]

#offset of stmnt_list showing statement currently being worked on
#different from current_stmnt in that it's used for tokenizing
stmnt_offset = [0]

#list of tokens appended by tokenize_stmnt
token_list = []

#represents the item of token_list currently being examined by
#a function in evaluation (like element, definition, etc)
token_offset = [0]

#focal offsets of token_list to be referenced by exceptions
saved_offsets = []

#list to store identifiers and their corresponding values as tokens
var_dict = {}
