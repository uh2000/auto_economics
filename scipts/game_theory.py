import pandas as pd

class Game:

    def __init__(self, player_1: dict, player_2: dict) -> None:
        self.player_1 = player_1
        self.player_2 = player_2

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def find_nash_equilibriums(self):
        cc = (self.player_1["cooperate-cooporate"], self.player_2["cooperate-cooporate"])
        cd = (self.player_1["cooperate-defect"], self.player_2["cooperate-defect"])
        dc = (self.player_1["defect-cooporate"], self.player_2["defect-cooporate"])
        dd = (self.player_1["defect-defect"], self.player_2["defect-defect"])

        nash_equilibriums = []

        if cc[0] >= cd[0] and cc[1] >= cd[1]:
            nash_equilibriums.append(("Cooperate", "Cooperate"))
        if cd[1] >= cc[1] and cd[0] >= cc[0]:
            nash_equilibriums.append(("Cooperate", "Defect"))
        if dc[0] >= cc[0] and dc[1] >= cc[1]:
            nash_equilibriums.append(("Defect", "Cooperate"))
        if dd[0] >= cd[0] and dd[1] >= cd[1]:
            nash_equilibriums.append(("Defect", "Defect"))

        return nash_equilibriums

    def print_game_matrix(self) -> None:
        matrix = pd.DataFrame([
            [self.player_1["cooperate-cooporate"], self.player_1["cooperate-defect"]],
            [self.player_1["defect-cooporate"], self.player_1["defect-defect"]]
        ], columns=["Cooperate", "Defect"], index=["Cooperate", "Defect"])

        
        matrix = matrix.astype(str) + ", " + pd.DataFrame([
            [self.player_2["cooperate-cooporate"], self.player_2["cooperate-defect"]],
            [self.player_2["defect-cooporate"], self.player_2["defect-defect"]]
        ], columns=["Cooperate", "Defect"], index=["Cooperate", "Defect"]).astype(str)

        print(matrix)

if __name__ == "__main__":
    player_1 = {
        "cooperate-cooporate": 0,
        "cooperate-defect": 0,
        "defect-cooporate": 0,
        "defect-defect": 0
    }
    player_2 = {
        "cooperate-cooporate": 3,
        "cooperate-defect": 5,
        "defect-cooporate": 0,
        "defect-defect": 1
    }
    game = Game(player_1, player_2)
    game.print_game_matrix()
    nash_equilibriums = game.find_nash_equilibriums()
    print("Nash Equilibriums:", nash_equilibriums)