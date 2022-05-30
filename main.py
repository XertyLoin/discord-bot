import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import youtube_dl
import asyncio
from data_handler import DataHandler
import random



intents = discord.Intents.all()

bot = commands.Bot(command_prefix="²", description="Bot by Xerty and ToinouX", intents = intents)

bot.remove_command('help')

musics = {}
ytdl = youtube_dl.YoutubeDL()

database_handler = DataHandler("database_bpgc.db")      


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    id = message.author.id
    username = message.author
    channel = message.channel
    message = 1
    if database_handler.check_id(id=id):
        database_handler.add_lvl(id=id)
    else:
        database_handler.creat_user(id=id, message=message, username=username)
        print(username)

@bot.command()
@commands.has_permissions(administrator=True)
async def nuclear_codes(ctx):
    await ctx.send("0135754456")

#autres
@bot.event
async def on_member_join(member):
    id = member.id
    channel = bot.get_channel(836330499005349959)
    role = discord.utils.get(member.guild.roles, id=836331956949876756)
    await member.add_roles(role)
    await channel.send(f"bienvenue a toi {member.mention}")
    database_handler.add_on_join(id)

@bot.event
async def on_ready():
    print("Ready !")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_permissions(manage_messages = True)
async def user(ctx):
    g = ctx.guild
    users = g.members
    print(users)

@bot.command()
async def roll(ctx):


@bot.command()
async def tos(ctx):
    embed = discord.Embed(title = " Les ToS", url = "https://discord.com/terms")
    await ctx.send(embed=embed)

@bot.command()
async def Help(ctx):
    embed = discord.Embed(title="Help", value ="Tu a besoin d'aide ?")
    embed.add_field(name = "²Mhelp `{commande}`", value = "Permet d'avoir sur les commandes musiques")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/878373756706373674/902481116164923392/Requin_005.png")
    await ctx.send(embed=embed)

@bot.command()
async def avatar(self, ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, reason):
    await member.ban(reason = reason)
    await ctx.send(f"{member.mention} a été bani pour : {reason}")

@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} a été débani")

@bot.command()
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f"{user.mention} a été kick")

@bot.command()
async def Mhelp(ctx, command):
    if command == "play":
        await ctx.send("Cette commande de te jouer la musique que donne se lien (ex : ²play https://www.youtube.com/watch?v=mp2njiaJWD0&t=61s&ab_channel=Xerty) **[!]** Attention sa peut jouer que les liens youtube")
    if command == "skip":
            await ctx.send("Cette commande permet de skip la musique qui est entrain d'être jouer ")
    if command == "stop":
        await ctx.send("Cette commande permet de arrêter toutes les musiques enregistrer dans la file d'attente et de déco le bot")

# Commandes musiques
class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    await ctx.send(f"j'ai skip : {video.url}")
    client.stop()

def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)



@bot.command()
async def play(ctx, url):
    print("sa marche")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        try:
            channel = ctx.author.voice.channel 
        except:
            await ctx.send("tu n'est pas dans un salon vocal")
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)
    
bot.run("OTExMzczODA0NDQwMjg5NDIw.YZgc_w.w7HZ7DCxCgAl3t90mokY7ubD52w")