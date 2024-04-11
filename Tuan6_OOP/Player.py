class Player:
    team_name ="Inter Milan"
    def __init__(seft,name):
        seft.name = name
        
Player1=Player("Messi")
Player2=Player("Messi2")
players=[Player1,Player2]
for player in players:
    print(player.team_name,player.name)