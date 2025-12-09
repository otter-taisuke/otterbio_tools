import os


__all__ = ["ROOT_DIR", "blast", "species"]


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
BLAST_DIR = os.path.join(ROOT_DIR, "blast")
SPECIES_DIR = os.path.join(ROOT_DIR, "species")
