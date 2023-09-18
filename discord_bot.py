# bot.py
import os

import discord
from utils import cp_words,score_dict
from wordle_core import MAX_TRIES
import random
import asyncio
sd = score_dict()
words = sd.sorted_words
TOKEN = 'MTE1MzI0NTc1NDIwNzUxODgyMA.GkzgT6.t5w0Rn_kod20HQ8x4S__ES4DGg-HqNNzRoAWiA'




class WordleBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$play-wordle'):
            await message.reply('Started a new game of Wordle.')

            def is_correct(m):
                return m.author == message.author and len(m.content)==5 and (m.content.lower() in words or m.content == '!quit')

            word = random.choice(words)
            print(word)
            guess_num = 1
            try:
                guess = await self.wait_for('message', check=is_correct, timeout=120)
                gc = guess.content.lower()
            except asyncio.TimeoutError:
                return await message.channel.send("Timed out. The answer was **{}**".format(word))

            while gc != word and guess_num <= MAX_TRIES:
                print("guessing")
                await message.reply("Guess number {}:\n".format(guess_num)+cp_words(gc,word))
                guess_num += 1
                try:
                    guess = await self.wait_for('message', check=is_correct, timeout=120)
                    gc = guess.content.lower()
                except asyncio.TimeoutError:
                    return await message.channel.send("Timed out. The answer was **{}**".format(word)) 
                if gc == '!quit':
                    break
            if word == gc:
                await message.channel.send("🟩"*5+"\nYou guessed it in {} tries".format(guess_num))
            else:
                await message.channel.send("You failed! The answer is {}".format(word))


intents = discord.Intents.default()
intents.message_content = True

client = WordleBot(intents=intents)
client.run(TOKEN)