import unittest
import subprocess
import os

class TestFlake8(unittest.TestCase):
    def test_flake8_dl_acquiring_in_wrong_order(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_acquiring_in_wrong_order.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_in_class(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_in_class.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_in_decorator(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_in_decorator.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_on_condition(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_on_condition.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_on_event(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_on_event.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_on_event_and_condition(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_on_event_and_condition.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_recursive(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_recursive.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_wait_on_each(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_wait_on_each.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_waits_on_itself(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE833_Deadlock/dl_waits_on_itself.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

    def test_flake8_dl_release_lock_fail(self):
        current_dir = os.getcwd()
        filepath = r"../testcases/CWE667_Improper_Locking/dl_release_lock_fail.py"
        command = ["flake8", "--select=DLC001", filepath]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')

        self.assertIn("DLC001 potential deadlock detected", output)

if __name__ == '__main__':
    unittest.main()
