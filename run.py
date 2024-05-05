# -*- coding:utf-8 -*-
# import dnf
import km
import time
import yaml
import random
import datetime

labels, game_box = {}, ()


# 跑步
def running(direction, t):
    km.release_all()
    km.key_press_and_release(direction)
    km.key_press(direction, t)
    km.release_all()


# 计算中心坐标
def center(xyxy):
    center_x = int((xyxy[0] + xyxy[2]) / 2)
    center_y = int((xyxy[1] + xyxy[3]) / 2)
    return center_x, center_y


# 移动点击
def move_click(forget, *w):
    forget = list(forget)[0]
    x, y = center(labels[forget])
    game_x, game_y = game_box[2] - game_box[0], game_box[3] - game_box[1]
    # 坐标调整x横轴y纵轴
    if 'NPC' in forget and 1 in w:
        x -= game_x * 0.25
        y += game_y * 0.25
    km.mouse_move(x + game_box[0], y + game_box[1])
    if '物品栏' in forget:
        return
    km.mouse_click(1)
    time.sleep(0.3)


# 关闭0点弹窗
def close_0():
    km.mouse_move((game_box[2] - game_box[0]) * 0.5 + game_box[0],
                  (game_box[3] - game_box[1]) * 0.76 + game_box[1])
    km.mouse_click(1)



def run(labels_, game_box_, h):

    # 读取本地快捷键
    with open('info.yaml', 'r') as f:
        data = yaml.safe_load(f)
        move_key = data['move_key']
        again_key = data['again_key']
        return_key = data['return_key']
        move_fighter = data['move_fighter']
        skill = data['skill']
        three = data['three']

    # 副本内无角色
    if not labels_ and 'START' in data[(str(h)+'_MARK')]:
        km.key_press(random.choice(['X', 'A']), random.uniform(0.5, 1.5))
        km.key_press('Up', random.uniform(0.5, 1))
        return

    # 标签识别
    global labels, game_box
    labels, game_box = labels_, game_box_
    set_labels = set(list(labels_.keys()))
    npc = {'NPC'} & set_labels
    treasury = {'账号金库'} & set_labels
    gold_key = {'存入金币'} & set_labels
    backpack = {'物品栏'} & set_labels
    finishing = {'整理'} & set_labels
    soul = {'灵魂之源'} & set_labels
    fly = {'飞空艇'} & set_labels
    move_fly = {'移动飞艇'} & set_labels
    move_storm = {'移动风暴'} & set_labels
    map1 = {'圣殿副本'} & set_labels
    map2 = {'风暴副本'} & set_labels
    fighter = {'角色'} & set_labels
    first_map = {'初始怪物'} & set_labels
    wait_door = {'等待入口'} & set_labels
    door = {'开启入口'} & set_labels
    goods = {'史诗装备'} & set_labels
    die = {'角色死亡'} & set_labels
    cracks = {'神秘裂缝'} & set_labels
    cracks_map = {'裂缝地面'} & set_labels
    boss = {'领主'} & set_labels
    card = {'翻牌奖励'} & set_labels
    again = {'再次挑战'} & set_labels
    machine = {'分解机'} & set_labels
    machine_page = {'分解页面'} & set_labels
    miya = {'通讯器'} & set_labels
    day_icon = {'每日图标'} & set_labels
    day_get = {'每日领取'} & set_labels
    day_task = {'每日任务'} & set_labels
    choice1 = {'选择角色'} & set_labels
    choice2 = {'返回城镇'} & set_labels
    data_mark = data[(str(h)+'_MARK')]

    # 本地写入数据
    def write(msg):
        with open('info.yaml', 'a+') as ff:
            ff.seek(0)
            dd = yaml.safe_load(ff)
            ll = dd[str(h) + '_MARK']
            if msg not in ll:
                ll.append(msg)
                dd.update({str(h) + '_MARK': ll})
            ff.truncate(0)
            yaml.dump(dd, ff)
        
    # 6点重置
    if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0:
        if choice1:
            move_click(choice1)
        elif not choice1 and not set_labels & (npc | fly):
            km.key_press_and_release('Esc')
            print('每日6点重置')
            return

    # 护盾
    if 'START' not in data_mark and set_labels & (wait_door | first_map):
        write('START')
        write('BUFF')
        km.key_press_and_release(skill)

    # 一次点击
    if npc and 'SOUL' not in data_mark:
        move_click(npc)
        km.KM.MoveMouseRelative(35, 35)
        km.mouse_click(1)
        write('SOUL')
    # 二次点击
    elif npc and not treasury:
        if not fighter:
            time.sleep(60)
            return
        move_click(npc, 1)
        x = (game_box[0]) + random.randint(1, 100)
        y = (game_box[1]) + random.randint(1, 100)
        km.mouse_move(int(x), int(y))
        # 通关次数重置
        with open('info.yaml', 'r+') as f:
            data = yaml.safe_load(f)
            data[h] = 0
            f.seek(0)
            f.truncate()
            yaml.dump(data, f)
            print('通关次数重置', data[h])
    # 兑换灵魂之源
    elif soul:
        km.KM.PressKey('Shift')
        move_click(soul)
        km.KM.ReleaseKey('Shift')
        for k in ['4', '0', 'Enter', 'Space', 'Esc']:
            km.key_press(k)
    # 仅物品栏页面
    elif len(set_labels) == 2 and backpack and finishing:
        km.key_press_and_release('Esc')
    # 账号金库
    elif treasury and not gold_key:
        move_click(treasury)
    # 存入金币
    elif gold_key:
        move_click(treasury)
        move_click(gold_key)
        move_click(gold_key)
        km.key_press('a')
        km.key_press('Space')
        if backpack and finishing:
            forget = list(backpack)[0]
            x, y = center(labels[forget])
            km.mouse_move(x + game_box[0], y + game_box[1] + 30)
            km.mouse_click(1)
            move_click(finishing)
        km.key_press('Esc')
        km.key_press('Down', 1)
        km.key_press_and_release('5')
        return
    # 飞空艇
    elif fly:
        move_click(fly)
        time.sleep(0.5)
        km.key_press_and_release('Space')
        km.key_press('Left', 8)
    # 移动风暴
    elif move_storm:
        pass
        move_click(move_storm)
        km.key_press('Right', 5)
    # 圣殿-风暴
    elif map1 or map2:
        map0 = map1 if map1 else map2
        move_click(map0)
        time.sleep(1)
        km.mouse_click(1)
        km.key_press_and_release('Space')
        for i in range(random.randint(2, 4)):
            time.sleep(0.5)
        km.key_press_and_release(return_key)
    # 无分解机
    elif miya and day_icon and not set_labels & (machine | day_task):
        if data[h] < 26:
            if 'PL' not in data_mark:
                write('PL')
                print('通关次数不足1111111111111111', data[h], '正在重新进入副本...')
                km.key_press('Left', 0.5)
                km.key_press('Right', 2)
                return
            else:
                data[h] = 26
                print('通关次数不足1111111111111111', data[h], '重新进入副本失败---------')
        if data[h] >= 26:
            km.key_press('Left', 3)
    # 分解机
    elif machine and 'MACHINE' not in data_mark:
        if not miya:
            close_0()
        if not day_icon:
            km.key_press('Esc')
            return
        # 次数检测
        if data[h] < 26:
            if 'PL' not in data_mark:
                write('PL')
                print('通关次数不足', data[h], '正在重新进入副本...')
                km.key_press('Right', 0.5)
                km.key_press('Left', 2)
                return
            else:
                data[h] = 26
                print('通关次数不足', data[h], '重新进入副本失败---------')
        if data[h] >= 26:
            open_machine(machine)
            write('MACHINE')
    # 分解装备
    elif machine_page:
        if not backpack:
            km.key_press_and_release('Esc')
            # 删除分解机标记
            with open('info.yaml', 'r+') as f:
                data = yaml.safe_load(f)
                data[(str(h)+'_MARK')].remove('MACHINE')
                f.seek(0)
                f.truncate()
                yaml.dump(data, f)
            return
        # 关闭提示框
        km.key_press('Space')
        # 定位装备栏位置
        forget = list(backpack)[0]
        x, y = center(labels[forget])
        game_x, game_y = game_box[2] - game_box[0], game_box[3] - game_box[1]
        x = x + game_x * 0.01
        km.mouse_move(x + game_box[0], y + game_box[1])
        # 移动鼠标到装备第一行
        km.KM.MoveMouseRelative(-60, 60)
        for i in range(1, 17):
            km.KM.MoveMouseRelative(30, 0)
            km.mouse_click(1)
            time.sleep(0.2)
            if i % 8 == 0:
                km.KM.MoveMouseRelative(-120, 15)
                km.KM.MoveMouseRelative(-120, 15)
        km.key_press_and_release('Space')
        time.sleep(0.2)
        km.KM.MoveMouseRelative(-40, 0)
        km.mouse_click(1)
        time.sleep(3)
        km.key_press_and_release('Esc')
        # 随机发言
        km.key_press_and_release(13)
        km.key_press_and_release(9)
        time.sleep(0.2)
        instr = random.choice(['1', '2', '3', '4', '5', '6', '7'])
        km.KM.InputString(instr)
        km.key_press_and_release(13)
        time.sleep(0.2)
    # 每日领取
    elif day_get:
        move_click(day_get)
    # 每日任务
    elif day_task and not day_get:
        km.key_press_and_release('Esc')
        time.sleep(0.2)
        km.key_press_and_release('Esc')
    # 每日图标
    elif day_icon and not day_task:
        move_click(day_icon)
    # 关闭未知页面
    elif backpack and wait_door:
        km.key_press_and_release('Esc')
    # 初始图
    elif first_map and wait_door or die:
        km.release_all()
        if die:
            km.key_press_and_release(221)
            km.key_press_and_release('x')
            km.key_press_and_release('Space')
            km.key_press_and_release(skill)
        random_keys = random.sample(['W', 'E', 'A', 'S', 'D', 'F'], 2)
        [km.key_press(key, random.uniform(1, 2)) for key in ['Q'] + random_keys]
        running('Right', 2)
    # 通关结束
    elif card or again:
        if card:
            km.key_press_and_release('Esc')
        # 再次挑战后，增加通关次数, 删除无效目录, 出售装备/施放技能
        if data_mark:
            km.key_press_and_release(move_key)
            time.sleep(0.2)
            for i in range(2):
                km.key_press_and_release(221)
                km.key_press_and_release('x')
                time.sleep(0.2)
            time.sleep(0.3)
            km.key_press_and_release(again_key)
            sell()
            km.key_press_and_release(again_key)
            km.key_press_and_release(return_key)
            with open('info.yaml', 'r+') as f:
                data = yaml.safe_load(f)
                data[h] += 1
                data['all_times'] += 1
                data[(str(h)+'_MARK')] = []
                f.seek(0)
                f.truncate()
                yaml.dump(data, f)
                print('通关次数+1, 当前角色通关%s次' % data[h], '累计通关%s次' % data['all_times'])
        else:
            km.key_press('i')
            km.key_press_and_release('Esc')
            km.key_press_and_release(221)
            km.key_press_and_release('x')
            time.sleep(0.2)
            km.key_press_and_release(again_key)
            km.key_press_and_release(return_key)
    # 移动时缺少角色
    elif not fighter and set_labels & (goods | door | wait_door):
        km.key_press(random.choice(['Z', 'Q', 'W', 'E', 'A', 'S', 'D',]))
        km.key_press(random.choice(['Up', 'Down', 'Left', 'Right']), random.uniform(0.5, 1.5))
    # 拾取金币或装备
    elif goods:
        g = goods
        if backpack and finishing:
            km.key_press_and_release('Esc')
        if fighter:
            move(list(fighter)[0], list(g)[0])
        else:
            km.key_press('Up', random.uniform(0.5, 1))
    # 等待入口
    elif wait_door:
        if random.random() < 0.2:
            km.key_press(random.choice(['Z', 'Q', 'W', 'E', 'A', 'S', 'D',]))
        if fighter:
            km.key_press(random.choice(['Q', 'W', 'E', 'A', 'S', 'D', 'F', 'G']), random.uniform(0.5, 1))
            forget = list(fighter)[0]
            fx, fy = center(labels[forget])
            if fx > (game_box[2] - game_box[0]) * 0.8:
                running('Left', random.uniform(1.3, 1.9))
                return
            move(list(fighter)[0], list(wait_door)[0])
    # 入口
    elif door and not miya:
        if cracks:
            print('================神秘裂缝开始=================')
            km.key_press_and_release(move_fighter)
            time.sleep(0.2)
            km.key_press_and_release('Space')
            km.key_press('Down', 1)
            running('Right', 4)
            km.key_press('Up',0.7)
            time.sleep(3)
            print('================神秘裂缝结束=================')
        elif fighter:
            forget = list(fighter)[0]
            fx, fy = center(labels[forget])
            forget_door = list(door)[0]
            dx, dy = center(labels[forget_door])
            if fx > (game_box[2] - game_box[0]) * 0.8:
                km.key_press('a')
                km.key_press('Left', random.uniform(0.3, 0.6))
                km.key_press('Right',random.uniform(0.6, 0.9))
                direction = 'Down' if fy < dy else 'Up'
                km.key_press(direction, random.uniform(0.7, 1))
                return
            move(list(fighter)[0], list(door)[0])
    # 裂缝内部
    elif cracks and cracks_map:
        if fighter:
            move(list(fighter)[0], list(cracks)[0])
        else:
            km.key_press_and_release('Esc')
    # 领主
    elif boss:
        random_keys = random.sample(['Q', 'W', 'E', 'R', 'A', 'S', 'D', 'F', 'G'], 3)
        [km.key_press(key, random.uniform(0.8, 2)) for key in [three] + random_keys]
    # 选择角色
    elif choice1:
        km.key_press_and_release('Esc')
        time.sleep(0.5)
        from email_qq import send_mail
        import pyautogui
        image = pyautogui.screenshot()
        image.save(f'{game_box}.jpg')
        send_mail(email_to=data['qqmail'], email_title='备注为【' +data['This']+ '】更换角色。次数%d,%d。' % (data[h], data['all_times']), email_image=f'{game_box}.jpg')
        km.key_press_and_release('Esc')
        time.sleep(1)
        move_click(choice1)
        time.sleep(3)
        default_direction = 'Right'
        # 选择角色
        if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0:
            for i in range(5):
                km.key_press_and_release('Up')
                time.sleep(0.2)
            km.key_press_and_release('Space')
            time.sleep(5)
            return
        km.key_press_and_release(default_direction)
        km.key_press_and_release('Space')
        time.sleep(5)
    # 返回城镇
    elif choice2 and not again:
        move_click(choice2)
        km.key_press_and_release('Space')
        with open('info.yaml', 'a+') as f:
            f.seek(0)
            data = yaml.safe_load(f)
            data.update({'SLEEP_%s' % h: int(time.time())})
            f.truncate(0)
            yaml.dump(data, f)
            print('--------------返回城镇-------------------')
    # 通讯器
    elif miya and not machine:
        km.key_press_and_release('m')
        time.sleep(0.5)
        km.key_press_and_release('Esc')
    # 仅角色
    elif len(labels) == 1 and fighter and 'BOSS' not in data_mark and 'START' in data_mark:
        random_direction = ['Left', 'Right']
        running(random_direction, random.uniform(0.5, 1.5))
        forget = list(fighter)[0]
        fx, fy = center(labels[forget])
        game_x = game_box[2] - game_box[0]
        if fx < game_x * 0.3:
            km.key_press('a')
            running('Right', random.uniform(1.5, 2))
        elif fx < game_x * 0.6:
            running('Right', random.uniform(1.5, 2))
        elif fx > game_x * 0.8:
            running('Left', random.uniform(0.5, 1))


# 出售
def sell():
    km.key_press('a')
    km.key_press_and_release('Space')
    km.key_press_and_release('Left')
    km.key_press_and_release('Space')
    km.key_press_and_release('m')
    km.key_press_and_release('Esc')


# 分解
def open_machine(machine):
    move_click(machine)
    km.key_press_and_release('Down')
    km.key_press_and_release('Down')
    km.key_press_and_release('Space')
    time.sleep(0.5)
    x = (game_box[0]) + random.randint(1, 100)
    y = (game_box[1]) + random.randint(1, 100)
    km.mouse_move(int(x), int(y))


# 移动
def move(f1, f2):
    # km.KM.ReleaseAllKey()
    f1x, f1y = center(labels[f1])
    f2x, f2y = center(labels[f2])
    if '入口' in f2:
        f2x = game_box[2] - game_box[0] + 300
    if '等待入口' in f2:
        f2x -= 300
    x_direction = 'Right' if f1x < f2x else 'Left'
    y_direction = 'Down' if f1y < f2y else 'Up'
    x_time = abs(f1x - f2x) / 300
    y_time = abs(f1y - f2y) / 400

    t = time.time()
    km.KM.ReleaseAllKey()
    if '入口' in f2:
        x_direction = 'Right'
        km.key_press_and_release(x_direction)
        time.sleep(0.33)
    while 1:
        km.KM.PressKey(x_direction)
        # km.KM.PressKey(y_direction)
        if time.time() - x_time >= t:
            if '入口' in f2:
                km.key_press_and_release(random.choice([88, 'z']))
            km.KM.ReleaseKey(x_direction)
        if f2 in ['史诗装备'] and time.time() - y_time >= t or abs(f1y - f2y) > 50:
            km.key_press(y_direction, random.uniform(0.1, 0.5))
        if time.time() - max(x_time, y_time) >= t:
            km.KM.ReleaseAllKey()
            km.release_all()
            break
