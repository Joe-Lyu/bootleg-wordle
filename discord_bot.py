# bot.py
import discord
from utils import cp_words,score_dict
from wordle_core import rank_words,get_remaining
import random
import asyncio
import pickle
import sys
sd = score_dict()
words = sd.sorted_words
all_words = sd.all_words
TOKEN = pickle.load(open('token.pkl','rb')) #not gonna show my token to ya :)

class WordleBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
    
    

    async def on_message(self, message):
        joe = 803676742639550544
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        mention = "@"+str(self.user.id)
        mention_replies = ["I will now hack your servers.",
                            "WHat",
                            "Please go to Joe for complaints.",
                            "I am not responsible for your limited vocabulary of five-letter words.",
                            "The best starter word for Wordle is \"esses\". Wait, or is that the worst?",
                            "If you're from the New York Times, please don\'t sue me. :pleading_face:",
                            "What's up?",
                            "Fun fact, the original creator of Wordle, Josh Wardle, has also created the original Place, on Reddit!",
                            "https://tweakimp.github.io/unfairwordle/"
                            "My dictionary currently contains around 12972 words, 2315 of which can be the answers to a game. The rest are rather hard to guess. Unless...",
                            "There are two words that were added to my dictionary manually, by request. Guess which two they are. No, I will not set up a game just for this.",
                            "*Totally some random statement chosen from a predetermined list*"]
        if message.author.id == joe and message.content == '#em-terminate':
            await message.reply('Emergency termination.')
            sys.exit()
        
        if mention in message.content:
            await message.reply(random.choice(mention_replies))
        
        if 'wordle' in message.content.lower() and random.random()<0.5 and not message.content.startswith("$"):
            await message.reply("Wordle?")

        if message.content.startswith('$play-wordle'):
            await message.reply('Started a new game of Wordle.')
            await message.reply('Choose a difficulty: easy, medium, hard, or random')
            def is_valid_difficulty(m):
                d = m.content
                conds = d.lower() in ['easy','medium','hard','random']
                return m.author == message.author and conds
            try:
                difficultym = await self.wait_for('message',check=is_valid_difficulty,timeout=600)
                difficulty = difficultym.content.lower()
            except asyncio.TimeoutError:
                return await message.reply("Timed out.")
            
            from wordle_core import MAX_TRIES
            MAX_TRIES = MAX_TRIES
            
            if difficulty == 'easy':
                word = sd.get_difficulty('easy')
            elif difficulty == 'medium':
                word = sd.get_difficulty('medium')
            elif difficulty == 'hard':
                word = sd.get_difficulty('hard')
                MAX_TRIES = 10
                await message.reply("Maximum number of tries is 10 for this game. Good luck.")
            else:
                word = sd.get_difficulty()
            
            await message.reply("Difficulty is set to: **{}**".format(difficulty))

            def is_correct(m):
                return m.author == message.author and len(m.content)==5

            print(word)
            guess_num = 1
            try:
                guess = await self.wait_for('message', check=is_correct, timeout=600)
                gc = guess.content.lower()
            except asyncio.TimeoutError:
                return await message.reply("Timed out. The answer was **{}**".format(word))
            
            
            guess_list = []

            while gc != word and guess_num <= MAX_TRIES:
                
                guess_list.append(guess.content.lower())
                print("guessing: {}".format(gc))
                if gc == '!quit':
                    return

                if gc not in all_words and gc != '!quit':
                    await message.reply("That is not in my dictionary.")
                    valid_word = False
                else:
                    valid_word = True

                if valid_word:
                    await message.reply("Guess number {}:\n".format(guess_num)+cp_words(gc,word))
                    guess_num += 1
                try:
                    guess = await self.wait_for('message', check=is_correct, timeout=600)
                    gc = guess.content.lower()
                except asyncio.TimeoutError:
                    return await message.reply("Timed out. The answer was **{}**".format(word)) 
                
            if word == gc:
                await message.reply("🟩"*5+"\nYou guessed it in {} tries".format(guess_num))
            elif gc != '!quit':
                #easter egg :)
                print(guess_list)
                if set(guess_list)==set({'twink'}) and difficulty == 'hard':
                    await message.reply("Look, you win, okay? The answer is twink, whatever")
                else:
                    await message.reply("You failed! The answer is **{}**".format(word))
            else:
                await message.reply("Quit the current Wordle game. The answer was **{}**".format(word))





        if message.content.startswith('$solve-wordle'):
            await message.reply('Solving an external Wordle game.')

            dev = True if 'dev' in message.content else False

            if dev and message.author==joe:
                await message.reply("Hi, Joe. Looks like you entered dev mode.")
                await message.reply("Choose your ranking algorithm")
                def is_valid_alg(m):
                    return m.content in ['score','alt_score'] and m.author==message.author
                try:
                    algm = await self.wait_for('message',check=is_valid_alg, timeout = 600)
                    alg = algm.content.lower()
                except asyncio.TimeoutError:
                    return await message.reply("Timed out.")



            def is_valid_hint(m):
                hint = m.content.upper()
                cond = len(hint)==5 and set(hint).issubset(set(('Y','G','?')))
                return m.author == message.author and (cond or hint=='!QUIT')
            def is_valid_guess(m):
                guess = m.content.lower()
                cond = guess in all_words
                return m.author == message.author and (cond or guess=='!quit')
                
            filtered_sorted_words = all_words
            await message.reply("Current best 5 guesses are:\n"+"\n".join(["**{}**".format(word) for word in all_words[:5]]))
            await message.reply("What is your choice?")
            try:
                guessm = await self.wait_for('message',check=is_valid_guess, timeout = 600)
                guess = guessm.content.lower()
            except asyncio.TimeoutError:
                return await message.reply("Timed out.")
            
            print(guess)

            await message.reply("What are the colors from Wordle?\nReply \"G\" for green, \"Y\" for yellow, and \"?\" for grey\ne.g. ?YY?G")
            try:
                hintm = await self.wait_for('message',check=is_valid_hint,timeout=600)
                hint = hintm.content.upper()
            except asyncio.TimeoutError:
                return await message.reply("Timed out.")
            
            print(hint)

            while hint != 'G'*5:
                if hint == '!QUIT':
                    await message.reply("Quit current session.")
                    return
                
                filtered_sorted_words = rank_words(filtered_sorted_words,
                                                   hint,
                                                   guess,
                                                   alg=alg,
                                                   symbolset=False)

                if len(filtered_sorted_words) == 1:
                    await message.reply("Only possible answer is: \t"+filtered_sorted_words[0])
                    return
                await message.reply("Current best 5 guesses are:\n"+"\n".join(["**{}**".format(word) for word in filtered_sorted_words[:5]]))
                await message.reply("What is your choice?")
                try:
                    print('listening for guess')
                    guessm = await self.wait_for('message',check=is_valid_guess, timeout = 600)
                    guess = guessm.content
                except asyncio.TimeoutError:
                    return await message.reply("Timed out.")

                if guess == '!quit':
                    return
                await message.reply("What are the colors from Wordle?")
                
                try:
                    hintm = await self.wait_for('message',check=is_valid_hint,timeout=600)
                    hint = hintm.content
                except asyncio.TimeoutError:
                    return await message.reply("Timed out.")
            if hint == 'G'*5:
                await message.reply("Congrats, you solved it! Well, I solved it, you kinda just put in all the letters and stuff.")



        if message.content.startswith('$challenge-wordle'):
            await message.reply("So you challenged me to a Wordle game!\nTell me the answer and I will show you how I would guess it, using Joe\'s algorithm.")
            
            dev = True if 'dev' in message.content else False

            if dev and message.author==joe:
                await message.reply("Hi, Joe. Looks like you entered dev mode.")
                await message.reply("Choose your ranking algorithm")
                def is_valid_alg(m):
                    return m.content in ['score','alt_score'] and m.author==message.author
                try:
                    algm = await self.wait_for('message',check=is_valid_alg, timeout = 600)
                    alg = algm.content.lower()
                except asyncio.TimeoutError:
                    return await message.reply("Timed out.")
                
            def is_correct(m):
                return m.author == message.author and len(m.content)==5
            try:
                answerm = await self.wait_for('message', check=is_correct, timeout=600)
                answer = answerm.content.lower()
            except asyncio.TimeoutError:
                return await message.reply("Timed out.")
            
            guess = all_words[0]

            filtered_sorted_words = all_words
            while guess != answer:
                await message.reply(guess+'\n'+cp_words(guess,answer))
                #await message.reply('Calculating next best move...')
                hints = cp_words(guess,answer)
                filtered_sorted_words = rank_words(filtered_sorted_words,
                                                hints,
                                                guess,
                                                alg=alg)
                
                guess = filtered_sorted_words[0]
            
            await message.reply(guess+'\n'+cp_words(guess,answer))
            await message.reply("I got it!")



intents = discord.Intents.default()
intents.message_content = True

client = WordleBot(intents=intents)
client.run(TOKEN)