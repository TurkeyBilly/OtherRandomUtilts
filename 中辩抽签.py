import random



__doc__ = """
202/5/27
吃货杯初赛分组
"""

groupNameToMembersMap: dict[str, tuple[str, str]] = {
    "鸡蛋": ("冯宣睿 Aslan" ," 王锦敖Michael"),
    "吴彦组": ("陈仲懿 Mara", "郑文心 Claire"),
    "无言以队": ("时诺冰 Robyn", "李源 Ryan"),
    "有请下一队": ("洪一宁 Coco", "朱津元 Catherine"),
    "readers": ("李思仑", "黄琬寓"),
    "地衣": ("刘家林", "耿君豪"),
    "宏玺说的都队": ("徐苏宸", "刘宏玺"),
    "好运来": ("崔妮可", "陈恩雅"),
    "莎锅米线": ("田明瑄 Michelle", "刘彦岑 Sarah"),
    "fate": ("林心意", "张译元"),
    "上一组": ("赵耿媛 Tina", "吕泽伶 Katelynn"),
    "上火": ("张子健", "崔容源"),
    "嘉李伏尼亚": ("李双羽", "伏羽嘉"),
    "猛犸象采茶叶": ("马铭轩", "曹楚依")
}

groupNameList: list[str] = [
    "鸡蛋", "吴彦组", "无言以队", "有请下一队", "readers", "地衣", "宏玺说的都队", 
    "好运来", "莎锅米线", "fate", "上一组", "上火", "嘉李伏尼亚", "猛犸象采茶叶"
]

timeList: list[str] = [
    "周五晚9点-10点",
    "周六晚8点-9点",
    "周六晚9点-10点",
    "周日晚8点-9点",
    "周日晚9点-10点"
]

random.shuffle(groupNameList)
random.shuffle(groupNameList)
random.shuffle(groupNameList)

print("shuffled groupNameList: \n", groupNameList)
for i in range(int(len(groupNameList) / 2)):
    print(f"组号：{2 * i + 1}")
    print(f"队伍名：{groupNameList[2 * i]}")
    print("组员：", *groupNameToMembersMap[groupNameList[2 * i]])
    print("持方：正")
    print()
    print(f"组号：{2 * i + 2}")
    print(f"队伍名：{groupNameList[2 * i + 1]}")
    print("组员：", *groupNameToMembersMap[groupNameList[2 * i + 1]])
    print("持方：反")
    print()


print(
f"""
对阵规则：单持方，租号为[a]的组将分别与组号为[a-1]，以及[a+1]的组对战
例子：
组3 ({groupNameList[2]}) (正) 将分别对阵
    组2 ({groupNameList[1]}) (反)
    与
    组4 ({groupNameList[3]}) (反)
"""
)


# Update Result
groupNameList = ...
