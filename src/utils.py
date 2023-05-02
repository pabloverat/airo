# utils.py

def read_file(fname: str) -> str:
    with open(fname) as f:
        return '\n'.join(line.rstrip() for line in f)