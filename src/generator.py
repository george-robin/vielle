CHORD_SHAPES = { "C": [0,1,0,2,3,'X'],
                 "A": [0,2,2,2,0,'X'],
                 "G": [3,0,0,0,2,3],
                 "E": [0,0,1,2,2,0],
                 "D": [2,3,2,0,'X','X'],
                 "F": [1,1,2,3,3,'X'],
                 "Em":[0,0,0,2,2,0],
                 "Am":[0,1,2,2,0,'X'],
                 "Dm":[1,3,2,0,'X','X']}

STRING_NAMES = ['e','B','G','D','A','E']
COLUMN_WIDTH = 12

def generate_progression_tab(chord_names):
    if len(chord_names) < 2:
        raise ValueError("Enter at least two chords")
    for name in chord_names:
        if name not in CHORD_SHAPES:
            raise ValueError(f"Unknown chord:,{name}")
    header = "   " + "".join(name.ljust(COLUMN_WIDTH) for name in chord_names)
    lines = [header]
    shapes = [CHORD_SHAPES[name] for name in chord_names]
    for string_index, string_name in enumerate(STRING_NAMES):
        line = f"{string_name}|"
        for shape in shapes:
            fret = shape[string_index]
            fret_text = str(fret)
            cell = "-" + fret_text.ljust(COLUMN_WIDTH - 1, "-")
            line += cell
        lines.append(line + "|")
    return "\n".join(lines)
