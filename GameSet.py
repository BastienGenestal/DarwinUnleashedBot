class GameSet:
    def __init__(self, client, Director, forWinner, signUpMsg):
        self.director = Director
        self.forWinner = forWinner
        self.signUpMsg = signUpMsg
        self.bracket = None
        self.init_set(client)

    def init_bracket(self, client):
        for role in client.BracketRoles:
            if not len(client.BracketRoles[role].members):
                self.bracket = client.BracketRoles[role]
                break
        if not self.bracket:
            raise Exception("No Free Bracket")

    def init_director(self, client):
        if self.director in client.usefulRoles["organizingRole"].members:
            raise Exception("Director already active")

    def init_set(self, client):
        self.init_bracket(client)
        self.init_director(client)

    def is_player_already_in_a_bracket(self, player):
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
