import os
from telegram.ext import Application
from dotenv import load_dotenv
import asyncio
import re
import html


load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def enviar_mensagem(txt):
    app = Application.builder().token(TOKEN).build()
    try:
        await app.bot.send_message(chat_id=CHAT_ID, text=txt, parse_mode='HTML')
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
    finally:
        await app.shutdown()

def escapar_markdown(texto):
    # Lista de caracteres especiais que precisam ser escapados no Markdown V2
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', texto)

def escapar_html(texto):
    return html.escape(texto, quote=True)
