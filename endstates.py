from itertools import combinations

from utils import *

def gen_end_states(n=5, m=4):
    cells = [str(i)+str(j) for j in range(1,m+1) for i in range(1,n+1)]
    winning_combinations = [comb for comb in combinations(cells, 4) if is_winning(comb)]

    end_states = []

    for white in winning_combinations:
        reduced_cells = [c for c in cells if c not in white]
        for black in combinations(reduced_cells, 4):
            if black not in winning_combinations:
                end_states.append("".join(white) + "".join(black) + "b")

    for i in range(len(end_states)):
        end_states.append(end_states[i][8:-1] + end_states[i][:8] + "w")

    return end_states