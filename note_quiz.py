import random

# 三种音名（大调自然排列，从C开始）
letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
numbers = ['1', '2', '3', '4', '5', '6', '7']
# 我用 si（或 xi）表示第七音，根据你的习惯可以改成'xi'
solfege = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']

# intervals[i] 表示 度 i -> 度 i+1 的间隔（大调）
# 顺序对应 degrees: 1->2, 2->3, 3->4, 4->5, 5->6, 6->7, 7->1
intervals = ['全音', '全音', '半音', '全音', '全音', '全音', '半音']

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

def quiz_once():
    mode = random.choice(['letters', 'numbers', 'solfege'])
    idx = random.randrange(7)
    if mode == 'letters':
        prompt = letters[idx]
    elif mode == 'numbers':
        prompt = numbers[idx]
    else:
        prompt = solfege[idx]
    print(f"\n🎼 题目（记法：{mode}）： {prompt}")
    input("👉 思考并回答（按回车显示标准答案）...")
    show_answer(idx)

def main():
    print("音名练习（英名 / 数字 / 唱名），显示左右邻音及全/半音关系。输入 q 退出。")
    while True:
        quiz_once()
        cont = input("\n是否继续？(回车继续，输入 q 退出)：")
        if cont.strip().lower() == 'q':
            break

if __name__ == '__main__':
    main()
