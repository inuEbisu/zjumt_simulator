import random as r
import task as t
import event as e
import misc as m

disnames = ("骨折", "骨质疏松", "关节炎", "气胸", "哮喘", "腰间盘突出", "日光性皮炎", "日光性荨麻疹", "糖尿病", "心脏病", "癌症")
disnames_weights = (3, 3, 3, 3, 3, 2, 2, 2, 1, 2, 0.998244353)

def somealgo(num: int, var: int, st: int):
    if var < 0:
        com = st // 10
        var = min(var + com, 0)
    # print(f"var={var}")
    return min(num + var, 100)

class Player:
    name = "Zjuer"

    mood = 100
    san = 100
    eng = 100
    health = 100

    iq = 100
    eq = 100
    st = 100 # stamina

    dis = 0
    disname = "健康" # 0: Healthy :P / >0: Half-training x day(s) / -1: Eternal

    states = []

    score = 0

    def __init__(self, _iq: int, _eq: int, _st: int, _dis: int):
        self.iq = _iq
        self.eq = _eq
        self.st = _st
        self.dis = _dis

        if not self.dis == 0:
            self.disname = r.choices(disnames, disnames_weights)[0]

    def print_stat(self):
        _stat = f"姓名: {self.name}   生命: {self.health}/100   疾病: {self.disname}\n心情: {self.mood}/100   理智: {self.san}/100   精力: {self.eng}/100"
        if m.debug:
            _stat += f"\n智力：{self.iq}   情商：{self.eq}   体能：{self.st}   分数：{self.score}   疾病：{self.dis}"
        print(_stat)

    def do_task(self, task: t.Task):
        # print(f"""self.mood = somealgo({self.mood}, {task.mood}, {self.st})
        # self.san = somealgo({self.san}, {task.san}, {self.st})
        # self.eng = somealgo({self.eng}, {task.eng}, {self.st})""")
        self.mood = somealgo(self.mood, task.mood, self.st)
        self.san = somealgo(self.san, task.san, self.st)
        self.eng = somealgo(self.eng, task.eng, self.st)
        self.iq += task.iq
        self.eq += task.eq
        self.st += task.st
        # self.score += task.score
        self.score = min(self.score + task.score, 100)

        if task.risk:
            rid = r.choices(task.risk[0], task.risk[1])[0]

            risk = e.Event()
            if not rid == "":
                for each in e.occasionals:
                    if each.id == rid:
                        risk = each
                        break
            if not risk.id == "":
                self.do_event(risk)
                m.cls()
                print(str(risk))
                input("按回车键继续……")

    def do_event(self, event: e.Event) -> bool:
        chance = event.chance_calc(self)
        suc = m.judge(chance)
        if suc:
            self.do_task(event)
            exec(event.operation)
        return suc

def rand_player() -> Player:
    iq = int(r.gauss(100, 10)) # normal distribution is zju's culture
    eq = int(r.gauss(100, 10))
    st = int(r.gauss(0, 20))
    dis = r.choices((0, -1), (9, 1))[0]
    return Player(iq, eq, st, dis)

def cheat_player() -> Player:
    print("真正的名字。")
    while True:
        try:
            iq = int(input("决定你的智力: "))
            eq = int(input("决定你的情商: "))
            st = int(input("决定你的体能: "))
            dis = int(input("决定你的疾病: "))
            break
        except KeyboardInterrupt as e:
            raise e
        except:
            print("无效输入。")
    return Player(iq, eq, st, dis)