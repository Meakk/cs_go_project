from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from adjustText import adjust_text
from io import BytesIO
import base64
from matplotlib.patches import Rectangle

def plot_map_list_of_game(dataframe_position,carte,text = False,nb_games = 4):
    map_bg = plt.imread("demo_csgo/map_adjustement/"+carte+".png")
    plt.figure()
    fig, ax = plt.subplots(figsize=(15, 15))
    color = ['blue','orange','green','red','purple','black','pink','brown','cyan','olive','gray','darkred','teal']
    ax.set_title('Plot position')
    for i in range(nb_games):
        ax.scatter(
                        [dataframe_position['x'][((dataframe_position['Match_ID']==i) & (dataframe_position['Bombsite']=='A'))]],
                        [dataframe_position['y'][((dataframe_position['Match_ID']==i)& (dataframe_position['Bombsite']=='A'))]],
                        color=color[i],
                            alpha=1,
                            zorder=3,
                            cmap='hot',
                            marker = '+'
                        )
        ax.scatter(
                        [dataframe_position['x'][((dataframe_position['Match_ID']==i) & (dataframe_position['Bombsite']=='B'))]],
                        [dataframe_position['y'][((dataframe_position['Match_ID']==i)& (dataframe_position['Bombsite']=='B'))]],
                        color=color[i],
                            alpha=1,
                            zorder=3,
                            cmap='hot',
                        )
    hb = ax.hexbin(x=[dataframe_position['x']],y= [dataframe_position['y']], gridsize=6,mincnt=0.01,alpha=0.5)
    ax.imshow(map_bg,zorder=0)
   
    if text:
        texts = [plt.text(dataframe_position['x'][i], dataframe_position['y'][i], str(dataframe_position['info'][i]), fontsize=10,
                 color="white") for i in range(len(dataframe_position))]
        adjust_text(texts)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad = 1)
    cb = fig.colorbar(hb, ax=ax, cax=cax)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")

