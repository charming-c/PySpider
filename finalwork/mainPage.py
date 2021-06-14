from __future__ import print_function, unicode_literals
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
    for item in db.col.find():
        print(item)


def Rankmenu():
    sourcedata = getVedio()
    data = []
    for item in sourcedata:
        temp = {}
        temp['name'] = item['tag']
        data.append(temp)
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
            ],
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        }
    ]

    answers = prompt(questions)
    select = []
    for i in sourcedata:
        for j in answers['topList']:
            if j == i['tag']:
                select.append(i)

    chioces = answers['listOption']
    if chioces == 'save in mongoDB':
        save(select)
    elif chioces == 'getDanmu':
        for i in select:
            print(getDanmu1(i['Bvid']))


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
                'Search user',
                'Search vedio by bvid',
                'Login',
                'Exit'
            ]
            # 'validate': lambda answer: 'You must choose at least one option.'
            # if len(answer) == 0 else True
        }
    ]
    answer = prompt(questions)
    return answer


# def nologinOption():


if __name__ == "__main__":
    loginAnswer = mainMenu()
    if loginAnswer['option'] == 'Top 50 vedio daily':
        Rankmenu()
