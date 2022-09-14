from Match_recuperation.Data_Parse import *
import pandas as pd

def gunround_T_analysis(player_name,map_select):
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    prob_place = pd.DataFrame()
    for num_match in range(len(list_match)):

        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][7]['t']['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][7]['t']['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15

        place = pd.DataFrame(index=['position_match' + str(num_match)])
        for player_id in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][7]['t']) - 1):
            try:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['t']["players"][player_id][
                    'lastPlaceName']] += 1
            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['t']["players"][player_id][
                    'lastPlaceName']] = 1
        prob_place = pd.concat([place, prob_place]).fillna(0)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    return prob_place


def gunround_CT_analysis(player_name,map_select):
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    prob_place = pd.DataFrame()
    for num_match in range(len(list_match)):

        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][7]['ct']['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][7]['ct']['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15

        place = pd.DataFrame(index=['position_match' + str(num_match)])
        for player_id in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][7]['ct']) - 1):
            try:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['ct']["players"][player_id][
                    'lastPlaceName']] += 1
            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['ct']["players"][player_id][
                    'lastPlaceName']] = 1
        prob_place = pd.concat([place, prob_place]).fillna(0)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    return prob_place