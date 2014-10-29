from Exercice_1 import CalculGeo
calc = CalculGeo()


distance = calc.calculDistance("s4", "s3")
proche = calc.selectProcheStation()
print "la distance entre s1 et s2 et de %.2f km"%distance
print "la plus proche distance est de : %.2f km , il est entre (%s, %s)"%(proche[0], proche[1], proche[2])