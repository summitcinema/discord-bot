import discord
from discord.ext import commands

import random, re
from datetime import date

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.NECO_ARC_IMAGES = (
            "https://64.media.tumblr.com/4d8454d42284442ac7da95eb384af7b7/df24abf55e1f0c95-c8/s1280x1920/754c2a133b14f1112518c7077ed417fc9a65f83a.png",


            "https://i.kym-cdn.com/photos/images/newsfeed/002/194/260/b58.jpg",
            "https://i.kym-cdn.com/photos/images/newsfeed/002/412/845/4ca",
            "https://i.kym-cdn.com/photos/images/newsfeed/002/466/027/116",
            "https://i.kym-cdn.com/photos/images/newsfeed/002/473/277/eb6",
            "https://i.kym-cdn.com/photos/images/original/002/165/126/b5a",
            "https://i.kym-cdn.com/photos/images/original/002/183/579/219",
            "https://i.kym-cdn.com/photos/images/original/002/194/251/1bd.jpg",
            "https://i.kym-cdn.com/photos/images/original/002/194/253/530.jpg",
            "https://i.kym-cdn.com/photos/images/original/002/194/255/837.jpg",
            "https://i.kym-cdn.com/photos/images/original/002/213/131/07f",
            "https://i.kym-cdn.com/photos/images/original/002/224/803/ee5.png",
            "https://i.kym-cdn.com/photos/images/original/002/252/180/e8c",
            "https://i.kym-cdn.com/photos/images/original/002/273/434/7b3.gif",
            "https://i.kym-cdn.com/photos/images/original/002/286/546/5e6",
            "https://i.kym-cdn.com/photos/images/original/002/302/069/449.gif",
            "https://i.kym-cdn.com/photos/images/original/002/384/068/bce.jpg",
            "https://i.kym-cdn.com/photos/images/original/002/400/019/66f",
            "https://i.kym-cdn.com/photos/images/original/002/466/028/803",
            "https://i.kym-cdn.com/photos/images/original/002/485/959/078",
            "https://i.kym-cdn.com/photos/images/original/002/345/872/da9.jpg",

            "https://images.goodsmile.info/cgm/images/product/20100621/2889/10464/large/8268e868588add7d4158ad40281f06a6.jpg",

            "https://pbs.twimg.com/media/E-2hgfQXEAk6uE5?format=jpg&name=large",
            "https://pbs.twimg.com/media/E-Y2ep2XECUld-y.jpg",
            "https://pbs.twimg.com/media/E9lAWJsXsAYq6Aj?format=jpg&name=4096x4096",

            "https://c.tenor.com/-WPg9ST7N_oAAAAM/neco-arc-neco.gif",
            "https://c.tenor.com/oqv1lX_NwxcAAAAd/neco-arc-tsukihime.gif",

            "https://tenor.com/view/neco-arc-gif-22199714",
            "https://tenor.com/view/neco-arc-gif-24678049",
            "https://tenor.com/view/neco-arc-gif-26175742",
            "https://tenor.com/view/neco-arc-neco-melty-melty-blood-carnival-phantasm-gif-23290890",
            "https://tenor.com/view/neco-arc-neco-meme-memes-helicopter-gif-25843522",
            "https://tenor.com/view/neco-arc-neco-rumba-dance-rumba-gif-23889144",
            "https://tenor.com/view/neko-neco-arc-neco-arc-neko-arc-gif-22451604",
            "https://tenor.com/view/typemoon-neco-arc-melty-blood-kamehameha-kamehameha-neco-arc-gif-26194611",
        )

        self.RANDOM_WEED_MESSAGES = (
            "bro weed", "420 bro", "bro blaze it", "blaze it bro", "blaze it 420 bro", "bro 420 blaze it", "WEEEEEEEEEEEEEEED",
            "WEEED I NEED WEED", "muthafuckin 4 2 0", "chuffin a fat dart rn"
        )

        self.OWO_KAOMOJI = (
            "owo", "uwu", "OwO", "UwU", "Ow<", ">wO", ">w<", ">w>", "<w<", "TwT", "(* ^ ω ^)", "(´ ∀ ` *)",
            "☆*:.｡.o(≧▽≦)o.｡.:*☆", "。.:☆*:･'(*⌒―⌒*)))", "(￣ω￣)", "(´｡• ω •｡`)", "(o^▽^o)", "(´• ω •`)",
            "o(≧▽≦)o", "nya", "nyaa~", "nya~", "nyan", "(￢‿￢ )", "(─‿‿─)♡", "(´ ε ` )♡", "( ´ ∀ `)ノ～ ♡",
            "(｡・//ε//・｡)", "(*・ω・)ﾉ", "(つ≧▽≦)つ", "(＾• ω •＾)", "ヘ(￣ω￣ヘ)", "〜(￣▽￣〜)", "( ͡• ͜ʖ ͡• )", "( ´-ω･)︻┻┳══━一",
            "*pounces on you*", "!", "!!", "!!!", "!!!!"
        )

        self.FUCK_YOU_MESSAGES = (
            "shut the fuck up you stupid whore",
            "suck my dick and balls",
            "how bout you get in the kitchen and make me a sandwich",
            "FUCK YOU!!!!",
            "WOAH LOOK AT THIS ✊ WHAT'S IT GONNA DO?? :middle_finger: OH :middle_finger: SHIT :middle_finger:!!!!",
            "EAT A DICK",
            "Fuck you. You useless piece of shit. You absolute waste of space and air. You uneducated, ignorant, idiotic dumb swine, you’re an absolute embarrassment to humanity and all life as a whole. The magnitude of your failure just now is so indescribably massive that one hundred years into the future your name will be used as moniker of evil for heretics. Even if all of humanity put together their collective intelligence there is no conceivable way they could have thought up a way to fuck up on the unimaginable scale you just did.",
            "FUCK :middle_finger: YOU :middle_finger:"
        )

        self.KLEINER_QUOTES = (
            # https://combineoverwiki.net/wiki/Isaac_Kleiner/Quotes/Half-Life_2
            # City 17 Trainstation
            "Alyx is around here somewhere. She would have a better idea how to get him here.",
            "Well, Barney, what do you intend?",
            "Great Scott! Gordon Freeman! I expected more warning.",
            "Very well. And, eh, Gordon? Good to see you!",
            "Yes, Barney, what is it? I'm in the middle of a critical test.",

            # Lab 1
            "Ah!",
            "What? Oh dear, you're right, I almost forgot.",
            "Barney, I'll give you the honor.",
            "All right, Barney. Your turn.",
            "Barney? If you'd be so kind?",
            "Blast that little...where did she get to? Lamarr? Come out of there!",
            "Bon voyage, and best of luck in your future endeavors.",
            "We can't continue until you're in the teleport chamber, Gordon.",
            "You can't just wade into the field, it will peel you apart!",
            "Good idea. There's a charger on the wall. I've modified your suit to draw power from Combine energy outlets, which are plentiful wherever they patrol.",
            "Oh, fie! It'll be another week before I can coax her out of there.",
            "Well I can't take all the credit, Doctor Freeman proved an able assistant.",
            "Dear me.",
            "Certainly not! Never fear, Gordon, she's de-beaked and completely harmless.",
            "Gordon, the longer you delay, the greater the danger to us all.",
            "Well, did it work?",
            "Once you're safely ensconced in the transmitter, we can begin.",
            "Excellent.",
            "Right you are! Speak to you again in a few moments.",
            "Oh, fiddlesticks. What now?",
            "Very good. Final sequence. Commencing...now.",
            "Final sequence.",
            "Well, Gordon, I see your HEV suit still fits you like a glove At least the glove parts do.",
            "The worst she might do is attempt to couple with your head. Fruitlessly!",
            "Gordon, as soon as you're in position, we'll send you to Eli's.",
            "Gordon! You must get out of here! Run!",
            "Gordon, go right ahead.",
            "Throw your switch, Gordon.",
            "Lamarr? Hedy! No!",
            "Oh, hello, Alyx! Well, almost all right. Lamarr has gotten out of her crate again. If I didn't know better, I'd suspect Barney of trapping and...",
            "Here, my pet. Hop up.",
            "No, not up there!",
            "What do you mean he's not there?",
            "Yes, yes, Eli, bit of a holdup on this end. You'll never guess who found his way into our lab this morning.",
            "Initializing in three... two... one...",
            "I'm encountering unexpected interference!",
            "Is Lamarr with him?",
            "Lamarr! There you are!",
            "Let's see. The massless field-flux should self-limit and I've clamped the manifold parameters to CY base and LG orbifold, Hilbert inclusive.",
            "I've made a few modifications, but I'll just acquaint you with the essentials. Now, let's see... The Mark V Hazardous Environment Suit has been redesigned for comfort and utility—",
            "Conditions could hardly be more ideal!",
            "My Goodness! Gordon Freeman! It really is you, isn't it?",
            "No, no! Careful, Lamarr! Those are quite fragile!",
            "Nonsense. Your talents surpass your loveliness.",
            "Now, now, there's nothing to be nervous about. We've made major strides since then. Major strides.",
            "Oh, dear!",
            "I must say, Gordon, you come at a very opportune time. Alyx has just installed the final piece for our resurrected teleport.",
            "Indeed it is. And it's our intention to send him packing straightaway, in the company of your lovely daughter.",
            "Dear me, you're right. Gordon, would you mind plugging us in?",
            "Yes, indeed. We're ready to project you, Gordon.",
            "That's right, Barney. This is a red letter day. We'll inaugurate the new teleport with a double transmission!",
            "Oh, thank goodness. My relief is almost palpable.",
            "Well, Gordon, go ahead. Slip into your suit now.",
            "Gordon, if you please? I'm eager to see if your old suit still fits.",
            "Then, where is he?",
            "Gordon, why don't you position yourself near the panel over there and wait for my word?",
            "We owe a great deal to Dr. Freeman, even if trouble does tend to follow in his wake.",
            "What is it?",
            "I wish I knew. I'm encountering unexpected interference!",
            "It's your turn, Gordon.",

            # Lab 2
            "Now, now, she's around here someplace.",
            "Well, that is most troubling",
            "According to the vortigaunts, he is a prisoner at the Citadel.",
            "Indeed it did... and the repercussions were felt far and wide, but... That was over a week ago!",
            "A great deal, my dear.",
            "The blow you struck at Nova Prospekt was taken as a signal to begin the uprising.",
            "Just a minute.",
            "I can't leave without Lamarr. Now where did she get to?",
            "Come out, Lamarr!",
            "Barney has been leading a push with that very aim in mind.",
            "And another of your friends arrived several days ago.",
            "My dear, I had given up hope of ever seeing you again.",
            "Great Scott!",
            "Alyx? Gordon?",
            "My god... how did you get here? And when?",
            "Lamarr? Lamarr!",
            "Yes, Gordon, please do go on.",
            "Lamarr is extremely wary of your crowbar.",
            "Yes, Barney, and I'm no longer alone.",
            "Alyx and Gordon have just arrived.",
            "So there, you see?",
            "It's not all hopeless.",
            "There's only one Hedy.",
            "Fascinating.",
            "We seem to have developed a very slow teleport.",
            "This suggests an entirely new line of investigation.",

            "WHOAO!",
            "RUN!"
        )

        self.HAPPY_BIRTHDAY_MESSAGES = (
            "HAPPY BIRTHDAY {user} FROM YOUR FRIEND DR. KLEINER",
            "HAPPY BIRTHDAY {user}!!!!!",
            "HAVE A HAPPY HAPPY BIRTHDAY {user}!!!!!!!!!!",
            "happy birthday {user} f.from me dr.kleiner!!!",
        )
        
        self.HAPPY_BIRTHDAY_EMOTES = (
            ":birthday:",
            ":balloon:",
            ":confetti_ball:",
            ":partying_face:",
            ":tada:"
        )

        self.HAPPY_BIRTHDAY_FILES = (
            "images/jerma_birthday.jpg",
            "videos/berdthday_boy.mp4",
            "videos/pickle_chin_birthday.mp4",
            "videos/rick_may_birthday.mp4",
            "videos/summit_birthday.mp4"
        )

    @classmethod
    async def get_date_int(self):
        date_today = date.today()
        date_str = str(date_today.year + date_today.month + date_today.day)

        return int(date_str)

    @classmethod
    async def get_gay_percent(self, user: discord.Member):
        if discord.utils.get(user.roles, name="gay nigga"):
            return 99999.999

        date_num = await self.get_date_int()
        user_rng = random.Random(user.id + date_num)

        if user_rng.randint(1, 30) == 1:
            return 1000.0
        else:
            return user_rng.randint(0, 1000) / 10

    @classmethod
    async def get_match_percent(self, user1, user2):
        date_num = await self.get_date_int()
        user_rng = random.Random(user1.id + user2.id + date_num)

        if user_rng.randint(1, 30) == 1:
            return 1000.0
        else:
            return user_rng.randint(0, 1000) / 10

    @classmethod
    async def get_match_emoji(self, match_percent):
        if match_percent >= 100:
            return ":heart_on_fire:"
        elif match_percent >= 90:
            return ":heartpulse:"
        elif match_percent >= 70:
            return ":heart:"
        elif match_percent >= 30:
            return ":broken_heart:"
        else:
            return ":black_heart:"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Prevent the bot from listening to other bots
        if message.author.bot: return

        msg_lower = message.content.lower()
        user_id_mention = "<@" + str(self.client.user.id) + ">"

        if "treat yourself" in msg_lower:
            await message.channel.send("<:ltglys:911739432774828072>")

        if "weed bro" in msg_lower or "dude weed" in msg_lower:
            await message.channel.send(random.choice(self.RANDOM_WEED_MESSAGES))

        if "you should step into your hev suit... now!" in msg_lower:
            await message.channel.send("https://tenor.com/view/ltg-gmod-low-tier-god-kys-you-should-gif-23638964")

        if msg_lower == "pretty boy":
            await message.channel.send("<:necoarc:910646131548119111>")

        if msg_lower.startswith(user_id_mention):
            await message.channel.send(random.choice(self.KLEINER_QUOTES))
        elif user_id_mention in msg_lower:
            if "fuck you" in msg_lower:
                newmsg = random.choice(self.FUCK_YOU_MESSAGES)
                await message.channel.send(newmsg)

    @commands.hybrid_command(
        description="GREAT SCOTT!"
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def greatscott(self, ctx):
        await ctx.send("GREAT SCOTT!")

    @commands.hybrid_command(
        description="the funny cat"
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def necoarc(self, ctx):
        await ctx.send(random.choice(self.NECO_ARC_IMAGES))

    @commands.hybrid_command(
        description="Turns the provided text into degeneracy.",
        usage="[text]",
        aliases=["uwu"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def owo(self, ctx, *, text:str = ""):
        # Convert R and L to W
        tstable = text.maketrans("rlRL", "wwWW", "")
        owotext = text.translate(tstable)
        # Replace punctuation
        owotext = ''.join(["!"*random.randint(1, 5) if ch in {',', '.'} and random.choice([True, False]) else ch for ch in owotext])
        # Add a random emoticon to the end
        owotext += " " + random.choice(self.OWO_KAOMOJI)

        # N<vowel> becomes ny<vowel> - \g<1> refers to regex group 1 in the match
        owotext = re.sub(r"[Nn]([aeiouAEIOU])", r"ny\g<1>", owotext)

        await ctx.send(owotext)

    @commands.hybrid_command(
        description="Shows how well two people romantically pair up!",
        usage="<user1> [user2]",
        aliases=["ship", "shipmeter", "lovemeter", "matchmeter"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def match(self, ctx, user1: discord.Member, user2: discord.Member = None):
        user2 = user2 if user2 else ctx.author

        match_percent = await self.get_match_percent(user1, user2)
        emoji = await self.get_match_emoji(match_percent)

        after_msg = "\nLove yourself! I mean that one hundred percent, with a thousand percent!" if user1.id == user2.id and match_percent >= 90 else ""

        await ctx.send(f"{emoji} {user1.display_name} + {user2.display_name} {emoji}\nMatch percent: **{match_percent}%**{after_msg}")

    @commands.hybrid_command(
        description="Finds the perfect match for the provided user.",
        usage="[user]",
        aliases=["onetruelove", "perfectship", "bestmatch", "bestship"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def perfectmatch(self, ctx, user: discord.Member = None):
        user = user if user else ctx.author

        greatest_match = ("0", 0)

        for otherUser in ctx.guild.members:
            match_percent = await self.get_match_percent(user, otherUser)

            if match_percent > greatest_match[1]:
                greatest_match = (otherUser, match_percent)

        await ctx.send(f":heart_on_fire: {user.display_name}'s greatest match: **{greatest_match[0].display_name}** :heart_on_fire:\nMatch percent: **{greatest_match[1]}%**")

    @commands.hybrid_command(
        description="Finds the worst match for the provided user.",
        usage="[user]",
        aliases=["worstship"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def worstmatch(self, ctx, user: discord.Member = None):
        user = user if user else ctx.author

        worst_match = ("0", 100)

        for otherUser in ctx.guild.members:
            match_percent = await self.get_match_percent(user, otherUser)

            if match_percent < worst_match[1]:
                worst_match = (otherUser, match_percent)

        await ctx.send(f":black_heart: {user.display_name}'s worst match: **{worst_match[0].display_name}** :black_heart:\nMatch percent: **{worst_match[1]}%**")
    
    @commands.hybrid_command(
        description="Shows how gay a user is.",
        usage="[user]",
        aliases=["gayometer"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def gaymeter(self, ctx, *, user: discord.Member = None):
        chosen_member = user if user else ctx.author

        gay_percent = await self.get_gay_percent(chosen_member)

        await ctx.send(f"**{chosen_member.display_name}** is {gay_percent}% gay. :rainbow_flag:")

    @commands.hybrid_command(
        description="Shows who the gayest and least gay users are.",
        aliases=["leastgay"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def mostgay(self, ctx):
        least_gay = ("0", 100)
        most_gay = ("0", 0)

        for user in ctx.guild.members:
            gay_percent = await self.get_gay_percent(user)

            if gay_percent > most_gay[1]:
                most_gay = (user, gay_percent)
            if gay_percent < least_gay[1]:
                least_gay = (user, gay_percent)

        line1 = f"**{most_gay[0].display_name}** is **{most_gay[1]}%** gay - the gayest user in the server."
        line2 = f"**{least_gay[0].display_name}** is **{least_gay[1]}%** gay - the least gay user in the server."

        await ctx.send(line1 + "\n" + line2)

    @commands.hybrid_command(
        description="Shows a person\'s dick size.",
        usage="[user]",
        aliases=["mydicksize", "penissize", "weinersize"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def dicksize(self, ctx, *, user: discord.Member = None):
        chosen_member = user if user else ctx.author

        # RNG seed based on user id (so that the same result is always given to the same discord ID)
        date_num = await self.get_date_int()
        user_rng = random.Random(chosen_member.id - date_num)
        dick_length = user_rng.randint(0, 16) - 3

        # If there is a dick length to display
        if dick_length >= 0:
            await ctx.send(f"**{chosen_member.display_name}**\'s dick size: 8{'='*dick_length}D")
        else:
            random_text = random.choice([
                "it's not even worth displaying.",
                "it's basically a vagina.",
                "I can't even show how small it is through text."
            ])
            await ctx.send(f"**{chosen_member.display_name}**\'s dick is so small, {random_text}")

    @commands.hybrid_command(
        description="Shows a person's IQ.",
        usage="[user]",
        aliases=["intelligence", "iqtest", "showiq"]
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def iq(self, ctx, *, user: discord.Member = None):
        chosen_member = user if user else ctx.author

        # RNG seed based on user id (so that the same result is always given to the same discord ID)
        date_num = await self.get_date_int()
        user_rng = random.Random(chosen_member.id - date_num)

        int_values = user_rng.choice([(1, 50), (1, 50), (1, 50), (1, 50), (50, 140), (50, 140), (140, 300)])
        iq_value = user_rng.randint(*int_values)

        after_msg = ""
        if iq_value <= 25:
            after_msg = " <:steamdeadpan:946469853009702973>"
        elif iq_value >= 150:
            after_msg = " <:nerd:946466565342236682>"

        await ctx.send(f"**{chosen_member.display_name}**\'s IQ: **{iq_value}**{after_msg}")

    @commands.hybrid_command(
        description="Wish a happy birthday to the specified user, which provides a random special image/video for them.",
        usage="[user]",
        aliases=["birthday"]
    )
    async def happybirthday(self, ctx, *, user: discord.Member = None):
        chosen_member = user if user else ctx.author

        msg_to_send = random.choice(self.HAPPY_BIRTHDAY_MESSAGES)
        msg_to_send = msg_to_send.format(user=chosen_member.mention)

        emotes_to_spam_tb = [random.choice(self.HAPPY_BIRTHDAY_EMOTES) for _ in range(random.randint(3, 15))]
        emotes_to_spam = " ".join(emotes_to_spam_tb)

        msg_to_send += " " + emotes_to_spam

        file_to_send = random.choice(self.HAPPY_BIRTHDAY_FILES)

        await ctx.send(content=msg_to_send, file=discord.File(file_to_send))


async def setup(bot):
    await bot.add_cog(Fun(bot))
