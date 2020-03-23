import asyncio
import inspect

from const_messages import SIGN_UP_HERE_MSG
from const import MINUTES_TO_END_SET, MINUTES_TO_SIGN_UP

class GameSet:
    def __init__(self):
        self.director = None
        self.forWinner = None
        self.signUpMsg = None
        self.bracket = None

        self.last_fun_code_public_msg = None

        self.forFun = True
        self.isFull = False
        self.task = None
        self.endTask = None
        pass

    async def create_sign_up_msg(self, client):
        if self.forWinner:
            emoji = client.usefulBasicEmotes['signUpWinner']
        else:
            emoji = client.usefulBasicEmotes['signUpNoWinner']
        mentionPlayers = client.usefulRoles['playerRole'].mention
        msg = SIGN_UP_HERE_MSG.format(mentionPlayers, self.director.mention, emoji, emoji)
        self.signUpMsg = await client.usefulChannels['signUpChan'].send(msg)
        await self.signUpMsg.add_reaction(client.usefulBasicEmotes['signUp'])

    async def call_this_in(self, func, args, time):
        await asyncio.sleep(time)
        if inspect.iscoroutinefunction(func):
            return await func(args)
        return func(args)

    async def create(self, client, Director, forWinner):
        self.director = Director
        self.forWinner = forWinner
        self.bracket = None
        await self.init_set(client)
        args = client, '{} minutes passed.'.format(MINUTES_TO_SIGN_UP)
        self.task = client.loop.create_task(self.call_this_in(self.sign_up_ends, args, MINUTES_TO_SIGN_UP*60))
        self.endTask = client.loop.create_task(self.call_this_in(self.end, client, MINUTES_TO_END_SET*60))
        return self

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

    async def sign_up_ends(self, *args):
        if type(args[0]) == tuple:
            client, why = args[0][0], args[0][1]
        else:
            client, why = args[0], args[1]
        if self.signUpMsg:
            await self.signUpMsg.delete()
            self.signUpMsg = None
            await client.usefulChannels['startSetChan'].send(
                '{} Players joined\n'
                '{}\n'
                'The set should start now.'.format(len(self.bracket.members), why))


    async def init_set(self, client):
        self.init_bracket(client)
        await self.init_director(client)
        await self.create_sign_up_msg(client)

    async def complete(self, client):
        self.task.cancel()
        args = client, '{} is full.'.format(self.bracket.name)
        await self.sign_up_ends(args)

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
        try:
            await player.add_roles(client.usefulRoles['activeRole'], self.bracket)
        except Exception as e:
            print('Can not give role')
            print(e)
        self.isFull = len(self.bracket.members) >= client.MAX_NB_PLAYER_PER_GAME

    async def remove_player(self, client, player):
        await player.remove_roles(client.usefulRoles['activeRole'], self.bracket)
        self.isFull = len(self.bracket.members) >= client.MAX_NB_PLAYER_PER_GAME

    async def end(self, client):
        print("ENDING", self.bracket.name)
        for player in self.bracket.members:
            await player.remove_roles(client.usefulRoles['activeRole'], self.bracket)
        self.bracket = None
        self.isFull = False
        emoteToRemove = client.usefulBasicEmotes['signUpWinner' if self.forWinner else 'signUpNoWinner']
        try:
            await client.startASetMsg.remove_reaction(emoteToRemove, self.director.name)
        except:
            print('No reacion from {} on the start a set message.'.format(self.director.name))
        try:
            await self.director.remove_roles(client.usefulRoles['organizingRole'])
        except:
            print('No director role to remove from {}.'.format(self.director))
        self.director = None
        self.forWinner = None

        if self.signUpMsg:
            await self.signUpMsg.delete()
            self.signUpMsg = None
        if self.last_fun_code_public_msg:
            self.last_fun_code_public_msg.delete()
            self.last_fun_code_public_msg = None
        self.forFun = True
        if self.task and not self.task.cancelled:
            self.task.cancel()
        if self.endTask and not self.endTask.cancelled:
            self.endTask.cancel()
        client.Sets.remove(self)
