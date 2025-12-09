import os
from glob import glob

from constants import BLAST_DIR
from utils.file_loader import *
from constants import *
from utils.file_loader import load_sepcies


def merge_fasta(gene_prefix: str = "slc26", check: bool = False) -> None:
    """check means to skip ths species is not in species list."""
    blast_files = glob(os.path.join(BLAST_DIR, "*", "*.txt"))  # blast/species/gene.txt
    check_species = load_sepcies("check")
    species = []
    for blast_file in blast_files:
        if os.path.basename(os.path.dirname(blast_file)) not in species:
            species.append(os.path.basename(os.path.dirname(blast_file)))
    for s in species:
        if s not in check_species and check:
            continue
        files = glob(os.path.join(BLAST_DIR, s, f"*{gene_prefix}*.txt"))
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
        with open(os.path.join(BLAST_DIR, s, f"{gene_prefix}_merged.txt"), mode="w") as f:
            for k, v in merge_dict.items():
                f.write(f"{k}\n{v}\n")


def create_fasta_from_excel(excelpath: str) -> None:
    pass
