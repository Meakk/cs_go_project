from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

def plot_map_list_of_game(dataframe_position,carte,text = False):
    map_bg = plt.imread("C:/Users/thibault/cs_go_project/map_adjustement/"+carte+".PNG")
    plt.figure()
    fig, ax = plt.subplots(figsize=(15, 15))
    color = ['blue','red','green','orange']
    ax.set_title('Plot position')
    for i in range(4):
        ax.scatter(
                        [dataframe_position['x'][5*i:5*i+5]],
                        [dataframe_position['y'][5*i:5*i+5]],
                        color=color[i],
                            alpha=1,
                            zorder=1,
                            cmap='hot'
                        )
    hb = ax.hexbin(x=[dataframe_position['x']],y= [dataframe_position['y']], gridsize=10,mincnt=0.01,alpha=0.5)
    ax.imshow(map_bg,zorder=0)
    if text:
        for i in range(len(dataframe_position)):
            plt.text(dataframe_position['x'][i], dataframe_position['y'][i], str(dataframe_position['info'][i]), fontsize=10,
                 color="white")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad = 1)
    cb = fig.colorbar(hb, ax=ax, cax=cax)
