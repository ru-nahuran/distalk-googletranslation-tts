import asyncio
import discord
from discord.ext import commands
import os
import traceback
import urllib.parse
import re
import emoji
import json
from logging import  getLogger

prefix = os.getenv('DISCORD_BOT_PREFIX', default='/')
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix=prefix)
with open('emoji_ja.json', encoding='utf-8') as file:
    emoji_dataset = json.load(file)
    
channel = {} # テキストチャンネルID
connected_channel = {}
logger = getLogger(__name__)

@client.event
async def on_ready():
    presence = f'{prefix}ヘルプ | 0/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@client.event
async def on_guild_join(guild):
    presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@client.event
async def on_guild_remove(guild):
    presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))


    
@client.command()
async def 辞書(ctx, arg1, arg2):
    with open('dic.txt', mode='a') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました')
    
    

@client.command()
async def 接続(ctx):
    global connected_channel
    if ctx.author.voice is None:
        await ctx.channel.send(f"{ctx.author.mention}さんはボイスチャンネルに接続していません")
        logger.info(f"{ctx.author}さんはボイスチャンネルに接続していません")
        return
    if ctx.guild.voice_client is not None:
        await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
        embed = discord.Embed(title="読み上げ開始", inline="false", color=0x3399cc)
        embed.add_field(name="テキストチャンネル", value=f"{ctx.channel.name}", inline="false")
        embed.add_field(name="ボイスチャンネル", value=f"{ctx.author.voice.channel.name}", inline="false")
        await ctx.send(embed=embed)
        logger.info(f"{ctx.author.voice.channel.name}に接続しました")
        connected_channel[ctx.guild] = ctx.channel
        return
    
    await ctx.author.voice.channel.connect()
    embed = discord.Embed(title="読み上げ開始", inline="false", color=0x3399cc)
    embed.add_field(name="テキストチャンネル", value=f"{ctx.channel.name}", inline="false")
    embed.add_field(name="ボイスチャンネル", value=f"{ctx.author.voice.channel.name}", inline="false")
    await ctx.send(embed=embed)
    logger.info(f"{ctx.author.voice.channel.name}に接続しました")
    connected_channel[ctx.guild] = ctx.channel
    

@client.command()
async def 切断(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        else:
            await ctx.voice_client.disconnect()
            

@client.event
async def on_message(message):
    global connected_channel
    if message.author.bot:
        return
    if message.content.startswith(prefix):
        pass
    else:
        if message.channel in connected_channel.values() and message.guild.voice_client is not None:
            if message.guild.voice_client:
                text = message.content
                text = text.replace('\n', '、')
                text = re.sub(r'[\U0000FE00-\U0000FE0F]', '', text)
                text = re.sub(r'[\U0001F3FB-\U0001F3FF]', '', text)
                pattern = r'https://tenor.com/view/[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '画像', text)
                pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
                text = re.sub(pattern, '、画像', text)
                pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '、URL', text)
                #text = message.author.name + '、' + text
                pattern = r'七七'
                text = re.sub(pattern, '、なな', text)
                pattern = r'原神'
                text = re.sub(pattern, '、げんしん', text)
                pattern = r'小恋色'
                text = re.sub(pattern, '、ここいろ', text)
                pattern = r'みー様'
                text = re.sub(pattern, '、みーさま', text)
                pattern = r'魈'
                text = re.sub(pattern, '、しょう', text)
                pattern = r'万葉'
                text = re.sub(pattern, '、かずは', text)
                pattern = r'申鶴'
                text = re.sub(pattern, '、しんかく', text)
                pattern = r'胡桃'
                text = re.sub(pattern, '、ふぅたお', text)
                pattern = r'雲菫'
                text = re.sub(pattern, '、うんきん', text)
                pattern = r'刻晴'
                text = re.sub(pattern, '、こくせい', text)
                pattern = r'煙緋'
                text = re.sub(pattern, '、えんひ', text)
                pattern = r'磐岩結緑'
                text = re.sub(pattern, '、ばんがんけつろく', text)
                pattern = r'層岩巨淵'
                text = re.sub(pattern, '、そうがんきょえん', text)
                pattern = r'ct'
                text = re.sub(pattern, '、しーてぃー', text)
                pattern = r'四風原典'
                text = re.sub(pattern, '、しふうげんてん', text)
                pattern = r'凍れ'
                text = re.sub(pattern, '、こおれ', text)
                pattern = r'岩王帝君'
                text = re.sub(pattern, '、がんおうていくん', text)
                pattern = r'璃月'
                text = re.sub(pattern, '、りーゆえ', text)
                if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                    while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                        text = text[:-1]
                    text = text[:-1] + '、ワラ'
                if text[-1:] == '?' or text[-1:] == '？' or text[-1:] == '?' or text[-1:] == '？':
                    while text[-2:-1] == '?' or text[-2:-1] == '？' or text[-2:-1] == '？' or text[-2:-1] == '?':
                        text = text[:-1]
                    text = text[:-1] + '、はてな'
                for attachment in message.attachments:
                    if attachment.filename.endswith((".jpg", ".jpeg", ".gif", ".png", ".bmp")):
                        text += '、画像'
                    else:
                        text += '、添付ファイル'
                if len(text) < 100:
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while message.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
                else:
                    await message.channel.send('100文字以上は読み上げできません。')
            else:
                pass
        else:
            pass
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                #await after.channel.connect()
            else:
                if member.guild.voice_client.channel is after.channel:
                    text = member.name + 'さんが入室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif after.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client:
                if member.guild.voice_client.channel is before.channel:
                    if len(member.guild.voice_client.channel.members) == 1:
                        await asyncio.sleep(0.5)
                        await member.guild.voice_client.disconnect()
                    else:
                        text = member.name + 'さんが退室しました'
                        s_quote = urllib.parse.quote(text)
                        mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                        while member.guild.voice_client.is_playing():
                            await asyncio.sleep(0.5)
                        member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif before.channel != after.channel:
        if member.guild.voice_client:
            if member.guild.voice_client.channel is before.channel:
                if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                    await asyncio.sleep(0.5)
                    await member.guild.voice_client.disconnect()
                    await asyncio.sleep(0.5)
                    await after.channel.connect()

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    
@client.command()
async def ヘルプ(ctx):
    message = f'''◆◇◆{client.user.name}の使い方◆◇◆
{prefix}＋コマンドで命令できます。
{prefix}接続：ボイスチャンネルに接続します。
{prefix}切断：ボイスチャンネルから切断します。'''
    await ctx.send(message)

client.run(token)
