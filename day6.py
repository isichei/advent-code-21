import attr
from typing import Optional, List
from collections import deque

@attr.s(auto_attribs=True)
class FishCounter:
    max_counter: int = attr.ib(default=6)
    young_age: int = attr.ib(default=2)
    fish_counter_array: Optional[deque] = attr.ib(default=None)

    @classmethod
    def from_fish_counters_list(cls, max_counter: int, young_age: int, fish_counters_list: List[int]):
        counter = [0] * (max_counter+young_age+1)
        for f in fish_counters_list:
            counter[f] += 1
        return cls(max_counter, young_age, deque(counter))

    def countdown(self):
        """
        The stack fish_counter_array which holds the total number of fish for that counter
        where the index = counter (aka element 0 has x amount of fish with a counter @ 0).
        Pop the left most element to the stack add that count to the i = self.max_counter
        and append that value to the right of the stack (total new number of fish).
        """
        resets = self.fish_counter_array.popleft()
        self.fish_counter_array[self.max_counter] += resets
        self.fish_counter_array.append(resets)


if __name__ == "__main__":
    with open("data/day6.txt") as f:
        raw_text = f.read()
    fish = [int(x) for x in raw_text.split(",")]
    fish_counter = FishCounter.from_fish_counters_list(6, 2, fish)
    for i in range(1, 256+1):
        fish_counter.countdown()
        print(f"After day {i}, {fish_counter.fish_counter_array}, ({sum(fish_counter.fish_counter_array)})")
