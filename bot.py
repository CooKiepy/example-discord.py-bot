import discord
import random
import asyncio
from discord.ext import commands
from itertools import cycle

bot = commands.Bot(command_prefix = '.')
TOKEN = open("TOKEN.TXT", "r").read()

@bot.event
async def on_ready():
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')

#ping

@bot.command()
async def ping(ctx):
    """Pings the bot."""
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

#ping

#help

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot", description="Commands:", color=0xA121FF)

    embed.add_field(
        name=".help", value="Gives this message.", inline=False)
    embed.add_field(
        name=".ping", value="Pings the bot.", inline=False)
    embed.add_field(
        name=".8ball", value="Gives responses like an 8ball.", inline=False)
    embed.add_field(
        name=".kick", value="Kicks a member.", inline=False)
    embed.add_field(
        name=".ban", value="Bans a member.", inline=False)

    await ctx.send(embed=embed)

#help

#8ball


@bot.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    """Gives responses like an 8ball. (You can use _8ball, 8ball, or eightball to activate the command.)"""
    responses = ['It is certain',
                 'It is decidebly so.',
                 'Without a doubt',
                 'Yes - definetely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to write the question after the command.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Give an intiger.")

    raise error

#8ball

#clear


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clears the amount of messages that you filled in."""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} messages got deleted.")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify an amount.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Give an intiger.")

    raise error

#clear

#kick


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member."""
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

#kick

#ban


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member."""
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

#ban

#unban


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#unban

#background tasks

async def chng_pr():
    await bot.wait_until_ready()

    statuses = [".help", ".ping", ".kick", ".ban", ".clear", ".8ball"]
    statuses = cycle(statuses)

    while not bot.is_closed():
        status = next(statuses)

        await bot.change_presence(activity=discord.Game(status))

        await asyncio.sleep(5)

bot.loop.create_task(chng_pr())


async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the permission to perform that command.")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("The command is not found")

    raise error

#background tasks

bot.run(TOKEN)
