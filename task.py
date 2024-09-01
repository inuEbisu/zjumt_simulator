from typing import Callable

class Task:
    id = "id"
    title = "Title"
    des = "Description"
    mood = 0
    san = 0
    eng = 0
    iq = 0
    eq = 0
    st = 0
    score = 0
    timed: tuple = (1, 2, 3, 4, 5, 6, 7)
    require: Callable = lambda pl: True
    risk: list[tuple] = []

    def __init__(self, id: str = "", title: str = "", des: str = "", mood: int = 0, san: int = 0, eng: int = 0, iq: int = 0, eq: int = 0, st: int = 0, score: int = 0, timed: tuple = (1, 2, 3, 4, 5, 6, 7), require: Callable = lambda pl: True, risk: list[tuple] = []):
        self.id = id
        self.title = title
        self.des = des
        self.mood = mood
        self.san = san
        self.eng = eng
        self.iq = iq
        self.eq = eq
        self.st = st
        self.score = score
        self.timed = timed
        self.require = require
        self.risk = risk

    def print(self, index: int = 0):
        print(f"{index}. {self.title}\n{self.des}\n")

    def __str__(self):
        return f"{self.title}\n{self.des}"

tasks = {
    "daybreak_training": Task(
        id = "daybreak_training",
        title = "早操",
        des = "清晨操练，精力 - 25，获得一点点体能，加一点点分",
        timed = (1, ), # (, )
        eng = -25,
        st = 1,
        score = 1,
        risk = [("", "training_e1", "training_e2", "training_e3", "injury"), (11, 3, 3, 2, 1)],
    ),
    "training": Task(
        id = "training",
        title = "站军姿",
        des = "日常训练，精力 - 30，获得一点点体能，加一点点分",
        timed = (2, 4), # (6, )
        eng = -30,
        st = 1,
        score = 1,
        require = lambda pl: pl.st < 32 and not pl.dis,
        risk = [("", "training_e1", "training_e2", "training_e3", "injury"), (12, 2, 3, 2, 1)],
    ),
    
    "training_2": Task(
        id = "training_2",
        title = "踢正步",
        des = "日常训练，精力 - 35，获得少许体能，加一点点分",
        timed = (2, 4), 
        eng = -35,
        st = 2,
        score = 1,
        require = lambda pl: pl.st >= 15 and not pl.dis,
        risk = [("", "training_e1", "training_e2", "training_e3", "injury"), (12, 2, 3, 2, 1)],
    ),
    "training_3": Task(
        id = "training_3",
        title = "军体拳",
        des = "日常训练，精力 - 50，获得一些体能，加一点分",
        timed = (2, 4), 
        eng = -40,
        st = 3,
        score = 2,
        require = lambda pl: pl.st >= 32 and not pl.dis,
        risk = [("", "training_e1", "training_e2", "training_e3", "injury"), (11, 2, 3, 2, 2)],
    ),
    "chorus": Task(
        id = "chorus",
        title = "练合唱",
        des = "心情 + 1，理智 - 1，精力 - 20, 加一点点分",
        timed = (2, 4, 6),
        mood = 1,
        san = -1,
        eng = -20,
        score = 1,
        require = lambda pl: "Chorus" in pl.states,
        risk = [("", "chorus_e1"), (9, 1)],
    ),
    "lecture": Task(
        id = "lecture",
        title = "听讲座",
        des = "安排了讲座，听就完了。无事发生，数值不变。",
        timed = (6, ), # (2, 4),
        require = lambda pl: not "Chorus" in pl.states,
        risk = [("", "lecture_e1", "lecture_e2", "lecture_e3"), (1, 2, 3, 3)],
    ),
}

high_temp_nap = Task(
    id = "high_temp_nap",
    title = "小憩",
    des = "今天没早训，浅浅睡会儿，心情、理智 + 5，精力 + 20",
    timed = (1,),
    mood = 5,
    san = 5,
    eng = 20,
)

injury = Task(
    id = "injury",
    title = "守水瓶",
    des = "坐在阴凉处守水瓶，精力 - 10，加一点点分数",
    timed = (2, 4),
    eng = -10,
    score = 1,
)

tasks_self = {
    "nap": Task(
        id = "nap",
        title = "小憩",
        des = "浅浅睡会儿，心情、理智 + 5，精力 + 20",
        timed = (3, 5), # (1, 3, 5)
        mood = 5,
        san = 5,
        eng = 20,
        risk = [("", "be_late"), (19, 1)],
    ),
    "nightsleep": Task(
        id = "nightsleep",
        title = "睡觉",
        des = "安心睡觉，精力 + 70",
        timed = (7, ),
        eng = 70,
        risk = [("", "be_late"), (19, 1)],
    ),
    "videogame": Task(
        id = "videogame",
        title = "玩电脑",
        des = "心情 + 35，理智 - 10，精力 - 15",
        timed = (3,5,7),
        mood = 35,
        san = -10,
        eng = -15,
    )
}

tasks_lianbu = {
    "work": Task(
        id = "work",
        title = "写稿子",
        des = "心情 - 5，理智 - 10，精力 - 20，提升一点点智力，获得一点点分数",
        timed = (2, 3, 4, 5, 6, 7),
        iq = 1,
        score = 1,
        mood = -5,
        san = -10,
        eng = -20,
    ),
    "sleep": Task(
        id = "sleep",
        title = "趴桌上睡觉",
        des = "心情、理智 + 10，精力 + 15",
        timed = (2, 3, 4, 5, 6, 7),
        mood = 10,
        san = 10,
        eng = 15,
        risk = [("", "lianbu_risk"), (99, 1)],
    ),
    "fish": Task(
        id = "fish",
        title = "摸鱼刷 98",
        des = "心情 + 10，精力 - 5，提升一点点情商",
        timed = (2, 3, 4, 5, 6, 7),
        mood = 10,
        eng = -5,
        eq = 1,
    ),
    "work_2": Task(
        id = "work_2",
        title = "高技术力制作",
        des = "心情 + 10，理智 - 20，精力 - 40，提升少许智力，获得少许分数",
        timed = (2, 3, 4, 5, 6, 7),
        mood = 10,
        san = -20,
        eng = -40,
        iq = 2,
        score = 2,
        require = lambda pl: pl.iq >= 110,
    ),
    "sleep_2": Task(
        id = "sleep_2",
        title = "倒连部沙发上睡觉",
        des = "心情、精力、理智 + 30，提升一点点智力",
        timed = (2, 3, 4, 5, 6, 7),
        iq = 1,
        mood = 30,
        san = 30,
        eng = 30,
        require = lambda pl: pl.iq >= 104 and pl.eq >= 106,
        risk = [("", "lianbu_risk"), (9, 1)],
    ),
    "study_2": Task(
        id = "study_2",
        title = "悄悄提前内卷高数线代四六级",
        des = "心情 - 30，理智 + 30，精力 - 30，提升一些智力",
        timed = (2, 3, 4, 5, 6, 7),
        iq = 3,
        mood = -30,
        san = 30,
        eng = -30,
        require = lambda pl: pl.iq >= 116,
    ),
    "fish_2": Task(
        id = "fish_2",
        title = "连部聊天",
        des = "心情 + 30，理智 - 10，精力 - 20，提升少许情商",
        timed = (2, 3, 4, 5, 6, 7),
        eq = 2,
        mood = +30,
        san = -10,
        eng = -20,
        require = lambda pl: pl.eq >= 118,
    ),
    "work_3": Task(
        id = "work_3",
        title = "制作 3A 大作",
        des = "理智 - 50，精力 - 90，提升一些智力，获得大量分数",
        timed = (2, 3, 4, 5, 6, 7),
        iq = 3,
        score = 8,
        san = -50,
        eng = -90,
        require = lambda pl: pl.iq >= 128,
    ),
    "fish_3": Task(
        id = "fish_3",
        title = "连部 K 歌",
        des = "心情 + 50，理智 + 10，精力 - 30，提升大量情商",
        timed = (2, 3, 4, 5, 6, 7),
        eq = 5,
        mood = 50,
        san = 10,
        eng = -30,
        require = lambda pl: pl.eq >= 125,
        risk = [("", "lianbu_risk"), (9, 1)],
    )
}

lack_sleep = Task(
    id = "lack_sleep",
    title = "LackSleep",
    des = "RT",
    timed = (7, ),
    mood = -10,
    san = -20,
    eng = -30,
)