from revChatGPT.Official import AsyncChatbot
import json

def get_config() -> dict:
    import os
    # get config.json path
    config_dir = os.path.abspath(__file__ + "/../../")
    config_name = 'config.json'
    config_path = os.path.join(config_dir, config_name)

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config

config = get_config()
openAI_key = config['openAI_key']
openAI_model = config["model"]
chatbot = AsyncChatbot(api_key=openAI_key, engine=openAI_model)

async def handle_response(message) -> str:
    response = await chatbot.ask(message)
    responseMessage = response["choices"][0]["text"]
    print(responseMessage)
    return responseMessage