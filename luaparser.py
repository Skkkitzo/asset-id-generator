class LuaStringError(Exception):
    """Exception raised when a lua formatting error is discovered

    Attributes:
        message -- explanation of the error message
    """

    def __init__(self, message = "Lua formatting error"):
        self.message = message
        super().__init__(self.message)

def get_string_contents(string):
    indexTupleList = [ ]

    a = None

    # Find the indexes at which the strings start and end
    for i in range(0, len(string)):
        char = string[i]

        if char == "\"" or char == "\'":
            if string[i - 1] != "\\": # ignore all ' and " that are included in the string
                if a == None:
                    a = i
                else:
                    indexTupleList.append((a, i))
                    a = None

    # If lua code is being funky, let's just raise an exception
    if a != None:
        raise LuaStringError
    
    # Get the strings from the designated indexes
    strings = [ ]

    for a,b in indexTupleList:
        strings.append(string[a+1:b])

    return strings


if __name__ == "__main__":
    print("Script not to be run indepedently, please import as module")

