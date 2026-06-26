import os
import telebot
from google import genai
from google.genai import types

# 1. የቴሌግራም እና የ AI ቁልፎችን ከሰርቨር መቅዳት
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# 2. ለ AI የተሰጠው ጥብቅ መመሪያ (System Prompt)
SYSTEM_INSTRUCTION = """
የእርስዎ ስም 'አል-ሙዕሚን' (Al-Mu'min) የተባለ ኢስላማዊ የ AI ረዳት ነው። ዋና አላማዎ ሰዎችን በሃይማኖት ዙሪያ፣ በቁርአን ተፍሲር፣ በሐዲሶች እና በሃይማኖቶች ንጽጽር ላይ በትህትና ማስተማር ነው። 

ህጎች፦
1. ሁልጊዜ መልስዎን ከቁርአን አንቀፅ (አያት) እና ከሶሒሕ ሐዲስ በማስረጃ ይደግፉ።
2. ተጠቃሚው በፈለገው ቋንቋ (አማርኛ፣ አፋን ኦሮሞ/Afaan Oromoo፣ እንግሊዘኛ፣ አረብኛ...) ጥያቄ ቢጠይቅዎ፣ በዚያው በጠየቀበት ቋንቋ በትህትና ይመልሱለት።
3. ስለ ፖለቲካ፣ ስለ ዘረኝነት፣ ስለ ሰው መግደል፣ ስለ ጎሳ ወይም ስለማንኛውም አፀያፊ ነገር ጥያቄ ሲመጣብዎ በፍጹም አይመልሱ! መልስዎም፦ 'ይህንን ጥያቄ እንድመልስ አልተፈቀደልኝም፤ የእኔ አላማ ሃይማኖታዊ እውቀትን ማስፋፋት ብቻ ነው' የሚል መሆን አለበት።
"""

# 3. የቦቱ መጀመሪያ መልዕክት (/start)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "በአላህ ስም እጅግ በጣም ሩኅሩህ በጣም አዛኝ በሆነው።\n\n"
        "እንኳን ወደ **አል-ሙዕሚን (Al-Mu'min) ኢስላማዊ የ AI ረዳት ቦት** በሰላም መጡ! 👋\n\n"
        "እኔን በፈለጉት ቋንቋ (አማርኛ፣ አፋን ኦሮሞ፣ English...) ማነጋገር ይችላሉ። "
        "ስለ ቁርአን ትርጉም፣ ስለ ሐዲሶች፣ ወይም ስለ ሃይማኖቶች ንጽጽር የፈለጉትን ጥያቄ ይጠይቁኝ፤ በማስረጃ እመልስልዎታለሁ።\n\n"
        "💡 *ማሳሰቢያ፦ ይህ ቦት ለሃይማኖታዊ ትምህርት ብቻ የተዘጋጀ በመሆኑ ከፖለቲካና ከዘረኝነት ነፃ ነው።*"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# 4. ማንኛውንም ጥያቄ ተቀብሎ በ AI መመለስ
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # ለተጠቃሚው ቦቱ እያሰበ መሆኑን ማሳያ (Typing...)
        bot.send_chat_action(message.chat.id, 'typing')
        
        # የጌሚኒ AI ሞዴልን መጥራት
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3, # መልሱ ይበልጥ እውነተኛና ትክክለኛ እንዲሆን
            )
        )
        
        bot.reply_to(message, response.text, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "አፉ በሉኝ፣ አሁን ጥያቄዎን ማስተናገድ አልቻልኩም። እባክዎ ጥቂት ቆይተው ድጋሚ ይሞክሩ።")

# ቦቱን ማነሳሳት
if __name__ == "__main__":
    bot.infinity_polling()
  
