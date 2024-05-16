from translations.env_config import OPENAI_API_KEY
from translations.gpt.chat_gpt import ChatGPTService


chat_gpt_service = ChatGPTService(OPENAI_API_KEY)
