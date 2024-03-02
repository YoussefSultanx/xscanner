import subprocess

# Assuming PwnXSS.py is in the same directory as this script
# If not, provide the full path to PwnXSS.py
script_path = "./PwnXSS.py"

# Example command line arguments to pass to PwnXSS.py
# Modify these according to your requirements
args = ["python3", script_path, "-u", "http://testphp.vulnweb.com", "--depth", "1"]

# Trigger the script
subprocess.run(args)

print("ITS OVER ")