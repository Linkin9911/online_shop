import os
import sys
from subprocess import run

# ВАЖНО: Мы явно очищаем переменные окружения, которые могут ломать psycopg2.
# Это безопасно для запуска одной команды.
env = os.environ.copy()

# Удаляем потенциально проблемные переменные, если они есть
for key in ['DOTENV_LOCATION', 'DATABASE_URL', 'PATH']:
    env.pop(key, None)

# Запускаем manage.py migrate в этом «чистом» окружении
result = run([sys.executable, 'manage.py', 'migrate'], env=env)
sys.exit(result.returncode)
