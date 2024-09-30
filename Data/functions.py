import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from adjustText import adjust_text

def display_circles(pcs, n_comp, pca, axis_ranks, labels=None, label_rotation=0, lims=None):
    for d1, d2 in axis_ranks: # On affiche les 3 premiers plans factoriels, donc les 6 premières composantes
        if d2 < n_comp:

            # initialisation de la figure
            fig, ax = plt.subplots(figsize=(10,8))

            # détermination des limites du graphique
            if lims is not None :
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30 :
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else :
                xmin, xmax, ymin, ymax = min(pcs[d1,:]), max(pcs[d1,:]), min(pcs[d2,:]), max(pcs[d2,:])

            # affichage des flèches
            # s'il y a plus de 30 flèches, on n'affiche pas le triangle à leur extrémité
            if pcs.shape[1] < 30 :
                plt.quiver(np.zeros(pcs.shape[1]), np.zeros(pcs.shape[1]),
                   pcs[d1,:], pcs[d2,:], 
                   angles='xy', scale_units='xy', scale=1, color="grey", width =0.001)
                # (voir la doc : https://matplotlib.org/api/_as_gen/matplotlib.pyplot.quiver.html)
            else:
                lines = [[[0,0],[x,y]] for x,y in pcs[[d1,d2]].T]
                ax.add_collection(LineCollection(lines, axes=ax, alpha=.1, color='black'))
            
            # affichage des noms des variables  
            
            x_list=[]
            y_list=[]
            if labels is not None:  
                for i, (x, y) in enumerate(pcs[[d1, d2]].T):
                    stop=[]
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                        if len(x_list)>1:
                            for k in range(len(x_list)):
                                if abs(x-x_list[k]) < 0.03 and abs(y-y_list[k]) < 0.03 :
                                    stop.append("stop")
                                else :
                                    pass
                                    
                        x_list.append(x)
                        y_list.append(y)
                            
                        if len(stop)==0:
                            plt.text(x, y, labels[i], fontsize='9', ha='center', va='center', rotation=label_rotation, color="royalblue",alpha=1)
                            
            
            
            # affichage de l'inertie totale 
            
            plt.text(-0.95, 0.9, f"Inertie totale expliquée par F{d1+1} et F{d2+1} : {round(100*(pca.explained_variance_ratio_[d1]+pca.explained_variance_ratio_[d2]),2)}%", fontsize=11, color="dimgray")
            
            # affichage du cercle
            #circle = plt.Circle((0,0), 1, facecolor='none', edgecolor='grey')
            #plt.gca().add_artist(circle)

            # définition des limites du graphique
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        
            # affichage des lignes horizontales et verticales
            plt.plot([-1, 1], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-1, 1], color='grey', ls='--')

            # nom des axes, avec le pourcentage d'inertie expliqué
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)),fontweight="bold", alpha=0.7)
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)),fontweight="bold", alpha=0.7)

            plt.title(f"Cercle des corrélations (F{d1+1} et F{d2+1})", loc="center", fontsize=12)
            plt.show(block=False)
        
def display_factorial_planes(X_projected, n_comp, pca, axis_ranks, labels=None, alpha=1, illustrative_var=None, team=None):
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # initialisation de la figure       
            fig = plt.figure(figsize=(10,8))
        
            # affichage des points
            if illustrative_var is None:
                plt.scatter(X_projected[:, d1], X_projected[:, d2], alpha=alpha, color="grey")
            else:
                illustrative_var = np.array(illustrative_var)
                for value in np.unique(illustrative_var):
                    selected = np.where(illustrative_var == value)
                    plt.scatter(X_projected[selected, d1], X_projected[selected, d2], alpha=alpha, label=value, color="grey")
                plt.legend()

            # affichage des labels des points
            texts=[]
            if labels is not None:
                for i,(x,y) in enumerate(X_projected[:,[d1,d2]]):
                    if (abs(x) > np.max(X_projected[:,0])/2 or abs(y) > np.max(X_projected[:,1])/2) or (labels[i]==team ):
                        if labels[i]==team :
                            texts.append(plt.text(x, y, labels[i],
                                      fontsize='8', fontweight="bold"))
                        else:
                            texts.append(plt.text(x, y, labels[i],
                                      fontsize='8'))
                        
                adjust_text(texts, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="-", color='black',lw=0.5))
                        
                    
            # Ajout de texte pour aider à l'interprétation des axes
            
            #plt.text(4, -6.5, "Hight Attack, High Defense", color='seagreen', fontweight="bold")
            #plt.text(-7.5, 6, "Low Attack , Low Defense", color='indianred', fontweight="bold")
            

            # détermination des limites du graphique
            boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            plt.xlim([-10,10])
            plt.ylim([-10,10])
        
            # affichage des lignes horizontales et verticales
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # nom des axes, avec le pourcentage d'inertie expliqué
            plt.xlabel("Performances offensives", fontweight="bold", alpha=0.7)
            plt.ylabel("Performances defensives", fontweight="bold", alpha=0.7)

            plt.title("Projection des équipes (sur F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)

def display_scree_plot(pca):
    scree = pca.explained_variance_ratio_*100
    plt.bar(np.arange(len(scree))+1, scree)
    plt.plot(np.arange(len(scree))+1, scree.cumsum(),c="black",marker='o')
    plt.xlabel("rang de l'axe d'inertie")
    plt.xticks([k+1 for k in range(len(scree))])
    plt.ylabel("pourcentage d'inertie")
    plt.title("Eboulis des valeurs propres")
    plt.show(block=False)

def plot_dendrogram(Z, names):
    plt.figure(figsize=(10,25))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('distance')
    dendrogram(
        Z,
        labels = names,
        orientation = "left",
    )
    plt.show()

