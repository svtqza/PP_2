import shutil
import os

os.makedirs("destination", exist_ok=True)

shutil.move("sample.txt", "destination/sample.txt")

for file in os.listdir("destination"):
    if file.endswith(".txt"):
        print("Found:", file)