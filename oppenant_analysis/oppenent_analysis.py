from Match_recuperation.Data_Parse import *
from Graphic_build.coord_managing import *
from Graphic_build.heatmap import *

def gunround_analysis(player_name, map_select,side = 't',frame = 7,text = False, info = None):
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    prob_place = pd.DataFrame()
    for num_match in range(len(list_match)):

        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][frame][side]['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15

        place = pd.DataFrame(index=['position_match' + str(num_match)])
        for player_id in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]) - 1):
            try:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]["players"][player_id][
                    'lastPlaceName']] += 1
            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]["players"][player_id][
                    'lastPlaceName']] = 1

        dataframe_position_final = get_coord_dataframe(map_select, list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]["players"], 'x', 'y',text,info)
        dataframe_grenade = get_coord_dataframe(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY", text, ["grenadeType","throwerSide"])
        prob_place = pd.concat([place, prob_place]).fillna(0)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    print(dataframe_grenade)
    plot_map_list_of_game(dataframe_position_final, map_select,text = False)
    plot_map_list_of_game(dataframe_grenade, map_select, text)


    return prob_place

def coordonate_analysis_any_round(dic_list,map_select,x,y,text = False, info= None):
    dataframe_position_final = get_coord_dataframe(map_select,dic_list, x, y,text,info)
    plot_map_list_of_game(dataframe_position_final, map_select,text)
    return dataframe_position_final


