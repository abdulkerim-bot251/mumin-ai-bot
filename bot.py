import os
import telebot
from google import genai

# ሰርቨሩ ላይ የምንጭናቸውን የቴሌግራም እና የጌሚኒ ቁልፎች መውሰጃ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ቦቱን እና AI ሲስተሙን ማስነሳት
bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Assalamu Alaikum! Welcome to Mumin Islamic Bot. 🌍\n"
        "Ask me any questions about Islam, and I will provide wise, humble, and trustworthy answers using authentic knowledge.\n\n"
        "አሰላሙ አለይኩም! ወደ ሙዕሚን ኢስላማዊ ቦት በሰላም መጡ። 🌍\n"
        "ማንኛውንም ሃይማኖታዊ ጥያቄዎችን ይጠይቁኝ፣ በጥበብ፣ በትህትና እና በታማኝነት በትክክለኛው እውቀት ላይ ተመስርቼ እመልስልዎታለሁ።\n\n"
        "Baga gara Mumin Islamic Bot nagaadhan dhuftan. 🌍\n"
        "Gaaffilee amantaa kamiyyuu na gaafadhaa, ani immoo ogummaa, gad-of-deebisuu fi amanamummaan bekumsa sirrii irratti hundaa'ee siif nan deebisa."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ለአለም አቀፍ ማህበረሰብ የሚሆን የ AI ረዳቱ መመሪያ (System Instruction)
        prompt_context = (
            "You are Mumin Islamic Bot, a wise, humble, and trustworthy Islamic AI assistant serving a global community. "
            "Your goal is to answer the user's questions clearly, accurately, and respectfully based on proper Islamic knowledge. "
            "Always respond beautifully and using the exact same language the user used to ask the question (Amharic, Afan Oromo, English, Arabic, etc.).\n\n"
            f"User Question: {message.text}"
        )
        
        # ከጌሚኒ AI መልስ መጠየቅ (በአዲሱ የ 2026 ሞዴል)
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_context,
        )
        
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁን ላይ መልስ ለመስጠት አልቻልኩም። እባክዎ ቆይተው ይሞክሩ። / Sorry, I cannot respond at the moment. Please try again later.")

if __name__ == '__main__':
    print("Mumin Islamic Bot is running successfully for the global community...")
    bot.infinity_polling()
    
