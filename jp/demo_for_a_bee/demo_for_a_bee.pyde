# Farbkonstanten
SKY_BLUE = 0xFF87CEEB
BLACK = 0xFF000000
WHITE = 0xFFFFFFFF
YELLOW = 0xFFFFFF00
PINK = 0xFFFFC0CB


# globale Variablen
x = 400  # Horizontale Mitte
y = 300  # Vertikale Mitte
r = 50   # Radius
f = 5    # Für die Flügel


def setup():
    size(800, 600)


def draw():
    global x, y, f
    f *= -1  # Na was macht das? :D

    x = mouseX
    y = mouseY

    background(SKY_BLUE)  # Himmel blauer Hintergrund

    # Der Stachel
    stroke(BLACK)
    strokeWeight(5)

    start_x = x - 30
    line(start_x, y, x, y)

    # Linien dicke wieder auf Anfang
    strokeWeight(2)

    # Flügel 1
    fill(WHITE)
    ellipse(x + 40, y - 20 + f, 40, 40)

    # PoPo
    i = 0
    while i < 6:
        i += 1
        x2 = x + (i * 10)
        if i % 2 == 0:
            fill(BLACK)
        else:
            fill(YELLOW)
        ellipse(x2, y, r, r)

    # Flügel 2
    fill(WHITE)
    ellipse(x + 10, y - 20 + f, 40, 40)

    # Mund
    if mousePressed:
        fill(PINK)
        rect(x + 55, y + 8, 25, 10)
        noStroke()
        fill(BLACK)
        text('... sum sum sum', x + 85, y + 25)
        stroke(BLACK)

    # Augen
    fill(WHITE)
    ellipse(x + 55, y - 5, 20, 20)
    ellipse(x + 80, y - 5, 20, 20)
    fill(BLACK)
    ellipse(x + 55, y - 5, 10, 10)
    ellipse(x + 80, y - 5, 10, 10)

    # Hübscher Rahmen
    noFill()
    rect(10, 10, width - 21, height - 21)











































# ENDE
