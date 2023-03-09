import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import time
import animec
import os

intents = discord.Intents.all()

riku = commands.Bot(command_prefix="r?", intents = intents)
riku.remove_command("help")

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@riku.event
async def on_ready():
    idk = (colors.GREEN + time.strftime("%a, %d %b %Y %I:%M %p") + colors.ENDC)    
    print(idk + colors.FAIL + "     Riku just woke up!" + colors.ENDC)
    sync = await riku.tree.sync()
    print(idk + colors.BOLD + colors.BLUE + f"     Synced {len(sync)} commands" + colors.ENDC)


@riku.event
async def on_command_error (interaction: discord.Interaction, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
                await interaction.response.send_message ("Required arguments are missing", delete_after=5)
        elif isinstance(error, commands.errors.BadArgument):
                await interaction.response.send_message (f"The data type passed is invalid\n {str(error)}")
        elif isinstance(error, commands.errors.NotOwner):
                await interaction.response.send_message ("You are not the owner of me!")
        elif isinstance(error, commands.errors.MissingAnyRole):
                await interaction.response.send_message ("This command requires `Administrator` or `Owner`, name must be exactly the same to use this command")
        elif isinstance(error, commands.errors.MissingPermissions):
                await interaction.response.send_message ("You do not have required permissions to use this command")
        elif isinstance(error, commands.errors.CheckFailure):
                await interaction.response.send_message ("You can't use this command, because its made for a specific server command")
        else:
            raise error

@riku.tree.command(name="help", description="Help menu")
async def help(interaction: discord.Interaction):
        user = interaction.user
        embed=discord.Embed(color=0x2f3136)
        embed.set_author(name="Riku's commands")
        embed.set_thumbnail(url = user.avatar)
        embed.add_field(name="<:Icon_Diamond:1074200776689324133> Standard", value="`help` `avatar` `userinfo` `serverinfo` `latency` `botinfo`", inline=False)
        embed.add_field(name="<:Icon_Star:1074200070909607998> 4fun", value="`say` `beep` `gay` `pp`", inline=False)
        embed.add_field(name="<:Icon_Staff:1074200242653765632> Moderation *In development*", value="`slowmode` `nickname`", inline=False)
        embed.add_field(name="<a:shiggy:1074200490423877663> Anime related", value="`search_anime` `search_character` `anime_news`\n`waifu` `neko` `shinobu` `megumin`\n`hug` `kill` `cry` `bite` `blush` `kick` `smug` `kiss` `lick`", inline=False)
        embed.add_field(name="<:Icon_Developer:1074200034695983144> Bot developer only", value="`changestatus`", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Requested by {user.name}#{user.discriminator}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@riku.tree.command(name="avatar", description="Fetches user's avatar")
async def avatar(interaction: discord.Interaction,  user : discord.Member=None):
        if user is None:
            user = interaction.user
        embed = discord.Embed( color = user.color)
        embed.set_author(name = f"{user.name}'s Avatar")
        embed.set_image(url = user.avatar)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Requested by {user.name}#{user.discriminator}")
        await interaction.response.send_message(embed=embed, ephemeral=True)


@riku.tree.command(name="botinfo", description="Shows information about the bot")
async def botinfo(interaction: discord.Interaction):
        embed = discord.Embed(color=0x2f3136)
        embed.set_author(name= "Information about Riku!")
        embed.add_field(name="<:Icon_Developer:1074200034695983144> Language and Libraries", value="Language: [Python](https://www.python.org/)\nLibraries: [discord.py](https://discordpy.readthedocs.io/en/stable/), [animec](https://animec.readthedocs.io/en/latest/)", inline=True)
        embed.add_field(name="<a:shiggy:1074200490423877663> Riku's ID", value="1060061912710258699", inline=True)
        embed.add_field(name="<a:blondenekowave:1074276292108750889> Riku's owner", value="<@670986272377929743>", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}")
        await interaction.response.send_message(embed=embed)

    # Userinfo command
@riku.tree.command(name="userinfo", description="Shows information about the user")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None): 
        if user is None:
            user = interaction.user     
        
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0x2f3136, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Joined server at", value=user.joined_at.strftime(date_format))
        embed.add_field(name="Joined discord at", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Top role", value=f"<@&{user.top_role.id}>", inline=True)
        embed.add_field(name="Permissions", value=perm_string, inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='ID: ' + str(user.id))
        return await interaction.response.send_message(embed=embed)

    # Serverinfo command
@riku.tree.command(name="serverinfo", description="Shows information about the server")
async def serverinfo(interaction: discord.Interaction):
        creationDate = interaction.guild.created_at.__format__('%A, %d. %B %Y')
        embed = discord.Embed(color=0x2f3136)
        embed.add_field(name = "Owner", value=f"<@{interaction.guild.owner_id}>", inline=True)
        embed.add_field(name = "Categories", value=f"{len(interaction.guild.categories)}", inline=True)
        embed.add_field(name = "Text channels", value=f"{len(interaction.guild.text_channels)}", inline=True)
        embed.add_field(name = "Voice channels", value=f"{len(interaction.guild.voice_channels)}", inline=True)
        embed.add_field(name = "Members", value=f"{interaction.guild.member_count}", inline=True)
        embed.add_field(name = "Roles", value=f"{len(interaction.guild.roles)}", inline=True)
        embed.add_field(name = "Verification level", value=f"{len(interaction.guild.verification_level)}", inline=True)
        embed.add_field(name = "NSFW Filter", value=f"{(interaction.guild.explicit_content_filter)}", inline=True)
        embed.add_field(name = "MFA Level", value=f"{(interaction.guild.mfa_level)}", inline=True)
        embed.add_field(name = "Emojis", value=f"{len(interaction.guild.emojis)}", inline=True)
        embed.set_thumbnail(url=interaction.guild.icon) 
        embed.set_footer(text = f"Server created at {creationDate} | " "ID: " + str(interaction.guild.id))
        embed.set_author(name = f"{interaction.guild.name}", icon_url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)

# ===============================================================================
# ===============================================================================

@riku.tree.command(name="latency", description="Shows the latency of the bot")
async def latency(interaction: discord.Interaction):
        await interaction.response.send_message( f"Current latency is **{round(riku.latency * 1000)}ms**")

# ===============================================================================
# ===============================================================================

@riku.tree.command(name="search_anime", description="Search for given anime")
@app_commands.describe(query = "What anime you want to search?")
async def search_anime(interaction: discord.Interaction, query: str):
        try: 
            anime = animec.Anime(query)
        except:
            await interaction.response.send_message("<a:blondenekocry:1074276279920103496> No corresponding anime is found for the search query")
            return
        embed = discord.Embed(title = anime.title_english, url = anime.url, description = f"{anime.description[:400]}...", color = 0x2f3136)
        embed.add_field(name = "Episodes", value = str(anime.episodes))
        embed.add_field(name = "Status", value = str(anime.status))
        embed.add_field(name = "Genres", value = str(anime.genres))
        embed.add_field(name = "Series Type", value = str(anime.type))
        embed.add_field(name = "Rating", value = str(anime.rating))
        embed.add_field(name = "NSFW Status", value = str(anime.is_nsfw()))
        embed.set_thumbnail(url = anime.poster)
        await interaction.response.send_message(embed = embed)

@riku.tree.command(name="search_character", description="Search for anime character")
@app_commands.describe(query = "What character you want to search?")
async def search_character(interaction: discord.Interaction, query: str):
        try: 
            char = animec.Charsearch(query)
        except:
            await cinteraction.response.send_message("<a:blondenekocry:1074276279920103496> No corresponding anime character is found for the search query")
            return
        embed=discord.Embed(title = char.title, url = char.url, color = 0x2f3136)
        embed. set_image(url = char.image_url)
        embed. set_footer(text = ", " .join(list(char.references.keys())[:3]))
        await interaction.response.send_message(embed=embed)
                                
@riku.tree.command(name="anime_news", description="Sends latest anime news")
async def anime_news(interaction: discord.Interaction ,amount:int=3):
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        desc = news.description

        embed = discord.Embed(title = "Latest anime news", color = 0x2f3136)
        embed.set_thumbnail(url = news.images[0])
        embed.timestamp = datetime.datetime.utcnow()

        for i in range(amount):
            embed.add_field(name = f"{i+1}) {titles[i]}", value =f"{desc[i][:400]}...\n[Read more]({links[i]})",inline=False)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="waifu", description="Sends random waifu")
async def waifu(interaction: discord.Interaction):
    
        waifus = animec.Waifu.waifu()
    
        embed=discord.Embed(title = f"Here's your waifu~!" ,url = waifus,color = 0x2f3136)
        embed.set_image(url = waifus)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="neko", description="Sends random neko")
async def neko(interaction: discord.Interaction):
    
        nekos = animec.Waifu.neko()
    
        embed=discord.Embed(title = f"Here's your lovely neko!" ,url = nekos,color = 0x2f3136)
        embed.set_image(url = nekos)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="megumin", description="Sends random megumin")
async def megumin(interaction: discord.Interaction):
    
        megumin = animec.Waifu.megumin()
    
        embed=discord.Embed(title = f"Here's your lovely megumin!" ,url = megumin,color = 0x2f3136)
        embed.set_image(url = megumin)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="shinobu", description="Sends random shinobu")
async def shinobu(interaction: discord.Interaction):
    
        shinobu = animec.Waifu.shinobu()
    
        embed=discord.Embed(title = f"Here's your lovely shinobu!" ,url = shinobu,color = 0x2f3136)
        embed.set_image(url = shinobu)
        await interaction.response.send_message(embed=embed)
        
@riku.tree.command(name="rgif", description="Sends random anime gif")
async def rgif(interaction: discord.Interaction):
    
        rgif = animec.Waifu.random_gif()
    
        embed=discord.Embed(title = f"Random anime gif" ,url = rgif,color = 0x2f3136)
        embed.set_image(url = shinobu)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="rpic", description="Sends random waifus from random category")
async def rpic(interaction: discord.Interaction):
    
        rpic = animec.Waifu.random()
    
        embed=discord.Embed(title = f"Random waifu" ,url = rpic,color = 0x2f3136)
        embed.set_image(url = shinobu)
        await interaction.response.send_message(embed=embed)

# ===============================================================================
# ===============================================================================

@riku.tree.command(name="hug", description="You need a hug? :c")
async def hug(interaction: discord.Interaction, user : discord.Member):

        
        hugs = [f"hugs {user.name}. Aww, adorable!", f"hugs {user.name}. uwu", f"hugs {user.name}. OwO", f"hugs {user.name}. Huggy hug", f"hugs {user.name}. <3!",
                f"hugged {user.name}. Aww, adorable!", f"is hugging {user.name}. uwu", f"is hugging {user.name}. OwO", f"hugged {user.name}. Huggy hug", f"is hugging {user.name}. <3!"]
        hug = animec.Waifu.hug()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(hugs))}", icon_url = interaction.user.avatar)
        embed.set_image(url = hug)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="kill", description="kill someone idk")
async def kill(interaction: discord.Interaction, user : discord.Member):
        
        kills = [f"kills {user.name}. Ouch!", f"killed {user.name}. Brutal!", f"brutally killed {user.name}. Oh my..", f"killed {user.name}.. What have you done...?"]
        kill = animec.Waifu.kill()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{ctx.author.name} {(random.choice(kills))}", icon_url = ctx.author.avatar)
        embed.set_image(url = kill)
        await ctx.send(embed=embed)

@riku.tree.command(name="blush", description="blushy blush")
async def blush(interaction: discord.Interaction):
        
        blushes = [" has turned into a tomato", "'s face is red~", " is blushing! cute~", " blushed!! >///<"]
        blush = animec.Waifu.blush()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name}{(random.choice(blushes))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = blush)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="cry", description="why are you crying lol")
async def cry(interaction: discord.Interaction):
        
        cries = ["cries... :'c", "is crying... there there...", "is crying... :c", "needs a hug..."]
        cry = animec.Waifu.cry()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{ctx.author.name} {(random.choice(cries))}.", icon_url = ctx.author.avatar)
        embed.set_image(url = cry)
        await interaction.response.send_message(embed=embed)

@riku.command(name="bite", description="Bite someone")
async def bite(interaction: discord.Interaction, user : discord.Member):
        
        bites = [f"gives {user.name} a bite! Yumm~", f"bites {user.name}! Owie", f"bites {user.name}!! Kinky ;)"]
        bite = animec.Waifu.bite()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(bites))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = bite)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="kick", description="Kick someone in the ass lol")
async def akick(interaction: discord.Interaction, user : discord.Member):
        
        kickes = [f"kicks {user.name}. Holy shit!", f"kicked {user.name}. You felt that pain?", f"just kicked {user.name}. Very hard!!"]
        kick = animec.Waifu.kick()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(kickes))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = kick)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="smug", description="smug idk lol")
async def smug(interaction: discord.Interaction):
        
        smugs = ["thinks little of you ;)", "scoffs c:<", "has a smug look c;"]
        smug = animec.Waifu.smug()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(smugs))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = smug)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="kiss", description="Kiss someone uwu")
async def kiss(interaction: discord.Interaction, user : discord.Member):
        
        kisses = [f"kissed {user.name}! Cute!", f"kisses {user.name}'s lips~", f"kisses {user.name}!! OwO"]
        kiss = animec.Waifu.kiss()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(kisses))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = kiss)
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="lick", description="Lick someone")
async def lick(interaction: discord.Interaction, user : discord.Member):
        licks = [f"licks {user.name}! OwO", f"licks {user.name}!! How does it taste?!", f"gives {user.name} a lick!"]
        lick = animec.Waifu.lick()
    
        embed=discord.Embed(color = 0x2f3136)
        embed.set_author(name = f"{interaction.user.name} {(random.choice(licks))}.", icon_url = interaction.user.avatar)
        embed.set_image(url = lick)
        await interaction.response.send_message(embed=embed)

# ===============================================================================
# ===============================================================================

@riku.tree.command(name="say", description="Send a message as bot")
@app_commands.describe(say = "What you want me to say?")
async def say(interaction: discord.Interaction, say: str):
        await interaction.response.send_message(say)

    # Gay command
@riku.tree.command(name="gay", description="the funi")
async def gay(interaction: discord.Interaction, user : discord.Member=None):
        gay = random.randint(0, 100)
        if user == None:
            user = interaction.user
            embed = discord.Embed(description = f"You are {gay}% gay :gay_pride_flag:", color = 0x2f3136)
        else:
            embed = discord.Embed(description = f"{user.name} is {gay}% gay :gay_pride_flag:", color = 0x2f3136)
        embed.set_author(name = "gay r8 machine")
        await interaction.response.send_message(embed=embed)

    # Beep command
@riku.tree.command(name="beep", description="boop")
async def beep(interaction: discord.Interaction):
        await interaction.response.send_message("boop")

@riku.tree.command(name="pp", description="the funi")
async def pp(interaction: discord.Interaction, user : discord.Member=None):
        if user == None:
            user = interaction.user
        dick = "8{}D".format("=" * random.randint(0, 15))
        embed = discord.Embed(description = f"{user.name}'s penis\n{dick}", color = 0x2f3136)
        embed.set_author(name = "peepee size machine")
        await interaction.response.send_message(embed=embed)

@riku.tree.command(name="changestatus", description="Changes status of the bot")
async def changestatus(interaction: discord.Interaction, text: str = None):
        if interaction.user.id == 670986272377929743:
                if text == None:
                        await  interaction.response.send_message("My status has been changed to default")
                        await riku.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= f"in {len(riku.guilds)} servers! | /help"))
                else:
                        await  interaction.response.send_message("My status has been changed")
                        await riku.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name= f"{text}"))
        else:
                await interaction.response.send_message ("You are not the owner of me!")
# ==============================================

@riku.tree.command(name="nickname", description="Changes someones nickname")
@app_commands.describe(member = "Choose the member", nick = "Type something you want to change the nickname to")
async def nickname(interaction: discord.Interaction, member: discord.Member, nick: str):
        if interaction.permissions.change_nickname == True:
                await member.edit(nick=nick)
                await interaction.response.send_message('Nickname has been changed. ')
        else:
                await interaction.response.send_message ("You do not have required permissions to use this command")

    # Slowmode command
@riku.tree.command(name="slowmode", description="Allows you to change the slowmode of the channel")
@app_commands.describe(seconds = "How many seconds for the slowmode you want?")
async def slowmode(interaction: discord.Interaction, seconds: int=None):
        if interaction.permissions.manage_channels == True:
                try:
                        await interaction.channel.edit(slowmode_delay=seconds)
                        await interaction.response.send_message(f"Cooldown has been set to **{seconds} seconds**")
                except ValueError:
                        await interaction.response.send_message("You are such an idiot")
        else:
                await interaction.response.send_message ("You do not have required permissions to use this command")


riku.run(os.getenv("riku_token"))