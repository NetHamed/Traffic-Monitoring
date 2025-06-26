#!/bin/bash

echo "🛠 در حال ساخت دیتابیس..."
python3 -c "
import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (chat_id TEXT PRIMARY KEY, port TEXT)')
conn.commit()
conn.close()
"

echo "🔐 ساخت زنجیره iptables مخصوص پورت‌ها..."
sudo iptables -N PORT_TRAFFIC 2>/dev/null
sudo iptables -C INPUT -j PORT_TRAFFIC 2>/dev/null || sudo iptables -I INPUT -j PORT_TRAFFIC

echo "✅ نصب اولیه کامل شد."
echo "فایل bot.py را ویرایش و سپس اجرا کنید:"
echo "python3 bot.py"
