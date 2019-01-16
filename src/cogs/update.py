"""
Dynamic cogs for a bot named Nolka
"""

from libs import Macro, Messages
from discord.ext import commands

#TODO Refresh command to load and unload a cog

class Update:
    def __init__(self, bot):
        self.bot = bot

    def _load(self, *args):
        """
        Private method for loading cogs
        """
        for arg in args:
            try:
                self.bot.load_extension(arg)
                yield True
            except ModuleNotFoundError:
                yield False

    def _unload(self, *args):
        """
        Private method for unloading cogs
        """
        for arg in args:
            self.bot.unload_extension(arg)

    @commands.group(pass_context = True, aliases = ["extension", "package"])
    @commands.check(Macro.snakeEater)
    async def cog(self, ctx):
        """
        Group for loading, unloading, and modifying command groups
        """
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.noSubcommand)
            )

    @cog.command(pass_context = True, aliases = ["add"])
    async def load(self, ctx, *args):
        """
        Load cogs for Nolka to use if they exist
        Takes a list of cogs, and requires at least one cog
        """
        if len(args) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        #TODO: use a generator to do this in one statement
        success = []
        failure = []
        index = 0
        for status in self._load(*args):
            success.append(args[index]) if status else failure.append(args[index])
            index += 1
        if success:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.cogsLoaded.format(", ".join(success)))
            )
        if failure:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.cogsNotLoaded.format(", ".join(failure)))
            )

    @cog.command(pass_context = True)
    async def unload(self, ctx, *args):
        """
        Unload cogs for Nolka to use if they are loaded
        Takes a lsit of cogs, and requires at least one loaded cog
        """
        if len(args) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        #TODO: use a generator here too
        self._unload(*args)
        await ctx.channel.send(
            embed = await Macro.Embed.message(Messages.cogsUnloaded.format(", ".join(args)))
        )

    # TODO: have no arguments reload all cogs
    @cog.command(pass_context = True)
    async def reload(self, ctx, *args):
        """
        Unload and load cogs for Nolka to update
        Takes a list of cogs, and requires at least one cog
        """
        if len(args) is 0:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.missingArgs)
            )
            return
        failure = []
        success = []
        index = 0
        self._unload(*args)
        for status in self._load(*args):
            success.append(args[index]) if status else failure.append(args[index])
        if success:
            await ctx.channel.send(
                embed = await Macro.Embed.message(Messages.cogsReloaded.format(", ".join(success)))
            )
        if failure:
            await ctx.channel.send(
                embed = await Macro.Embed.error(Messages.cogsNotLoaded.format(", ".join(failure)))
            )

def setup(bot):
    bot.add_cog(Update(bot))