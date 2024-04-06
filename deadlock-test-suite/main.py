import subprocess
import os


def run_example(file_path):
    try:
        process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=1)
        if stderr:
            return True
        return False
    except subprocess.TimeoutExpired:
        return True


test_folders = ["testcases/CWE667_Improper_Locking", "testcases/CWE833_Deadlock"]

deadlocks_count = 0

for folder in test_folders:
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            print(f'{file_path}')
            if run_example(file_path):
                print(f"Deadlock occurred in {file_path} \n")
                deadlocks_count += 1

print(f"Total deadlocks occurred: {deadlocks_count}")
