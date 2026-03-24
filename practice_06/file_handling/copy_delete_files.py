import shutil
import os

with open("sample.txt", "a") as f:
    f.write("Appended line.\n")


shutil.copy("sample.txt", "backup_sample.txt")
print("File copied successfully.")


if os.path.exists("backup_sample.txt"):
    os.remove("backup_sample.txt")
    print("Backup file deleted.")
else:
    print("File not found.")