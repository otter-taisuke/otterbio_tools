import os


__all__ = [
    "ROOT_DIR", "BLAST_DIR", "SPECIES_DIR", "EXCEL_DIR", "FASTA_DIR", "DATABASE_DIR", 
    "BLAST_VALID_NUM", "PROTEIN_LEN_FILTER", 
    ]


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
BLAST_DIR = os.path.join(ROOT_DIR, "blast")
SPECIES_DIR = os.path.join(ROOT_DIR, "species")
EXCEL_DIR = os.path.join(ROOT_DIR, "excel")
FASTA_DIR = os.path.join(ROOT_DIR, "fasta")
DATABASE_DIR = r"X:\BIO\database"

BLAST_VALID_NUM = 6
PROTEIN_LEN_FILTER = 9999
