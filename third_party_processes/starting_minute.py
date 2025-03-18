import subprocess
import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

COLLECTING_INFO = '../classification_of_data/collecting_information.py'
INTEGRATION = '../website/integration.py'
REPORT = '../export_to_excel/reports.py'

SCRIPT_DIR_ONE = os.path.dirname(os.path.abspath(COLLECTING_INFO))
SCRIPT_DIR_TWO = os.path.dirname(os.path.abspath(INTEGRATION))
SCRIPT_DIR_THREE = os.path.dirname(os.path.abspath(REPORT))

TIMEOUT_COLLECTING = 40
TIMEOUT_RETRY = 120
TIMEOUT_INTEGRATION = 30

def run_script(script, cwd, timeout=None):
    try:
        logging.info(f"Запуск скрипта: {script}")
        result = subprocess.run(['python', script], cwd=cwd, timeout=timeout)
        if result.returncode == 0:
            logging.info(f"Скрипт {script} выполнен успешно.")
            return True
        else:
            logging.error(f"Скрипт {script} завершился с ошибкой. Код возврата: {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        logging.warning(f"Скрипт {script} превысил таймаут {timeout} секунд.")
        return False
    except Exception as e:
        logging.error(f"Ошибка при выполнении скрипта {script}: {e}")
        return False

def run_report():
    try:
        logging.info(f"Запуск скрипта REPORT (без таймаута)...")
        subprocess.run(['python', REPORT], cwd=SCRIPT_DIR_THREE)
    except Exception as e:
        logging.error(f"Ошибка при выполнении скрипта REPORT: {e}")

def run_collecting():
    try:
        if run_script(COLLECTING_INFO, SCRIPT_DIR_ONE, TIMEOUT_COLLECTING):
            return True
        else:
            logging.info("Повторный запуск COLLECTING_INFO...")
            return run_script(COLLECTING_INFO, SCRIPT_DIR_ONE, TIMEOUT_RETRY)
    except Exception as e:
        logging.error(f"Ошибка в run_collecting: {e}")
        return False

def run_integration():
    try:
        run_script(INTEGRATION, SCRIPT_DIR_TWO, TIMEOUT_INTEGRATION)
    except Exception as e:
        logging.error(f"Ошибка в run_integration: {e}")

def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(run_report)

        while True:
            try:
                logging.info("Запуск COLLECTING_INFO и INTEGRATION...")
                future_collecting = executor.submit(run_collecting)
                future_integration = executor.submit(run_integration)

                if future_collecting.result():
                    logging.info("COLLECTING_INFO завершен успешно.")
                else:
                    logging.error("COLLECTING_INFO завершился с ошибкой.")

                future_integration.result()

                logging.info("Ожидание следующего запуска через 1 час...")
                time.sleep(3600)
            except KeyboardInterrupt:
                logging.info("Программа завершена пользователем.")
                break
            except Exception as e:
                logging.error(f"Ошибка в основном цикле: {e}")
                time.sleep(60)

if __name__ == "__main__":
    main()
