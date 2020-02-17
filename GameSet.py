from const_messages import SIGN_UP_HERE_MSG


class GameSet:
    def __init__(self):
        self.director = None
        self.forWinner = None
        self.signUpMsg = None
        self.bracket = None
        pass

    async def create_sign_up_msg(self, client, react, user):
        mentionPlayers = client.usefulRoles['playerRole'].mention
        msg = SIGN_UP_HERE_MSG.format(mentionPlayers, user.mention, react.emoji, react.emoji)
        signUpMsg = await client.usefulChannels['signUpChan'].send(msg)
        await signUpMsg.add_reaction(client.signUpEmoji)
        return signUpMsg

    async def create(self, client, Director, forWinner):
        self.director = Director
        self.forWinner = forWinner
        self.bracket = None
        await self.init_set(client)
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
            await self.director.send('You are already active.')
            raise Exception("Director already active")
        await self.director.add_roles(client.usefulRoles["organizingRole"])

    async def init_set(self, client):
        self.init_bracket(client)
        await self.init_director(client)

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

    async def add_player(self, player):
        if self.is_player_already_in_a_bracket(player):
            return
        if self.is_bracket_full():
            return
        await player.add_roles(self.bracket)
