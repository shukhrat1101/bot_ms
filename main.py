from flask import request
from app import create_app
from app.handlers import dispatcher
from config import BOT_TOKEN
from telegram import Update

app = create_app()

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), dispatcher.bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
