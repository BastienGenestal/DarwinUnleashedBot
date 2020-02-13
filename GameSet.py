
class GameSet:
    def __init__(self, client, Director, forWinner, signUpMsg):
        self.director = Director
        self.forWinner = forWinner
        self.signUpMsg = signUpMsg
        self.bracket = None
        for role in client.BracketRoles:
            if not len(role.members):
                self.bracket = role
                break
        if not self.bracket:
            print("No Free Bracket")
            raise Exception("No Free Bracket")


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
