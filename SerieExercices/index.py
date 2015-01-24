from Exercice_1 import CalculGeo

donnes = (("S1", 145, 155), ("S2", 150, 155), ("S3", 160, 155), ("S4", 170, 155),
        ("S5", 180, 155), ("S6", 197, 155), ("S7", 200, 155), ("S8", 210, 155))

calc = CalculGeo(donnes)

s1 = raw_input("Entrer la premiere station : ")
s2 = raw_input("Entrer la deuxieme station : ")
distance = calc.calculDistance(s1, s2)
proche = calc.selectProcheStation()
print "la distance entre s1 et s2 et de %.2f km"%distance
print "la plus proche distance est de : %.2f km , il est entre (%s, %s)"%(proche[0], proche[1], proche[2])

input()