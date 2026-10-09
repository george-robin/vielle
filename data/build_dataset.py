import json
import random
from pathlib import Path

from src.generator import CHORD_SHAPES, generate_progression_tab
from src.input_parser import parse_progression

SEED = 42
VOCABULARY = sorted(CHORD_SHAPES)

def progression_id(chords):
    return "|".join(chords)

def variants(chords):
    return {
        "canonical": " - ".join(chords),
        "lowercase": " - ".join(chords).lower(),
        "compact": "-".join(chords),
        "commas": ", ".join(chords),
        "spaces": " ".join(chords),
    }

def make_groups(reserved):
    rng = random.Random(SEED)
    splits = {'train': [], 'val': [], 'test': []}
    for length in range (2,7):
        chosen = set()
        while len(chosen) < 40:
            candidate = tuple(rng.choice(VOCABULARY) for _ in range(length))
            if candidate not in reserved:
                chosen.add(candidate)
        ordered = sorted(chosen)
        rng.shuffle(ordered)
        splits["train"].extend(ordered[:28])
        splits["val"].extend(ordered[28:34])
        splits["test"].extend(ordered[34:])
    return splits

def check_groups(reserved, splits):
    train = set(splits["train"])
    val = set(splits["val"])
    test = set(splits["test"])
    assert train.isdisjoint(val)
    assert train.isdisjoint(test)
    assert val.isdisjoint(test)
    assert (train | val | test).isdisjoint(reserved)
    assert {chord for group in train for chord in group} == set(VOCABULARY)
    for name,groups in splits.items():
        if name == "train":
            expected_per_length = 28
        else:
            expected_per_length = 6
        for length in range(2,7):
            assert sum(len(group) == length for group in groups) == expected_per_length
        assert any(len(set(group)) < len(group) for group in groups)

def make_records(groups):
    records = []
    for group in groups:
        chords = list(group)
        pid = progression_id(chords)
        target = generate_progression_tab(chords)
        for variant,text in variants(chords).items():
            assert parse_progression(text) == chords
            records.append({
                "id": f"{pid}::{variant}",
                "progression_id": pid,
                "chords": chords,
                "variant": variant,
                "input": text,
                "output": target,
            })
    return records

def main():
    fixtures = json.loads(Path("data/golden_tests.json").read_text(encoding="utf-8"))
    assert len(fixtures) == 10
    reserved = {tuple(fixture["chords"]) for fixture in fixtures}
    splits = make_groups(reserved)
    check_groups(reserved, splits)
    paths = { "train": "dataset", "val": "val_set", "test": "test_set" }
    manifest = {"seed" : SEED, "version" : "vielle-data-v1", "splits": {} }
    for split, groups in splits.items():
        records = make_records(groups)        
        path = Path("data") / f"{paths[split]}.jsonl"
        with path.open("x", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record) + "\n")
        manifest["splits"][split] = {
            "groups" : len(groups),
            "rows" : len(records),
            "progression_ids": [progression_id(group) for group in groups],
        }
        print(split, len(groups), len(records))
    manifest["reserved_progression_ids"] = sorted(progression_id(g) for g in reserved)
    with Path("data/split_manifest.json").open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, indent=2) + "\n")

if __name__ == "__main__":
    main()
