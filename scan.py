from pathlib import Path
import shutil

files = []
for i in Path("History").iterdir():
    if 'completed' not in i.stem and i.exists():
        shutil.rmtree(i.absolute())


