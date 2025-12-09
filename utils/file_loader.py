import os
from glob import glob
from shutil import SpecialFileError
from typing import Literal


from constants import *
from constants import SPECIES_DIR

__all__ = ["load_input", "load_fasta", "select_species", ]


def load_input(path) -> list[str]:
    for enc in ["utf-8", "shift-jis", "cp932"]:
        try:
            with open(path, "r", encoding=enc) as f:
                inputs = f.read().splitlines()
            break
        except UnicodeDecodeError:
            continue
    if inputs is None:
        print(f"Error: Could not load \"{os.path.basename(path)}\" in utf-8, shift-jis, cp932.")
        return []
    return inputs


def load_fasta(path) -> None | dict:
    lines = load_input(path)
    if lines is None:
        return None
    seq_dict = {}
    former_seq = ""
    for line in lines:
        if line != "":
            if line[0] == '>':
                acc = line.split(" ")[0]
                seq_dict[acc] = ""
                former_seq = acc
            else:
                seq_dict[former_seq] += line.splitlines()[0]
    return seq_dict


GAP_TYPE = Literal["blank", "unnderscore"]
def load_sepcies(tag: str = "", gap: GAP_TYPE = "blank") -> list[str]:
    if tag != "" and os.path.exists(os.path.join(SPECIES_DIR, f"species_for_{tag}.txt")):
        species = load_input(os.path.join(SPECIES_DIR, f"species_for_{tag}.txt")) 
    else:
        species =  load_input(os.path.join(SPECIES_DIR, "species.txt"))

    match gap:
        case "blank":
            species = [s.replace("_", " ") for s in species]
        case "unnderscore":
            species = [s.replace(" ", "_") for s in species]

    return list(set(species))
