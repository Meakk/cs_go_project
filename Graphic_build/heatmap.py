from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt

def plot_map_list_of_game(dataframe_position,carte):
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