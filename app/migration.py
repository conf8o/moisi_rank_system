from config import DATABASE_URL
import sys
import subprocess
import os

# 設定ファイルの初期化
ini_template = open("./migration/alembic.ini_temp.txt").read()
with open("./migration/alembic.ini", "w") as f:
    f.write(ini_template.format(DATABASE_URL))

# 引数
_, direction, version = sys.argv

# マイグレーションのフォルダで、alembicを実行
os.chdir("./migration")

result = subprocess.run(
    f"alembic {direction} {version}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(result.returncode)
print(result.stdout)
print(result.stderr)
