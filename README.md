# Telegram Bot - V2Ray Port Traffic Monitor (Download Only)

## 🔧 Features

- Users can only view their download usage.
- Only the admin can register ports for users.
- Admin can see download usage of all users.

## 🚀 Setup

```bash
chmod +x setup.sh
./setup.sh
```

Edit `bot.py`:
- Replace `YOUR_BOT_TOKEN_HERE` with your Telegram bot token
- Set `ADMIN_CHAT_ID` to your Telegram numeric ID

## 🧪 Run the bot

```bash
python3 bot.py
```

## 📋 Commands

- `/start` - Welcome message
- `/usage` - Check user's download usage
- `/register chat_id port` - Admin only: register user to a port
- `/allusage` - Admin only: view all user traffic
