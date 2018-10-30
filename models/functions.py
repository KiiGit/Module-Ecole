# -*- coding: utf-8 -*-


# Fonction qui permet de convertir un nombre positif en binaire
def dec2bin(d, nb=0):
    """dec2bin(d,nb=0): conversion nombre entier positif ou nul ->
    chaîne binaire (si nb>0, complète à gauche par des zéros)"""
    if d == 0:
        b = "0"
    else:
        b = ""
        while d != 0:
            b = "01"[d & 1] + b
            d = d >> 1
    return b.zfill(nb)
# Exemple d'utilisation:
# print dec2bin(75)  # affiche: "1001011"
# print type(dec2bin(11, 7))  # affiche: "0001011"


# Fonction qui permet de convertir un nombre binaire en nombre positif
def bin2dec(b):
    """bin2dec(b): Conversion chaîne binaire de longueur quelconque -> nombre entier positif"""
    return int(b, 2)
# Exemple d'utilisation:
# print bin2dec("1001011")  # affiche 75


# Fonction qui permet de renvoyer le total decimal pour valeur jours d'inscription restauration scolaire
def calcul_decimal_value(monday, tuesday, wednesday, thursday, friday):
    # On assigne une valeur si c'est True ou False à chaque jours
    if monday:
        monday_decimal = 1
    else:
        monday_decimal = 0

    if tuesday:
        tuesday_decimal = 2
    else:
        tuesday_decimal = 0

    if wednesday:
        wednesday_decimal = 4
    else:
        wednesday_decimal = 0

    if thursday:
        thursday_decimal = 8
    else:
        thursday_decimal = 0

    if friday:
        friday_decimal = 16
    else:
        friday_decimal = 0

    # On fait le total
    total_decimal = monday_decimal + tuesday_decimal + wednesday_decimal + thursday_decimal + friday_decimal

    return total_decimal
