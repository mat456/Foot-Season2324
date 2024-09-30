
### COEFFCIENTS ###
coefs = {"creation occases" : 5,
          "creation occases reg" : 5,
          "defense" : 5,
          "defense reg" : 5,
          "domination" : 10,
          "defaite" : 10,
          "gardien" : 10,
          "efficacite": 10,
          "joueurs clefs": 10,
          "dom_ext": 10,
          "moral" : 5,
          "jeu collectif": 10,
          "possession": 10,
          "erreurs": 5,
          "expulsions": 5,
          "expulsions prov": 5,
          "conservation score": 10,
          "retour score": 10,
          "outsider": 10,
          "Set piece": 10   
         }

### FONCTIONS ###

# Fonction creation d'occases
def crea(xg1a, xg1b):
    bareme = coefs["creation occases"]
    ratio = xg1a / xg1b
    if ratio >= 1.2:
        return bareme * 2
    elif 1.05 < ratio < 1.2:
        return bareme
    elif 0.95 <= ratio <= 1.05:
        return 0
    elif 0.8 < ratio < 0.95:
        return -bareme
    elif ratio <= 0.8:
        return -bareme * 2

# Fonction creation d'occases régulières
def occase_reg(reg1a, reg1b):
    bareme = coefs["creation occases reg"]
    difference = round(reg1a, 2) - round(reg1b, 2)
    if difference > 0.1 and reg1a > 0.4:
        return bareme * 2
    elif (0.03 < difference <= 0.1) or (difference > 0.1 and reg1a <= 0.4):
        return bareme
    elif (-0.1 <= difference < -0.03) or (difference < -0.1 and reg1b <= 0.4):
        return -bareme
    elif difference < -0.1 and reg1b > 0.4:
        return -bareme * 2
    else:
        return 0

# Fonction défense
def defense(xg2a, xg2b):
    bareme = coefs["defense"]
    ratio = xg2a / xg2b
    if ratio >= 1.2:
        return -bareme * 2
    elif 1.05 < ratio < 1.2:
        return -bareme
    elif 0.8 < ratio <= 0.95:
        return bareme
    elif ratio <= 0.8:
        return bareme * 2
    else:
        return 0

# Fonction défense régulière
def defense_reg(xg2a, xg2b, clustera, clusterb):
    bareme = coefs["defense reg"]
    difference = round(xg2a, 2) - round(xg2b, 2)
    if difference > 0.1:
        value = bareme * 2
    elif 0.03 < difference <= 0.1:
        value = bareme
    elif -0.1 <= difference < -0.03:
        value = -bareme
    elif difference < -0.1:
        value = -bareme * 2
    else:
        value = 0

    if clusterb > clustera and xg2b > 0.66 and value > 5:
        value = value / 2
                

    return value

# Domination
def domination(doma, domb, clustera, clusterb):
    bareme = coefs["domination"]
    difference = round(doma, 2) - round(domb, 2)
    if difference > 0.09:
        domination_value = bareme
    elif 0.03 < difference <= 0.09:
        domination_value = bareme / 2
    elif -0.09 <= difference < -0.03:
        domination_value = -bareme / 2
    elif difference < -0.09:
        domination_value = -bareme
    else:
        domination_value = 0

    if clustera == clusterb:
        if difference >= 0.19:
            domination_value = bareme * 1.5
        elif difference <= -0.19:
            domination_value = -bareme * 1.5

    return domination_value


# Défaite
def defaite(defa, defb, clustera, clusterb):
    bareme = coefs["defaite"]
    if clustera == clusterb:
        if defa < defb - 5/100:
            defaite_value = bareme
        elif defb < defa - 5/100:
            defaite_value = -bareme
        else:
            defaite_value = 0
    else:
        defaite_value = 0
        
    return defaite_value

# Gardien
def gardien(psxga, psxgb, ga, gb):
    
    bareme = coefs["gardien"]
    ratioa = ga / psxga
    ratiob = gb / psxgb
    
    if (ratioa > (ratiob * 1.2)) & (ga>=1):
        value = -bareme * 1.5
    elif (ratioa > (ratiob * 1.2)) & (ga<1):
        value = -bareme * 1
    elif ratioa > (ratiob * 1.02) and ratioa <= (ratiob * 1.2):
        value = -bareme
    elif ratiob > (ratioa * 1.02) and ratiob <= (ratioa * 1.2):
        value = bareme
    elif (ratiob > (ratioa * 1.2)) & (gb>=1):
        value = bareme * 1.5
    elif (ratioa > (ratiob * 1.2)) & (gb<1):
        value = bareme * 1
    else:
        value = 0

    if ratioa > 1.1 and value > 0:
        value = value / 2
    if ratiob > 1.1 and value < 0:
        value = value / 2

    return value

# Efficacité
def efficacite(xg1a, xg1b, g1a, g1b, morala, moralb, clustera, clusterb):
    bareme = coefs["efficacite"]
    ratioa = g1a / xg1a
    ratiob = g1b / xg1b
    
    if (ratioa > (ratiob * 1.17)) & (ratiob <= 1):
        if g1a < 1.3 and ratiob <= 1.1:
            value = 0
        elif g1a < 1.3 and ratiob > 1.1:
            value = bareme * 0.5
        elif (g1a >= 1.3) & (morala != "Bas"):
            value = bareme * 1.5
        else :
            value = bareme
    elif (ratioa > (ratiob * 1.17)) & (ratiob > 1):
        value = bareme
    elif ratioa > (ratiob * 1.08) and ratioa <= (ratiob * 1.17) and g1a >= 1.3:
        value = bareme
    elif ratiob > (ratioa * 1.08) and ratiob <= (ratioa * 1.17) and g1b >= 1.3:
        value = -bareme
    elif (ratiob > (ratioa * 1.1)) & (ratioa <=1):
        if g1b < 1.3 and ratioa <= 1.1:
            value = 0
        elif g1b < 1.3 and ratioa > 1.1:
            value = bareme * 0.5
        elif (g1b >= 1.3) & (moralb != "Bas"):
            value = -bareme * 1.5
        else :
            value = -bareme
    elif (ratiob > (ratioa * 1.17)) & (ratioa > 1):
        value = bareme
    else:
        value = 0

    if value > 0 and ratiob > 1.1 and g1b > 2 and clustera < clusterb:
        value = value / 2
    if value < 0 and ratioa > 1.1 and g1a > 2 and clusterb < clustera:
        value = value / 2

    return value


# Joueurs clefs
def absence(absa, absb):
    bareme = coefs["joueurs clefs"]
    value = (absb - absa) * bareme
    return value



# Impact dom/ext
def impact_lieu(lieua, lieub,lieu):
    bareme = coefs["dom_ext"]

    if (lieu=="H") & (lieua=="Oui") & (lieub=="Oui"):
        value = bareme
    elif (lieu=="A") & (lieua=="Oui") & (lieub=="Oui"):
        value = -bareme
    elif (lieu=="H") & (lieua=="Oui") & (lieub=="Non"):
        value = bareme/2
    elif (lieu=="A") & (lieua=="Non") & (lieub=="Oui"):
        value = -bareme/2
    else:
        value = 0
        
    return value
        
# Moral
def moral(morala, moralb, lieu, clustera, clusterb):
    bareme = coefs["moral"]
    dict_moral = {"Haut": 2, "Normal": 1, "Bas": 0}
    if dict_moral[morala] > dict_moral[moralb] + 1 :
        value = bareme
    elif dict_moral[moralb] > dict_moral[morala] + 1:
        value = -bareme
    else:
        value = 0

    if clustera < clusterb and lieu == "H":
        value = 0
        
    return value

# Jeu collectif
def jeu_col(xaa, xab, pass_proga, pass_progb, amta, amtb, pass_surfa, pass_surfb, clustera, clusterb):
    bareme = coefs["jeu collectif"]    
    if xaa > xab and pass_proga > pass_progb and (amta > amtb or amtb < 25):
        jeu_col_value = bareme
    elif xaa < xab and pass_proga < pass_progb and (amta < amtb or amta < 25):
        jeu_col_value = -bareme
    elif xaa < xab and xaa > xab * 0.95 and pass_surfa > pass_surfb * 0.1:
        jeu_col_value = bareme
    elif xab < xaa and xab > xaa * 0.95 and pass_surfb > pass_surfa * 0.1:
        jeu_col_value = -bareme
    else:
        jeu_col_value = 0

    if clustera < clusterb and xab>=2 and xaa<2.35:
        jeu_col_value = 0
    elif clustera < clusterb and xaa >= 2.5 and xab <= 2:
        jeu_col_value = jeu_col_value
    elif clustera < clusterb and xab >=2.7:
        jeu_col_value /= 2

    if clusterb > clustera and pass_progb > pass_proga and pass_surfb > pass_surfa:
        jeu_col_value = jeu_col_value*2
        if jeu_col_value == 0:
            jeu_col_value = -5



    return jeu_col_value

# Possession progressive
def poss(proga, progb, surfa, surfb, clustera, clusterb, morala, moralb):
    bareme = coefs["possession"]
    poss_value = 0 
    if clustera == clusterb:
        if proga > progb and surfa > surfb:
            poss_value = bareme
        elif proga < progb and surfa < surfb:
            poss_value = -bareme
        else:
            poss_value = 0

    elif clustera < clusterb:
        if proga < progb and surfa < surfb:
            poss_value = -bareme
        elif proga > progb * 1.5 and surfa > surfb * 1.5 and morala=="Haut":
            poss_value = bareme
        else :
            poss_value = 0
        
    
    return poss_value

# Erreurs
def erreur(erra, errb):
    bareme = coefs["erreurs"]
    if (erra == 0) & (errb == 0):
        value = 0
    elif (erra == 0) & (errb > 0.1):
        value = bareme
    elif (errb == 0) & (erra > 0.1):
        value = -bareme
    else :
        ratio = erra / errb
        if ratio >= 1.2:
            value = -bareme * 2
        elif 1.05 < ratio < 1.2:
            value = -bareme
        elif 0.8 < ratio <= 0.95:
            value = bareme
        elif ratio <= 0.8:
            value = bareme * 2
        else:
            value = 0

        if value > 0 and errb < 0.2:
            value = value /2

        if value < 0 and erra < 0.2:
                value = value /2
    
    return value

# Expulsions 
def expulsions(expulsa, expulsb, clustera, clusterb):
    bareme = coefs["expulsions"]
    if clustera == clusterb:
        if expulsa < expulsb - 5/100:
            value = bareme
        elif expulsb < expulsa - 5/100:
            value = bareme
        else:
            value = 0
    else:
        value = 0

    return value

# Expulsions provoquées
def expulsions_prov(expulsa, expulsb, clustera, clusterb):
    bareme = coefs["expulsions prov"]
    if clustera == clusterb:
        if expulsa > expulsb + 5/100:
            value = bareme
        elif expulsb > expulsa + 5/100:
            value = bareme
        else:
            value = 0
    else:
        value = 0

    return value
    
# Conservation du score
def conserve(garde_scorea, garde_scoreb, clustera, clusterb):
    bareme = coefs["conservation score"]
    if clustera == clusterb:
        if garde_scorea > garde_scoreb * 1.2:
            value = bareme
        elif (garde_scorea <= garde_scoreb * 1.2) & (garde_scorea >= garde_scoreb * 1.02):
            value = bareme
        elif (garde_scoreb <= garde_scorea * 1.2) & (garde_scoreb >= garde_scorea * 1.02):
            value = -bareme
        elif garde_scoreb > garde_scorea * 1.2:
            value = -bareme
        else:
            value = 0
    else:
        value = 0
        
    return value

# Retour score
def retours(retour_scorea, retour_scoreb, conservea, conserveb,clustera, clusterb):
    bareme = coefs["retour score"]
    if clustera == clusterb:
        if retour_scorea > retour_scoreb * 1.2:
            value = bareme
        elif retour_scorea <= retour_scoreb * 1.2 and retour_scorea >= retour_scoreb * 1.1:
            value = bareme
        elif retour_scoreb <= retour_scorea * 1.2 and retour_scoreb >= retour_scorea * 1.1:
            value = -bareme
        elif retour_scoreb > retour_scorea * 1.2:
            value = -bareme
        else:
            value = 0
    elif clustera <= clusterb:
        if retour_scorea >= 0.8 and conserveb <= 0.5:
            value = bareme
        else:
            value = 0
    else :
        value = 0
        
    return value

# Outsider
def outsider(joura, jourb, aeriena, aerienb, garde_scorea, garde_scoreb, retour_scorea, retour_scoreb, xg1a, xg1b, g1a, g1b, xg21, xg2b, morala, moralb, lieu, clustera, clusterb):
    bareme = coefs["outsider"]
    value = 0
    if clusterb > clustera:
        if garde_scoreb > garde_scorea * 1.1:
            value = -bareme
        elif (garde_scoreb > 0.66) & (xg1b >= 1):
            value = -bareme
        if xg1b > 1.8 and g1b/xg1b>=1:
            value += -bareme
        #if g1b / xg1b >= 1 and xg2b <=1.6:
            #value += -bareme
        if lieu == "A" and morala == "Bas":
            value += -bareme*1.5
        if lieu == "A" and joura <=3 and jourb>=6:
            value += -bareme*1.5
        #if aerienb > 1.1 * aeriena:
            #value += -bareme/2
        if jourb == 3 and joura > jourb:
            value += bareme / 2

    
    return value

# Set piece
def set_piece(g1_deada, g1_deadb, g2_deada, g2_deadb, g1a, g1b, clustera, clusterb):
    
    bareme = coefs["Set piece"]
    value = 0
    if clusterb > clustera:
        if g1_deadb > 0.15 and (g1_deadb / g1b) > (g1_deada / g1a) and g1_deada < 0.2:
            value = -bareme
        elif (g1_deadb - g2_deadb) > (g1_deada - g2_deada) and (g1_deada - g2_deada) <= 0 and g1_deadb >= 0.09 and g2_deada >= 0.15:
            value = -bareme 
        else:
            value = 0

    

    return value
    
