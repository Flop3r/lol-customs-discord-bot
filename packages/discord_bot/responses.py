import discord

# COMMANDS
HELLO_RESPONSE = "✨🔔🎵 ･ﾟ✧:･.⋆♫⋆｡♪ ₊˚☾˚｡･ﾟ✧:･.🎵🔔✨"
PONG_RESPONSE = "**PONG!** 🏓"
SET_RIOT_ID_RESPONSE = "**Ups! 😟** Wygląda na to, że podałeś nieprawidłowe **Riot ID**.\nSprawdź, czy używasz formatu: **<nick>#<tag>!** 🔍"
INVALID_ARGUMENT_RESPONSE = "Hmm, coś poszło nie tak z tym argumentem: {}.\nSpróbuj ponownie używając: **set riot_id <wartość>** 🔄"
MISSING_ARGUMENTS_RESPONSE = "Za mało argumentów. Użyj: **{}** ⚠️"
ERROR_RESPONSE = "**Ups! 😟 Wystąpił błąd:** {} ❌"

RIOT_ID_RESPONSE_TEMPLATE = "Riot ID przypisane do twojego profilu to: **{}**! 🌐"

# GAME
RIOT_ID_CHANGED_RESPONSE = "Zmieniłeś swoje Riot ID na: **{}#{}** 🎮"
INVALID_PLAYER_RESPONSE = "**Ten gracz nie istnieje.** Sprawdź poprawność wprowadzonych danych. ❓"

FILE_ERROR_RESPONSE = "Ups! 😟Coś poszło nie tak podczas odczytu pliku: {} 📂"
SAVING_FILE_ERROR_RESPONSE = "Ups! 😟 Wystąpił problem podczas zapisywania zmian do pliku. Spróbuj ponownie. 🔄"

# Helper functions
def embedded_response(response, title=None, color=None, thumbnail=None, image=None, author=None, footer=None):
    embed = discord.Embed(
        colour=color if color else discord.Colour.yellow(),
        description=response
    )
    if title:
        embed.title = title
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    if author:
        embed.set_author(name=author.get('name', ''), icon_url=author.get('icon_url', ''))
    if footer:
        embed.set_footer(text=footer.get('text', ''), icon_url=footer.get('icon_url', ''))
    return embed

async def embed_reply(message, text="", title=None, color=None, thumbnail=None, image=None, author=None, footer=None):
    embed = embedded_response(text, title, color, thumbnail, image, author, footer)
    await message.reply(embed=embed, mention_author=False)


