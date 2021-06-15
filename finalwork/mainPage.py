from __future__ import print_function, unicode_literals
from traceback import print_tb
from history import getHistory
from user import searchUser
from random import choices
from danmu import generateCloud
from danmu import getDanmu1
from pprint import pprint
from PyInquirer import prompt, Separator
from PyInquirer import style_from_dict
from bilibili_top100 import getVedio
from pymongo import MongoClient


def save(data):
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for i in data:
        db.col.insert_one(i)


def saveDanmu(danmu):
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for i in danmu:
        db.danmu.insert_one(i)


def wordCloud(display, data):
    questions = [
        {
            'type': 'list',
            'qmark': '☁️',
            'message': ' Danmu Option',
            'name': 'danmuOption',
            'choices': display,
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        }
    ]
    answers = prompt(questions)
    for i in data:
        if i['tag'] == answers['danmuOption']:
            generateCloud(i['Bvid'])


def getMore(display, data):
    questions = [
        {
            'type': 'list',
            'qmark': '☁️',
            'message': ' Information Option',
            'name': 'infoOption',
            'choices': display,
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        }
    ]
    answers = prompt(questions)

    for item in data:
        if item['tag'] == answers['infoOption']:
            print(f'No:' + item['No'], end='\n')
            print(f'Title:' + item['Title'], end='\n')
            print(f'Author:' + item['Author'], end='\n')
            print(f'播放量:' + item['Play Volume'], end='\n')
            print(f'弹幕数:' + item['View'], end='\n')
            print(f'Bvid:' + item['Bvid'], end='\n')
            print(" ")


def Rankmenu():
    sourcedata = getVedio()
    data = []
    for item in sourcedata:
        temp = {}
        temp['name'] = item['tag']
        data.append(temp)
    exit = {'name': 'exit'}
    data.append(exit)
    questions = [
        {
            'type': 'checkbox',
            'qmark': '😃',
            'message': 'Rank List',
            'name': 'topList',
            'choices': data,
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        },
        {
            'type': 'list',
            'qmark': '😁',
            'message': 'list Option',
            'name': 'listOption',
            'choices': [
                'save in mongoDB',
                'getMoreInformation',
                'getDanmu',
                'exit',
            ],
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        }
    ]

    answers = prompt(questions)
    select = []
    for i in sourcedata:
        for j in answers['topList']:
            if j == 'exit':
                return 0
            if j == i['tag']:
                select.append(i)

    chioces = answers['listOption']
    if chioces == 'save in mongoDB':
        save(select)
        return 1
    elif chioces == 'getDanmu':
        danmuList = []
        for i in select:
            danmu = {}
            danmu[i['No']] = getDanmu1(i['Bvid'])
            danmuList.append(danmu)
        saveDanmu(danmuList)
        wordCloud(answers['topList'], select)
        return 1
    elif chioces == 'getMoreInformation':
        getMore(answers['topList'], select)
        return 1
    else:
        return 0


def mainMenu():
    questions = [
        {
            'type': 'rawlist',
            'qmark': '⭐️',
            'message': 'Welcome To The BiLiBili Zone !',
            'name': 'option',
            'choices': [
                Separator('here are some choice you can choose:'),
                'Top 50 vedio daily',
                'Search',
                'Login and save',
                'Mongo',
                'Exit'
            ]
            # 'validate': lambda answer: 'You must choose at least one option.'
            # if len(answer) == 0 else True
        }
    ]
    answer = prompt(questions)
    return answer


def displayUser(user):
    display = []
    for item in user:
        temp = {}
        temp['name'] = item['username']
        display.append(temp)
    question = [
        {
            'type': 'checkbox',
            'qmark': '👓',
            'name': 'userSelect',
            'message': 'Search result:',
            'choices': display,

        }
    ]
    answer = prompt(question)
    for item in user:
        for j in answer['userSelect']:
            if j == item['username']:
                print(f'用户名: '+item['username'])
                print(f'稿件数: '+item['vedio'])
                print(f'链接地址: '+item['page'])
                print(f'粉丝数: '+item['fans'])
                print(" ")


def searchByUser():
    question = [
        {
            'qmark': '😝',
            'type': 'input',
            'name': 'userInput',
            'message': 'please input the keyword:'
        }
    ]
    answer = prompt(question)
    userData = searchUser(answer['userInput'])
    displayUser(userData)
    return 1


def searchByBvid():
    return 1


def searchMenu():
    questions = [
        {
            'type': 'rawlist',
            'qmark': '🔍',
            'message': 'Search by',
            'name': 'search option',
            'choices': [
                Separator('By user or by Bvid?'),
                'User',
                'Bvid',
                'Exit',
            ],
        }
    ]
    answer = prompt(questions)
    if answer['search option'] == 'User':
        return searchByUser()
    elif answer['search option'] == 'Bvid':
        return searchByBvid()
    else:
        return 0


def dataBase_vedio():
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for item in db.col.find():
        print(item)
    return 1


def dataBase_danmu():
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for item in db.danmu.find():
        print(item)
    return 1


def saveHistory(data):
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for i in data:
        db.history.insert_one(i)


def dataBase_history():
    conn = MongoClient("mongodb://localhost:27017/")
    db = conn.bilibili
    for item in db.history.find():
        print(item)
    return 1


def dataBaseMenu():
    questions = [
        {
            'type': 'list',
            'qmark': '📖',
            'message': 'database option',
            'name': 'dataOption',
            'choices': [
                'vedio',
                'danmu',
                'history',
                'exit',
            ],
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        }
    ]
    answer = prompt(questions)
    if answer['dataOption'] == 'vedio':
        return dataBase_vedio()
    elif answer['dataOption'] == 'danmu':
        return dataBase_danmu()
    elif answer['dataOption'] == 'history':
        return dataBase_history()
    else:
        return 0


def loginMenu():
    questions = [
        {
            'type': 'input',
            'qmark': '👀',
            'name': 'username',
            'message': 'input username:',
        },
        {
            'type': 'password',
            'qmark': '🤭',
            'message': 'input password:',
            'name': 'password',
        }
    ]
    answers = prompt(questions)
    historyData = getHistory(answers['username'], answers['password'])
    print(f"共获得" + str(len(historyData)) + '条历史记录')
    saveHistory(historyData)
    print(f'已保存到数据库!\n前十条如下:\n')
    for i in range(0, 10):
        print(f'No ' + str(i + 1) + '.' + historyData[i]['title'])
    print(" ")
    return 1


if __name__ == "__main__":
    switch = 1
    while switch:
        loginAnswer = mainMenu()
        if loginAnswer['option'] == 'Top 50 vedio daily':
            flag = 1
            while flag == 1:
                flag = Rankmenu()

        elif loginAnswer['option'] == 'Search':
            flag = 1
            while flag == 1:
                flag = searchMenu()

        elif loginAnswer['option'] == 'Mongo':
            flag = 1
            while flag == 1:
                flag = dataBaseMenu()

        elif loginAnswer['option'] == 'Login and save':
            flag = loginMenu()
        else:
            switch = 0
