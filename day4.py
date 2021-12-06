import attr 
from typing import Counter, List

@attr.s(auto_attribs=True)
class BingoBoard:
    board: List[List[int]] = attr.Factory(list)
    _counter: List[List[bool]] = attr.Factory(list)

    @classmethod
    def from_raw_lines(cls, lines: List[str]):
        rows = []
        for line in lines:
            rows.append([int(x) for x in line.split()])
            if len(rows[-1]) != 5:
                raise ValueError(f"{rows[-1]=} was not correctly length")
        
        c = []
        for i in range(5):
            c.append([False]*5)
        return cls(rows, c)

    def tick_board(self, value: int):
        breaker = False
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == value:
                    self._counter[i][j] = True
                    breaker = True
                    break
            if breaker:
                break
    
    def get_sum(self) -> int:
        total = 0
        for i in range(5):
            for j in range(5):
                if not self._counter[i][j]:
                    total += self.board[i][j]
        return total
                

    def check_win(self) -> bool:
        win = False
        transposed_counter = list(zip(*self._counter))
        for i in range(5):
            if all(self._counter[i]) or all(transposed_counter[i]):
                win = True
                break
        return win

if __name__ == "__main__":
    boards = []
    with open("data/day4.txt") as f:
        seq = next(f)
        seq = [int(x) for x in seq.replace("\n", "").split(",")]
        _ = next(f)

        raw_lines = []
        for line in f:
            if line == "\n":
                boards.append(BingoBoard.from_raw_lines(raw_lines))
                raw_lines = []
            else:
                raw_lines.append(line.replace("\n", ""))
        
    breaker = False
    for s in seq:
        winners = []
        print(f"{s=}")
        # board.tick_board(s)
        # if board.check_win():
        #     print(f"Board {i} is the winner!")
        #     break
        for i, board in enumerate(boards):
            board.tick_board(s)
            if board.check_win():
                print(f"board: {i} won")
                winners.append(i)
                if len(boards) == 1:
                    print(f"Ans: {board.get_sum()*s}")
                    breaker = True
                    break
        if breaker:
            break

        # Remove winners
        for w in reversed(winners):
            boards.pop(w)

        print(f"{len(boards)} remaining")



