#from Match_recuperation.Data_Parse import *
from .Graphic_build.coord_managing import *
from .Graphic_build.heatmap import *
from .Graphic_build.vectorization import coordonee_bomb_site
from .Graphic_build.vectorization import distance_point
import json
import re
import numpy as np
import os


def read_all_csgo_match_of_one_map_json(map_wanted):
    list_match=[]
    print("map_wanted :",map_wanted)
    for root, dirs, files in os.walk("demo_csgo/DataBase/"+map_wanted):
        for filename in files:
            pattern = "(.*?).json"
            filename = re.search(pattern, filename).group(1)
            print(filename)
            with open("demo_csgo/DataBase/"+map_wanted+"/"+filename+".json") as file:
                data=json.load(file)
                list_match.append(data)
    return list_match

def gunround_analysis(player_name, map_select,list_match, side = 't',frame = 7):
    print("test")
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])
    dataframe_grenade = pd.DataFrame(columns=['x', 'y', "info"])
    bombsite = []
   #list_match = read_all_csgo_match_of_one_map_json(map_select)
    kit = 0
    prob_place = pd.DataFrame()
    cpt = 0
    list_cpt = []
    for num_match in range(len(list_match)):

        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][frame][side]['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15
                
        bombsiteA,bombsiteB = coordonee_bomb_site(list_match[0])
        bomb = [list_match[num_match]["gameRounds"][round_t]["frames"][-1]['bomb']['x'],
                    list_match[num_match]["gameRounds"][round_t]["frames"][-1]['bomb']['y']]
        distA = distance_point(bomb, bombsiteA)
        distB = distance_point(bomb, bombsiteB)
        if distA <= distB:
            for i in range(5):
                bombsite.append('A')
                list_cpt.append(cpt)
            cpt += 1
        else :
            for i in range(5):
                bombsite.append('B')
                list_cpt.append(cpt)
            cpt += 1
            
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
    dataframe_position_final['Bombsite'] = bombsite
    dataframe_position_final['Match_ID'] = list_cpt
    dataframe_grenade['Bombsite'] = len(dataframe_grenade)*[None]
    dataframe_grenade['Match_ID'] = len(dataframe_grenade)*[None]
    data_player = plot_map_list_of_game(dataframe_position_final, map_select,text = True, nb_games = len(list_match))
   # if not dataframe_grenade.empty:
     #   data_grenade = plot_map_list_of_game(dataframe_grenade, map_select, text = True,nb_games = len(list_match))

    return prob_place

def grenade_analysis(dic_list,map_select,x,y,text = False, info= None):
    dataframe_position_final = get_coord_dataframe(map_select,dic_list, x, y,text,info)
    plot_map_list_of_game(dataframe_position_final, map_select,text)
    return dataframe_position_final

def fav_bomb_site_analysis(player_name,list_match, map_select,side = 't',frame = -1):
    #list_match = read_all_csgo_match_of_one_map_json(map_select)
    
    bombsiteA,bombsiteB = coordonee_bomb_site(list_match[0])

    round_time_before_plant_Full_Eco = []
    round_time_before_plant_Semi_Eco = []
    round_time_before_plant_Semi_Buy = []
    round_time_before_plant_Full_Buy = []
    round_time_before_plant_pistol = []

    Full_Eco_a = 0
    Semi_Eco_a = 0
    Semi_Buy_a = 0
    Full_Buy_a = 0
    Full_Eco_b = 0
    Semi_Eco_b = 0
    Semi_Buy_b = 0
    Full_Buy_b = 0

    ct_Full_Eco_a = 0
    ct_Full_Eco_b = 0
    
    pistol_t_b = 0
    pistol_t_a = 0

    for num_match in range(len(list_match)):
        round_t = 0
        for i in range(len(list_match[num_match]["gameRounds"][round_t]["frames"][frame][side]['players'])):
            if list_match[num_match]["gameRounds"][0]["frames"][frame][side]['players'][i]["name"] == player_name:
                round_t = 0
                break
            else:
                round_t = 15
        for round in range(round_t, int(round_t * len(list_match[num_match]["gameRounds"]) / 15 + 15 - round_t)):
            buy_type = list_match[num_match]["gameRounds"][round]['tBuyType']
            ct_buy_type = list_match[num_match]["gameRounds"][round]['ctBuyType']
            bomb = [list_match[num_match]["gameRounds"][round]["frames"][frame]['bomb']['x'],
                    list_match[num_match]["gameRounds"][round]["frames"][frame]['bomb']['y']]
            distA = distance_point(bomb, bombsiteA)
            distB = distance_point(bomb, bombsiteB)
            
            if distA <= distB:
                if buy_type == "Full Eco":
                    Full_Eco_a += 1
                if buy_type == "Semi Eco":
                    Semi_Eco_a += 1
                if buy_type == "Semi Buy":
                    Semi_Buy_a += 1
                if buy_type == "Full Buy":
                    Full_Buy_a += 1

                if ct_buy_type == "Semi Eco":
                    ct_Full_Eco_a += 1
                if ct_buy_type == "Full Eco":
                    ct_Full_Eco_a += 1
                    
                if ((round == 15)|(round == 0)):
                    pistol_t_a +=1

            if distB < distA:
                if buy_type == "Full Eco":
                    Full_Eco_b += 1
                if buy_type == "Semi Eco":
                    Semi_Eco_b += 1
                if buy_type == "Semi Buy":
                    Semi_Buy_b += 1
                if buy_type == "Full Buy":
                    Full_Buy_b += 1

                if ct_buy_type == "Semi Eco":
                    ct_Full_Eco_b += 1
                if ct_buy_type == "Full Eco":
                    ct_Full_Eco_b += 1
                    
                if ((round == 15)|(round == 0)):
                    pistol_t_b +=1
                
            
            # mean time round
            if ((round == 15)|(round == 0)):
                round_duration = list_match[num_match]["gameRounds"][round]['frames'][-1]['seconds']
                for i in list_match[num_match]["gameRounds"][round]['bombEvents']:
                    if i["bombAction"] == "plant":
                        round_duration = i['seconds']
                        break
                round_time_before_plant_pistol.append(round_duration)
                
            if buy_type == "Full Eco":
                round_duration = list_match[num_match]["gameRounds"][round]['frames'][-1]['seconds']
                for i in list_match[num_match]["gameRounds"][round]['bombEvents']:
                    if i["bombAction"] == "plant":
                        round_duration = i['seconds']
                        break
                round_time_before_plant_Full_Eco.append(round_duration)
            if buy_type == "Semi Eco":
                round_duration = list_match[num_match]["gameRounds"][round]['frames'][-1]['seconds']
                for i in list_match[num_match]["gameRounds"][round]['bombEvents']:
                    if i["bombAction"] == "plant":
                        round_duration = i['seconds']
                        break
                round_time_before_plant_Semi_Eco.append(round_duration)
            if buy_type == "Semi Buy":
                round_duration = list_match[num_match]["gameRounds"][round]['frames'][-1]['seconds']
                for i in list_match[num_match]["gameRounds"][round]['bombEvents']:
                    if i["bombAction"] == "plant":
                        round_duration = i['seconds']
                        break
                round_time_before_plant_Semi_Buy.append(round_duration)
            if buy_type == "Full Buy":
                round_duration = list_match[num_match]["gameRounds"][round]['frames'][-1]['seconds']
                for i in list_match[num_match]["gameRounds"][round]['bombEvents']:
                    if i["bombAction"] == "plant":
                        round_duration = i['seconds']
                        break
                round_time_before_plant_Full_Buy.append(round_duration)

    round_time_before_plant_Full_Eco = np.array(round_time_before_plant_Full_Eco)
    round_time_before_plant_Semi_Eco = np.array(round_time_before_plant_Semi_Eco)
    round_time_before_plant_Semi_Buy = np.array(round_time_before_plant_Semi_Buy)
    round_time_before_plant_Full_Buy = np.array(round_time_before_plant_Full_Buy)
    round_time_before_plant_pistol = np.array(round_time_before_plant_pistol)
    
    data = pd.DataFrame(index= ["Full_eco_T","Semi_eco_T","Semi_buy_T","Full_buy_T","CT_in_Eco","Pistol_rounds"],
                        columns = ["prob_go_A","prob_go_B","Mean_Sec_Round_before_plant(s)","Med_Sec_Round_before_plant(s)"
                                   ,"std_Sec_Round_before_plant","nb_sample"],
                        data = ([[Full_Eco_a / (Full_Eco_a + Full_Eco_b),Full_Eco_b / (Full_Eco_a + Full_Eco_b),round_time_before_plant_Full_Eco.mean(),np.median(round_time_before_plant_Full_Eco),
          round_time_before_plant_Full_Eco.std(), len(round_time_before_plant_Full_Eco)],
                                         [Semi_Eco_a / (Semi_Eco_a + Semi_Eco_b), Semi_Eco_b / (Semi_Eco_a + Semi_Eco_b), round_time_before_plant_Semi_Eco.mean(), np.median(round_time_before_plant_Semi_Eco),
          round_time_before_plant_Semi_Eco.std(), len(round_time_before_plant_Semi_Eco)],
                                         [Semi_Buy_a / (Semi_Buy_a + Semi_Buy_b),Semi_Buy_b / (Semi_Buy_a + Semi_Buy_b), round_time_before_plant_Semi_Buy.mean(), np.median(round_time_before_plant_Semi_Buy),
          round_time_before_plant_Semi_Buy.std(), len(round_time_before_plant_Semi_Buy)],
                                         [Full_Buy_a / (Full_Buy_a + Full_Buy_b),Full_Buy_b / (Full_Buy_a + Full_Buy_b),round_time_before_plant_Full_Buy.mean(), np.median(round_time_before_plant_Full_Buy),
          round_time_before_plant_Full_Buy.std(), len(round_time_before_plant_Full_Buy)],
                                         [ct_Full_Eco_a / (ct_Full_Eco_a + ct_Full_Eco_b),ct_Full_Eco_b / (ct_Full_Eco_a + ct_Full_Eco_b)],
                                         [pistol_t_a / (pistol_t_a + pistol_t_b),pistol_t_b / (pistol_t_a + pistol_t_b),round_time_before_plant_pistol.mean(), np.median(round_time_before_plant_pistol),
          round_time_before_plant_pistol.std(), len(round_time_before_plant_pistol)]]))
    return data
