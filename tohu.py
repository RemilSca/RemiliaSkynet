import os
import random
import threp
import pickle

def gen():
    i = f''
    for x in range(0, 6):
        i += str(random.randint(0,9))
    return i

class Thser:
    def __init__(self, id):
        self.id = id
        self.lp = 0
        self.lastscore = 0
        self.submit = False
        self.stage = 1
        self.akey = gen()



def save(u):
    f = open(f'users/{u.id}.plik', 'wb')
    pickle.dump(u, f)
    f.close()

def floady(id):
    f = open(f'users/{id}.plik', 'rb')
    u = pickle.load(f)
    f.close()
    return u

def create(id):
    u = Thser(id)
    save(u)
    return f'Twój klucz to {u.akey}'

def parse(id):
    try:
        u = floady(id)
        h = open(f'replays/{id}.rpy', 'rb')
        data = h.read()
        game = str(data[0:3])[2:5]
        game = game.replace('R', '').lower()
        tr = threp.THReplay(f'replays/{id}.rpy')
        f = open(f'week', 'r')
        week = eval(f.read())
        f.close()

        check = False
        if len(game) < 3:
            if game[1] in week['g']:
                check = True
        else:
            if game[1:2] in week['g']:
                check = True

        nope_msg = 'Replay nie przyjety:'

        if not check:
            return f'{nope_msg} Nie ta gra'

        if tr.getPlayer() != u.akey:
            return f'{nope_msg} Nieprawidlowa nazwa gracza'

        repl = tr.getBaseInfoDic()
        score = tr.getStageScore()
        character = repl['character'] + repl['shottype']

        if week['m'] != repl['rank'].lower():
            return f'{nope_msg} Nie ten poziom trudnosci'

        if character != week['c']:
            return f'{nope_msg} Nie ta postac'

        if week['t'] == 'nobomb' and tr.getX() != []:
            return f'{nope_msg} Wcisnieto X'

        if week['t'] == 'noshoot' and tr.getZ() != []:
            return f'{nope_msg} Wcisnieto Z'

        if week['t'] == 'nofocus' and tr.getShift() != []:
            return f'{nope_msg} Wcisnieto Shift'

        u.stage = len(score)
        u.lastscore = score[-1]
        u.submit = True
        save(u)
        return f'Zapisano score {u.lastscore} stage: {u.stage}'

    except Exception as err:
        return f'Dupa totalna: {err}'


def newweek():
    mode = ['easy', 'normal', 'hard', 'lunatic', 'extra']
    game = ['th06', 'th07', 'th08', 'th10', 'th11', 'th12', 'th13', 'th14', 'th15', 'th16', 'th17', 'th18']
    task = ['1cc', 'nobomb', 'nofocus']
    chara = {
    'th06': ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB'],
    'th07': ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB', 'SakuyaA', 'SakuyaB'],
    'th08': ['Reimu', 'Sakuya', 'Yukari', 'Remilia', 'Marisa', 'Alice', 'Youmu', 'Yuyuko', 'Rm & Yk', 'Ms & Al',
             'Sk & Rr', 'Ym & Yy'],
    'th10': ['ReimuA', 'ReimuB', 'ReimuC', 'MarisaA', 'MarisaB', 'MarisaC'],
    'th11': ['ReimuA', 'ReimuB', 'ReimuC', 'MarisaA', 'MarisaB', 'MarisaC'],
    'th12': ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB', 'SanaeA', 'SanaeB'],
    'th13': ['Reimu', 'Marisa', 'Sanae', 'Youmu'],
    'th14': ['ReimuA', 'ReimuB', 'MarisaA', 'MarisaB', 'SakuyaA', 'SakuyaB'],
    'th15': ['Reimu', 'Marisa', 'Sanae', 'Reisen'],
    'th16': ['ReimuSpring', 'ReimuSummer', 'ReimuAutumn', 'ReimuWinter', 'MarisaSpring', 'MarisaSummer', 'MarisaAutumn',
             'MarisaWinter', 'CirnoSpring', 'CirnoSummer', 'CirnoAutumn', 'CirnoWinter', 'AyaSpring', 'AyaSummer',
             'AyaAutumn', 'AyaWinter'],
    'th17': ['ReimuWolf', 'ReimuOtter', 'ReimuEagle', 'MarisaWolf', 'MarisaOtter', 'MarisaEagle', 'YoumuWolf',
             'YoumuOtter', 'YoumuEagle'],
    'th18': ['Reimu', 'Marisa', 'Sakuya', 'Sanae']}

    g = random.choice(game)
    m = random.choice(mode)
    t = random.choice(task)
    c = random.choice(chara[g])
    if g == 'th07':
        if m == 'extra':
            m = random.choice(['extra', 'phantasm'])
    elif g == 'th16':
        if m == 'extra':
            m = 'lunatic'
        t = random.choice(['1cc', 'nobomb', 'noshoot', 'nofocus', 'norelease'])

    week = {'g': g, 'm': m, 't': t, 'c': c}
    with open(f'week', 'w') as f:
        f.write(str(week))
    return week


def sta():
    files = os.listdir(f'users')
    scores = []

    for x in files:
        fikle = x.split('.')
        tab = []
        us = floady(fikle[0])
        if us.submit:
            tab.append(us.id)
            tab.append(us.lastscore)
            tab.append(us.stage)

            scores.append(tab.copy())
    y = sorted(scores, key = lambda x: x[1], reverse=True)
    return y

def endweek():
    scores = sta()
    if scores != []:
        files = os.listdir(f'users')
        use = floady(int(scores[0][0]))
        highest = use.lastscore
        for x in files:
            fikle = x.split('.')
            us = floady(fikle[0])
            if us.submit == True:
                us.lp += round(100*(us.lastscore/highest))
                us.submit = False
            save(us)
        return use.id
    return f'Nikt nie wygral'

def staty():
    files = os.listdir(f'users')
    scores = []

    for x in files:
        fikle = x.split('.')
        tab = []
        us = floady(fikle[0])
        tab.append(us.id)
        tab.append(us.lp)
        scores.append(tab.copy())

    y = sorted(scores, key = lambda x: x[1], reverse=True)
    return y

