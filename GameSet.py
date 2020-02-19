import asyncio

from const_messages import SIGN_UP_HERE_MSG
import datetime

class GameSet:
    def __init__(self):
        self.director = None
        self.forWinner = None
        self.signUpMsg = None
        self.bracket = None
        self.timeStartedSignUps = None
        self.timeStartedGame = None
        self.cancelled = False

        self.isFull = False

        self.task = None
        pass

    async def create_sign_up_msg(self, client):
        if self.forWinner:
            emoji = client.usefulBasicEmotes['signUpWinner']
        else:
            emoji = client.usefulBasicEmotes['signUpNoWinner']
        mentionPlayers = client.usefulRoles['playerRole'].mention
        msg = SIGN_UP_HERE_MSG.format(mentionPlayers, self.director.mention, emoji, emoji)
        self.signUpMsg = await client.usefulChannels['signUpChan'].send(msg)
        self.timeStartedSignUps = datetime.datetime.now().time()
        await self.signUpMsg.add_reaction(client.signUpEmoji)

    async def create(self, client, Director, forWinner):
        self.director = Director
        self.forWinner = forWinner
        self.bracket = None
        await self.init_set(client)
        self.task = asyncio.create_task(
            self.delay_before_sign_up_ends(1, client)
        )
        return self

    async def delay_before_sign_up_ends(self, minutes, client):
        await asyncio.sleep(minutes * 60)
        await self.sign_up_ends(client, '{} minutes passed.'.format(minutes))

    def init_bracket(self, client):
        for role in client.BracketRoles:
            if not len(client.BracketRoles[role].members):
                self.bracket = client.BracketRoles[role]
                break
        if not self.bracket:
            raise Exception("No Free Bracket")

    async def init_director(self, client):
        if self.director in client.usefulRoles["organizingRole"].members:
            await self.director.send('You are already directing a set.')
            raise Exception("Director already active")
        await self.director.add_roles(client.usefulRoles["organizingRole"])

    async def cancel(self, client):
        await self.director.send("Set cancelled")
        await self.director.remove_roles(client.usefulRoles['organizingRole'])

    async def sign_up_ends(self, client, why):
        if self.signUpMsg:
            await self.signUpMsg.delete()
            self.signUpMsg = None
            await client.usefulChannels['startASetChan'].send(
                '{} Players joined\n'
                '{}\n'
                'The set should start now.'.format(len(self.bracket.members), why))

    async def await_task(self):
        return await self.task

    async def init_set(self, client):
        self.init_bracket(client)
        await self.init_director(client)
        await self.create_sign_up_msg(client)

    async def complete(self, client):
        await self.sign_up_ends(client, '{} is full.'.format(self.bracket.name))

    @staticmethod
    def is_player_already_in_a_bracket(player):
        for role in player.roles:
            if "Bracket" in role.name:
                return True
        return False

    def is_bracket_full(self):
        if not self.bracket:
            return True
        return len(self.bracket.members) > 9

    async def add_player(self, client, player):
        if self.is_player_already_in_a_bracket(player):
            return
        if self.is_bracket_full():
            return
        await player.add_roles(client.usefulRoles['activeRole'], self.bracket)
        self.isFull = len(self.bracket.members) >= client.MAX_NB_PLAYER_PER_GAME

    async def remove_player(self, client, player):
        await player.remove_roles(client.usefulRoles['activeRole'], self.bracket)
        self.isFull = len(self.bracket.members) >= client.MAX_NB_PLAYER_PER_GAME

