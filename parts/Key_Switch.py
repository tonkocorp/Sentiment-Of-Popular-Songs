def keySwitch(int):

    switch = {
        0: "C",
        1: "C#/D♭ ",
        2: "D",
        3: "D#/E♭",
        4: "E",
        5: "F",
        6: "F#/G♭",
        7: "G",
        8: "G#/A♭",
        9: "A",
        10: "A#/B♭",
        11: "B"

    }

    return switch.get(int, "no key value")

#print(keySwitch(1))