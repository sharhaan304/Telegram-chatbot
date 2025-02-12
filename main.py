from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()
model_name = "gpt-4o-mini"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    """
    A function to clear the chat history.
    """
    reference.response = ""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    This handler to clear the chat history.
    """
    clear_past()
    await message.answer("Chat history cleared!")
    

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messaged with '/start' or '/help' command
    """
    await message.answer("Hi! I am EchoBot! how can I can assist you!")
    
    
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler to display the help menu.
    """
    help_command = """
    Hi! thatkuri, what do you need help with? Please follow these commands -
    /start - To start the conversation
    /clear - To clear the chat history
    /help - To display the help menu
    ithe sari olunga padi thatkuri soker.:)
    """
    await message.answer("I am an AI chatbot, I can help you with your queries, just ask me anything!")
    
    
@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user"s input and generate a response using the Chatgpt API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = model_name,
        messages = [
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text},
        ]
    )
    reference.response = response['choices'][0]['message']["content"]
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)
    
    
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
     