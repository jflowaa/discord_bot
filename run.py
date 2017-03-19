#!/usr/bin/env python
import discord
import asyncio
import settings

from plugins import GuessingGame
from bot_logic import track_word_count, get_word_stats, get_stats_for_word, get_count_for_author
from database import wipe_database


client = discord.Client()
guessing_game = GuessingGame()


@client.event
async def on_ready():
    print("[+] Connected!")
    print("[*] Username: {}".format(client.user.name))
    print("[*] User ID: {}".format(client.user.id))


@client.event
async def on_message(message):
    if message.content.startswith("!guess"):
        await client.send_message(message.channel, guessing_game.get_starting_message())
        if not guessing_game.is_game_active():
            guessing_game.start_game(message.channel)
            start_game(run_game())
    elif message.content.startswith("!statsme"):
        get_word_stats(message.author.id)
        await client.send_file(message.channel, settings.WORD_COUNT_CHART_FILENAME)
    elif message.content.startswith("!statsall"):
        get_word_stats()
        await client.send_file(message.channel, settings.WORD_COUNT_CHART_FILENAME)
    elif message.content.startswith("!statsword"):
        word = message.content.replace("!statsword", "").split()
        if len(word) == 1 and not word[0].isdigit():
            message_content = get_stats_for_word(word[0])
            await client.send_message(message.channel, message_content)
        else:
            await client.send_message(message.channel, "Improper usage: !statsword *word*")
    elif message.content.startswith("!statsperson"):
        mentions = message.mentions
        if len(mentions) == 1:
            get_count_for_author(mentions[0].id)
            await client.send_file(message.channel, settings.WORD_COUNT_CHART_FILENAME)
        else:
            await client.send_message(message.channel, "Improper usage: !statsperson @person")
    elif message.content.startswith("!statsclear"):
        wipe_database()
    elif guessing_game.is_game_active and message.content.isdigit():
        guessing_game.add_guess(message)
    else:
        if message.author.display_name != "Cacabot" and not message.content.isdigit():
            track_word_count(message.author.id, message.content.split())


def start_game(target, *, loop=None):
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop=loop)


async def run_game():
    await asyncio.sleep(settings.GUESSING_GAME_LENGTH)
    guessing_game.end_game()
    await client.send_message(guessing_game.game_channel, guessing_game.check_for_winner())


@asyncio.coroutine
def run():
    yield from client.login(settings.DISCORD_TOKEN)
    yield from client.connect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()
