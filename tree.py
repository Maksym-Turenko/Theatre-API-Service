from pathlib import Path

EXCLUDE = {'__pycache__', '.git', '.venv', 'env', '.env', 'venv', '.gitignore', '.dockerignore', 'migrations'}

def tree(directory: Path, prefix: str = ""):
    contents = [p for p in directory.iterdir() if p.name not in EXCLUDE]
    pointers = [content for content in contents if content.is_file()]
    for pointer in pointers:
        print(f"{prefix}├── {pointer.name}")
    pointers = [content for content in contents if content.is_dir()]
    for pointer in pointers:
        print(f"{prefix}└── {pointer.name}")
        tree(pointer, prefix + "    ")

tree(Path('.'))
