from fonctions import *
import pandas as pd
import datetime as dt
import numpy as np

def model(equipe1, equipe2, lieu, date, nb_games, abs1, abs2):

    games = pd.read_csv("games.csv", parse_dates=["Date"])
    
    lieu_adv = ["H", "A"]

    if lieu in lieu_adv :    
        lieu_adv.remove(lieu)
        lieu_adv = lieu_adv[0]
        games1 = games[~((games["Equipe"]==equipe1) & (games["Home_Away"]==lieu) & (games["Equipe adverse"]==equipe2))]
        games2 = games[~((games["Equipe"]==equipe2) & (games["Home_Away"]==lieu_adv) & (games["Equipe adverse"]==equipe1))]
    else :
        games1 = games.copy()
        games2 = games.copy()
    
    coef_home_away = 1.2

    date_min = "2023-10-30"
    date = max(date, date_min)
    
    games1 = games1[(games1["Equipe"]==equipe1) & (games1["Date"]<=date) & (pd.isna(games1["Fait marquant"])) ].iloc[:nb_games]
    games2 = games2[(games2["Equipe"]==equipe2) & (games2["Date"]<=date) & (pd.isna(games2["Fait marquant"]))].iloc[:nb_games]
    
    #### KPI offensifs ####
    
    # Moyenne des xG1
    xG1_mean_1 = games1["XG1"].mean()
    xG1_mean_2 = games2["XG1"].mean()
    
    # Ecart-type des xG1
    xG1_std_1 = games1["XG1"].std()
    xG1_std_2 = games2["XG1"].std()
    
    # Coef de variation des xG1
    coef_var_1 = xG1_std_1 / xG1_mean_1
    coef_var_2 = xG1_std_2 / xG1_mean_2
    
    # % de match avec xG1 > 1.5
    xG1_reg_1 = games1["Att_reg"].sum() / games1["Att_reg"].count()
    xG1_reg_2 = games2["Att_reg"].sum() / games2["Att_reg"].count()
    
    # Moyenne des xA1
    xA1_mean_1 = games1["XA1"].mean()
    xA1_mean_2 = games2["XA1"].mean()
    
    # % de match avec xG1 > xG2
    dom_1 = games1["Domination"].sum() / games1["Domination"].count()
    dom_2 = games2["Domination"].sum() / games2["Domination"].count()
    
    # Moyenne des passes progressives
    passes_prog_1 = games1["Passes prog"].mean()
    passes_prog_2 = games2["Passes prog"].mean()
    
    # Moyenne des passes dans la surface
    passes_surf_1 = games1["Passes surface"].mean()
    passes_surf_2 = games2["Passes surface"].mean()
    
    # Moyenne des possessions progressives
    poss_prog_1 = games1["Poss prog"].mean()
    poss_prog_2 = games2["Poss prog"].mean()
    
    # Moyenne des possessions surface
    poss_surf_1 = games1["Poss surface"].mean()
    poss_surf_2 = games2["Poss surface"].mean()
    
    # Moyenne des AMT
    amt_1 = games1["AMT"].mean()
    amt_2 = games2["AMT"].mean()
    
    # Moyenne des buts
    G1_1 = games1["G1"].mean()
    G1_2 = games2["G1"].mean()

    # Expected points
    Xpts_1 = games1["Xpts"].mean()
    Xpts_2 = games2["Xpts"].mean()
    
    #### KPI défensifs ####
    
    # Moyenne des xG2
    xG2_mean_1 = games1["XG2"].mean()
    xG2_mean_2 = games2["XG2"].mean()
    
    # Ecart-type des xG2
    xG2_std_1 = games1["XG2"].std()
    xG2_std_2 = games2["XG2"].std()
    
    # Coef de variation des xG2
    coef_var_xg2_1 = xG2_std_1 / xG2_mean_1
    coef_var_xg2_2 = xG2_std_2 / xG2_mean_2
    
    # % de match avec xG2 < 1.5
    xG2_reg_1 = games1["Def_reg"].sum() / games1["Def_reg"].count()
    xG2_reg_2 = games2["Def_reg"].sum() / games2["Def_reg"].count()
    
    # Moyenne des xA2
    xA2_mean_1 = games1["XA2"].mean()
    xA2_mean_2 = games2["XA2"].mean()
    
    # Moyenne des erreurs
    erreurs_1 = games1["Erreurs"].mean()
    erreurs_2 = games2["Erreurs"].mean()
    
    # Moyenne des PSXG
    psxg_1 = games1["PSXG"].mean()
    psxg_2 = games2["PSXG"].mean()
    
    # Moyenne des duels aériens
    aerien_1 = games1["Aerien win"].mean()
    aerien_2 = games2["Aerien win"].mean()
    
    # Moyenne des buts
    G2_1 = games1["G2"].mean()
    G2_2 = games2["G2"].mean()

    # Ppda
    ppda_1 = games1["Ppda"].mean()
    ppda_2 = games2["Ppda"].mean()

    # g1_dead
    g1_dead_1 = games1["g1_dead"].mean()
    g1_dead_2 = games2["g1_dead"].mean()

    # g2_dead
    g2_dead_1 = games1["g2_dead"].mean()
    g2_dead_2 = games2["g2_dead"].mean()
    
    #### KPI histo ####
    
    # % défaites
    def_1 = games1[games1["Resultat"]=="D"]["Resultat"].count() / games1["Resultat"].count()
    def_2 = games2[games2["Resultat"]=="D"]["Resultat"].count() / games2["Resultat"].count()
    
    # Conservation du score
    if games1["Garde score"].count() > 0:
        keep_1 = games1[games1["Garde score"]=="O"]["Resultat"].count() / games1["Garde score"].count()
    else:
        keep_1 = np.NaN
    if games2["Garde score"].count() > 0:    
        keep_2 = games2[games2["Garde score"]=="O"]["Resultat"].count() / games2["Garde score"].count()
    else:
        keep_2 = np.NaN
    
    # Retour au score

    if games1["Revenu score"].count() > 0:
        back_1 = games1[games1["Revenu score"]=="O"]["Resultat"].count() / games1["Revenu score"].count()
    else:
        back_1 = np.NaN
    if games2["Revenu score"].count() > 0: 
        back_2 = games2[games2["Revenu score"]=="O"]["Resultat"].count() / games2["Revenu score"].count()
    else:
        back_2 = np.NaN
    
    # Moral

    def cpt(res):
        if res=="V" :
            return 1
        elif res=="D":
            return -1
        else :
            return 0

    moral1 = games1["Resultat"][:3]
    cpt_moral1 = moral1.apply(cpt).sum()

    moral2 = games2["Resultat"][:3]
    cpt_moral2 = moral2.apply(cpt).sum()

    rang1 = games1["Rang Equipe"].iloc[0]
    rang2 = games2["Rang Equipe"].iloc[0]

    
    def etat_moral(moral, rang):
        rang = int(rang)
        if rang == 1:
            if moral >= 2:
                value = "Haut"
            elif moral < 2 and moral >= 1:
                value = "Normal"
            else :
                return "Bas"        
        elif rang == 2:
            if moral > 1:
                value = "Haut"
            elif moral < 1 and moral >= 0:
                value = "Normal"
            else :
                 value = "Bas"          
        elif rang > 2 :
            if moral > 0:
                value = "Haut"
            elif moral < 0 and moral >= -1:
                value = "Normal"
            else :
                value = "Bas"  
                
        return value
                    
    moral_1 = etat_moral(cpt_moral1, rang1)
    moral_2 = etat_moral(cpt_moral2, rang2)
    
    
    # Impact dom/ext
    mask_home = games1["Home_Away"]=="H"
    mask_away = games1["Home_Away"]=="A"
    xg1_home = games1[mask_home]["XG1"].mean()
    xg2_home = games1[mask_home]["XG2"].mean()
    xg1_away = games1[mask_away]["XG1"].mean()
    xg2_away = games1[mask_away]["XG2"].mean()
    ratio_home_1 = xg1_home / xg2_home
    ratio_away_1 = xg1_away / xg2_away
    home_away_1 = ratio_home_1 / ratio_away_1
    if home_away_1 > coef_home_away :
        impact_home_1 = "Oui"
    else:
        impact_home_1 = "Non"
    
    mask_home = games2["Home_Away"]=="H"
    mask_away = games2["Home_Away"]=="A"
    xg1_home = games2[mask_home]["XG1"].mean()
    xg2_home = games2[mask_home]["XG2"].mean()
    xg1_away = games2[mask_away]["XG1"].mean()
    xg2_away = games2[mask_away]["XG2"].mean()
    ratio_home_2 = xg1_home / xg2_home
    ratio_away_2 = xg1_away / xg2_away
    home_away_2 = ratio_home_1 / ratio_away_1
    if home_away_2 > coef_home_away :
        impact_home_2 = "Oui"
    else:
        impact_home_2 = "Non"

    # Cluster
    cluster_1 = games1["Cluster"].iloc[0]
    cluster_2 = games2["Cluster"].iloc[0]
        
    #### Autres KPI ####
    
    # Expulsions concédées
    
    games1_expul = games[(games["Equipe"]==equipe1) & (games["Date"]<=date) ]
    games2_expul = games[(games["Equipe"]==equipe2) & (games["Date"]<=date) ]
    
    expul_prov_1 = games1_expul[games1_expul["Fait marquant"]=="Rouge 2"]["Fait marquant"].count() / games1_expul["Equipe"].count()
    expul_prov_2 = games2_expul[games2_expul["Fait marquant"]=="Rouge 2"]["Fait marquant"].count() / games2_expul["Equipe"].count()
    
    # Expulsions provoquées
    
    expul_conc_1 = games1_expul[games1_expul["Fait marquant"]=="Rouge 1"]["Fait marquant"].count() / games1_expul["Equipe"].count()
    expul_conc_2 = games2_expul[games2_expul["Fait marquant"]=="Rouge 1"]["Fait marquant"].count() / games2_expul["Equipe"].count()
    
    # Dribbles tentés
    dt_1 = games1["Dribbles tentés"].mean()
    dt_2 = games2["Dribbles tentés"].mean()
    
    # Dribbles réussis
    dr_1 = games1["Dribbles tentés"].mean()
    dr_2 = games2["Dribbles tentés"].mean()
    
    # ratio_dribble
    ratio_1 = dr_1 / dt_1
    ratio_2 = dr_2 / dt_2
    
    # Duels aériens
    duels_aer_1 = games1["Aerien win"].mean()
    duels_aer_2 = games2["Aerien win"].mean()
    
    # tacles et interceptions
    TCL_1 = games1["TCL"].mean()
    TCL_2 = games2["TCL"].mean()
    
    # Moyenne des variables ACP
    ACP_1_1 = games1["ACP_1"].mean()
    ACP_1_2 = games2["ACP_1"].mean()
    ACP_2_1 = games1["ACP_2"].mean()
    ACP_2_2 = games2["ACP_2"].mean()    

    # Jours recup depuis dernier match
    #jours_recup_1 = abs(games1["Date"].diff().iloc[1].days)
    #jours_recup_2 = abs(games2["Date"].diff().iloc[1].days)

    
    date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
    last_date_1 = games1["Date"].iloc[0] 
    last_date_2 = games2["Date"].iloc[0] 
    
    jours_recup_1 = (date_obj - last_date_1).days + 1
    jours_recup_2 = (date_obj - last_date_2).days + 1


    Crea = crea(xG1_mean_1, xG1_mean_2)
    Occase_reg = occase_reg(xG1_reg_1, xG1_reg_2)
    Defense = defense(xG2_mean_1, xG2_mean_2)
    Defense_reg =  defense_reg(xG2_reg_1, xG2_reg_2, cluster_1, cluster_2)
    Domination = domination(dom_1, dom_2, cluster_1, cluster_2)
    Defaite = defaite(def_1, def_2, cluster_1, cluster_2)
    Gardien = gardien(psxg_1, psxg_2, G2_1, G2_2)
    Efficacite = efficacite(xG1_mean_1, xG1_mean_2, G1_1, G1_2, moral_1, moral_2, cluster_1, cluster_2)
    Absence = absence(abs1, abs2)
    Impact_lieu = impact_lieu(impact_home_1, impact_home_2, lieu)
    Moral = moral(moral_1, moral_2, lieu, cluster_1, cluster_2)
    Jeu_col = jeu_col(xA1_mean_1, xA1_mean_2, passes_prog_1, passes_prog_2, amt_1, amt_2, passes_surf_1, passes_surf_2, cluster_1, cluster_2)
    Poss = poss(poss_prog_1, poss_prog_2, poss_surf_1, poss_surf_2, cluster_1, cluster_2, moral_1, moral_2)
    Erreur = erreur(erreurs_1, erreurs_2)
    Expulsions = expulsions(expul_conc_1, expul_conc_2, cluster_1, cluster_2)
    Expulsions_prov = expulsions_prov(expul_prov_1, expul_prov_2, cluster_1, cluster_2)
    Conserve = conserve(keep_1, keep_2, cluster_1, cluster_2)
    Retours = retours(back_1, back_2, keep_1, keep_2, cluster_1, cluster_2)
    Outsider = outsider(jours_recup_1, jours_recup_2, aerien_1, aerien_2, keep_1, keep_2, back_1, back_2, xG1_mean_1, xG1_mean_2, G1_1, G1_2, xG2_mean_1, xG2_mean_2, moral_1, moral_2, lieu, cluster_1, cluster_2)
    Setpiece = set_piece(g1_dead_1, g1_dead_2, g2_dead_1, g2_dead_2, G1_1, G1_2, cluster_1, cluster_2)

    Total = Crea + Occase_reg + Defense + Defense_reg + Domination + Defaite + Gardien + Efficacite + Absence + Impact_lieu + Moral + Jeu_col + Poss + Erreur + Expulsions + Expulsions_prov + Conserve + Retours + Outsider + Setpiece

    df_stats = pd.DataFrame({"Stats" :["xG1", "G1", "coef_var", "xG1 reg", "xA1", "Domination", "Passes progressives", "Passes surface", "Possession progressive", "Possession surface", "AMT", "Xpts", "xG2", "coef_var_2", "xG2 reg", "xA2", "Ppda", "Erreurs", "PSxG", "Aerien win", "G2", "Defaites", "Conservation", "Retour", "Moral", "Impact lieu", "Cluster", "Jours_recup", "G1 set piece", "G2 set piece"],
                             equipe1 : [
    round(xG1_mean_1, 2), round(G1_1,2), round(coef_var_1, 2), round(xG1_reg_1, 2), round(xA1_mean_1, 2), 
    round(dom_1, 2), round(passes_prog_1, 2), round(passes_surf_1, 2), round(poss_prog_1, 2), 
    round(poss_surf_1, 2), round(amt_1, 2), round(Xpts_1, 2), round(xG2_mean_1, 2), 
    round(coef_var_xg2_1, 2), round(xG2_reg_1, 2), round(xA2_mean_1, 2), round(ppda_1,2),round(erreurs_1, 2), 
    round(psxg_1, 2), round(aerien_1, 2), round(G2_1, 2), round(def_1, 2), round(keep_1, 2), 
    round(back_1, 2), moral_1, impact_home_1, cluster_1, jours_recup_1, round(g1_dead_1,2), round(g2_dead_1,2)
]
,
equipe2 : [
    round(xG1_mean_2, 2), round(G1_2, 2), round(coef_var_2, 2), round(xG1_reg_2, 2), round(xA1_mean_2, 2), 
    round(dom_2, 2), round(passes_prog_2, 2), round(passes_surf_2, 2), round(poss_prog_2, 2), 
    round(poss_surf_2, 2), round(amt_2, 2), round(Xpts_2,2), round(xG2_mean_2, 2), 
    round(coef_var_xg2_2, 2), round(xG2_reg_2, 2), round(xA2_mean_2, 2), round(ppda_2,2), round(erreurs_2, 2), 
    round(psxg_2, 2), round(aerien_2, 2), round(G2_2, 2), round(def_2, 2), round(keep_2, 2), 
    round(back_2, 2), moral_2, impact_home_2, cluster_2, jours_recup_2, round(g1_dead_2,2), round(g2_dead_2,2)
]

                            }
                             )   
    
    df_stats.set_index("Stats", inplace=True)


    df_model = pd.DataFrame({"KPI" : ["Chances created", "Regular chances", "Defence", "Regular defence", "Domination", "Defeats", "Top goalkeeper", "Shooters efficiency", "Key players missing", "Impact home/away", "Mood", "Teamwork", "Possession", "Mistakes", "Expulsions", "Expulsions provoked", "Keep score", "Back to score", "Outsider", "Setpiece", "Total"],
                       "Barème" : [coefs["creation occases"], coefs["creation occases reg"], coefs["defense"], coefs["defense reg"], coefs["domination"], coefs["defaite"], coefs["gardien"], coefs["efficacite"], coefs["joueurs clefs"], coefs["dom_ext"], coefs["moral"], coefs["jeu collectif"], coefs["possession"], coefs["erreurs"], coefs["expulsions"], coefs["expulsions prov"], coefs["conservation score"], coefs["retour score"], coefs["outsider"],  coefs["Set piece"], np.NaN],
                       "Score" : [Crea, Occase_reg, Defense, Defense_reg, Domination, Defaite, Gardien, Efficacite, Absence, Impact_lieu, Moral, Jeu_col, Poss, Erreur, Expulsions, Expulsions_prov, Conserve, Retours, Outsider, Setpiece, Total]})
                      
    
    df_model.set_index("KPI", inplace=True)

    
    return Total, df_stats, df_model




