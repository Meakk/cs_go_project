import pandas as pd
import os


def pointx_to_resolutionx(xinput, map_of_games, resX=1024):
    df_map_adjustement = pd.read_csv("demo_csgo/map_adjustement/map_data.csv")
    startX = df_map_adjustement[df_map_adjustement["map"] == map_of_games][
        "StartX"
    ].values
    endX = df_map_adjustement[df_map_adjustement["map"] == map_of_games]["EndX"].values
    #   try:
    sizeX = endX - startX
    if startX < 0:
        xinput += startX * (-1.0)
    else:
        xinput += startX
    xoutput = float((xinput / abs(sizeX)) * resX)
    return xoutput


#   except:
#   print(xinput)


def pointy_to_resolutiony(yinput, map_of_games, resY=1024):
    df_map_adjustement = pd.read_csv("demo_csgo/map_adjustement/map_data.csv")
    startY = df_map_adjustement[df_map_adjustement["map"] == map_of_games][
        "StartY"
    ].values
    endY = df_map_adjustement[df_map_adjustement["map"] == map_of_games]["EndY"].values
    try:
        sizeY = endY - startY
        if startY < 0:
            yinput += startY * (-1.0)
        else:
            yinput += startY
        youtput = float((yinput / abs(sizeY)) * resY)

        return resY - youtput
    except:
        print(yinput)


def get_coord_dataframe(map_select, dic_list, x, y, dataframe_position_final):
    for element in dic_list:
        X = element[x]
        Y = element[y]
        dataframe_position_final = position_coordinate(
            dataframe_position_final, map_select, X, Y
        )
    return dataframe_position_final


def position_coordinate(
    dataframe_position_final, map, names, x, y, z, information=None
):
    x_correct = pointx_to_resolutionx(x, map)
    y_correct = pointy_to_resolutiony(y, map)
    dataframe_position = pd.DataFrame(
        [[x_correct, y_correct, z]], columns=["x", "y", "z"]
    )
    if information != None:
        dataframe_position = pd.DataFrame(
            [[x_correct, y_correct, z, information, names]],
            columns=["x", "y", "z", "info", "name"],
        )
    dataframe_position_final = pd.concat(
        [dataframe_position_final, dataframe_position], ignore_index=True
    )
    return dataframe_position_final.reset_index(drop=True)


def get_coord_dataframe_with_info(
    map_select, dic_list, x, y, z, dataframe_position_final, clock, round_num, info=None
):
    for element in dic_list:
        information = []
        X = element[x]
        Y = element[y]
        Z = element[z]
        names = element["name"]
        for i in info:
            information.append(element[i])
        information.append(clock)
        information.append(round_num)
        information_str = ",".join(str(e) for e in information)
        dataframe_position_final = position_coordinate(
            dataframe_position_final, map_select, names, X, Y, Z, information_str
        )
    return dataframe_position_final
