import sqlite3
import subprocess
from telegram.ext import Updater, CommandHandler

DB_PATH = "users.db"
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_CHAT_ID = 123456789  # Replace with your own Telegram numeric ID

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id TEXT PRIMARY KEY,
            port TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(chat_id, port):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (chat_id, port) VALUES (?, ?)", (chat_id, port))
    conn.commit()
    conn.close()

def get_port(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT port FROM users WHERE chat_id=?", (chat_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_port_download(port):
    try:
        result = subprocess.run(['sudo', 'iptables', '-L', 'PORT_TRAFFIC', '-v', '-n'],
                                capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if f"dpt:{port}" in line:
                parts = line.split()
                bytes_download = int(parts[1])
                return round(bytes_download / 1024 / 1024, 2)
    except Exception as e:
        print("Error reading iptables:", e)
    return 0.0

def start(update, context):
    update.message.reply_text("سلام! اگر توسط مدیر ثبت شده باشید، با /usage می‌توانید مصرف دانلود پورت خود را ببینید.")

def register(update, context):
    if update.message.chat_id != ADMIN_CHAT_ID:
        update.message.reply_text("⛔ فقط مدیر می‌تواند کاربران را ثبت کند.")
        return

    if len(context.args) != 2:
        update.message.reply_text("فرمت صحیح: /register chat_id port")
        return

    chat_id, port = context.args
    if not port.isdigit():
        update.message.reply_text("پورت معتبر نیست.")
        return

    register_user(chat_id, port)
    subprocess.run(['sudo', 'iptables', '-C', 'PORT_TRAFFIC', '-p', 'tcp', '--dport', port, '-j', 'ACCEPT'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'iptables', '-A', 'PORT_TRAFFIC', '-p', 'tcp', '--dport', port, '-j', 'ACCEPT'])

    update.message.reply_text(f"✅ پورت {port} برای chat_id {chat_id} ثبت شد.")

def usage(update, context):
    chat_id = str(update.message.chat_id)
    port = get_port(chat_id)
    if not port:
        update.message.reply_text("⛔ شما هنوز توسط مدیر ثبت نشده‌اید.")
        return

    downloaded = get_port_download(port)
    update.message.reply_text(f"📥 پورت {port}:
🔻 دانلود: {downloaded:.2f} MB")

def all_usage(update, context):
    if update.message.chat_id != ADMIN_CHAT_ID:
        update.message.reply_text("⛔ فقط مدیر به این دستور دسترسی دارد.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id, port FROM users")
    rows = c.fetchall()
    conn.close()

    if not rows:
        update.message.reply_text("هیچ کاربری ثبت نشده است.")
        return

    msg = "📊 مصرف همه کاربران:
"
    for chat_id, port in rows:
        traffic = get_port_download(port)
        msg += f"👤 {chat_id} | پورت {port} → {traffic:.2f} MB
"
    update.message.reply_text(msg)

def main():
    init_db()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("usage", usage))
    dp.add_handler(CommandHandler("allusage", all_usage))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
