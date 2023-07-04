from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from adjustText import adjust_text
from io import BytesIO
import base64
from matplotlib.patches import Rectangle

def plot_map_list_of_game(dataframe_position,carte,frame,text = False,nb_games = 4,premade = [],color_set = "Round_id"):
    try:
        loop_len = dataframe_position['Round_id'].max() + 1
    except:
        loop_len = nb_games
    if premade != []:
        dataframe_position = dataframe_position[dataframe_position['name'].isin(premade)].reset_index()
        color_set = "Match_ID"
        loop_len = nb_games
    if not dataframe_position.empty:
        plt.ioff() # DISABLE GRAPH SHOW
        map_bg = plt.imread("demo_csgo/map_adjustement/"+carte+".png")
        plt.figure()
        fig, ax = plt.subplots(figsize=(15, 15))
        color = ['blue','orange','green','red','purple','black','pink','brown','cyan','olive','gray','darkred','teal','navy','white','lime','aquamarine','indigo','darkolivegreen','beige','thistle','fuchsia','coral']
        ax.set_title('Plot position')
        for i in range(0,loop_len,1):
            ax.scatter(
                            [dataframe_position['x'][((dataframe_position[color_set]==i) & (dataframe_position['Bombsite']=='A'))]],
                            [dataframe_position['y'][((dataframe_position[color_set]==i)& (dataframe_position['Bombsite']=='A'))]],
                            color=color[i],
                                alpha=1,
                                zorder=3,
                                cmap='hot',
                                marker = '+'
                            )
            ax.scatter(
                            [dataframe_position['x'][((dataframe_position[color_set]==i) & (dataframe_position['Bombsite']=='B'))]],
                            [dataframe_position['y'][((dataframe_position[color_set]==i)& (dataframe_position['Bombsite']=='B'))]],
                            color=color[i],
                                alpha=1,
                                zorder=3,
                                cmap='hot',
                            )
        hb = ax.hexbin(x=[dataframe_position['x']],y= [dataframe_position['y']], gridsize=6,mincnt=0.01,alpha=0.5)
        ax.imshow(map_bg,zorder=0)
    
        if text:
            texts = [plt.text(dataframe_position['x'][i], dataframe_position['y'][i], str(dataframe_position['info'][i]), fontsize=7,
                    color="white") for i in range(len(dataframe_position))]
            adjust_text(texts)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad = 1)
        cb = fig.colorbar(hb, ax=ax, cax=cax)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        plt.savefig(fname = f'./demo_csgo/img/img_{frame}.png',transparent = False,
                    facecolor = 'white')
        
        plt.show()
        return base64.b64encode(buf.getbuffer()).decode("ascii")
    else :
        print(dataframe_position,"nothing in df")
        return 1
    
def plot_from_df(dataframe_position,carte):
        
        plt.figure()
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.set_title('Plot position')
        ax.scatter(
                            [dataframe_position['x'][dataframe_position['side_A']==True]],
                            [dataframe_position['y'][dataframe_position['side_A']==True]],
                                alpha=1,
                                zorder=3,
                                cmap='hot',
                                marker = '+'
                            )
        ax.scatter(
                        [dataframe_position['x'][dataframe_position['side_A']==False]],
                        [dataframe_position['y'][dataframe_position['side_A']==False]],
                            alpha=1,
                            zorder=3,
                            cmap='hot',
                            )
        
        map_bg = plt.imread("demo_csgo/map_adjustement/"+carte+".png")
       # plt.plot([690, 690], [760, 900], 'k-', lw=2)
       # plt.plot([530, 530], [400, 560], 'k-', lw=2,color = "red")
       # plt.plot([0, 530], [400, 400], 'k-', lw=2,color = "red")
       # plt.plot([0, 530], [560, 560], 'k-', lw=2,color = "red")
       # plt.plot([500, 800], [500, 540], 'k-', lw=2)
       
       #df['push_mid_inferno'] = (df['x'] < 650) & (df['y'] < 750) & (df['y'] > 600)
       
        ax.imshow(map_bg,zorder=0)
        
        plt.show()


def plot_from_simple_df(dataframe_position, carte):
    plt.figure()
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title('Plot position')
    ax.scatter(
        [dataframe_position['x']],
        [dataframe_position['y']],
        alpha=1,
        zorder=3,
        cmap='hot'
    )

    map_bg = plt.imread("demo_csgo/map_adjustement/" + carte + ".png")
    hb = ax.hexbin(x=[dataframe_position['x']], y=[dataframe_position['y']], gridsize=6, mincnt=0.01, alpha=0.5)
    ax.imshow(map_bg, zorder=0)
    texts = [
        plt.text(dataframe_position['x'][i], dataframe_position['y'][i], str(dataframe_position['player'][i]) +','+ str(dataframe_position['clock'][i])
                 +','+str(dataframe_position['weapon'][i]), fontsize=7,
                 color="white") for i in range(len(dataframe_position))]
    adjust_text(texts)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=1)
    cb = fig.colorbar(hb, ax=ax, cax=cax)
    buf = BytesIO()
    # plt.plot([690, 690], [760, 900], 'k-', lw=2)
    # plt.plot([530, 530], [400, 560], 'k-', lw=2,color = "red")
    # plt.plot([0, 530], [400, 400], 'k-', lw=2,color = "red")
    # plt.plot([0, 530], [560, 560], 'k-', lw=2,color = "red")
    # plt.plot([500, 800], [500, 540], 'k-', lw=2)

    # df['push_mid_inferno'] = (df['x'] < 650) & (df['y'] < 750) & (df['y'] > 600)

    ax.imshow(map_bg, zorder=0)

    plt.show()
    
        