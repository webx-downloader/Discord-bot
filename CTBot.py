import discord
from discord import message
import requests

API_KEY = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  
REGION = "europe"
PLATFORM = "eun1"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_summoner_info(gameName, tagLine):
    account_url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": API_KEY}

    account_res = requests.get(account_url, headers=headers)
    account_data = account_res.json()

    puuid = account_data["puuid"]

    summoner_url = f"https://{PLATFORM}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    summoner_res = requests.get(summoner_url, headers=headers)
    summoner_data = summoner_res.json()

    return {
        "gameName": gameName,
        "tagLine": tagLine,
        "level": summoner_data["summonerLevel"],
    }

# Játékosok listája
players = {
    "Domi": ("12dominik1234567", "12125"),
    "TMZ": ("marcellzalan", "EUNE"),
    "Turista": ("SzakacsMilan", "EUNE"),
    "Dinnye": ("Nem görögdinnye", "EUNE"),
    "Dani": ("Dani906252", "dani"),
    "Hege": ("YETI", "8611"),
}
# lol-stats bot indítása/bejelentkezés

@client.event
async def on_ready():
    print(f"Bot bejelentkezett: {client.user}")
# SIS/TR(session based information sending/transmitting and receiving)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
# !help parancs kezelése/működése
    if message.content.lower() == "!help":
        help_text = (
            "**Elérhető parancsok:**\n"
            "'!help' - Parancsok listája\n"
            "'!list' - Spielerek listázása\n"
            "'!lol <név>' - Adott spieler lol stats lekérése\n" 
        )
        await message.channel.send(help_text)
        return
    
    if message.content == "!list":
        list = "**Spielerek listája:**\n"
        for name in players.keys():
            list += f"- {name}\n"
        await message.channel.send(list)
        return   

# !lol parancs kezelése/működése
    if message.content.startswith("!lol"):
        parts = message.content.split(" ")

        if len(parts) < 2:
            await message.channel.send("Használat: !lol <név>")
            return

        name = parts[1]

        if name not in players:
            await message.channel.send("Nincs ilyen játékos a listában.")
            return

        gameName, tagLine = players[name]
        data = get_summoner_info(gameName, tagLine)

        await message.channel.send(
            f"**{name}** → {data['gameName']}#{data['tagLine']} – Level {data['level']}"
        )
        return
    
# ismeretlen parancs kezelése/működése
    if message.content.startswith("!"):
        help_text = (
            "**Ismeretlen parancs.**\n"
            "Használd a '!help'-et a parancsok listájához.\n\n"
        )
        await message.channel.send(help_text)
        return
   
# Üres üzenet vagy hiányzó paraméter kezelése/bullshit
    help_text = (
    "**Ismeretlen parancs vagy üzenet vagy hiányzó paraméter.**\n"
    "Használd a '!help'-et a parancsok listájához.\n\n"
    )  
    await message.channel.send(help_text) 
    return    
    
# Indítás
client.run("Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")