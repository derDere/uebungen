"""Demonstration einer while-Schleife mit Multiplikation.

Startwerte: a = 0, b = 8.
Iteration 1: a += 1 -> 1; a = a * b -> 8.
Iteration 2: a += 1 -> 9; a = a * b -> 72 (>=10, Schleife endet).
Ausgabe: 72.
"""

a = 0
b = 8

while a < 10:  # fehlender Doppelpunkt war Ursache für SyntaxError
    a += 1     # erhöhen
    a = a * b  # multiplizieren

print(a)  # 72
