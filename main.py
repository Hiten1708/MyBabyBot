
import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()
my_secret = os.environ['TOKEN']
sad_words = ["dejected", "depressed", "despondent", "down", "droopy", "hangdog", "inconsolable", "low", "melancholic", "melancholy", "mirthless", "sad", "unhappy", "woebegone", "woeful", "dim", "discomfiting", "discouraging", "disheartening", "dismaying", "dispiriting", "distressful", "distressing", "upsetting", "desperate", "hopeless", "pessimistic", "lamentable", "mournful", "plaintive", "sorrowful", "colorless", "drab", "dull", "dour"," grim", "lowering (also louring)", "lowery (also loury)"," menacing", "negative", "oppressive", "threatening"]
encouraging_words = ["Cheer up!", "Hang in there!", "You are a great person/bot!"]




def get_quotes():
  response = requests.get('https://animechan.vercel.app/api/quotes')
  json_data = json.loads(response.text)
  quote = f" `{json_data[0]['quote']}` - *{json_data[0]['character']} ({json_data[0]['anime']})*"
  return quote

def add_words(words):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(words)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [words]

def del_words(index):
  encouragements = db["encouragements"]
  if len( encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print(f"I am ON - {client.user}")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
    
  if msg.startswith("$inspire"):
    await message.channel.send(get_quotes())

  options = encouraging_words
  if "encouragements" in db.keys():
    options = options.extend(db["encouragements"])
  
  if any(word in message.content for word in sad_words):
    await message.channel.send("random.choice(options)")

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    add_words(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragments = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ", 1)[1])
      del_words(index)
      encouragments = db["encouragements"].value
    await message.channel.send(encouragments)
      
      
client.run(my_secret)