import telebot
import google.generativeai as genai

bot = telebot.TeleBot("7088679882:AAFxuU7bUOgEvW6-iRvw15YEUQimVNqVqSk")

genai.configure(api_key="AIzaSyB_nWdzwRc4dRS239KfQcjVZ0kCtGViZhc")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Привет"]
  },
  {
    "role": "model",
    "parts": ["Привет! Я рад тебя видеть. Как дела?"]
  },
  {
    "role": "user",
    "parts": ["Кто ты?"]
  },
  {
    "role": "model",
    "parts": ["Я Gemini Telegram Bot "]
  },
])


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global convo
    if convo is None:
        convo = model.start_chat(history=[
            {"role": "user", "parts": [message.text]}
        ])
    else:
        convo.send_message(message.text)

    
    if convo.last is not None:
        response = convo.last.text
        bot.reply_to(message, response)

bot.infinity_polling()
