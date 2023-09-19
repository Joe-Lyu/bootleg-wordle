# bot.py
import discord
from utils import cp_words,score_dict
from wordle_core import MAX_TRIES
import random
import asyncio
import pickle
sd = score_dict()
words = sd.sorted_words

TOKEN = pickle.load(open('token.pkl','rb')) #not gonna show my token to ya :)

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
                if gc == '!quit':
                    break
                await message.reply("Guess number {}:\n".format(guess_num)+cp_words(gc,word))
                guess_num += 1
                try:
                    guess = await self.wait_for('message', check=is_correct, timeout=120)
                    gc = guess.content.lower()
                except asyncio.TimeoutError:
                    return await message.channel.send("Timed out. The answer was **{}**".format(word)) 
                
            if word == gc:
                await message.reply("🟩"*5+"\nYou guessed it in {} tries".format(guess_num))
            else:
                await message.reply("You failed! The answer is {}".format(word))

        if message.content.startswith('$solve-wordle'):
            await message.reply('Solving an external Wordle game.')

            def is_valid_hint(m):
                hint = m.content.upper()
                cond = len(hint)==5 and set(hint).issubset(set(('Y','G','?')))
                return m.author == message.author and (cond or hint=='!quit')
            def is_valid_guess(m):
                guess = m.content.lower()
                cond = guess in words
                return m.author == message.author and (cond or guess=='!quit')
                
            filtered_sorted_words = words
            await message.reply("Current best 5 guesses are:\n"+"\n".join(["**{}**".format(word) for word in words[:5]]))
            await message.reply("What is your choice?")
            try:
                guessm = await self.wait_for('message',check=is_valid_guess, timeout = 120)
                guess = guessm.content
            except asyncio.TimeoutError:
                return await message.channel.send("Timed out.")
            
            print(guess)

            await message.reply("What are the colors from Wordle?\nReply \"G\" for green, \"Y\" for yellow, and \"?\" for grey\ne.g. ?YY?G")
            try:
                hintm = await self.wait_for('message',check=is_valid_hint,timeout=120)
                hint = hintm.content
            except asyncio.TimeoutError:
                return await message.channel.send("Timed out.")
            
            print(hint)

            while hint != 'G'*5:
                if hint == '!quit':
                    break
                new_filter = []
                for sw in filtered_sorted_words:
                    conds = True
                    for i in range(5):
                        if hint[i] == 'G':
                            conds = conds and sw[i] == guess[i]
                        elif hint[i] == 'Y':
                            conds = conds and guess[i] in sw and sw[i] != guess[i]
                        elif guess[i] not in guess[:i]:
                            conds = conds and guess[i] not in sw
                    if conds:
                        new_filter.append(sw)
                filtered_sorted_words = new_filter
                if len(filtered_sorted_words) == 1:
                    await message.reply("Only possible answer is: \t"+filtered_sorted_words[0])
                    break
                await message.reply("Current best 5 guesses are:\n"+"\n".join(["**{}**".format(word) for word in filtered_sorted_words[:5]]))
                await message.reply("What is your choice?")
                try:
                    print('listening for guess')
                    guessm = await self.wait_for('message',check=is_valid_guess, timeout = 120)
                    guess = guessm.content
                except asyncio.TimeoutError:
                    return await message.channel.send("Timed out.")
                    break
                
                await message.reply("What are the colors from Wordle?")
                if guess == '!quit':
                    break
                try:
                    hintm = await self.wait_for('message',check=is_valid_hint,timeout=120)
                    hint = hintm.content
                except asyncio.TimeoutError:
                    return await message.channel.send("Timed out.")
                    break
            if hint == 'G'*5:
                await message.reply("Congrats, you solved it! Well, I solved it, you kinda just put in all the letters and stuff.")




intents = discord.Intents.default()
intents.message_content = True

client = WordleBot(intents=intents)
client.run(TOKEN)