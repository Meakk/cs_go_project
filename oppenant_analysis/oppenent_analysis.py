from Match_recuperation.Data_Parse import *
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

def gunround_T_analysis(player_name, map_select):
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])
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

                dataframe_position_final = position_coordonate(list_match, num_match, round_t, player_id,
                                                               dataframe_position_final,"t",map_select)

            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['t']["players"][player_id][
                    'lastPlaceName']] = 1

                dataframe_position_final = position_coordonate(list_match, num_match, round_t, player_id,
                                                               dataframe_position_final,"t",map_select)

        prob_place = pd.concat([place, prob_place]).fillna(0)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    return prob_place, dataframe_position_final


def gunround_CT_analysis(player_name,map_select):
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])
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
                dataframe_position_final = position_coordonate(list_match, num_match, round_t, player_id,
                                                               dataframe_position_final,"ct",map_select)
            except:
                place[list_match[num_match]["gameRounds"][round_t]["frames"][7]['ct']["players"][player_id][
                    'lastPlaceName']] = 1
                dataframe_position_final = position_coordonate(list_match, num_match, round_t, player_id,
                                                               dataframe_position_final,"ct",map_select)

        prob_place = pd.concat([place, prob_place]).fillna(0)

    prob_place = prob_place.groupby(prob_place.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'records'})
    prob_place['prob'] = prob_place['records'] / len(list_match)
    prob_place = prob_place.drop('records', axis=1)
    return prob_place, dataframe_position_final


def position_coordonate(list_match,num_match,round_t,player_id,dataframe_position_final,side,map):
    x = list_match[num_match]["gameRounds"][round_t]["frames"][7][side]["players"][player_id]['x']
    y = list_match[num_match]["gameRounds"][round_t]["frames"][7][side]["players"][player_id]['y']
    x_correct = pointx_to_resolutionx(x,map)
    y_correct = pointy_to_resolutiony(y,map)
    dataframe_position = pd.DataFrame([[x_correct,y_correct]],columns=['x','y'])
    return  dataframe_position_final.append(dataframe_position).reset_index(drop=True)


def plot_map(dataframe_position,carte,couleur='red'):
    map_bg = plt.imread("C:/Users/thibault/cs_go_project/map_adjustement/"+carte+".PNG")
    plt.figure()
    fig, ax = plt.subplots(figsize=(15, 15))
    color = ['blue','red','green','orange']
    ax.set_title('Plot position')
    for i in range(4):
        ax.scatter(
                        [dataframe_position['x'][4*i:4*i+4]],
                        [dataframe_position['y'][4*i:4*i+4]],
                        color=color[i],
                            alpha=1,
                            zorder=1,
                            cmap='hot'
                        )
    hb = ax.hexbin(x=[dataframe_position['x']],y= [dataframe_position['y']], gridsize=10,mincnt=0.01,alpha=0.5)
    ax.imshow(map_bg,zorder=0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad = 1)
    cb = fig.colorbar(hb, ax=ax, cax=cax)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("left", size="5%", pad = 1)
    cb = fig.colorbar(hb, ax=ax, cax=cax)


def pointx_to_resolutionx(xinput,map_of_games,resX=1024):
    df_map_adjustement = pd.read_csv ("C:/Users/thibault/cs_go_project/map_adjustement/map_data.csv")
    startX=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["StartX"].values
    endX=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["EndX"].values
    try:
        sizeX=endX-startX
        if startX < 0:
            xinput += startX *(-1.0)
        else:
            xinput += startX
        xoutput = float((xinput / abs(sizeX)) * resX)
        return xoutput
    except:
        print(xinput)

def pointy_to_resolutiony(yinput,map_of_games,resY=1024):
    df_map_adjustement = pd.read_csv ("C:/Users/thibault/cs_go_project/map_adjustement/map_data.csv")
    startY=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["StartY"].values
    endY=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["EndY"].values
    try:
        sizeY=endY-startY
        if startY < 0:
            yinput += startY *(-1.0)
        else:
            yinput += startY
        youtput = float((yinput / abs(sizeY)) * resY)

        return resY-youtput
    except:
        print(yinput)