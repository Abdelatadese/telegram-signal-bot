import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

user_settings = {}

def get_user_data(user_id):
    if user_id not in user_settings:
        user_settings[user_id] = {
            "status": "Stopped",
            "balance": 100.0,
            "amount": 10,
            "accuracy": 80,
            "payout": 75,
            "expiration": "1m",
            "limit": 500
        }
    return user_settings[user_id]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    data["status"] = "Active"
    await update.message.reply_text("🚀 Signal Bot አገልግሎት ተጀምሯል!\nሲግናሎችን ለመቀበል ዝግጁ ነው።")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    data["status"] = "Stopped"
    await update.message.reply_text("🛑 Signal Bot አገልግሎት ቆሟል።")

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    await update.message.reply_text(f"💰 ያንተ ወቅታዊ የሂሳብ መጠን: ${data['balance']:.2f}")

async def my_settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    msg = (
        "⚙️ **የአሁኑ መቼቶችህ (Current Settings):**\n\n"
        f"• Status: {data['status']}\n"
        f"• Trade Amount: ${data['amount']}\n"
        f"• Min Accuracy: {data['accuracy']}%\n"
        f"• Min Payout: {data['payout']}%\n"
        f"• Expiration Time: {data['expiration']}\n"
        f"• Balance Limit: ${data['limit']}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 **መቼት ለመቀየር የሚከተሉትን ትእዛዛት መጠቀም ትችላለህ:**\n\n"
        "• `/amount 10` - Trade amount ለመቀየር\n"
        "• `/accuracy 85` - Min accuracy ለመቀየር (%)\n"
        "• `/payout 80` - Min payout ለመቀየር (%)\n"
        "• `/expiration 5m` - Expiration time ለመቀየር\n"
        "• `/limit 1000` - Balance limit ለመቀየር\n"
        "• `/deposit 50` - Deposit ለማድረግ",
        parse_mode="Markdown"
    )

async def amount_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        try:
            val = float(context.args[0])
            data["amount"] = val
            await update.message.reply_text(f"✅ Trade amount ወደ ${val} ተቀይሯል።")
        except ValueError:
            await update.message.reply_text("❌ እባክህ ትክክለኛ ቁጥር አስገባ። ምሳሌ: /amount 15")
    else:
        await update.message.reply_text(f"የአሁኑ Trade Amount: ${data['amount']}\nለመቀየር: `/amount 15` ብለህ ጻፍ።", parse_mode="Markdown")

async def accuracy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        try:
            val = int(context.args[0])
            data["accuracy"] = val
            await update.message.reply_text(f"✅ Minimum accuracy ወደ {val}% ተቀይሯል።")
        except ValueError:
            await update.message.reply_text("❌ እባክህ ትክክለኛ ቁጥር አስገባ። ምሳሌ: /accuracy 85")
    else:
        await update.message.reply_text(f"የአሁኑ Minimum Accuracy: {data['accuracy']}%\nለመቀየር: `/accuracy 85` ብለህ ጻፍ።", parse_mode="Markdown")

async def payout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        try:
            val = int(context.args[0])
            data["payout"] = val
            await update.message.reply_text(f"✅ Minimum payout ወደ {val}% ተቀይሯል።")
        except ValueError:
            await update.message.reply_text("❌ እባክህ ትክክለኛ ቁጥር አስገባ። ምሳሌ: /payout 80")
    else:
        await update.message.reply_text(f"የአሁኑ Minimum Payout: {data['payout']}%\nለመቀየር: `/payout 80` ብለህ ጻፍ።", parse_mode="Markdown")

async def expiration_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        val = context.args[0]
        data["expiration"] = val
        await update.message.reply_text(f"✅ Expiration time ወደ {val} ተቀይሯል።")
    else:
        await update.message.reply_text(f"የአሁኑ Expiration Time: {data['expiration']}\nለመቀየር: `/expiration 5m` ብለህ ጻፍ።", parse_mode="Markdown")

async def limit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        try:
            val = float(context.args[0])
            data["limit"] = val
            await update.message.reply_text(f"✅ Balance limit ወደ ${val} ተቀይሯል።")
        except ValueError:
            await update.message.reply_text("❌ እባክህ ትክክለኛ ቁጥር አስገባ። ምሳሌ: /limit 1000")
    else:
        await update.message.reply_text(f"የአሁኑ Balance Limit: ${data['limit']}\nለመቀየር: `/limit 1000` ብለህ ጻፍ።", parse_mode="Markdown")

async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_data(update.effective_user.id)
    if context.args:
        try:
            val = float(context.args[0])
            data["balance"] += val
            await update.message.reply_text(f"✅ ${val} በስኬት ተጨምሯል!\nአዲሱ ባላንስህ: ${data['balance']:.2f}")
        except ValueError:
            await update.message.reply_text("❌ እባክህ ትክክለኛ የገንዘብ መጠን አስገባ። ምሳሌ: /deposit 50")
    else:
        await update.message.reply_text("Deposit ለማድረግ የገንዘብ መጠኑን አብረህ ጻፍ። ምሳሌ: `/deposit 50`", parse_mode="Markdown")

def main():
    BOT_TOKEN = "8731252801:AAGou6CXmsLIShbpkrfDw-GUxki9NIZ51_0"

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("my_settings", my_settings_command))
    app.add_handler(CommandHandler("amount", amount_command))
    app.add_handler(CommandHandler("accuracy", accuracy_command))
    app.add_handler(CommandHandler("payout", payout_command))
    app.add_handler(CommandHandler("expiration", expiration_command))
    app.add_handler(CommandHandler("limit", limit_command))
    app.add_handler(CommandHandler("deposit", deposit_command))

    print("🤖 ቦቱ ስራ ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()
