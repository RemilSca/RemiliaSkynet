import csv
import random

def op():
    with open(f'czapkifix.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        czapki = {}
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                czapki[row[0]] = row[1:]
        return czapki

def new():
    czapki = op()
    c = list(czapki.keys())
    today = str(random.choice(c))
    with open(f'weekc', encoding='utf-8') as f:
        f.write(today)

def verify(character):
    czapki = op()
    with open(f'weekc', encoding='utf-8') as f:
        orig = f.read()
    z = czapki[character]
    r = f''
    i = 0
    tf = []
    for x in czapki[character]:
        g = z[i].split(';')
        if len(g) == 1:
            if x == g:
                tf.append(1)
            else:
                tf.append(0)
            i += 1
        else:
            if x in g:
                tf.append(2)
            else:
                tf.append(0)
            i += 1

    return tf





