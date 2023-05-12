import hashlib
import random
import gmpy2

def home_mod_exponent(x, y, n):  # exponentiation modulaire
    return pow(x, y, n)


def home_ext_euclide(a, b):  # algorithme d'euclide étendu pour la recherche de l'exposant secret
    r, u, v = a, 1, 0
    r2, u2, v2 = b, 0, 1

    while r2 != 0:
        q = r // r2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q * r2, u - q * u2, v - q * v2
    return u


def theoreme_chinois(c, d, n, p, q):
    if p < q:
        q, p = p, q

    phip = (p - 1)
    phiq = (q - 1)
    dp = d % phip
    dq = d % phiq

    qinv = home_ext_euclide(q, p)

    mp = home_mod_exponent(c, dp, p)
    mq = home_mod_exponent(c, dq, q)

    h = ((mp - mq) * qinv) % p
    m = (mq + h * q) % n

    return m


def extract_message(message):
    parts = message.split("00||02||")
    message = ''
    for part in parts:
        subparts = part.split("||00")
        for subpart in subparts:
            if not subpart.isdigit() and subpart:
                message += subpart

    return message


def home_pgcd(a, b):  # recherche du pgcd
    if b == 0:
        return a
    else:
        return home_pgcd(b, a % b)


def home_string_to_int(x):  # pour transformer un string en int
    z = 0
    for i in reversed(range(len(x))):
        z = int(ord(x[i])) * pow(2, (8 * i)) + z
    return (z)


def home_int_to_string(x):  # pour transformer un int en string
    txt = ''
    res1 = x
    while res1 > 0:
        res = res1 % (pow(2, 8))
        res1 = (res1 - res) // (pow(2, 8))
        txt = txt + chr(res)
    return txt


def home_list_to_string(x):  # pour transformer une list en string
    txt = ''
    res1 = x
    while res1 > 0:
        res = res1 % (pow(2, 8))
        res1 = (res1 - res) // (pow(2, 8))
        txt = txt + chr(res)
    return txt


def mot20char():  # entrer le secret
    secret = input("donner un secret de 20 caractères au maximum : ")
    while len(secret) > 20:
        secret = input("c'est beaucoup trop long, 20 caractères S.V.P : ")
    return secret


def mot():
    secret = input("donner un secret : ")
    return formalisation(cut_message(secret, 7))


def cut_message(m, k):  # couper le message en k parties
    if len(m) < k:  # on s'assure d'abord que le message est coupable
        print("The message is too short to be cut in", k, "parts")
        return None
    n = len(m)
    l = int(n / k)  # nombre de blocs nécessaire
    m_list = []
    if n % k != 0:
        l = l + 1
    for i in range(l):
        m_list.append(m[i * k:(i + 1) * k])
    print(m_list)
    return m_list


def formalisation(list):  # mettre le message sous la forme 00||02||xi||00||mi
    # générer des nombres aléatoire
    x_list = []
    for i in range(len(list)):
        x_list.append(random.randint(0, 255) + 1)

    # créer des blocs de la forme 00||02||xi||00||mi
    blocs = []
    for i in range(len(list)):
        bloc = ['00||', '02||', str(x_list[i]), '||00', str(list[i])]
        sbloc = ''.join(bloc)
        blocs.append(sbloc)
    print(blocs)
    return ''.join(blocs)


# voici les éléments de la clé d'Alice

# MD5 :
# x1a = 2010942103422233250095259520183  # p
# x2a = 3503815992030544427564583819137  # q

# SHA256 :
x1a = 3413540401136516591521150540440519747493668091969270838391823306731626050553081496265161524563677773  # p
x2a = 8492477647934073533907936878606529490877820810063627562309979164932115908064900020334463062426446547  # q

na = x1a * x2a  # n
phia = ((x1a - 1) * (x2a - 1)) // home_pgcd(x1a - 1, x2a - 1)
ea = 17  # exposant public
da = home_ext_euclide(ea, phia) % phia  # exposant privé

# voici les éléments de la clé de bob

# MD5 :
# x1b = 9434659759111223227678316435911  # p
# x2b = 8842546075387759637728590482297  # q

# SHA256 :
x1b = 6229856537876381926828501147482927302364921498661842284076882710125735604350342143830336693691118771  # p
x2b = 3100850290997031733207481210210140920912497136874645179644558727218136844959910587732066887044353341  # q

nb = x1b * x2b  # n
phib = ((x1b - 1) * (x2b - 1)) // home_pgcd(x1b - 1, x2b - 1)
eb = 23  # exposants public
db = home_ext_euclide(eb, phib) % phib  # exposant privé

print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =", nb)
print("exposant :", eb)
print("voici votre précieux secret")
print("d =", db)
print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut consulter")
print("n =", na)
print("exposent :", ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x = input("appuyer sur entrer")

secret = mot()
print("*******************************************************************")
print("voici la version en nombre décimal de ", secret, " : ")
num_sec = home_string_to_int(secret)
print(num_sec)

print("voici le message chiffré avec la publique d'Alice : ")
chif = home_mod_exponent(num_sec, ea, na)
print(chif)
print("*******************************************************************")
print("On utilise la fonction de hashage SHA256 pour obtenir le hash du message", secret)
Bhachis0 = hashlib.sha256(str(num_sec).encode('utf-8')).digest()  # SHA256 du message
print("voici le hash en nombre décimal ")
Bhachis3 = int.from_bytes(Bhachis0, byteorder='big')
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe = home_mod_exponent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n", chif, "\n \t 2-et le hash signé \n", signe)
print("*******************************************************************")
x = input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n", chif, "\nce qui donne ")
dechif = home_int_to_string(home_mod_exponent(chif, da, na))
print(dechif)

print("*******************************************************************")
print("Alice déchiffre la signature de Bob \n", signe, "\n ce qui donne  en décimal")
designe = home_mod_exponent(signe, eb, nb)
print(designe)

print("Alice vérifie si elle obtient la même chose avec le hash de ", dechif)
Ahachis0 = hashlib.sha256(str(home_string_to_int(dechif)).encode('utf-8')).digest()  # SHA256 du message déchiffré
Ahachis3 = int.from_bytes(Ahachis0, byteorder='big')
print(Ahachis3)
print("La différence =", Ahachis3 - designe)
if Ahachis3 - designe == 0:
    print("Alice : Bob m'a envoyé : ", dechif)
else:
    print("oups")

# THEOREME CHINOIS
print("*******************************************************************")
print("Alice déchiffre le message chiffré grâce au théorème chinois :")
dechifCRT = home_int_to_string(theoreme_chinois(chif, da, na, x1a, x2a))
print(dechifCRT)
print("*******************************************************************")

print("*******************************************************************")
print("Alice déchiffre la signature de Bob grâce au théorème chinois :")
designeCRT = home_mod_exponent(signe, eb, nb)
print(designeCRT)
print("*******************************************************************")

print("Alice vérifie si elle obtient la même chose avec le hash de ", dechifCRT)

Ahachis0 = hashlib.sha256(str(home_string_to_int(dechifCRT)).encode('utf-8')).digest()  # SHA256 du message déchiffré
Ahachis3 = int.from_bytes(Ahachis0, byteorder='big')
print(Ahachis3)
print("La différence =", Ahachis3 - designe)
if Ahachis3 - designeCRT == 0:
    print("Alice : Bob m'a envoyé : ", extract_message(dechifCRT))
else:
    print("oups")
