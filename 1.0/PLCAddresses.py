Ports = {
    "Inputs": {
        "X0": 0,
        "X1": 1,
        "X2": 2,
        "X3": 3,
        "X4": 4,
        "X5": 5,
        "X6": 6,
        "X7": 7,
        "X10": 8,
        "X11": 9,
        "X12": 10,
        "X13": 11,
        "X14": 12,
        "X15": 13,
        "X16": 14,
        "X17": 15,
        "X20": 16,
        "X21": 17,
        "X22": 18,
        "X23": 19,
        "X24": 20,
        "X25": 21,
        "X26": 22,
        "X27": 23,
        "X30": 24,
        "X31": 25,
        "X32": 26,
        "X33": 27,
        "X34": 28,
        "X35": 29,
        "X36": 30,
        "X37": 31,
    },
    "Outputs": {
        "Y0": 0,
        "Y1": 1,
        "Y2": 2,
        "Y3": 3,
        "Y4": 4,
        "Y5": 5,
        "Y6": 6,
        "Y7": 7,
        "Y10": 8,
        "Y11": 9,
        "Y12": 10,
        "Y13": 11,
        "Y14": 12,
        "Y15": 13,
        "Y16": 14,
        "Y17": 15,
        "Y20": 16,
        "Y21": 17,
        "Y22": 18,
        "Y23": 19,
        "Y24": 20,
        "Y25": 21,
        "Y26": 22,
        "Y27": 23,
        "Y30": 24,
        "Y31": 25,
        "Y32": 26,
        "Y33": 27,
        "Y34": 28,
        "Y35": 29,
        "Y36": 30,
        "Y37": 31,
    },
}


def get_bit(port):
    type = list(port)[0]
    if type == "X":
        bit = Ports["Inputs"][port]
    elif type == "Y":
        bit = Ports["Outputs"][port]
    elif type == "M":
        bit = int(port[1:])
    else:
        bit = "Invalid config"
    return type, bit


if __name__ == "__main__":
    io = "M60"
    type, io = get_bit(io)
    print(int(io))
