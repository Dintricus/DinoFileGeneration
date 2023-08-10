ASCII_REPRESENTATIONS = {
    "NOTHING": [[]],
    "TEST": [
        ["/", "=", "=", "\\"],
        ["|", "T", "E", "|"],
        ["|", "S", "T", "|"],
        ["\\", "=", "=", "/"],
    ],
    "CURSOR": [
        ["", "", "", ""],
        ["", "/", "\\", ""],
        ["", "\\", "/", ""],
        ["", "", "", ""],
    ],
    "WOOD_WALL": [
        ["+", "=", "=", "+"],
        ["|", "W", "O", "|"],
        ["|", "O", "D", "|"],
        ["+", "=", "=", "+"],
    ],
    "WOOD_WINDOW": [
        ["+", "W", "O", "+"],
        ["|", " ", " ", "|"],
        ["|", "_", "_", "|"],
        ["+", "O", "D", "+"],
    ],
    "WOOD_DOOR": [
        ["+", "W", "O", "+"],
        ["|", "O", "D", "|"],
        ["|", "D", "O", "|"],
        ["+", "O", "R", "+"],
    ],
    "HUMAN": [
        [" ", "@", " ", "H"],
        ["-", "|", "-", "M"],
        [" ", "^", " ", "A"],
        ["/", " ", "\\", "N"],
    ]
}

def getAsciiRepresentation(name):
    return ASCII_REPRESENTATIONS.get(name)