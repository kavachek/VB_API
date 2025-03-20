import subprocess
import sys

modules = [
    "Flask==3.0.0",
    "Werkzeug==3.0.1",
    "requests==2.31.0",
    "pandas==2.1.2",
    "gspread==6.0.0",
    "oauth2client==4.1.3",
    "google-api-python-client==2.104.0",
    "google-auth==2.23.3",
    "google-auth-httplib2==0.1.1",
    "google-auth-oauthlib==1.0.0",
    "google-cloud-speech==2.17.0",
    "openpyxl==3.1.2",
    "flask-cors==4.0.0"
]

def install_modules():
    for module in modules:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            return f"Модуль {module} успешно установлен."
        except subprocess.CalledProcessError as e: return f"Ошибка при установке модуля {module}: {e}"

if __name__ == "__main__":
    install_modules()