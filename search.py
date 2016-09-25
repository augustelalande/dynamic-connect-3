import pickle
from collections import defaultdict
from math import ceil
from sys import stdout
from time import clock

from endstates import gen_end_states
from utils import get_parents

full_start = clock()

print("generating end states...", end="")
stdout.flush()
start = clock()
end_states = gen_end_states()
print("{:,} end states found in {:.1f} secs".format(len(end_states), clock() - start))

game_states = defaultdict(lambda: 'U')
queued = {}

count = 0
steps = round(len(end_states) / 100)
start = clock()
for s in end_states:
    if count % steps == 0:
        stdout.write("\rappending end states...{:,} states appended in {:.1f} secs".format(len(game_states), clock() - start))
    value = 100 if s[-1] == 'b' else -100
    game_states[s] = value
    for p in get_parents(s):
        queued[p] = value
    count += 1
stdout.write("\rappending end states...{:,} states appended in {:.1f} secs\n".format(len(game_states), clock() - start))
print("{:,} states queued for analysis.".format(len(queued)))
print("appending immediatly winning states")
count = 0
steps = round(len(queued) / 100)
start = clock()
new_queued = {}
for k in queued.keys():
    if count % steps == 0:
        stdout.write("\rappending winning states...{:,} states appended in {:.1f} secs".format(count, clock() - start))
    game_states[k] = queued[k]
    for p in get_parents(k):
        new_queued[p] = 0
    count += 1
stdout.write("\rappending winning states...{:,} states appended in {:.1f} secs\n".format(len(game_states), clock() - start))
print("propagating state values through parent states...")

queued = new_queued
new_queued = defaultdict(lambda: 0)
iteration = 0
while queued:
    iteration += 1
    print("iteration {}: {:,} states queued".format(iteration, len(queued)))
    count = 0
    step = ceil(len(queued) / 100)
    start = clock()
    for label in queued.keys():
        if count % step == 0:
            stdout.write("\r{:,} states analysed in {:.1f} secs. {:,} states added to queue".format(count, clock() - start, len(new_queued)))
        count += 1
        current_val = game_states[label]
        queued_val = queued[label]
        if current_val == 100 or current_val == -100 or current_val == 'D':
            continue
        if label[-1] == 'w':
            if queued_val == 0 and current_val == 'U':
                game_states[label] = 0
                for p in get_parents(label):
                    new_queued[p] -= 1
            elif queued_val > 0 and current_val == 'U':
                game_states[label] = queued_val
                for p in get_parents(label):
                    new_queued[p] += 0
            elif queued_val > 0 and current_val == 0:
                game_states[label] = queued_val
                for p in get_parents(label):
                    new_queued[p] += 1
            elif queued_val > 0 and current_val > 0:
                game_states[label] += queued_val
            elif queued_val < 0 and current_val > 0:
                game_states[label] += queued_val
                if game_states[label] == 0:
                    for p in get_parents(label):
                        new_queued[p] -= 1
        else:
            if queued_val == 0 and current_val == 'U':
                game_states[label] = 0
                for p in get_parents(label):
                    new_queued[p] += 1
            elif queued_val < 0 and current_val == 'U':
                game_states[label] = queued_val
                for p in get_parents(label):
                    new_queued[p] += 0
            elif queued_val < 0 and current_val == 0:
                game_states[label] = queued_val
                for p in get_parents(label):
                    new_queued[p] -= 1
            elif queued_val < 0 and current_val < 0:
                game_states[label] += queued_val
            elif queued_val > 0 and current_val < 0:
                game_states[label] += queued_val
                if game_states[label] == 0:
                    for p in get_parents(label):
                        new_queued[p] += 1
        if iteration >= 26:
            game_states[label] = 'D'
            # for p in get_parents(label):
            #     if game_states[p] == 0:
            #         if p[-1] == 'w':
            #             new_queued[p] += 1
            #         else:
            #             new_queued[p] -= 1
    stdout.write("\r{:,} out of {:,} states analysed in {:.1f} secs. {:,} states added to queue\n".format(count, len(queued), clock() - start, len(new_queued)))
    queued = dict(new_queued)
    new_queued = defaultdict(lambda: 0)

print("storing game states to 'game_states.pkl'")
f = open('game_states.pkl', 'wb')
pickle.dump(dict(game_states), f)
f.close()

print("finished in {:.1f} secs = {:.1f} minutes".format(clock() - full_start, (clock() - full_start) / 60))