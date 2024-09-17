import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
print("base_dir:",base_dir)
parents = Path(__file__).resolve().parents
for item in parents:
    print("parent:",item)
path = Path(__file__).resolve()
print("path:",path)
print("os.name:",os.name)
print("os.environ:", os.environ)
print("os.getlogin():",os.getlogin())
# Get the current working
# directory (CWD)
cwd = os.getcwd()
     
# Print the current working
# directory (CWD)
print("Current working directory:", cwd)
print("os.listdir():",os.listdir())
for item in os.listdir():
    print("size of", item, "is", os.path.getsize(item))
