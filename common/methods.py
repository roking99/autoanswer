# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser
import urllib.parse
import GetImgTool
# # 颜色兼容Win 10
from colorama import init, Fore




init()


def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + urllib.parse.quote(question))


def open_webbrowser_count(question, choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')

    counts = []
    for i in range(len(choices)):
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
        content = req.text
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
        print(choices[i] + " : " + count)


def count_base(question, choices):
    print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --\n')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})
    content = req.text
    # print(content)
    counts = []
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        # print(choices[i] + " : " + str(counts[i]))
    output(choices, counts)


def output(choices, counts):
    counts = list(map(int, counts))
    # print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return

    for i in range(len(choices)):
        print()
        if i == index_max:
            # 绿色为计数最高的答案
            print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
        elif i == index_min:
            # 红色为计数最低的答案
            print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
        else:
            print("{0} : {1}".format(choices[i], counts[i]))


def run_algorithm(al_num, question, choices):
    # if al_num == 0:
    #     open_webbrowser(question)
    # el
    if al_num == 1:
        open_webbrowser_count(question, choices)
    # elif al_num == 2:
    #     count_base(question, choices)
    elif al_num == 3:
        x,y = get_choice_coordinate(question, choices)
        GetImgTool.click_screen(x,y)


def get_choice_coordinate(question, choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')

    counts = []
    if 0 == len(choices):
        return

    for i in range(len(choices)):
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
        content = req.text
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
    print("keyword {}".format(getMaxKeyWord(choices, counts)))
    for i in range(len(choices)):
        if "下一题" in choices[i] or "查看答案" in choices[i] or "考考TA" in choices[i]:
            return "330", "620"
    word = getMaxKeyWord(choices, counts)
    # 240, 560, 240, 640, 240, 720, 240, 800
    if "A" in word:
        return "240", "560"
    elif "B" in word:
        return "240", "640"
    elif "C" in word:
        return "240", "720"
    elif "D" in word:
        return "240", "800"
    elif "下一题" in word or "查看答案" in word:
        return "330", "620"



def getMaxKeyWord(choices, counts):
    counts = list(map(int, counts))
    # print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return

    for i in range(len(choices)):
        print()
        if i == index_max:
            # 绿色为计数最高的答案
            return choices[i]


if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['A甲醛', 'B苯', 'C甲醇']
    run_algorithm(1, question, choices)
