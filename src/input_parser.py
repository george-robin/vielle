from src.generator import CHORD_SHAPES

def parse_progression(text):
    if not isinstance(text,str) or not text.strip():
        raise ValueError("Enter atleast one chord")
    if "\n" in text or "\r" in text:
        raise ValueError("Only write progression in one line")

    text = text.replace(",", " ").replace("-", " ").split()
    chords = []
    for chord in text:
        chord = chord.strip().capitalize()
        if chord in CHORD_SHAPES:
            chords.append(chord)
        else:
            raise ValueError("Invalid/Unsupported chord")
    return(chords)