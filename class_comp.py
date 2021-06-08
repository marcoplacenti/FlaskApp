from pathlib import Path

def get_dict(file, player, round):
    with open(file) as f:
        player_data = {}
        for line in f:
            line = line.strip().replace(' ', '-').split("-")
            line[-1] = int(line[-1])
            line[-2] = int(line[-2])
            player_data[line[0]+line[1]] = [line[2], line[3]]
    
    return player_data

def check_exact_result(player_data, res_data):
    p = 0
    for k in player_data.keys():
        if player_data[k] == res_data[k]:
            p += 10
    return p

def check_correct_draw(player_data, res_data):
    p = 0
    for k in player_data.keys():
        if player_data[k] != res_data[k]:
            if sum([a_i - b_i for a_i, b_i in zip(player_data[k], res_data[k])]) == 0:
                p += 7
    return p

def check_correct_winner(player_data, res_data):
    p = 0
    for k in player_data.keys():
        diff_player = player_data[k][0] - player_data[k][1]
        diff_real = res_data[k][0] - res_data[k][1]
        if (diff_player > 0 and diff_real > 0) or (diff_player < 0 and diff_real < 0):
            p += 5 
    return p

def check_correct_goals(player_data, res_data):
    p = 0
    for k in player_data.keys():
        if player_data[k] != res_data[k]:
            flag = True
            for value, idx in enumerate(player_data[k]):
                if flag:
                    if player_data[k][idx] == res_data[k][idx]:
                        flag = False
                        p += 2
    return p

def compute_player_score(player, round, res_path):
    accumulator = 0
    try:
        player_data = get_dict("static/preds/"+player+"Giornata"+str(round)+".txt", player, round)
    except FileNotFoundError:
        return -100

    res_data = get_dict(res_path, player, round)

    accumulator += check_exact_result(player_data, res_data)
    accumulator += check_correct_draw(player_data, res_data)
    accumulator += check_correct_winner(player_data, res_data)
    accumulator += check_correct_goals(player_data, res_data)

    return accumulator

def compute_scores():
    scores = {}
    scores['Giuseppe'] = 0
    scores['Marco'] = 0
    scores['Alessio'] = 0

    rounds = [i+1 for i in range(7)] 
    for r in rounds: 
        r_path = Path("static/preds/RisultatiGiornata"+str(r)+".txt")
        if r_path.is_file():
            for k in scores.keys():
                scores[k] += compute_player_score(k, r, r_path)
                
    return scores