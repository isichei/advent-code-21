import attr 

@attr.s(auto_attribs=True)
class Submarine:
    horizon: int = 0
    depth: int = 0
    aim: int = 0

    def forward(self, x:int):
        self.horizon += x
        self.depth += self.aim * x

    def down(self, x:int):
        self.aim += x

    def up(self, x:int):
        self.aim -= x

if __name__ == "__main__":
    yellow = Submarine()

    with open("data/day2.txt") as f:
        for line in f:
            command, value = line.split()
            getattr(yellow, command)(int(value))
        
    print(f"{yellow.horizon=}")
    print(f"{yellow.depth=}")
    print(f"Answer: {yellow.horizon*yellow.depth}")
