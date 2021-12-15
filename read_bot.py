#!/usr/bin/python3

import discord
import asyncio
from discord.ext import commands
import subprocess
import ffmpeg

token= "your-token-here"
client = commands.Bot(command_prefix='.')
voice_client = None
global bot_c
bot_c = 0
global temp
temp = []

@client.event
async def on_ready():
    print(client.user.name + ' 起動')
    asyncio.ensure_future(play_voice())

# --------------------------------------------------------
# tempリストに音声ファイルがあれば再生
# --------------------------------------------------------
async def play_voice():
    while True:
        global temp
        if bot_c and temp:
            if not bot_c.guild.voice_client.is_playing():
                create_wav(temp[0])
                ffmpeg_audio_source = discord.FFmpegPCMAudio("open_jtalk.wav")
                bot_c.guild.voice_client.play(ffmpeg_audio_source)
                temp.pop(0)
        await asyncio.sleep(0.5)

# --------------------------------------------------------
# 起動時の処理
# --------------------------------------------------------
@client.command()
async def join(ctx):
    vc = ctx.author.voice.channel
    await vc.connect()
    mes = "読み上げを開始します"
    global bot_c
    bot_c = ctx
    await ctx.send(mes)

# --------------------------------------------------------
# 終了時の処理
# --------------------------------------------------------
@client.command()
async def bye(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("さようなら")

# --------------------------------------------------------
# チャットが送信された時の処理
# --------------------------------------------------------
@client.event
async def on_message(message):
    global temp
    if message.content.startswith('.'):
        pass
    elif message.author.bot:
        pass
    elif message.content.startswith('!'):
        pass
    elif message.content.startswith('?'):
        pass
    else:
        mes = message.content
        if mes.startswith("http"):
            mes = "URL"
        if  mes.startswith("<@!"):
            mes = mes.replace("<@!","")
            mes = mes.replace(">","")
            user = client.get_user(int(mes))
            mes = "@" + user.display_name
        temp.append(mes)
    await client.process_commands(message)

# --------------------------------------------------------
# テキストの音声変換処理
# --------------------------------------------------------
def create_wav(txt):
    open_jtalk=['open_jtalk']
    mech=['-x','/usr/local/share/open_jtalk_dic_utf_8-1.07']
    htsvoice=['-m','htsvoice/neutral.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(txt.encode('utf-8'))
    c.stdin.close()
    c.wait()

client.run(token)
