import pickle

def clean_states(full_states, player_color, remove_losing_states=True):
    with open(full_states, 'rb') as f:
        state_list = pickle.load(f)
    player_value = 1 if player_color == 'w' else -1
    for k in list(state_list.keys()):
        if k[-1] == player_color:
            del state_list[k]
        elif remove_losing_states and state_list[k] != 0 and \
                state_list[k] != 100 * player_value and state_list[k] != 'D':
            del state_list[k]
    return state_list

if __name__ == "__main__":
    white_winning_states = clean_states("game_states.pkl", 'w', False)
    with open('white_winning_states.pkl', 'wb') as f:
        pickle.dump(dict(white_winning_states), f)

    black_winning_states = clean_states("game_states.pkl", 'b', False)
    with open('black_winning_states.pkl', 'wb') as f:
        pickle.dump(dict(black_winning_states), f)