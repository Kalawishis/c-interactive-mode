#This is a module to contain classes to model the behaviors of the C++
#primitive types, and the exceptions relating to these classes

from reference import *


#exception for when a c++ object doesn't support a certain operator
#not used at all as of now
"""
class Invalid_Operator(Exception):
    def __init__(self, *why):
        self.why = why
"""

#exception for when two incompatible c++ objects are being combined
#not used at all as of now
"""
class Cannot_Convert(Exception):
    def __init__(self, *why):
        self.why = why
"""

#exception thrown when a user tries to divide a c++ object by 0
#form: saved_offsets offsets accepted as *why arguments (as of now)
class Divided_By_0(Exception):
    def __init__(self, *why):
        self.why = why

#exception thrown when a user tries to do modulo with doubles
#form: saved_offsets offsets accepted as *why arguments (as of now)
#CURRENTLY NOT IMPLEMENTED YET
"""
class Double_Modulo(Exception):
    def __init__(self, *why):
        self.why = why
"""


#following values are the limits of C_Types
        
#the maximum and minimum amounts a regular unsigned int can have in c++
UNSIGNED_INT_MAX = 4294967295
UNSIGNED_INT_MIN = 0

#the maximum and minimum amounts a regular signed int can have in c++
SIGNED_INT_MAX = 2147483647
SIGNED_INT_MIN = -2147483648


#the numbers of places after a decimal in a double
DOUBLE_PLACE_LIMIT = 5

#MUST EMULATE DOUBLES BETTER
DOUBLE_WHAT = "FIX THIS"

#the maximum and minimum amounts a regular unsigned char can have in c++
UNSIGNED_CHAR_MAX = 255
UNSIGNED_CHAR_MIN = 0

#the maximum and minimum amounts a regular signed char can have in c++
SIGNED_CHAR_MAX = 127
SIGNED_CHAR_MIN = -128


#following classes deal with modeling c++ types

#base class for all c++ types (thus no constructor)
class C_Type:
    
    #special operator that models c++'s upper and lower bounds
    #like how a signed char loops from 127 to -128
    def limit_oper(self, oper, other):
        other = type(self.value)(other)
        temp = eval(str(self.value) + oper + str(other))
        temp2 = temp % self.limits_distance
        if (self.sign == SIGNS["signed"] and
            int(temp2) >= self.limits_distance / 2):
            temp2 -= self.limits_distance
        if temp != temp2:
            print("wrap-around:", temp, "becomes", temp2)
        return temp2

    #returns value of object
    def output(self):
        return self.value

    #checks if the object is compatible with the operator it is using
    #IMPORTANT: function is not completed, and runs with the expectation that
    #all C_Type derivates are compatible with all the operators included
    #here (which is the case now but won't be later)
    def oper_compat(self, oper):
        if oper in self.accepted_opers:
            return True
        #to be later implemented:
        #raise Invalid_Operator("Depreciated")

    #checks if the object is compatible with the object it is being combined with
    #IMPORTANT: function is not completed, and runs with the expectation that
    #all C_Type derivates are compatible with each other (which is the case
    #now but won't be later)
    def other_compat(self, other):
        if type(self) == C_Double or type(other) == C_Double:
            return True
        return False
        #to be later implemented:
        #raise Cannot_Convert("Depreciated")
    
    #following functions model the C++ operators
    #can be overriden by derived classes for functionality, although none
    #are now
    def __add__(self, other):
        if self.oper_compat(SYMBOLS["add"]):
            type_change = C_Double if self.other_compat(other) else C_Int
            if (self.sign is SIGNS["unsigned"] or \
                other.sign is SIGNS["unsigned"]) and \
               (type(self) is C_Int or \
                type(other) is C_Int):
                new_sign = SIGNS["unsigned"]
            else:
                new_sign = SIGNS["signed"]
            return type_change(self.value + other.value, sign = new_sign)
        
    def __sub__(self, other):
        if self.oper_compat(SYMBOLS["subtract"]):
            type_change = C_Double if self.other_compat(other) else C_Int
            if (self.sign is SIGNS["unsigned"] or \
                other.sign is SIGNS["unsigned"]) and \
               (type(self) is C_Int or \
                type(other) is C_Int):
                new_sign = SIGNS["unsigned"]
            else:
                new_sign = SIGNS["signed"]
            return type_change(self.value - other.value, sign = new_sign)
        
    def __mul__(self, other):
        if self.oper_compat(SYMBOLS["times"]):
            type_change = C_Double if self.other_compat(other) else C_Int
            if (self.sign is SIGNS["unsigned"] or \
                other.sign is SIGNS["unsigned"]) and \
               (type(self) is C_Int or \
                type(other) is C_Int):
                new_sign = SIGNS["unsigned"]
            else:
                new_sign = SIGNS["signed"]
            return type_change(self.value * other.value, sign = new_sign)

    #method can throw Divided_By_0 exception
    def __truediv__(self, other):
        if self.oper_compat(SYMBOLS["divide"]):
            type_change = C_Double if self.other_compat(other) else C_Int
            if (self.sign is SIGNS["unsigned"] or \
                other.sign is SIGNS["unsigned"]) and \
               (type(self) is C_Int or \
                type(other) is C_Int):
                new_sign = SIGNS["unsigned"]
            else:
                new_sign = SIGNS["signed"]
            try:
                return type_change(self.value / other.value, sign = new_sign)
            except ZeroDivisionError:
                raise Divided_By_0(saved_offsets[-2], saved_offsets[-1])

    #method can throw Divided_By_0 and Double_Modulo exceptions
    def __mod__(self, other):
        #if type(self) is C_Double or type(other) is C_Double:
            #raise Double_Modulo(0 \
                                #placeholder
                                #)
        if self.oper_compat(SYMBOLS["modulo"]):
            type_change = C_Double if self.other_compat(other) else C_Int
            if (self.sign is SIGNS["unsigned"] or \
                other.sign is SIGNS["unsigned"]) and \
               (type(self) is C_Int or \
                type(other) is C_Int):
                new_sign = SIGNS["unsigned"]
            else:
                new_sign = SIGNS["signed"]
            try:
                return type_change(self.value % other.value, sign = new_sign)
            except ZeroDivisionError:
                raise Divided_By_0(saved_offsets[-2], saved_offsets[-1])
        
    def __lt__(self, other):
        if self.oper_compat(SYMBOLS["less_than"]):
            self.other_compat(other)
            return C_Bool(self.value < other)
        
    def __gt__(self, other):
        if self.oper_compat(SYMBOLS["grt_than"]):
            self.other_compat(other)
            return C_Bool(self.value > other)
        
    def __le__(self, other):
        if self.oper_compat(SYMBOLS["less_or_eql"]):
            self.other_compat(other)
            return C_Bool(self.value <= other)
        
    def __ge__(self, other):
        if self.oper_compat(SYMBOLS["grt_or_eql"]):
            self.other_compat(other)
            return C_Bool(self.value >= other)
        
    def __eq__(self, other):
        if self.oper_compat(SYMBOLS["eql_check"]):
            self.other_compat(other)
            return C_Bool(self.value == other)
        
    def __ne__(self, other):
        if self.oper_compat(SYMBOLS["uneql_check"]):
            self.other_compat(other)
            return C_Bool(self.value != other)
        
    def __iadd__(self, other):
        if self.oper_compat(SYMBOLS["add_eql"]):
            return type(self)(self + other, sign = self.sign)
            
    def __isub__(self, other):
        if self.oper_compat(SYMBOLS["subtract_eql"]):
            return type(self)(self - other, sign = self.sign)

#models a C++ integer
class C_Int(C_Type):
    
    def __init__(self, arg, sign = SIGNS["signed"], init = True):
        #placeholder value
        self.value = 0

        #list of acceptable operators (all of them as of now)
        self.accepted_opers = [SYMBOLS["subtract_eql"],
                               SYMBOLS["add_eql"],
                               SYMBOLS["uneql_check"],
                               SYMBOLS["grt_or_eql"],
                               SYMBOLS["less_or_eql"],
                               SYMBOLS["increment"],
                               SYMBOLS["deincrement"],
                               SYMBOLS["eql_check"],
                               SYMBOLS["add"],
                               SYMBOLS["subtract"],
                               SYMBOLS["times"],
                               SYMBOLS["divide"],
                               SYMBOLS["modulo"],
                               SYMBOLS["grt_than"],
                               SYMBOLS["less_than"]]
        
        #whether int is signed or unsigned (keyword argument, signed by default)
        self.sign = sign
        
        #sets limits and limit distances based on whether int is signed or not
        if self.sign == SIGNS["signed"]:
            self.upper_limit = SIGNED_INT_MAX
            self.lower_limit = SIGNED_INT_MIN
        else:
            self.upper_limit = UNSIGNED_INT_MAX
            self.lower_limit = UNSIGNED_INT_MIN
        self.limits_distance = self.upper_limit + abs(self.lower_limit) + 1
        self.set_value(arg)
        #tells if initialized or not
        self.init = init

    #sets value (obviously), designed to handle all other C++ types
    #as well as Python base types too
    def set_value(self, arg):
        if issubclass(type(arg), C_Type):
            temp = arg.value
            if type(temp) is str and len(temp) == 1:
                self.value = ord(temp)
            else:
                self.value = int(self.limit_oper(SYMBOLS["add"], temp))
        else:
            if type(arg) is str and len(arg) == 1:
                self.value = ord(arg)
            else:
                self.value = int(self.limit_oper(SYMBOLS["add"], arg))

#models a c++ double
class C_Double(C_Type):
    
    #if confused about the methods see C_Int's documentation
    #the specifics are so similar they can be explained there
    def __init__(self, arg, sign = SIGNS["signed"], init = True):
        self.value = 0.0
        self.accepted_opers = [SYMBOLS["subtract_eql"],
                               SYMBOLS["add_eql"],
                               SYMBOLS["uneql_check"],
                               SYMBOLS["grt_or_eql"],
                               SYMBOLS["less_or_eql"],
                               SYMBOLS["increment"],
                               SYMBOLS["deincrement"],
                               SYMBOLS["eql_check"],
                               SYMBOLS["add"],
                               SYMBOLS["subtract"],
                               SYMBOLS["times"],
                               SYMBOLS["divide"],
                               SYMBOLS["modulo"],
                               SYMBOLS["grt_than"],
                               SYMBOLS["less_than"]]
        self.sign = sign
        self.set_value(arg)
        self.init = init

    def set_value(self, arg):
        if issubclass(type(arg), C_Type):
            temp = arg.value
            if type(temp) is str and len(temp) == 1:
                self.value = float(ord(temp))
            else:
                self.value = float(temp)
        else:
            if type(arg) is str and len(arg) == 1:
                self.value = float(ord(arg))
            else:
                self.value = float(arg)

    #overrides C_Type for customizability
    def output(self):
        return round(self.value, DOUBLE_PLACE_LIMIT)
    
#models a c++ bool
#no limits since bools are so simple they don't need any
class C_Bool(C_Type):
    
    #if confused about the methods see C_Int's documentation
    #the specifics are so similar they can be explained there
    def __init__(self, arg, sign = SIGNS["signed"], init = True):
        self.value = 0
        self.accepted_opers = [SYMBOLS["subtract_eql"],
                               SYMBOLS["add_eql"],
                               SYMBOLS["uneql_check"],
                               SYMBOLS["grt_or_eql"],
                               SYMBOLS["less_or_eql"],
                               SYMBOLS["increment"],
                               SYMBOLS["deincrement"],
                               SYMBOLS["eql_check"],
                               SYMBOLS["add"],
                               SYMBOLS["subtract"],
                               SYMBOLS["times"],
                               SYMBOLS["divide"],
                               SYMBOLS["modulo"],
                               SYMBOLS["grt_than"],
                               SYMBOLS["less_than"]]
        self.sign = sign
        self.set_value(arg)
        self.init = init

    def set_value(self, arg):
        if issubclass(type(arg), C_Type):
            temp = arg.value
            if type(temp) is str and len(temp) == 1:
                self.value = bool(ord(temp))
            else:
                self.value = bool(self.value + temp)
        else:
            if type(arg) is str and len(arg) == 1:
                self.value = bool(ord(arg))
            else:
                self.value = bool(self.value + arg)

class C_Char(C_Type):

    #if confused about the methods see C_Int's documentation
    #the specifics are so similar they can be explained there
    def __init__(self, arg, sign = SIGNS["signed"], init = True):
        self.value = 0
        self.accepted_opers = [SYMBOLS["subtract_eql"],
                               SYMBOLS["add_eql"],
                               SYMBOLS["uneql_check"],
                               SYMBOLS["grt_or_eql"],
                               SYMBOLS["less_or_eql"],
                               SYMBOLS["increment"],
                               SYMBOLS["deincrement"],
                               SYMBOLS["eql_check"],
                               SYMBOLS["add"],
                               SYMBOLS["subtract"],
                               SYMBOLS["times"],
                               SYMBOLS["divide"],
                               SYMBOLS["modulo"],
                               SYMBOLS["grt_than"],
                               SYMBOLS["less_than"]]
        self.sign = sign
        if self.sign == SIGNS["signed"]:
            self.upper_limit = SIGNED_CHAR_MAX
            self.lower_limit = SIGNED_CHAR_MIN
        else:
            self.upper_limit = UNSIGNED_CHAR_MAX
            self.lower_limit = UNSIGNED_CHAR_MIN
        self.limits_distance = self.upper_limit + abs(self.lower_limit) + 1
        self.set_value(arg)
        self.init = init

    def set_value(self, arg):
        if issubclass(type(arg), C_Type):
            temp = arg.value
            if type(temp) is str and len(temp) == 1:
                self.value = ord(temp)
            else:
                self.value = int(self.limit_oper(SYMBOLS["add"], temp))
        else:
            if type(arg) is str and len(arg) == 1:
                self.value = ord(arg)
            else:
                self.value = int(self.limit_oper(SYMBOLS["add"], arg))

    #overrides C_Type for customizability
    def output(self):
        if self.sign == SIGNS["signed"]:
            if self.value < 0:
                return chr(self.limits_distance + self.value)
        return chr(self.value)
    
