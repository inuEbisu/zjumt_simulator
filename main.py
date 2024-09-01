import task as t
import misc as m
import player as p
import event as e
import random as r

# Init
m.cls()

player = p.Player(0, 0, 0, 0)

name = input("你的名字是: ")
namel = name.lower()

m.cls()

if namel == "frisk" or namel == "chara": # caidan
    player = p.cheat_player()
else:
    player = p.rand_player()

player.name = name

m.cls()

print(f"{player.name}，欢迎来到浙江大学！")
print("为期 21 天的军事训练，你可准备好？")
input("按任意键继续……")

high_temp = r.choices([True, False], [1, 4], k = 21)

timestamp = 0

m.cls()

# Event Init

events = e.events
events = sorted(events, key = lambda e: e.time)

occasionals = e.occasionals

# A Day
while timestamp <= e.s(21, 7):
    # Day Start
    time = e.s2t(timestamp)

    player.health = min(player.health + 1, 100)
    player.dis = -1 if player.dis == -1 else max(player.dis - 1, 0)

    # Events
    while True:
        if not events: break
        event = events[0]
        if not timestamp == event.time: break 

        events.pop(0)
        if not event.require(player): continue
        
        m.cls()
        print(str(event))

        if event.type == 0:
            if not input("输入 Y 做，输入其他不做") == "Y": continue
        else:
            input("按任意键继续。")

        suc = player.do_event(event)
        if suc:
            print("成功！")
            print(event.suc_msg)
        else:
            print("出了点差错？")
            print(event.fail_msg)
        input("按回车键继续……")
        m.cls()
    
    # Tasks

    e.print_time(timestamp)
    player.print_stat()

    ## Random
    tasks: dict[str, t.Task] = dict()

    if high_temp[time[0] - 1]:
        print("今日高温作息！白天不训晚上训。")
        t.tasks["daybreak_training"].timed = ()
        t.tasks["training"].timed = (6, )
        t.tasks["training_2"].timed = (6, )
        t.tasks["training_3"].timed = (6, )
        t.tasks["lecture"].timed = (2, 4)
        t.injury.timed = (6, )
        tasks.update({"high_temp_nap": t.high_temp_nap})
    else:
        print("今日正常作息！")
        t.tasks["daybreak_training"].timed = (1, )
        t.tasks["training"].timed = (2, 4)
        t.tasks["training_2"].timed = (2, 4)
        t.tasks["training_3"].timed = (2, 4)
        t.tasks["lecture"].timed = (6, )
        t.injury.timed = (1, 2, 4, )
        tasks.update({"daybreak_training": t.tasks["daybreak_training"]})

    if "Lianbu" in player.states:
        tasks.update(t.tasks_lianbu)
        tasks.update({"chorus": t.tasks["chorus"]})
    else:
        tasks.update(t.tasks)

        if player.dis:
            tasks.update({"injury": t.injury})

    tasks.update(t.tasks_self)

    tasks_2: dict[str, t.Task] = dict()
    for key, value in tasks.items():
        if not time[1] in value.timed:
            continue
        if not value.require(player):
            continue
        tasks_2.update({key: value})

    rkeylist: list[str] = []

    rkeylist = list(tasks_2.keys())
    if len(tasks_2) > 5:
        rkeylist = r.sample(rkeylist, k = 5)

    tasks_3: dict[str, t.Task] = dict()
    for key in rkeylist:
        tasks_3.update({key: tasks_2[key]})

    tasklist = list(tasks_3.values())
    for i, task in enumerate(tasklist):
        task.print(i + 1)
    
    ## Do
    while True:
        try:
            selected_index = int(input("决定要做的事情（写序号）：")) - 1
            if not 0 <= selected_index <= len(tasklist) - 1:
                if selected_index == 8: # input = 9
                    break
                raise Exception()
            break
        except KeyboardInterrupt as e:
            raise e
        except:
            print("无效输入。")

    if not selected_index == 8:
        selected_task = tasklist[selected_index]
        player.do_task(selected_task)

    # Time Finale

    if time[1] == 7 and not selected_task.id == "nightsleep":
        print("晚上好好睡觉，不要乱搞！随便找地儿睡也不行！\n精力 - 30")
        player.do_task(t.lack_sleep)
        input("按回车键继续……")

    if player.mood <= 0:
        player.health -= min(50 - player.st // 8, 20)
    if player.san <= 0:
        player.health -= min(50 - player.st // 8, 20)
    if player.eng <= 0:
        player.health -= min(50 - player.st // 8, 20)

    timestamp += 1
    m.cls()
    
    if player.health <= 0:
        print("你寄了！\n死因：", end="")
        if player.mood <= 0:
            print("玉玉紫砂")
        elif player.san <= 0:
            print("疯了")
        else:
            print("猝死")
        break

else:
    print(
        f"{player.name} 圆满完成了 21 天的浙大军训。",
        f"得分：{player.score}",
        f"绩点：{m.gp_calc(player.score)}"
    )

input("按回车键退出……")