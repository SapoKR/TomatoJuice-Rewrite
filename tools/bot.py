import json
import sys

import discord
import koreanbots
from discord.ext import commands

from tools.ui import selectview

try:
    with open("config.json", 'r+') as f:
        config = json.load(f)
except Exception as E:
    print(f"Error: {E}")
    sys.exit(-1)
colortmp = config['color']

class Juice(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config['prefixs'],
            intents=discord.Intents.all(),
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True
        )
        self.config = config
        if not self.config['koreanbot_token']:
            self.kb = koreanbots.Koreanbots(
                self,
                self.config['koreanbot_token'],
                run_task=True,
            )

            self.color = discord.Color.from_rgb(colortmp[0], colortmp[1], colortmp[2]),

    async def on_message(self, message):
        if not await check_User(message.author):
            embed = discord.Embed(
                title=f'{self.user.name}를 사용하시려면 아래의 약관에 동의를 하셔야해요!',
                description='봇 명령어의 내용이 일부 수집될수 있습니다.\n사용자의 아이디가 유저 DB에 등록됩니다.',
                color=self.color
            )
            view = selectview(message.author, [await load_text(message.author, 'yes'), await load_text(message.author, 'no')])
            msg = await message.channel.send(embed=embed, view=view)
            await view.wait()
            if view.value == 'yes':
                post = {'_id': message.author.id,
                        'money': 0,
                        'other': {},
                        'locate': 'en_US',
                        }
                await users.insert_one(post)
                processed = await load_text(message.author, 'registeruser')
            elif view.value == 'no':
                processed = await load_text(message.author, 'cancel')
            else:
                processed = await load_text(message.author, 'timeout')

            return msg.edit(content=processed, embed=None, view=None)