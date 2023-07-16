from email.mime import base
import discord
from discord.ext import commands

import random, json, io, time, re, aiohttp, math
from os import listdir
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime, date

# Used for shitpost generator
TEMPLATES_METADATA = None
# Read the templates metadata
with open("images/shitpost/templates_meta.json") as f:
    TEMPLATES_METADATA = json.loads(f.read())

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client

        #self.connector = aiohttp.TCPConnector()
        self.session = aiohttp.ClientSession()

        self.RANDOM_MEME_WORDS =  (
            "ass",
            "asshole",
            "asswipe",
            "baka",
            "bitch",
            "bitches",
            "bitching",
            "butt",
            "circumcised",
            "cock",
            "coochie",
            "cum",
            "daquan",
            "dick",
            "dicks",
            "eat my ass",
            "fuck",
            "fucked",
            "fucker",
            "fucking",
            "fucks",
            "gay",
            "horny",
            "is",
            "jordans",
            "lil",
            "lol",
            "nigga",
            "obama",
            "penis",
            "piss",
            "pissed",
            "pisser",
            "pisses",
            "pissing",
            "poop",
            "pooped",
            "pooping",
            "poopy",
            "pussy",
            "shit",
            "shits",
            "shitted",
            "shitter",
            "shitting",
            "slut",
            "stupid",
            "sus",
            "sussy",
            "swag",
            "swagger",
            "the",
            "tiddy",
            "vagina",
            "weed",
            "whore"
        )

    # For !meme, !randommeme
    @classmethod
    async def generate_meme(self, imagedata, toptext = None, bottomtext = None, strokewidth = None):
        img = Image.open(io.BytesIO(imagedata))
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        fontsize1 = 1
        fontsize2 = 1

        w, h = img.size

        MEME_FONT = "fonts/impact.ttf"

        font1 = ImageFont.truetype(MEME_FONT, fontsize1)
        font2 = ImageFont.truetype(MEME_FONT, fontsize2)

        # Determine font sizes
        if toptext:
            while (font1.getsize(toptext)[0] < img.size[0]) and (font1.getsize(toptext)[1] < img.size[1]):
                fontsize1 += 1
                font1 = ImageFont.truetype(MEME_FONT, fontsize1)
        if bottomtext:
            while (font2.getsize(bottomtext)[0] < img.size[0]) and (font2.getsize(bottomtext)[1] < img.size[1]):
                fontsize2 += 1
                font2 = ImageFont.truetype(MEME_FONT, fontsize2)

        # Only make both font sizes the same if there is top text and bottom text
        if toptext and bottomtext:
            minsize = min(fontsize1, fontsize2)

            # The generated text generally looks better when both texts are the same size
            fontsize1 = minsize
            fontsize2 = minsize

        if toptext:
            fontsize1 = min(fontsize1-2, int(h/4))
            font1 = ImageFont.truetype(MEME_FONT, fontsize1-1)
            # Text width/height in pixels + text offset x/y in pixels
            (tw1, th1), (o_x1, o_y1) = font1.font.getsize(toptext)
            tcw1, _ = (w-tw1)/2, (h-th1)/2

            draw.text((tcw1, 0 - o_x1 - o_y1 + 24), toptext, 0xFFFFFF, font=font1, spacing=0, stroke_width = int(strokewidth or fontsize1/15), stroke_fill=0x000000)

        if bottomtext:
            fontsize2 = min(fontsize2-2, int(h/4))
            font2 = ImageFont.truetype(MEME_FONT, fontsize2-1)
            _, desc2 = font2.getmetrics()
            (tw2, th2), (o_x2, o_y2) = font2.font.getsize(bottomtext)
            tcw2, _ = (w-tw2)/2, (h-th2)/2

            draw.text((tcw2, h-th2-o_x2-o_y2-desc2), bottomtext, 0xFFFFFF, font=font2, spacing=0, stroke_width = int(strokewidth or fontsize2/15), stroke_fill=0x000000)

        return img

    @classmethod
    async def generate_album_cover(self, imagedata):
        img = Image.open(io.BytesIO(imagedata))
        img = img.convert("L")

        target_size = 768

        pa_img = Image.open("images/parental_advisory.png")
        pa_padding = 16

        # Resize parental advisory image, but keep aspect ratio
        pa_size = math.floor(target_size * 0.12)
        pa_img.thumbnail((pa_size, pa_size), Image.BICUBIC)

        img.thumbnail((target_size, target_size), Image.BICUBIC)

        crop_size = min(*img.size)

        crop_left = (img.size[0] - crop_size) / 2
        crop_top = (img.size[1] - crop_size) / 2
        crop_right = (img.size[0] + crop_size) / 2
        crop_bottom = (img.size[1] + crop_size) / 2

        img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

        img = ImageOps.autocontrast(img, cutoff=3)

        pasteX = img.size[0] - pa_img.size[0] - pa_padding
        pasteY = img.size[1] - pa_img.size[1] - pa_padding
        img.paste(pa_img, box=(pasteX, pasteY))

        return img

    @classmethod
    async def generate_quote_bubble(self, imagedata):
        img = Image.open(io.BytesIO(imagedata)).convert("RGBA")

        pa_img = Image.open("images/quote_bubble.png").convert("RGBA")
        pa_img = pa_img.resize(img.size, resample=Image.BICUBIC)
        
        img.paste(pa_img, box=None, mask=pa_img)

        img = img.convert("RGB")

        return img

    @classmethod
    async def r_get(self, url, headers = {}, params = {}):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as r:
                    if r.status == 200:
                        return await r.read()
                    else:
                        print(f"HTTP GET Error {r.status} occurred for URL \'{url}\'.")
                        return None
        except Exception as e:
            print(f"HTTP GET Error occurred for URL \'{url}\'. Error: {e}")
            return None

    @classmethod
    async def get_date_int(self):
        date_today = date.today()
        date_str = str(date_today.year + date_today.month + date_today.day)

        return int(date_str)

    @commands.hybrid_command(
        description="Gets all template names for the shitpostbot command.",
        aliases=["shitposttemplates", "spbtemplatenames", "spbnames"],
        usage=""
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def spbtemplates(self, ctx):
        txt_to_send = []

        for template_name in TEMPLATES_METADATA["images"]:
            filename = template_name["filename"]
            # Remove extension
            filename = re.sub(r".(?:jpg|png|jpeg)$", "", filename)
            
            txt_to_send.append(filename)

        with io.BytesIO() as b:
            b.seek(0)

            filenames_concat = "\n".join(txt_to_send).encode()
            
            b.write(filenames_concat)
            b.seek(0)

            await ctx.send(file=discord.File(b, f"shitpost_templatenames_{time.time()}.txt"))

    @commands.hybrid_command(
        description="Generates a random shitpost.",
        aliases=["shitpostbot", "randomshitpost", "rshitpost", "shitpost"],
        usage="[allow-duplicates] [repeat-same-image] [image-name]"
    )
    @discord.app_commands.describe(
        allow_duplicates="Whether or not to allow duplicate source images, allowing the same image to appear multiple times.",
        repeat_picture="If true, all source images will be exactly the same.",
        file_name="The file name of the template to use. Use /spbtemplates to get a list of all template file names."
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def spb(self, ctx, allow_duplicates:bool = False, repeat_picture:bool = False, file_name: str = None):
        post_template = None

        # Lets user pick a template by its file name
        if file_name is not None:
            for data in TEMPLATES_METADATA["images"]:
                # Remove file extension for easier searching
                if data["filename"].split(".")[0] == file_name.lower():
                    post_template = data
                    break

        post_template = post_template or random.choice(TEMPLATES_METADATA["images"])
        # Open template as PIL image
        post_bg = Image.open(f"images/shitpost/template/{post_template['filename']}")

        # Transparent image to paste source images onto
        source_layer = Image.new('RGBA', post_bg.size, (0, 0, 0, 0))

        post_amount = len(post_template["sources"])
        post_sources_list = listdir("images/shitpost/source")
        post_sources = random.choices(post_sources_list, k=post_amount) if allow_duplicates else random.sample(post_sources_list, k=post_amount)

        # For April Fools
        today = datetime.today()
        #if True:
        #    neco_arc_sources = ("neco-arc-gun.jpg", "neco-arc-swag.jpg", "neco-arc-nirvana.jpg", "neco-arc-death.jpg", "neco-arc-ears.jpg")
        #    post_sources = [random.choice(neco_arc_sources) for _ in range(len(post_template["sources"]))]

        if today.month == 4 and today.day == 1:
            post_sources = ["heavy-tf2.jpg" for _ in range(len(post_template["sources"]))]
        elif repeat_picture:
            first_source = post_sources[0]
            post_sources = [first_source for _ in range(len(post_template["sources"]))]

        # Iterate every source
        for i, source in enumerate(post_template["sources"]):
            # Iterate every coordinate/size pair in that source image (if we want to re-use a source image)
            for s_i, size in enumerate(source["size"]):
                # Open source as PIL image, then resize it
                post_overlay = Image.open(f'images/shitpost/source/{post_sources[i]}').resize((size[0], size[1]))
                point = source["points"][s_i]
                # Paste source onto sources layer
                source_layer.paste(post_overlay, box=(point[0], point[1]))
        
        final_img = Image.new('RGBA', post_bg.size, (0, 0, 0, 0))

        # If the template is being overlayed on the source images
        if (post_template["overlay"]):
            final_img.paste(source_layer, (0, 0), source_layer)
            final_img.paste(post_bg, (0, 0), post_bg)
        # Otherwise, paste the template and then the source images
        else:
            final_img.paste(post_bg, (0, 0))
            final_img.paste(source_layer, (0, 0), source_layer)

        # Convert to a JPEG-compatible format
        final_img = final_img.convert('RGB')

        with io.BytesIO() as b:
            final_img.save(b, "JPEG", quality=80)
            b.seek(0)

            better_filename = post_template["filename"].split(".")[0]

            await ctx.send(file=discord.File(b, f'shitpost_{better_filename}_{time.time()}.jpg'))
    
    @commands.hybrid_command(
        description="Generates a random troll comic.",
        aliases=["trollcomic", "trollfacecomic", "ragecomic", "trollface"],
        usage="[# -of-panels] [# -of-columns]"
    )
    @discord.app_commands.describe(
        panel_count="Total # of panels in the comic. If omitted, it will randomly choose anywhere between 4 to 9 panels.",
        column_count="Total # of columns in the comic. If omitted, it will randomly choose anywhere between 2 to 4 columns."
    )
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def tcomic(self, ctx, panel_count: int = None, column_count: int = None):
        # Get all images from that folder
        all_images = listdir("images/trollface_comic")

        meta_json = None
        with open("images/trollface_comic_meta.json", "r") as f:
            meta_json = json.loads(f.read())

        # Resolution for each individual grid 
        image_resolution = (350, 250)
        # Padding around images
        image_padding = 4

        # How the images are laid out - 4, 1, 3 would mean row 1 has 4 images, row 2 has 1, row 3 has 3, etc.
        def get_grid_layout(img_count):
            # Clamp value to a reasonable range if user-provided, else just a random amount
            columns_count = min(16, max(1, column_count)) if column_count else random.randint(2, 4)

            img_layout = []

            while True:
                images_in_this_row = random.randint(1, columns_count)

                # If the images in this row does not exceed the remaining image count
                if images_in_this_row < img_count:
                    img_count -= images_in_this_row
                    img_layout.append(images_in_this_row)
                else:
                    img_layout.append(img_count)
                    break
            
            return img_layout

        # Chooses the panels to use for the comic, essentially a list of filenames
        chosen_images = random.choices(all_images, k=min(80, max(2, panel_count)) if panel_count else random.randint(4, 9))
        # Replace the first image with a proper "comic starter"
        chosen_images[0] = random.choice(meta_json["comic_starters"])
        # Replace the last image with a proper "comic finisher"
        chosen_images[-1] = random.choice(meta_json["comic_finishers"])

        # Gets the comic grid layout - a list where each entry is the panels for that row
        # E.g. [2, 4, 3, 4] - 2 panels on row 1, 4 panels on row 2, 3 panels on row 3, etc.
        grid_layout = get_grid_layout(len(chosen_images))

        grid_width, grid_height = max(grid_layout), len(grid_layout)
        img_width, img_height = grid_width * image_resolution[0], grid_height * image_resolution[1]

        base_img = Image.new('RGB', (img_width, img_height), (0, 0, 0))

        # Iterator for chosen_images (so we can use next())
        iter_images = iter(chosen_images)

        # Where the image size+offset calculation and pasting is done
        for row, grid_length in enumerate(grid_layout): 
            for i in range(grid_length):
                # Get the next image in the iteration
                img_path = next(iter_images)

                # Get the image width ratio
                img_x_ratio = grid_width/grid_layout[row]

                img_new_width = int((image_resolution[0]*img_x_ratio)-(image_padding*2))
                img_new_height = int(image_resolution[1]-(image_padding*2))
                x_offset = int(i*image_resolution[0]*img_x_ratio)+image_padding
                y_offset = row*image_resolution[1]+image_padding

                img_pil = Image.open(f"images/trollface_comic/{img_path}").convert("RGB").resize((img_new_width, img_new_height))

                base_img.paste(img_pil, (x_offset, y_offset))

        with io.BytesIO() as b:
            # Good photo quality isn't necessarily needed
            base_img.save(b, "JPEG", quality=80)
            b.seek(0)

            await ctx.send(file=discord.File(b, f"trollcomic_{time.time()}.jpg"))

    @commands.hybrid_command(
        description="Randomly generates a meme from the provided image.",
        aliases=["rmeme"],
        usage="<image-url> [stroke-width]"
    )
    @discord.app_commands.describe(image_url="An image URL to use as the input.")
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def randommeme(self, ctx, image_url, strokesize:int = None):
        img_bytes = await self.r_get(image_url, headers=self.client.HTTP_HEADERS)
        if not img_bytes: return

        if len(img_bytes) > self.client.MAX_IMAGE_FILESIZE:
            return await ctx.send("File is too big.")

        words = random.choices(self.RANDOM_MEME_WORDS, k=random.randint(1, 9))

        split = int(len(words)/2)
        text1 = " ".join(words[:split]).upper()
        text2 = " ".join(words[split:]).upper()

        print(f"Generating randomized meme requested by {ctx.message.author.display_name}...")

        img = await self.generate_meme(img_bytes, toptext=text1, bottomtext=text2, strokewidth=strokesize)

        print(f"Uploading randomized meme requested by {ctx.message.author.display_name}...")

        with io.BytesIO() as b:
            img.save(b, "JPEG")
            b.seek(0)
            await ctx.send(file=discord.File(b, f"generated_random_meme_{time.time()}.jpg"))

        print(f"Done uploading randomized meme requested by {ctx.message.author.display_name}.")

    @commands.hybrid_command(
        description="Turns the provided image into an album cover.",
        aliases=["album"],
        usage="<image-url>"
    )
    @discord.app_commands.describe(image_url="An image URL to use as the input.")
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def albumcover(self, ctx, image_url):
        img_bytes = await self.r_get(image_url, headers=self.client.HTTP_HEADERS)
        if not img_bytes: return

        if len(img_bytes) > self.client.MAX_IMAGE_FILESIZE:
            return await ctx.send("File is too big.")

        img = await self.generate_album_cover(img_bytes)

        with io.BytesIO() as b:
            img.save(b, "JPEG")
            b.seek(0)
            await ctx.send(file=discord.File(b, f"generated_album_cover_{time.time()}.jpg"))

    @commands.hybrid_command(
        description="Shows a person's stats.",
        usage="[user]",
        aliases=["statsmeter", "statistics", "playerstats"]
    )
    @commands.cooldown(1, 3, commands.BucketType.channel)
    async def stats(self, ctx, user: discord.Member = None):
        chosen_member = user if user else ctx.author

        IMAGE_WIDTH = 1200
        IMAGE_HEIGHT = 800
        LABEL_PADDING_X = 96
        LABEL_PADDING_Y = 24
        SIDE_COUNT = 8

        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), 0x1e1e1e)
        FONT_TITLE = ImageFont.truetype("fonts/arial.ttf", size=50)
        FONT_STATS = ImageFont.truetype("fonts/arial.ttf", size=40)

        angle_interval = 360 / SIDE_COUNT

        sides = []

        for i in range(0, SIDE_COUNT):
            rads = math.radians(i * angle_interval - 90)

            cosRad = math.cos(rads)
            sinRad = math.sin(rads)

            sides.append((cosRad, sinRad))

        imgRadius = (IMAGE_HEIGHT / 2)
        polyBaseCoords = []
        polyBaseRadius = (IMAGE_HEIGHT / 2) - math.floor(IMAGE_HEIGHT / 12)
        polyBaseOffset = 36

        for xUnit, yUnit in sides:
            x = xUnit * polyBaseRadius
            y = yUnit * polyBaseRadius

            # Use an offset of 12 since a pentagon has a weird offset
            polyBaseCoords.append((x + imgRadius, y + imgRadius + polyBaseOffset))

        draw = ImageDraw.Draw(img)
        draw.polygon(polyBaseCoords, fill=0xc3743e, outline=0x774726, width=math.floor(IMAGE_HEIGHT / 30))
        draw.text((IMAGE_HEIGHT / 2, polyBaseOffset - 32), f"{chosen_member.display_name}'s Statistics", 0xFFFFFF, anchor="ma", font=FONT_TITLE)

        # RNG seed based on user id (so that the same result is always given to the same discord ID)
        date_num = await self.get_date_int()
        user_rng = random.Random(chosen_member.id - date_num)

        ringValues = (0.2, 0.4, 0.6, 0.8)

        for value in ringValues:
            poly_coords = []

            for xUnit, yUnit in sides:
                x = xUnit * polyBaseRadius * value
                y = yUnit * polyBaseRadius * value

                # Use an offset of 12 since a pentagon has a weird offset
                poly_coords.append((x + imgRadius, y + imgRadius + polyBaseOffset))

            draw.polygon(poly_coords, None, 0x9d5d32, width=math.floor(IMAGE_HEIGHT / 100))
        
        def randStatValue():
            initialValue = user_rng.uniform(0, 1)
            
            return (2 * initialValue - 1)**4

        # This code is pretty bad
        userValues = [
            ("Based", randStatValue(), 0x3643F4),
            ("Cringe", randStatValue(), 0xF39621),
            ("Gay", randStatValue(), 0xB0279C),
            ("Sexy", randStatValue(), 0x631EE9),
            ("Funny", randStatValue(), 0x3BEBFF),
            ("Stupid", randStatValue(), 0x2257FF),
            ("Racist", randStatValue(), 0xB5513F),
            ("Horny", randStatValue(), 0xD0BBF8),
        ]
        
        userPolyCoords = []

        if discord.utils.get(chosen_member.roles, name="gay nigga"):
            userValues[2] = ("Gay", 99999.99)

        for i, userValue in enumerate(userValues):
            if i >= len(sides):
                continue

            value = userValue[1]

            sideCoords = sides[i]

            x = sideCoords[0] * polyBaseRadius * value
            y = sideCoords[1] * polyBaseRadius * value

            valueCoords = (x + imgRadius, y + imgRadius + polyBaseOffset)

            userPolyCoords.append(valueCoords)

        draw.polygon(userPolyCoords, (81, 151, 255), 0xFFFFFF, width=math.floor(IMAGE_HEIGHT / 70))
        
        statTextOffset = 64 + 16
        draw.rounded_rectangle((imgRadius * 2 - 32, 32, IMAGE_WIDTH + 32, IMAGE_HEIGHT - 32), 32, 0x121212)

        for i, userCoords in enumerate(userPolyCoords):
            title = userValues[i][0]
            value = userValues[i][1]
            color = userValues[i][2]

            outlineColor = 0xFFFFFF

            niceValue = round(value * 100)

            x = min(IMAGE_HEIGHT - LABEL_PADDING_X, max(userCoords[0], LABEL_PADDING_X))
            y = min(IMAGE_HEIGHT - LABEL_PADDING_Y, max(userCoords[1], LABEL_PADDING_Y))

            #draw.text((x, y), f"{niceValue:,d}% {title}", 0x000000, stroke_fill=0xFFFFFF, stroke_width=math.floor(IMAGE_HEIGHT / 170), anchor="mm", font=FONT_STATS)
            #draw.text((x, y), f"{i}", 0x000000, stroke_fill=0xFFFFFF, stroke_width=math.floor(IMAGE_HEIGHT / 170), anchor="mm", font=FONT_STATS)

            draw.text((imgRadius * 2 + 48, statTextOffset), f"{niceValue:,d}% {title}", fill=0xFFFFFF, anchor="lm", font=FONT_STATS)

            draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=color, outline=outlineColor, width=IMAGE_HEIGHT // 170)
            draw.ellipse((imgRadius * 2, statTextOffset - 16, imgRadius * 2 + 32, statTextOffset + 16), fill=color, outline=outlineColor, width=IMAGE_HEIGHT // 170)

            statTextOffset += 44

        with io.BytesIO() as b:
            img.save(b, "PNG")
            b.seek(0)

            dFile = discord.File(b, f"userstats_{chosen_member.id}_{time.time()}.jpg")

            await ctx.send(file=dFile)

    @commands.hybrid_command(
        description="Puts a quote bubble on top of the image.",
        aliases=["quote"],
        usage="<image-url>"
    )
    @discord.app_commands.describe(image_url="An image URL to use as the input.")
    @commands.cooldown(2, 1, commands.BucketType.channel)
    async def quotebubble(self, ctx, image_url):
        img_bytes = await self.r_get(image_url, headers=self.client.HTTP_HEADERS)
        if not img_bytes: return

        if len(img_bytes) > self.client.MAX_IMAGE_FILESIZE:
            return await ctx.send("File is too big.")

        img = await self.generate_quote_bubble(img_bytes)

        with io.BytesIO() as b:
            img.save(b, "PNG")
            b.seek(0)
            await ctx.send(file=discord.File(b, f"generated_quote_bubble_{time.time()}.gif"))

async def setup(bot):
    await bot.add_cog(Images(bot))
