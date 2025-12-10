import os
from glob import glob
from traceback import print_exc

import openpyxl as pyxl
import pandas as pd

from constants import BLAST_DIR
from utils.file_loader import *
from constants import *


def merge_fasta(gene_prefix: str = "slc26", check: bool = False) -> None:
    """
    blast結果を統合するために作成
    blast/species/query.txtの中から、queryがgene_prefixとマッチするものを選択し、
    その中の上位BLAST_VALID_NUM件の配列を全てfasta/gene_prefix/species_gene_prefix.fastaに統合する。
    """
    blast_files = glob(os.path.join(BLAST_DIR, "*", f"*{gene_prefix}*.txt"))  # blast/species/query.txt
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
                if flag == BLAST_VALID_NUM:
                    break
                if key not in merge_dict:
                    merge_dict[key] = value
                flag += 1
        os.makedirs(os.path.join(FASTA_DIR, gene_prefix), exist_ok=True)
        # ディレクトリツリーが深くなるから問題が起きてからfasta/merged/gene/*.fastaにする
        with open(os.path.join(FASTA_DIR, gene_prefix, f"{s}_{gene_prefix}.fasta"), mode="w") as f:
            for k, v in merge_dict.items():
                f.write(f"{k}\n{v}\n")


def create_fasta_from_excel(excelpath: str = "", gene_prefix: str = "") -> None:
    """
    excelからfastaを作成
    必要列はAbberation, ProteinName, AccesisonNo, Sequence
    ProteinNameは空欄可
    """
    if excelpath == "":
        try:
            excelpath = glob(os.path.join(EXCEL_DIR, f"*{input("enter excel file name in excel dir: ")}*"))[0]
        except IndexError:
            print("excel file is not found.")
            return
    output_dir = os.path.join(FASTA_DIR, "from_excel")
    os.makedirs(output_dir, exist_ok=True)
    sheet_list = pyxl.load_workbook(excelpath).sheetnames
    for sheet in sheet_list:
        df = pd.read_excel(excelpath, sheet_name=sheet, header=0, index_col=None, dtype=str)
        df.fillna("", inplace=True)
        with open(os.path.join(output_dir, f"{sheet}.fasta")) as f:
            for abb, prot, acc, seq in zip(df["Abberation"], df["ProteinName"], df["AccessionNo"], df["Sequence"]):
                if prot == "":
                    prot = "UN"
                if abb == "" or acc == "" or seq == "":
                    print(f"the protein \"{abb}-{prot}({acc})\" is skipped by containing blank")
                    continue
                if len(seq) > PROTEIN_LEN_FILTER:
                    print(f"the protein \"{abb}-{prot}({acc})\" is filtered by PROTEIN_LEN_FILTER.")
            f.write(f">{abb}_{gene_prefix}{prot}_{acc}\n{seq}\n")
