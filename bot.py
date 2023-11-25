import discord # import discordpy
from discord.ext import commands
from discord import Spotify, Game, DMChannel
#imports google api and datetime api
from googleapiclient.discovery import build
from datetime import datetime

userrunningbot = "Boxuga"
userrunningbotid = 485304692478312449
token = "" # Discord bot token go to https://discord.dev to generate one
bot = commands.Bot(command_prefix='of!', case_insensitive=True, self_bot=True, intents=discord.Intents.all()) # why did i make it of! it sounds like onlyfans
blacklistedchannel = [] # put youtube channel ids example "UCWyiqU4LAbrxNX7_Llw8D3w"
allowedcategoryid = [] # checks if in correct catagory so it doesn't block staff channels
googledevtoken = "" # google dev token you can generate one on https://console.cloud.google.com/apis/dashboard

async def blacklistyoutubechannel(videoid, message):
    youtube = build('youtube', "v3", developerKey=googledevtoken)
    response = youtube.videos().list(id=videoid, part='snippet').execute()
    if response['items'][0]['snippet']['channelId'] in blacklistedchannel:
        await message.author.send(f'You posted a video by {response['items'][0]['snippet']['channelTitle']} which this bot blacklists. if you don\'t remeber sending this meesage you\'re account may be compromised. Contact {userrunningbot} if you believe the channel has been wrongly blacklisted')
        print(message.author.name + "#" + message.author.discriminator + ": " + message.content + " - blacklisted user posted this at " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) + " - " + str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year))
        await message.delete()

def getyoutubeinfo(args):
    youtube = build('youtube', "v3", developerKey=googledevtoken)
    return youtube.videos().list(id=args, part='snippet').execute()

@bot.event
async def on_ready():
    print("bot started")
    await bot.change_presence(activity=discord.Game("Check Out 3TA Online discord.gg/3taonline"))
    #await bot.add_cog(YouTubeMessageBan(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #print(message.author.id)
    try:
        if message.channel.category_id in allowedcategoryid:
            count = 0
            for value in message.content.split(): # checks if youtu.be/youtube.com/ is in message and checks it if its in the blacklisted messages 
                if value.lower().count("youtu.be") != 0:
                    url = message.content.split()[count][message.content.split()[count].find(".be/")+4:]
                    await blacklistyoutubechannel(url[0:11], message)
                    print(message.author.name + "#" + message.author.discriminator + ": " + message.content + " - this message has a youtube link")
                    return
                elif value.lower().count("youtube.com/") != 0:
                    url = message.content.split()[count][message.content.split()[count].find("v=")+2:]
                    await blacklistyoutubechannel(url[0:11], message)
                    print(message.author.name + "#" + message.author.discriminator + ": " + message.content + " - this message has a youtube link")
                    return
                    #print(message.content.split()[count][message.content.split()[count].find(".be/")+4:])
                        
                count+=1
    except:
        print(message.author.name + "#" + message.author.discriminator + ": " + message.content + " - this message caused the message checking code to fail" + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) + " - " + str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year))

    if message.content.startswith("of!videoid") and (message.author.id == userrunningbotid or message.channel.id == 1099945430902636625):
        arg = message.content[11:22]
        try:
            await message.reply("Username = " + getyoutubeinfo(arg)['items'][0]['snippet']['channelTitle'] + "\nID = " + getyoutubeinfo(arg)['items'][0]['snippet']['channelId'])
        except:
            await message.reply("An error occured or invalid syntax")

    if message.content.startswith("of!blocktemp") and (message.author.id == userrunningbotid or message.channel.id == 1099945430902636625):
        args = message.content[13:24]
        channelid = getyoutubeinfo(args)['items'][0]['snippet']['channelId']
        #discord.user.User(id=userrunningbotid).send("Channel ID to add to blocklist perma add = " + channelid)
        blacklistedchannel.append(channelid)
    
    if message.content.startswith("of!boxtime"):
        await message.reply("The time for " + userrunningbot + " is currently " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + " which is Australian Western Standard Time (AWST)") # this is kinda stupid but its fun

@bot.command()
async def hi(ctx):
    await ctx.reply("Hey There")


@bot.command()
async def videoid(ctx: commands.Context, arg):
    print(arg)
    youtube = build('youtube', "v3", developerKey=googledevtoken)
    response = youtube.videos().list(id=arg, part='snippet').execute()
    try:
        await ctx.reply(response['items'][0]['snippet']['channelTitle'])
    except:
        await ctx.reply("Something wrong happend")



bot.run(token)