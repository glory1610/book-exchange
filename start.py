import subprocess
import time

print("🟢 Запускаємо сервер...")
server_process = subprocess.Popen(["python3", "server.py"])

time.sleep(2)

print("🌐 Запускаємо клієнт...")
subprocess.run([
    "streamlit", "run", "client.py",
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false"
])

server_process.terminate()
