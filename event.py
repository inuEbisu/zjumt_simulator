import random as r
import task as t
from typing import Callable

# s = timestamp, t = time
# s = (a, b). it's means Day A and B section.
# For b, 1 = daybreak, 2 = morning, 3 = noon, 4 = afternoon, 5 = evening, 6 = night, 7 = overnight.

def t2s(t: tuple) -> int:
    return (t[0] - 1) * 7 + (t[1] - 1)

def s2t(ts: int) -> tuple:
    return (ts // 7 + 1, ts % 7 + 1)

def s(a, b) -> int:
    return t2s((a, b))

def print_time(ts):
    time = s2t(ts)
    timetext = ["清晨", "早上", "正午", "下午", "傍晚", "晚上", "半夜"]
    print(f"第 {time[0]} 天，{timetext[time[1] - 1]}")

# if __name__ == "__main__":
#     print(s2t(int(input())))

class Event(t.Task):
    time_start = 0
    time_end = 0
    time = -1
    type = -1 # -1 - Required / 0 - Optional
    chance_calc = lambda pl: 100
    suc_msg = ""
    fail_msg = ""
    operation = ""
    # chance_calc: Callable[[p.Player], int] 
    def __init__(self, id: str = "", title: str = "", des: str = "", mood: int = 0, san: int = 0, eng: int = 0, iq: int = 0, eq: int = 0, st: int = 0, score: int = 0, timed: tuple = (1, 2, 3, 4, 5, 6, 7), require: Callable = lambda pl: True,  risk: list[tuple] = [],
                 time_start: int = 0, time_end: int = 0, time: int = -1, type = -1, chance_calc: Callable = lambda pl: 100, suc_msg = "You successed", fail_msg = "You failed", operation = ""):
        self.id = id
        self.title = title
        self.des = des
        self.mood = mood
        self.san = san
        self.eng = eng
        self.iq = iq
        self.eq = eq
        self.st = st
        self.timed = timed
        self.require = require
        self.risk = risk
        self.score = score

        self.time_start = time_start
        self.time_end = time_end
        self.time = time
        self.type = type
        self.chance_calc = chance_calc
        self.suc_msg = suc_msg
        self.fail_msg = fail_msg
        self.operation = operation

        if self.time == -1:
            self.time = r.randint(self.time_start, self.time_end)
    
events = [
    Event(
        id = "half_training",
        title = "半训",
        des = "我打军训……真的吗？……要半训吗？\n（扣除大量分数，游戏变简单。）",
        timed = s(1, 1),
        require = lambda pl: pl.dis == -1,
        time = 0,
        score = -10,
        suc_msg = "半训时光 Enjoy!",
    ),
    Event(
        id = "lianbu",
        title = "连部选拔？",
        des = "进入连部就只用做早操了，平日在连部里干文职打工。（扣大量分数，进入连部模式。）",
        type = 0,
        time_start = s(2, 1),
        time_end = s(6, 7),
        # time = s(2, 1),
        score = -15,
        eq = 10, # 连部欢乐多
        require = lambda pl: not pl.dis,
        chance_calc = lambda pl: (pl.iq + pl.eq) * 7 // 12,
        suc_msg = "连部欢迎你",
        fail_msg = "你特长为零。",
        operation = "self.states.append(\"Lianbu\")",
    ),
    Event(
        id = "lianbu_half_training",
        title = "连部选拔？",
        des = "进入连部，平日在连部里干文职打工赚分。（进入连部模式。）",
        type = 0,
        time_start = s(2, 1),
        time_end = s(6, 7),
        # time = s(2, 1),
        eq = 10,
        require = lambda pl: bool(pl.dis),
        chance_calc = lambda pl: pl.iq + pl.eq,
        suc_msg = "连部欢迎你",
        fail_msg = "你特长为零。",
        operation = "self.states.append(\"Lianbu\")",
    ),
    Event(
        id = "chorus",
        title = "合唱选拔？",
        des = "平时要练合唱，增加较多分数。",
        type = 0,
        time = s(3, 2),
        score = 7,
        chance_calc = lambda pl: (pl.iq + pl.eq + pl.st) // 3,
        suc_msg = "合唱队欢迎你",
        fail_msg = "他们说你五音不全。",
        operation = "self.states.append(\"Chorus\")",
    ),
    Event(
        id = "furnace",
        title = "寝室熔炼",
        des = "和室友一起跋山涉水在浙大跑图。如果团结一致，就能增加一些分数。",
        time = s(5, 4),
        score = 5,
        eq = 7,
        chance_calc = lambda pl: (pl.eq - 60) * 5 // 3,
        suc_msg = "和室友一起把游戏都玩遍了，盖了很多章！",
        fail_msg = "似乎出了点意外……？不过好在是跑完了。",
    ),
    Event(
        id = "course_selecting_1",
        title = "第一轮选课",
        des = "选课可得好好选。如果做足功课选课成功，就能获得一些智力，不过最终的结果还是取决于彩票系统。",
        time_start = s(5, 2),
        time_end = s(8, 5),
        # time = s(7, 2),
        iq = 7,
        mood = 50,
        chance_calc = lambda pl: max((pl.eq - 100) * 2, 0) + max((pl.eq - 110) * 3, 0) + r.randint(-30, 50),
        suc_msg = "做足调研的同时欧气爆发，选课大成功，好心情与大量的 4.8/5.0 一同向你招手",
        fail_msg = "Oh no, 选的课全掉了",
    ),
    Event(
        id = "trooping",
        title = "行军拉练",
        des = "全连深更半夜跑图浙大！？成功走完的话就能拿到一些分数。",
        time = s(9, 7),
        score = 5,
        chance_calc = lambda pl: pl.eng + pl.st,
        suc_msg = "完走！",
        fail_msg = "啊啊啊走着走着晕倒了。",
    ),
    Event(
        id = "shooting",
        title = "模拟射击",
        des = "成绩不错的话，就能拿到大量分数。",
        time = s(13, 4),
        score = 10,
        chance_calc = lambda pl: pl.iq // 3 + pl.st * 3 // 2,
        suc_msg = "打出了 10.9 的美丽成绩",
        fail_msg = "全脱靶了，怎么搞的",
    ),
    Event(
        id = "course_selecting_2",
        title = "第二轮选课",
        des = "选课可得好好选。如果做足功课选课成功，就能获得一些智力，不过最终的结果还是取决于彩票系统。",
        time_start = s(16, 2),
        time_end = s(18, 5),
        # time = s(7, 2),
        iq = 7,
        mood = 50,
        chance_calc = lambda pl: max((pl.eq - 100) * 2, 0) + max((pl.eq - 110) * 3, 0) + r.randint(-30, 50),
        suc_msg = "做足调研的同时欧气爆发，选课大成功，好心情与大量的 4.8/5.0 一同向你招手",
        fail_msg = "Oh no, 选的课全掉了",
    ),
]

occasionals = [
    Event(
        id = "training_e1",
        title = "训练很轻松",
        des = "心情 + 10，精力 + 10",
        mood = 10,
        eng = 10,
    ),
    Event(
        id = "training_e2",
        title = "训练爆炸累",
        des = "心情 - 10，精力 - 10",
        mood = -10,
        eng = -10,
    ),
    Event(
        id = "training_e3",
        title = "被夸了？",
        des = "心情 + 10，获得一点点分数",
        mood = 10,
        score = 1,
    ),
    Event(
        id = "injury",
        title = "脚崴了。",
        des = "精力 - 30，不过接下来几天不用训练了",
        operation = "self.dis = (-1 if self.dis == -1 else r.randint(1, 8))",
        eng = -30,
    ),
    Event(
        id = "be_late",
        title = "迟到",
        des = "睡过头了，可恶，闹钟没响啊！心情 - 10，扣除一点分数",
        mood = -10,
        score = -2,
    ),
    Event(
        id = "lecture_e1",
        title = "讲座还挺有意思",
        des = "心情 + 10，理智 + 10，精力 + 10，增加一些智力",
        mood = 10,
        san = 10,
        eng = 10,
        iq = 2,
    ),
    Event(
        id = "lecture_e2",
        title = "讲座无聊",
        des = "按计划进行，心情 - 10，理智 - 10，精力 - 10，丢失一点点智力",
        mood = -10,
        san = -10,
        eng = -10,
        iq = -1,
    ),
    Event(
        id = "lecture_e3",
        title = "讲座上睡着了",
        des = "上课睡觉格外香，精力随机增加 15 ~ 30，该奖励可突破上限",
        operation = "self.eng += r.randint(15, 30)",
    ),
    Event(
        id = "chorus_e1",
        title = "被选作领唱了",
        des = "心情 + 15，增加一些分数",
        mood = 15,
        score = 4,
    ),
    Event(
        id = "lianbu_risk",
        title = "纠察！",
        des = "纠察突然闯进连部，杀你个措手不及。\n扣除一些分数。",
        score = -5,
    )
]