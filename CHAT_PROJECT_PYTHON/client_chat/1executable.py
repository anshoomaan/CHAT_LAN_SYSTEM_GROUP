import os
import subprocess
import time 

print("This is file1.py. It will now run login.py.")

# Run login.py as a subprocess
subprocess.run(["python", "login.py"])

time.sleep(1)  # Pauses execution for 1 second

# After login.py finishes
print("login.py has closed. Now running a_main.py.")
os.execlp("python", "python", "a_main.py")
