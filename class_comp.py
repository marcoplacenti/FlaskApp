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

def check_exact_result(player_data, res_data, scores):
    for k in player_data.keys():
        if player_data[k] == res_data[k]:
            scores['score'] += 10
            scores['correct_result'] += 1
    return scores

def check_correct_draw(player_data, res_data, scores):

    for k in player_data.keys():
        if player_data[k] != res_data[k]:
            if sum([a_i - b_i for a_i, b_i in zip(player_data[k], res_data[k])]) == 0:
                scores['score'] += 7
                scores['correct_draw'] += 1
    return scores

def check_correct_winner(player_data, res_data, scores):
    for k in player_data.keys():
        diff_player = player_data[k][0] - player_data[k][1]
        diff_real = res_data[k][0] - res_data[k][1]
        if (diff_player > 0 and diff_real > 0) or (diff_player < 0 and diff_real < 0):
            scores['score'] += 5
            scores['correct_winner'] += 1
    return scores

def check_correct_goals(player_data, res_data, scores):
    for k in player_data.keys():
        flag = True
        for value, idx in enumerate(player_data[k]):
            if (player_data[k] != res_data[k]) and (player_data[k][idx] == res_data[k][idx]) and flag:
                flag = False
                scores['score'] += 2
                scores['correct_goals'] += 1
    return scores

def compute_player_score(player, round, res_path, scores):
    try:
        player_data = get_dict("static/preds/"+player+"Giornata"+str(round)+".txt", player, round)
    except FileNotFoundError:
        return scores

    res_data = get_dict(res_path, player, round)

    scores = check_exact_result(player_data, res_data, scores)
    scores = check_correct_draw(player_data, res_data, scores)
    scores = check_correct_winner(player_data, res_data, scores)
    scores = check_correct_goals(player_data, res_data, scores)

    return scores

def compute_scores():
    scores = {}
    scores['Giuseppe'] = {"score": 0, "correct_result":0, "correct_draw": 0, "correct_winner": 0, "correct_goals": 0}
    scores['Marco'] = {"score": 0, "correct_result":0, "correct_draw": 0, "correct_winner": 0, "correct_goals": 0}
    scores['Alessio'] = {"score": 0, "correct_result":0, "correct_draw": 0, "correct_winner": 0, "correct_goals": 0}

    rounds = [i+1 for i in range(7)] 
    for r in rounds: 
        r_path = Path("static/preds/RisultatiGiornata"+str(r)+".txt")
        if r_path.is_file():
            for player in scores.keys():
                temp = compute_player_score(player, r, r_path, scores[player])
                for k in temp.keys():
                    scores[player][k] = temp[k]

    return scores