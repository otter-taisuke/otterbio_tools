import os
from glob import glob

from constants import BLAST_DIR
from utils.file_loader import load_fasta, load_input
from constants import *


def merge_fasta(check: bool =False) -> None:
    """check means to skip ths species is not in species list."""
    blast_files = glob(os.path.join(BLAST_DIR, "*", "*.txt"))  # blast/species/gene.txt
    check_species = load_input()
    species = []
    for blast_file in blast_files:
        if os.path.splitext(os.path.basename(blast_file))[0] not in species:
            species.append(os.path.splitext(os.path.basename(blast_file))[0])
    for s in species:
        if s not in check_species and check:
            continue
        files = glob(os.path.join(blast_dir, "slc26a*", f"{s}.txt"))
        merge_dict = {}
        for file in files:
            seq_d = load_fasta(file)
            flag = 0
            for key, value in seq_d.items():
                if flag == 6:
                    break
                if key not in merge_dict:
                    merge_dict[key] = value
                flag += 1
        with open(os.path.join(merged_dir, f"{s}.txt"), mode="w") as f:
            for k, v in merge_dict.items():
                f.write(f"{k}\n{v}\n")
