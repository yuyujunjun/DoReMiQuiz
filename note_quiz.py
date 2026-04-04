import random

# 三种音名（大调自然排列，从C开始）
letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
numbers = ['1', '2', '3', '4', '5', '6', '7']
# 我用 si（或 xi）表示第七音，根据你的习惯可以改成'xi'
solfege = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']

# intervals[i] 表示 度 i -> 度 i+1 的间隔（大调）
# 顺序对应 degrees: 1->2, 2->3, 3->4, 4->5, 5->6, 6->7, 7->1
intervals = ['全音', '全音', '半音', '全音', '全音', '全音', '半音']

# 吉他指板音程规律（从低弦到高弦）
# 相邻弦之间的音程：3-2弦是大三度(4半音)，其他都是纯四度(5半音)
guitar_interval_up = {6: 5, 5: 5, 4: 4, 3: 5, 2: 5, 1: 5}  # 弦号 -> 往上到相邻弦的半音数
guitar_interval_down = {6: 5, 5: 5, 4: 5, 3: 4, 2: 5, 1: 5}  # 弦号 -> 往下到相邻弦的半音数

# 吉他调弦（从6弦到1弦，空弦音）
guitar_strings = ['E', 'A', 'D', 'G', 'B', 'E']  # 标准调弦

# 音符到半音数的映射（以C为0）
note_to_semitone = {
    'C': 0, 'C#': 1, 'Db': 1,
    'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5,
    'F#': 6, 'Gb': 6,
    'G': 7, 'G#': 8, 'Ab': 8,
    'A': 9, 'A#': 10, 'Bb': 10,
    'B': 11
}

# 半音数到音符的映射（不带升降号）
semitone_to_note = ['C', 'C', 'D', 'D', 'E', 'F', 'F', 'G', 'G', 'A', 'A', 'B']

def note_to_index(note):
    """将音符转换为0-11的半音数"""
    return note_to_semitone.get(note, 0)

def index_to_note(semitone):
    """将半音数转换为音符（优先使用升号）"""
    normalized = semitone % 12
    # 升号形式映射
    sharp_names = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
    return sharp_names[normalized]

def get_fret_positions(note):
    """获取一个音在吉他指板上的所有位置"""
    semitone = note_to_index(note)
    positions = []

    for string_idx, open_note in enumerate(guitar_strings):
        open_semitone = note_to_index(open_note)
        # 遍历0-11品（12品以上是更高八度，不常用）
        for fret in range(12):
            fret_semitone = (open_semitone + fret) % 12
            if fret_semitone == semitone:
                positions.append((string_idx + 1, fret))  # 弦号从6开始

    return positions

def get_neighbors(idx):
    left = (idx - 1) % 7
    right = (idx + 1) % 7
    return left, right

def show_answer(idx):
    left, right = get_neighbors(idx)
    # 左邻 -> 当前 的间隔是 intervals[left] （因为 left -> left+1 == current）
    left_interval = intervals[left]
    # 当前 -> 右邻 的间隔是 intervals[idx] （因为 current -> current+1 == right）
    right_interval = intervals[idx]

    print(f"✅ 对应（字母, 数字, 唱名）： {letters[idx]} , {numbers[idx]} , {solfege[idx]}")
    print(f"⬅ 左边的音：{letters[left]} / {numbers[left]} / {solfege[left]} （{left_interval}：{letters[left]} → {letters[idx]}）")
    print(f"➡ 右边的音：{letters[right]} / {numbers[right]} / {solfege[right]} （{right_interval}：{letters[idx]} → {letters[right]}）")

def quiz_single():
    while True:
        mode = random.choice(['letters', 'numbers', 'solfege'])
        idx = random.randrange(7)
        if mode == 'letters':
            prompt = letters[idx]
        elif mode == 'numbers':
            prompt = numbers[idx]
        else:
            prompt = solfege[idx]
        print(f"\n🎼 题目（记法：{mode}）： {prompt}")
        user_input = input("👉 思考并回答（按回车显示答案，q返回主菜单）...")
        if user_input.lower() == 'q':
            break
        show_answer(idx)

def quiz_multiple():
    """多音符练习（仿真谱训练）"""
    while True:
        mode = random.choice(['letters', 'numbers', 'solfege'])
        length = random.randint(3, 7)
        seq_indices = [random.randint(0, 6) for _ in range(length)]

        if mode == 'letters':
            seq = [letters[i] for i in seq_indices]
        elif mode == 'numbers':
            seq = [numbers[i] for i in seq_indices]
        else:
            seq = [solfege[i] for i in seq_indices]

        print("\n🎶 多音符练习（记法：{}）".format(mode))
        print("谱面： " + " ".join(seq))
        user_input = input("👉 请尝试念出对应的唱名或数字，按回车查看答案（q返回主菜单）...")
        if user_input.lower() == 'q':
            break

        print("\n✅ 对照答案：")
        for i in seq_indices:
            print(f"{letters[i]:<2}  {numbers[i]:<2}  {solfege[i]}")
        print("（顺序：字母  数字  唱名）")

def quiz_guitar_find_positions():
    """模式1：给音名，找出在指板上的所有位置"""
    while True:
        note = random.choice(letters)
        positions = get_fret_positions(note)

        print(f"\n🎸 吉他指板测验 - 找音位")
        print(f"题目：{note} 音在指板上的位置？")
        user_input = input("👉 思考并回答（按回车显示答案，q返回主菜单）...")
        if user_input.lower() == 'q':
            break

        print(f"\n✅ {note} 音位置：")
        # 按弦号从6到1排序
        positions.sort(key=lambda x: (-x[0], x[1]))
        for string_num, fret in positions:
            if fret == 0:
                print(f"  - {string_num}弦 空弦")
            else:
                print(f"  - {string_num}弦 {fret}品")

def quiz_guitar_find_note():
    """模式2：给位置，说出音名"""
    while True:
        # 随机选择弦和品
        string_num = random.randint(1, 6)  # 1-6弦
        fret = random.randint(0, 11)       # 0-11品

        # 计算该位置的音名（弦号1-6对应数组索引5-0）
        open_note = guitar_strings[6 - string_num]
        open_semitone = note_to_index(open_note)
        note = index_to_note(open_semitone + fret)

        print(f"\n🎸 吉他指板测验 - 猜音名")
        print(f"题目：{string_num}弦 {fret if fret > 0 else '空弦'} 是什么音？")
        user_input = input("👉 思考并回答（按回车显示答案，q返回主菜单）...")
        if user_input.lower() == 'q':
            break

        print(f"\n✅ 答案：{string_num}弦 {fret if fret > 0 else '空弦'} = {note} 音")

def quiz_guitar_mixed():
    """模式3：混合模式（循环出题）"""
    while True:
        if random.choice([True, False]):
            quiz_guitar_find_positions()
        else:
            quiz_guitar_find_note()

def quiz_guitar_interval():
    """模式4：最近路径推算（实用弹奏思维）"""
    while True:
        # 随机选择起始位置（中间把位）
        start_string = random.randint(2, 5)
        start_fret = random.randint(2, 7)

        # 计算起始音
        start_note_idx = note_to_index(guitar_strings[6 - start_string])
        start_semitone = (start_note_idx + start_fret) % 12
        start_note = index_to_note(start_semitone)

        # 随机选择常用音程（2-5品内）
        intervals_2to5 = [
            (2, '大二度'),   # 2品
            (3, '小三度'),   # 3品
            (4, '大三度'),   # 4品
            (5, '纯四度'),   # 5品
        ]
        interval, interval_name = random.choice(intervals_2to5)

        target_semitone = (start_semitone + interval) % 12
        target_note = index_to_note(target_semitone)

        # 计算同弦方案
        same_string_steps = interval

        # 计算跨弦方案（往上、往下）
        up_string = start_string - 1  # 更高（更细）的弦
        down_string = start_string + 1  # 更低（更粗）的弦

        # 往上跨弦（细弦）：原弦+品数，然后跨到上一弦同品
        if up_string >= 1:
            # 在上一弦找目标音需要多少品
            up_string_open = guitar_strings[6 - up_string]
            up_open_semitone = note_to_index(up_string_open)
            # 目标音在上弦的品数 = 目标半音 - 上弦空弦半音
            target_fret_up = (target_semitone - up_open_semitone) % 12
            if target_fret_up <= 7:  # 品数合理
                up方案 = (f"跨{up_string}弦", target_fret_up)

        # 往下跨弦（粗弦）
        if down_string <= 6:
            down_string_open = guitar_strings[6 - down_string]
            down_open_semitone = note_to_index(down_string_open)
            target_fret_down = (target_semitone - down_open_semitone) % 12
            if target_fret_down <= 7:
                down方案 = (f"跨{down_string}弦", target_fret_down)

        print(f"\n🎸 找最近音位")
        print(f"你按着 {start_string}弦 {start_fret}品 = {start_note}，")
        print(f"要用另一个手指弹出 {interval_name} → {target_note}，怎么走最近？")
        user_input = input("👉 思考后按回车看答案（q返回）...")
        if user_input.lower() == 'q':
            break

        print(f"\n✅ 最近方案：")
        print(f"  ▶ 同弦移动：按 {start_string}弦 {start_fret + same_string_steps}品")
        print(f"    （食指不动，中指往上走{interval}格）")

        # 检查跨弦是否更近
        better_found = False
        if up_string >= 1 and target_fret_up <= 7:
            if target_fret_up < same_string_steps:
                print(f"  ▶ 跨弦上行：换到 {up_string}弦 {target_fret_up}品")
                print(f"    （食指松开，小指横移到{up_string}弦）")
                better_found = True
        if down_string <= 6 and target_fret_down <= 7:
            if target_fret_down < same_string_steps:
                print(f"  ▶ 跨弦下行：换到 {down_string}弦 {target_fret_down}品")
                print(f"    （食指松开，横移到{down_string}弦）")
                better_found = True

        if not better_found:
            print(f"\n💡 同弦最方便，不需要换弦")

def main():
    print("请选择练习类型：")
    print("1=单音练习，2=多音谱训练，3=吉他指板记忆，q=退出")
    while True:
        mode = input("选择模式：").strip().lower()
        if mode == '1':
            quiz_single()
        elif mode == '2':
            quiz_multiple()
        elif mode == '3':
            while True:
                guitar_sub_mode = input("吉他测验：1=记音名→找位置，2=记位置→猜音名，3=混合模式，4=同弦推算，b=返回主菜单：").strip()
                if guitar_sub_mode.lower() == 'b':
                    break
                if guitar_sub_mode == '1':
                    quiz_guitar_find_positions()
                elif guitar_sub_mode == '2':
                    quiz_guitar_find_note()
                elif guitar_sub_mode == '3':
                    quiz_guitar_mixed()
                elif guitar_sub_mode == '4':
                    quiz_guitar_interval()
                else:
                    print("无效输入")
        elif mode == 'q':
            break
        else:
            print("无效输入，请重新选择。")

if __name__ == '__main__':
    main()
