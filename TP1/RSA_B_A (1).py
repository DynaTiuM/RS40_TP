import hashlib
import random


def home_mod_exponent(x, y, n):  # exponentiation modulaire
    # Utilisation simple de l'exponentiation modulaire implémentée par Python
    return pow(x, y, n)


def home_ext_euclide(a, b):  # Algorithme d'euclide étendu pour la recherche de l'exposant secret
    # L'algorithme est disponible dans notre cours
    # On initialise les coefficients de Bézout à (1,0) et (0,1)
    # Ainsi que nos valeurs a et b, nommées r et r2, grâce à nos paramètres de fonction
    r, u, v = a, 1, 0
    r2, u2, v2 = b, 0, 1

    # Tant que notre reste n'est pas nul,
    while r2 != 0:
        # On récupère q, qui permet de modifier les coefficients de Bézout
        q = r // r2
        # On met à jour nos nouvelles valeurs
        # a prend la valeur de b
        # b prend la valeur de r
        # (u,v) et (u2, v2) sont mis à jours grâce aux formules u - q * u2 et v - q * v2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q * r2, u - q * u2, v - q * v2
    return u


def theoreme_chinois(c, d, n, p, q): # théorème du reste chinois
    # Si p est inférieur à q, nous devons inverser leur valeur respectives pour s'assurer que p soit toujours
    # supérieur à q
    if p < q:
        q, p = p, q

    # Nous réalisons les opérations décrites dans l'annexe de TP concernant le CRT
    phip = (p - 1)
    phiq = (q - 1)
    dp = d % phip
    dq = d % phiq

    qinv = home_ext_euclide(q, p)

    mp = home_mod_exponent(c, dp, p)
    mq = home_mod_exponent(c, dq, q)

    h = ((mp - mq) * qinv) % p
    m = (mq + h * q) % n

    # Nous retournons m
    return m


def extract_message(message):   # Pour extraire seulement les informations essentielles au message
    # Nous extrayons les informations nécessaires pour une bonne lecture du message

    # On remplace tout d'abord le bourrage en espaces vides
    message = message.replace("/x02", "")
    # Nous divisons notre messages en blocs en les reconnaissant par leur début respectifs 00||02||
    parts = message.split("00||02||")
    message = ''
    for part in parts:
        # Pour chaque sous partie de bloc, nous les splitons à nouveau par leur élément respectif ||00||
        subparts = part.split("||00||")
        for subpart in subparts:
            if not subpart.isdigit() and subpart:
                # On ajoute au message final seulement les caractères du message
                message += subpart

    return message


def home_pgcd(a, b):  # recherche du pgcd
    if b == 0:
        return a
    else:
        return home_pgcd(b, a % b)


def home_string_to_int(x):  # transformer un string en int
    z = 0
    for i in reversed(range(len(x))):
        z = int(ord(x[i])) * pow(2, (8 * i)) + z
    return (z)


def home_int_to_string(x):  # transformer un int en string
    txt = ''
    res1 = x
    while res1 > 0:
        res = res1 % (pow(2, 8))
        res1 = (res1 - res) // (pow(2, 8))
        txt = txt + chr(res)
    return txt


def mot():  # demander un mot secret à l'utilisateur
    secret = input("Entrez un message secret : ")
    # Nous créons une taille de bloc random de taille 5 à 15
    rand = random.randint(5, 15)
    # Tant que le random est trop grand, nous recréons une nouvelle taille k
    while rand > len(secret) / 2:
        rand = random.randint(10, 20)
    print("Taille k : ", rand, "Longueur de message : ", len(secret))

    # Nous constituons nos blocs grace à la fonction constitute_blocks
    return constitute_blocks(cut_message(secret, rand), rand)


def cut_message(message, k):  # couper le message en k parties
    parties = []
    for i in range(0, len(message), k):
        partie = message[i:i + k]  # Nous découpons notre message en parties de taille k
        parties.append(partie)  # Nous ajoutons cette partie au tableau de parties
    return parties


def constitute_blocks(lst, k):  # message sous la forme 00||02||xi||00||mi+bourrage
    blocks = []
    # Pour chaque élément de la liste de parties de message
    for i in range(len(lst)):
        # Nous créons un nouveau x qui prend comme valeur random de 1 à 255
        x = random.randint(0, 255) + 1
        # Nous ajoutons à notre partie de message les parties 00|02....
        block = '00||02||' + str(x) + '||00||' + str(lst[i])
        # Si la partie de message est plus petite que d'autres, alors il est nécessaire d'ajouter un bourrage
        if len(str(lst[i])) < k:
            # Ajouter le bourrage avec des /x02
            block += '/x02' * (k - len(str(lst[i])))
        # On ajoute nos blocs dans un tableau de blocs
        blocks.append(block)
    print(blocks)
    # On retourne nos blocks sous forme de string
    return ''.join(blocks)

# SHA256 :
x1a = 22730680150470132399812423649013758565998892977817340568811461686886669950903983501444525685748588642260711586174062304975216661  # p
x2a = 61523825081985627595473143570580013894968922907001976232774710741606667336243335763940851996303185524296319985798889209804008209  # q

na = x1a * x2a  # n
phia = ((x1a - 1) * (x2a - 1)) // home_pgcd(x1a - 1, x2a - 1)
ea = 17  # exposant public
da = home_ext_euclide(ea, phia) % phia  # exposant privé


# SHA256 :
x1b = 83476323070424806405536601489169514701945609142110738731389787915203168312416088618280604434360623994985324900938615942564005101  # p
x2b = 65212579247195399530653298548735745459353786202728406245687819727099769470529134090060242513270806734124526791298578076338796071  # q

nb = x1b * x2b  # n
phib = ((x1b - 1) * (x2b - 1)) // home_pgcd(x1b - 1, x2b - 1)
eb = 23  # exposants public
db = home_ext_euclide(eb, phib) % phib  # exposant privé

print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
x = input("Appuyez sur entrer")

secret = mot()
print("voici la version en nombre décimal de ", secret, " : ")
num_sec = home_string_to_int(secret)

chif = home_mod_exponent(num_sec, ea, na)

Bhachis0 = hashlib.sha256(str(num_sec).encode('utf-8',  errors='strict')).digest()  # SHA256 du message
Bhachis3 = int.from_bytes(Bhachis0, byteorder='big')

signe = home_mod_exponent(Bhachis3, db, nb)

print("|-----------------------------------------------------------------------------------------------")
print("| Bob envoie \n| \t 1- le message chiffré avec la clé public d'Alice \n| ", chif,
      "\n| \t 2- et le hash signé \n| ", signe)
print("|-----------------------------------------------------------------------------------------------")

# THEOREME CHINOIS
print("\n")
print("|-----------------------------------------------------------------------------------------------")
print("|    Alice déchiffre grâce au théorème chinois :")
print("|-----------------------------------------------------------------------------------------------")
dechifCRT = home_int_to_string(theoreme_chinois(chif, da, na, x1a, x2a))
print("| Message déchiffré : ", dechifCRT)
print("|-----------------------------------------------------------------------------------------------")
designeCRT = home_mod_exponent(signe, eb, nb)
print("| Signature de Bob déchiffrée :", designeCRT)
print("|-----------------------------------------------------------------------------------------------")
print("\n")
print("|-----------------------------------------------------------------------------------------------")
print("|    Alice vérifie si elle obtient la même chose avec le hash de ", dechifCRT)
print("|-----------------------------------------------------------------------------------------------")

Ahachis0 = hashlib.sha256(str(home_string_to_int(dechifCRT)).encode('utf-8', errors='strict')).digest()  # SHA256 du message déchiffré
Ahachis3 = int.from_bytes(Ahachis0, byteorder='big')
print("Hachis obtenu : ", Ahachis3)

print("\n\n")
print("|--------------------------------|")
print("|    Vérification de l'égalité   |")
print("|--------------------------------|")
print("| La différence =", Ahachis3 - designeCRT)
if Ahachis3 - designeCRT == 0:
    print("| Alice : Bob m'a envoyé : ", extract_message(dechifCRT))
else:
    print("| ERREUR                         |")
print("|--------------------------------|")
