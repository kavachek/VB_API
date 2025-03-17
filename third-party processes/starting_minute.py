import subprocess
import os
import time

COLLECTING_INFO = '../classification_of_data/collecting_information.py'
INTEGRATION = '../website/integration.py'
SCRIPT_DIR_ONE = os.path.dirname(os.path.abspath(COLLECTING_INFO))
SCRIPT_DIR_TWO = os.path.dirname(os.path.abspath(INTEGRATION))

def run_process():
    try:
        one_process = subprocess.run(['python', COLLECTING_INFO], timeout=30, cwd=SCRIPT_DIR_ONE)

        if one_process.returncode == 0: subprocess.run(['python', INTEGRATION], timeout=30,
                                                                     cwd=SCRIPT_DIR_TWO)

    except subprocess.TimeoutExpired:
        try:
            one_process_retry = subprocess.run(['python', COLLECTING_INFO], timeout=120, cwd=SCRIPT_DIR_ONE)
            if one_process_retry.returncode == 0: subprocess.run(['python', INTEGRATION], timeout=30,
                                                                         cwd=SCRIPT_DIR_TWO)
            else: return
        except subprocess.TimeoutExpired: return None


while True:
    run_process()
    time.sleep(3600)
