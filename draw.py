# %%
# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.art3d as art3d

def create_polygon(zipped_list, ax, dict_color):
    lst_pt = zipped_list[0]
    color = np.random.rand(3,) if (not zipped_list[1]) else dict_color[zipped_list[1]]
    if(len(lst_pt) == 1):
        list_solo_x, list_solo_y, list_solo_z = [lst_pt[0][0]], [lst_pt[0][1]], [lst_pt[0][2]]
        ax.plot(list_solo_x, list_solo_y, list_solo_z, marker='o', linestyle="none",color=color)
    elif(len(lst_pt) == 2):
        ax.add_collection3d(art3d.Line3DCollection([lst_pt],color=color))
    else:
        ax.add_collection3d(art3d.Poly3DCollection([lst_pt],facecolors=color,edgecolors="black", linewidths=1,linestyle="-",  alpha=0.5))

def create_line(zipped_list, ax, dict_color):
    lst_pt = zipped_list[0]
    color = np.random.rand(3,) if (not zipped_list[1]) else dict_color[zipped_list[1]]
    if(len(lst_pt) == 1):
        list_solo_x, list_solo_y, list_solo_z = [lst_pt[0][0]], [lst_pt[0][1]], [lst_pt[0][2]]
        ax.plot(list_solo_x, list_solo_y, list_solo_z, marker='o', linestyle="none",color=color)
    else:
        ax.add_collection3d(art3d.Line3DCollection([lst_pt],color=color))

def parse_line(data_each):
    return list(map(lambda x: x.replace("\n", ""), 
           list(map(lambda x: x.replace(" ",""), data_each.split(",")))))
    

def get_line_2D(list_fig_data):
    lineType = ""
    if(not list_fig_data[0].replace(".","").replace("-","").isnumeric()):
        lineType = list_fig_data.pop(0)
        
    def pop_first(list_T, list_Tar):
        list_T.append(float(list_Tar.pop(0)))
        return list_T
    #TODO:ダイレクションのラッパー
    def add_list(x, y, z, direc, list_):
        if(not list_): 
            return None
        elif(direc==0): add_list(pop_first(x, list_), y , z, (direc+1)%3, list_)
        elif(direc==1): add_list(x, pop_first(y, list_) , z, (direc+1)%3, list_)
        elif(direc==2): add_list(x, y , pop_first(z, list_), (direc+1)%3, list_)
    
    list_x = []
    list_y = []
    list_z = []
    add_list(list_x, list_y, list_z, 0, list_fig_data)
    return [list(zip(list_x, list_y, list_z)),lineType]

def define_color_dict(list_type):
    dictionary = {}
    for _ , list_ind in list_type:
        dictionary.setdefault(list_ind, np.random.rand(3,)) 
    return dictionary

def get_limit(list_, get_, fir):
    res_x = res_y = res_z = fir
    for list_param, _ in list_:
        for list_param_each in list_param:
            res_x = get_(res_x, list_param_each[0])
            res_y = get_(res_y, list_param_each[1])
            res_z = get_(res_z, list_param_each[2])
    return [res_x, res_y, res_z]

#fig = plt.figure(figsize=plt.figaspect(1))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d',aspect='equal')

#mode別の関数辞書
dict_mode = {"line": create_line, "polygon": create_polygon}

file = open('data.txt', 'r')
mode= file.readline().replace("\n", "")
datas_all = file.readlines()
list_fig = list(map(get_line_2D, list(map(parse_line, datas_all))))
#print(list_fig)
dict_color = define_color_dict(list_fig)
for list_ in list_fig:
    dict_mode[mode](list_, ax, dict_color)
    #create_line(list_, ax,dict_color)

[xmin, ymin, zmin] = get_limit(list_fig, min, float('inf'))
[xmax, ymax, zmax] = get_limit(list_fig, max, -float('inf'))

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()

# %%

# %%
