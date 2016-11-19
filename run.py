#!/usr/bin/env python
import discord
import bot_logic
import asyncio
import configparser
import os


client = discord.Client()
config = configparser.ConfigParser()
config.readfp(open("settings.ini"))
bot_logic = bot_logic.BotLogic()


@client.event
async def on_ready():
    print("[+] Connected!")
    print("[*] Username: {}".format(client.user.name))
    print("[*] User ID: {}".format(client.user.id))


@client.event
async def on_message(message):
    if message.content.startswith("!guess"):
        await client.send_message(message.channel, "Guessing game started!")
        await client.send_message(message.channel, "Say a number in chat between 1 and {}".format(config["bot_settings"]["max_guess"]))
        await client.send_message(message.channel, "The game will end in {} seconds".format(config["bot_settings"]["game_length_seconds"]))
        if not bot_logic.is_game_active():
            bot_logic.start_game(message.channel)
            start_game(run_game())
    elif message.content.startswith("!statme"):
        await client.send_file(message.channel, bot_logic.get_word_stats(message.author.display_name))
    elif message.content.startswith("!statall"):
        await client.send_file(message.channel, bot_logic.get_word_stats())
    elif message.content.startswith("!statword"):
        word = message.content.replace("!statword", "").split()
        if len(word) == 1 and not word[0].isdigit():
            await client.send_message(message.channel, str(bot_logic.get_stats_for_word(word[0])))
        else:
            await client.send_message(message.channel, "Improper useage: !statword *word*")
    elif message.content.startswith("!wipedb"):
        bot_logic.db_wipe()
    elif bot_logic.is_game_active and message.content.isdigit():
        bot_logic.add_guess(message)
    else:
        if message.author.display_name != "cacabot" and not (message.content).isdigit():
            bot_logic.track_word_count(message)


def start_game(target, *, loop=None):
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop=loop)


async def run_game():
    await asyncio.sleep(game_length_seconds)
    bot_logic.end_game()
    await client.send_message(bot_logic.game_channel, bot_logic.check_for_winner())


def read_config_file():
    config.read("settings.ini")


@asyncio.coroutine
def run():
    yield from client.login(os.environ["cacabot_email"], os.environ["cacabot_password"])
    yield from client.connect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()
