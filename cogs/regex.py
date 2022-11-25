import math

import discord
from discord.ext import commands


tracks = {}


class regex(commands.Cog):

    def __init__(self, Client):
        self.Client = Client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.id in tracks.keys():
            tracks[before.id].append(after.embeds[0].description)

    @commands.command()
    async def regex(self, ctx):
        if ctx.message.reference is not None:
            msg_id = ctx.message.reference.message_id
            replay = await ctx.channel.fetch_message(msg_id)
            s = replay.embeds[0].description
            if msg_id not in tracks.keys():
                tracks[msg_id] = [s]
            await ctx.send(view=RowButtons(msg_id))


class RowButtons(discord.ui.View):
    def __init__(self, msg_id):
        self.msgs = tracks[msg_id]
        self.page = 0
        self.fr = 0
        self.to = 0
        self.page_total = 0
        self.embed = discord.Embed(
            description=self.regex(self.msgs[self.page]),
            color=0xE91E63,
        )
        super().__init__(timeout=60.0)

    def regex(self, msg):
        s = msg.replace('**', '').replace('​\n', '')
        inp = s.splitlines()
        temp2 = ''
        for i in inp:
            if not i or 'Page ' and ' / ' in i or 'Total value: ' in i or ':kakera:\r' in i or '\u200b' in i \
                    or 'Top 15 value: ' in i or 'AVG: ' in i or '🏆 TOP ' in i and ' TOP 1000' in i \
                    or ' $wa, ' in i and ' $ha, ' in i and ' $wg, ' in i and ' $hg' in i and '(' not in i and ')' \
                    not in i or ' wishlist (' in i and ')' in i:
                inp = inp[+1:]
                continue
            elif i[0] == '$':
                inp = s
                return inp
            temp = i
            if temp[0] == '#':
                temp = i.split(' - ')[1]
            temp = \
                temp.split(' · ')[0].replace('💞', '').replace('✅', '').replace('⭐', '').replace('🔐',
                                                                                                '').replace(
                    '❌', '').replace('🚫', '').replace(':kakera:', '').strip().split('  ')[0].split(' 🚫 ')[
                    0].split(
                    '(Soulkeys: ')[0].split(
                    ' - Touhou')[0].split(' | ')[0].split(' => ')[0].split(' ⚠')[0]
            if temp[len(temp) - 3:] == ' ka' or ' (' in i and ')' in i or ' - Touhou' in i:
                if temp.count(' - ') > 1:
                    temp = temp.split(' - ')[0] + ' - ' + temp.split(' - ')[1]
                else:
                    temp = temp.split(' - ')[0]
            if temp[len(temp) - 3:] == ' ka':
                remove_num = temp[:len(temp) - 3]
                while remove_num[len(remove_num) - 1].isnumeric():
                    remove_num = remove_num[:-1]
                temp = remove_num
            # DL Making Below and t flag without rank
            remove_dl = temp
            if remove_dl[len(remove_dl) - 1] == ')':
                remove_dl = remove_dl[:-1]
                while remove_dl[len(remove_dl) - 1].isnumeric() or remove_dl[len(remove_dl) - 1] == '(':
                    remove_dl = remove_dl[:-1]
                    if not remove_dl[len(remove_dl) - 1].isnumeric() or remove_dl[len(remove_dl) - 1] != '(':
                        break
                if remove_dl[len(remove_dl) - 3:] == '$hg':
                    remove_dl = remove_dl.split(' ~ ')[0]
                while remove_dl[len(remove_dl) - 1].isnumeric() or remove_dl[len(remove_dl) - 1] == '(' and \
                        remove_dl[
                            len(remove_dl) - 2] == ' ':
                    remove_dl = remove_dl[:-1]
                    temp = remove_dl
            # DL Making Above ^
            if inp[0] == i:
                temp2 = temp2 + temp + ''
            else:
                temp2 = temp2.strip() + " $" + temp + ''
        temp2 = temp2.rstrip('\n')
        return temp2

    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, inter: discord.Interaction, button: discord.ui.Button):
        if self.to <= len(self.msgs) - 1:
            self.page += 1
            self.to += 8
            self.fr = self.to - 8
            self.page_total = math.ceil(len(self.msgs)/8)
            description = self.regex('\n'.join(self.msgs[self.fr:self.to]))
            count = len(description.split('$'))
            self.embed.description = f"Total number of characters: {count}\n```\n{description}\n```"
            self.embed.set_footer(text=f'Page {self.page} / {self.page_total}')
            await inter.response.edit_message(embed=self.embed)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green)
    async def previous(self, inter: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            self.fr -= 8
            self.to -= 8
            self.page_total = math.ceil(len(self.msgs)/8)
            description = self.regex('\n'.join(self.msgs[self.fr:self.to]))
            count = len(description.split('$'))
            self.embed.description = f"Total number of characters: {count}\n```\n{description}\n```"
            self.embed.set_footer(text=f'Page {self.page} / {self.page_total}')
            await inter.response.edit_message(embed=self.embed)


async def setup(Client):
    await Client.add_cog(regex(Client))
