import csv
import os
import random
import pickle


class Ser:
    def __init__(self, id):
        self.id = id
        self.zg = 0
        self.tries = 0
        self.win = False
        self.streak = 0
        self.highest = 0





def save(u):
    f = open(f'usersw/{u.id}.worde', 'wb')
    pickle.dump(u, f)
    f.close()

def floady(id):
    f = open(f'usersw/{id}.worde', 'rb')
    u = pickle.load(f)
    f.close()
    return u

def op():
    with open(f'czapkifix.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        czapki = {}
        for row in csv_reader:
            if line_count == 0:
                dupa = row
                line_count += 1
            else:
                czapki[row[0]] = row[1:]
        return czapki, dupa

def new():
    czapki, _ = op()
    c = list(czapki.keys())
    today = str(random.choice(c))
    f = open(f'weekc', 'w', encoding='utf-8')
    f.write(today)
    f.close()
    return f'Wylosowano nowe postać'

def verify(character, id):
    czapki, row = op()
    u = floady(id)
    with open(f'weekc', encoding='utf-8') as f:
        orig = f.read()
    z = czapki[orig]
    i = 0
    r = f''
    tf = []
    u.tries += 1
    if orig == character:
        if not u.win:
            if u.tries > 5:
                save(u)
                return f'Zgadles ale przekroczono 5 prob, no badge given!'
            else:
                u.zg += 1
                u.win = True
                u.streak += 1
                save(u)
            return f'Zgadles! Odpowiedz to {orig}'
        else:
            return f'Juz to zgadles!'
    for x in czapki[character]:
        r+=f'{row[i+1]} {x}:'
        dupa = z[i].split(':')
        g = x.split(';')
        if type(g) == list:
            l = len(g)
        else:
            l = 1
        if l == 1:
            if dupa[0] in g[0]:
                tf.append(1)
                r+=f' Dobrze\n'
            else:
                tf.append(0)
                r += f' Zle\n'
            i += 1
        else:
            print(f'{x} aaa {g}')
            for y in dupa:
                if y in g:
                    tf.append(2)
                    r += f' Jedno z tych\n'
                else:
                    tf.append(0)
                    r += f' Zle\n'
                i += 1
    save(u)
    return r

def reset():
    files = os.listdir('usersw')
    for x in files:
        fikle = x.split('.')
        u = floady(fikle[0])
        if u.highest < u.streak:
            u.highest = u.streak
        if not u.win:
            u.streak = 0
        u.win = False
        u.tries = 0
        save(u)
    return f'juz'


def create(id):
    u = Ser(id)
    save(u)
    return f'Zalozono konto!'

def stats(id):
    u = floady(id)
    return f'Zgadles {u.zg} razy, najwieksza seria to {u.highest}'

def chars():
    czapki, _ = op()
    c = list(czapki.keys())
    r = f''
    for x in c:
        r += f'{x}\n'
    return r


