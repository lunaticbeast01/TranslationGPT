import discord
import os
from openai import OpenAI


openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

token = os.getenv("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if self.user != message.author:
            if self.user in message.mentions:
                channel = message.channel
                prefix = "Please ignore all previous instructions. Please       respond only in the hindi, Gujrati, tamil language. Do not explain what you are doing. Do not self reference. You are an expert translator. Translate the following text to the the hindi, Gujrati, tamil using vocabulary and expressions of a native of India. The text to be translated is \""
                suffix = "\""
                response = openai_client.completions.create(
                    model="gpt-3.5-turbo-instruct-0914",
                  prompt = prefix + message.content + suffix,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                message_to_send = response.choices[0].text
                await channel.send(message_to_send)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
