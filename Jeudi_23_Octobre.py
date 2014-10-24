#les fonction : il commence par le nom def (on miniscule)
#il faut respecter l'indentation pour rester dans la fonction
#fonction lambda : c'est une facons d'ecrire une fonction plus raccourcie
# lambda :  c'est un mot cle qu'il fait l'utiliser pour dire que nous allons utilise lambda et on ecrit par la suite
# l'expression vouler, et on affecte le resultat a une variable.
# MEthode 2 : (utilisation lambda)utiliser la fonction directement sont utiliser une variables
#(lambda expression)(arguments)
# fonction qui effectue une annonce

def annonce_ancf(ref,destination,retard):
    print "mes dammes et Mrs, le train %s, qui va vers %s va etre en retard pendant :%d minutes "%(ref,destination,retard)

annonce_ancf("sari3 wad zem","taza",10)

#recherche sur lambda function
#Scope la porte du langage
# par default toutes les variables declarer dans python sont globale

#gestion des exception :
try:
    # le code suceptule de declancher un erreur
    x = 3
except:
    print "non executed"

# les imports  : il sert a ettendre les fonctonnnalite des Script avec des bibliotheque native.
# import module
# import class from module
# imports module as alias (a pour but de rendre l'acces et l'utilisation plus facile et rapide)

#exep :

import math
math.cos(32) # la valeur returner c'est en radian et non pas en degree

# cree un alias
import math as m
m.cos(44)

# on peut importer un methode pour pouvoir l'utiliser directements dans notre projet:
from math import cos
cos(15)

########################################## Developpement sig avec python ##########################################

# les notion de base en poo :

#class : c'est un schema qui contient des fonctionnalite a pour but de decrire l'etat d'objet
# par c'est attribut et methodes.

# methode : c'est une fonction il est en relation avec la calss, il est declarer par le mot def()

# self :  il fait refences a la class actuel (en cours)
# il existe une convontion qu'il faut passer le mot self a la function avant de lui attribut des parameters

#constructeur : c'est methode special qui est lier a la class

# creation d'une classe
class oe:
    def __init__(self):
        name = self.__class__
        print "Class %s bien cree"%name

# objet : c'est une entite individuelle cree a partir d'un classe
ox = oe()

#parameters : au moment de creation de la fonction
#arguments : au moment d'execution de la fonction

# destructeur : pour s'assurer que la memoire et bien liberer
def __del__(self):
    print "objet bien supprimer"

def __repr__(self):
    print "objet ...."
# il sert a modifier l'objet, il est utiliser pour eviter les ambiguiter
# __str__ : specialement pour les print
# la premier des chose il cherche __repr__ s'il ne la trouve pas il va par la suite chercher __str__
#__repr__ou__str

#variable d'objet, ou d'instance ce sont des variables dynamique
# variable de classe : c'est un variable qui existe dans la class elle est statique

# utilisation du count avec la class !!!

# les 3 piliers de la POO (heritage, polymorphisme, encapsulation)

#encapsulation :

# norme d'ecriture pour rendrer le code lisible :
self.public = value
self._protected = val # avec une seul _ , il est mentionner
self.__private = val # super decurite, il ne faut pas la toucher, on utilise deux tiree __ (niveau de securite 2)
methode_proteger(self): ,# methode proteger avec une seul _
methode__private(self): # methode private avec deux __

# creation d'un class exemple

class Encapsulation():
    def __init__(self,a,b,c):
        self.a = a
        self._b = b
        self.__c = c

classe = Encapsulation(1,2,3)

classe._b = 5

print classe._b


# name mangling : c'est une methode qui sert a renvoyer un dictionnaire des attribut
dict = .classe.__dict__
# il sert a retourner les differentes attribut de la class meme s'il sont private.

# le decorateur :  @, il est declarer avant la methode

#property :

property(fget,fset,fdel,doc)
#fget : on realise la function et on la faire passe au parameters
#doc : string , c'est une documentation pour expliquer l'utilite de la class (resume), c'est optionnel
#

class omer:
    def __init__(self):
        print "bien cree"
    def getvar(self):
        return self._var
    def setvar(self,value):
        return self._var = value
    def delvar(self):
        return self._var


var = property(fget=getvar,fset=setvar,fdel=delvar,doc="this is a fucking bull shett")

# 2eme methode d'ecriture

class c(object):
    def __init__(self):
        pass

# pass : veut dire rien faire, justement passer pour ne pas generer des erreur...

    @property
    def x(self):
        return self._x

# polymorphisme n'existe pas en python!! par ce que pyton gere plusieur parameters a la fois
# en faire passer plusieur arguments a la fois func(self,*args)
# les autres langage on des problem avec le passage des parameters, si pour cela qu'il ont utilise
# le polymorphisme

# la signature du methode : comprend le nom de la classe, le nom de la methode (prototype)

