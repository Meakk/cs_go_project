from Match_recuperation.Data_Parse import *
from Graphic_build.coord_managing import *
from Graphic_build.heatmap import *

def gunround_analysis(player_name, map_select,side = 't',frame = 7):
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])
    dataframe_grenade = pd.DataFrame(columns=['x', 'y', "info"])
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    kit = 0
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
                if (side == "ct") & (list_match[num_match]["gameRounds"][round_t]["frames"][frame]["ct"]["players"][player_id]['hasDefuse']) & (kit<=num_match):
                    kit += 1
            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]["players"][player_id][
                    'lastPlaceName']] = 1
                if (side == "ct") & (list_match[num_match]["gameRounds"][round_t]["frames"][frame]["ct"]["players"][player_id]['hasDefuse'])& (kit<=num_match):
                    kit += 1

        dataframe_position_final = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]["players"], 'x', 'y',dataframe_position_final,["name"])
        dataframe_grenade = get_coord_dataframe_with_info(map_select, list_match[num_match]["gameRounds"][round_t]['grenades'], "grenadeX", "grenadeY",dataframe_grenade, ["grenadeType",'throwClockTime',"throwerSide"])
        prob_place = pd.concat([place, prob_place]).fillna(0)

    if side == "ct":
        print("Kit prob :",kit)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    if side == 't':
        SIDE = 'T'
    else:
        SIDE = 'CT'
    dataframe_grenade = dataframe_grenade[pd.Series([(","+SIDE in e) for e in dataframe_grenade['info']])].reset_index(drop=True)
    plot_map_list_of_game(dataframe_position_final, map_select,text = True)
    plot_map_list_of_game(dataframe_grenade, map_select, text = True)

    return prob_place

def grenade_analysis(dic_list,map_select,x,y,text = False, info= None):
    dataframe_position_final = get_coord_dataframe(map_select,dic_list, x, y,text,info)
    plot_map_list_of_game(dataframe_position_final, map_select,text)
    return dataframe_position_final

def fav_bomb_site_analysis(player_name, map_select,side = 't',frame = -1):
    list_match = read_all_csgo_match_of_one_map_json(map_select)
    bombsiteA,bombsiteB = vectorization.coordonee_bomb_site(list_match[0])
    a=0
    b=0
    for num_match in range(len(list_match)):

        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][frame][side]['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15
        for round in range(round_t,int(round_t*len(list_match[num_match]["gameRounds"])/15 + 15-round_t )):
            bomb = [list_match[num_match]["gameRounds"][round]["frames"][frame]['bomb']['x'],list_match[num_match]["gameRounds"][round]["frames"][frame]['bomb']['y']]
            distA = vectorization.distance_point(bomb, bombsiteA)
            distB = vectorization.distance_point(bomb, bombsiteB)
            if distA <= distB:
                a+=1
            if distB < distA :
                b+=1
    return "prob A :" + str(a/(a+b)) + ", prob B :" + str(b/(a+b))



