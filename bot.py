import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from g4f.client import Client

# የቴሌግራም ቦት ቶከንህ
TELEGRAM_TOKEN = '8205927906:AAHD6GfgCFmhXQAjE6ZyV67JUHdAms28gRc'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = Client()

@dp.message(Command("start", "help"))
async def start_handler(message: types.Message):
    welcome = (
        "አሰላሙ አለይኩም ወራህመቱላሂ ወበረካቱህ! 🌍✨\n\n"
        "ወደ አል-ሙዕሚን ኢስላማዊ ቦት በሰላም መጡ። ይህ ቦት ማንኛውንም ኢስላማዊ ጥያቄዎችዎን በጥልቀት ለመመለስ ዝግጁ ነው።\n\n"
        "እባክዎ ጥያቄዎን ያካፍሉኝ።"
    )
    await message.reply(welcome)

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text:
        return

    try:
        system_instruction = (
            "You are Al-Mu'min Islamic Bot, a deeply compassionate and professional Islamic AI assistant.\n\n"
            "CRITICAL RULES:\n"
            "1. NO ARABIC FOR EVIDENCE: When providing Quran verses or Hadiths, you MUST NOT write them in Arabic text. Instead, you MUST translate and write the core meaning of the evidence completely in the user's chosen language (e.g., full Amharic translation if the user asks in Amharic). Always explicitly cite the Surah name/number, Ayah number, or Hadith collection name in that same language.\n"
            "2. MULTILINGUAL & FLUENT: Reply 100% fluently in the exact language the user used (Amharic, Afaan Oromo, etc.).\n"
            "3. FAST AND CONCISE: Keep your responses structurally clean, easy to read, and quick to return."
        )
        
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": message.text}
            ]
        )
        
        answer = response.choices[0].message.content
        if answer:
            await message.reply(answer)
        else:
            await message.reply("እባክዎ ጥያቄዎን በድጋሚ ግልጽ አድርገው ይጻፉልኝ።")
            
    except Exception as error:
        print(f"ስህተት: {error}")
        await message.reply("ውድ ወንድሜ፣ ጥያቄህን ለመመለስ ጥቂት ሰከንዶች ስላለፉኝ ነው። እባክህ አሁኑኑ በድጋሚ ላክልኝ።")

async def main():
    print("Al-Mu'min Bot is running continuously and fast on Render...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
