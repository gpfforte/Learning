from pathlib import Path
from rich import print

print(Path(__file__).parent / "servizio")
print(Path(__file__).parent)
print(Path().resolve())
print(Path(__file__).cwd())
print(Path(__file__).resolve())


all_obj = Path().iterdir()
# for p in all_obj:
#     print(p)