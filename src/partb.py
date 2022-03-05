# -*-coding:utf-8-*-
import pandas as pd
import numpy as np
import datetime

def count_data_1():
    total = pd.read_csv('../data/total.csv')







def count_data_2():
    ids = set()
    pos = {'Shooting Guard': set(), 'Point Guard': set(), 'Center': set(), 'Power Forward': set(), 'Small Forward': set()}
    total_age = 0
    total_weight = 0
    total_experience = 0
    total_salary = 0
    total_ids = set()
    total_career_salary = 0
    min_salary = 925258

    salary = pd.read_csv('../data/salary.csv')
    for _, data in salary.iterrows():
        id = data['Name'] + data['Born']
        if data['Season'] == "2020-21":
            ids.add(id)

    data_info = pd.read_csv('../data/playerInfo.csv')
    for _, data in data_info.iterrows():
        id = data['Name'] + data['Born']
        if ids.__contains__(id):
            age = int((datetime.datetime.strptime('2021-06-30', '%Y-%m-%d') - datetime.datetime.strptime(data['Born'], '%Y-%m-%d')).days / 365)
            total_age += age
            if data['Experience'] == 'Rookie':
                total_experience += 1
            elif pd.isnull(data['Experience']) is False:
                total_experience += float(data['Experience'].split(' ')[0]) - 1 # experience is calculated in 2022
            else:
                total_experience += float(data['Career_length'].split(' ')[0])
            total_weight += float(data['Weight'][:-2])

            for p in pos.keys():
                if p in data['Position']:
                    pos[p].add(id)

    salary = pd.read_csv('../data/salary.csv')
    for _, data in salary.iterrows():
        total_ids.add(data['Name'] + data['Born'])
        if data['Season'] == "2020-21":
            if data['Salary'] == '< Minimum':
                total_salary += min_salary
            else:
                total_salary += float(data['Salary'])

        if data['Salary'] == '< Minimum':
            total_career_salary += min_salary
        else:
            total_career_salary += float(data['Salary'])

    print("2a. Number of active player is", len(ids))
    print('-------------------------')

    print("2b. Number of active player in each position:")
    for p in pos.keys():
        print(p, len(pos.get(p)))
    print('-------------------------')

    print("2c. average values:")
    print("average age", total_age / len(ids))
    print("average weight", total_weight / len(ids))
    print("average experience", total_experience / len(ids))
    print("average salary", total_salary / len(ids))
    print('-------------------------')

    print("2d. average career salaries:")
    print(total_career_salary / len(total_ids))
    print('-------------------------')


def count_data_3():
    ids = set()
    salaries_season = {'2009-10': {}, '2010-11': {}, '2011-12': {}, '2012-13': {}, '2013-14': {}, '2014-15': {},
                       '2015-16': {}, '2016-17': {}, '2017-18': {}, '2018-19': {}, '2019-20': {}, '2020-21': {}}
    min_salary = 925258
    salary = pd.read_csv('../data/salary.csv')
    for _, data in salary.iterrows():
        id = data['Name'] + '$' + data['Born']
        if data['Season'] == "2020-21":
            ids.add(id)

        d = data['Salary']
        if d == '< Minimum':
            d = min_salary

        salaries_season[data['Season']][id] = float(d) if salaries_season[data['Season']].__contains__(id) is False \
            else salaries_season[data['Season']][id] + float(d)

    top10_bar = np.percentile([v for v in salaries_season['2020-21'].values()], 90)
    top10_players = {}
    bottom10_bar = np.percentile([v for v in salaries_season['2020-21'].values()], 10)
    bottom10_players = {}

    top75_bar = np.percentile([v for v in salaries_season['2020-21'].values()], 25)
    top25_bar = np.percentile([v for v in salaries_season['2020-21'].values()], 75)
    middle50_players = {}

    for k in salaries_season['2020-21'].keys():
        if salaries_season['2020-21'].get(k) >= top10_bar:
            top10_players[k] = set()
        elif salaries_season['2020-21'].get(k) <= bottom10_bar:
            bottom10_players[k] = set()
        elif top75_bar <= salaries_season['2020-21'].get(k) <= top25_bar:
            middle50_players[k] = set()

    for _, data in salary.iterrows():
        if data['Season'] == "2020-21":
            id = data['Name'] + '$' + data['Born']
            if top10_players.__contains__(id):
                top10_players[id].add(data['Team'])
            elif bottom10_players.__contains__(id):
                bottom10_players[id].add(data['Team'])
            elif middle50_players.__contains__(id):
                middle50_players[id].add(data['Team'])

    salaries_per_season = {}
    for id in ids:
        salaries_per_season[id] = []
        for s in salaries_season.keys():
            if salaries_season[s].__contains__(id):
                salaries_per_season[id].append(salaries_season[s][id])

    print("3a. ")
    print(" Season Number       Mean        Std")
    for s in salaries_season.keys():
        print("%s    %d %.2f %.2f" % (s, len(salaries_season[s]), np.mean([v for v in salaries_season[s].values()]), np.std([v for v in salaries_season[s].values()])))
    print('-------------------------')

    print("3b. ")
    for p in top10_players.keys():
        print(p.split('$')[0], top10_players.get(p), salaries_season['2020-21'].get(p))
    print('-------------------------')

    print("3c. ")
    for p in bottom10_players.keys():
        print(p.split('$')[0], bottom10_players.get(p), salaries_season['2020-21'].get(p))
    print('-------------------------')

    print("3d. ")
    for p in middle50_players.keys():
        print(p.split('$')[0], middle50_players.get(p), salaries_season['2020-21'].get(p))
    print('-------------------------')

    print("3e. ")
    for p in salaries_per_season.keys():
        print(p.split('$')[0], sum(salaries_per_season[p]) / len(salaries_per_season[p]))
    print('-------------------------')


def count_data_4():
    ## count
    # 4a
    min_salary = 925258
    salary = pd.read_csv('../data/salary.csv')

    for _, data in salary.iterrows():
        if data['Salary'] == '< Minimum':
            data['Salary'] = min_salary
    salary['Salary'] = salary['Salary'].astype(int)
    salary_mean = salary.groupby(['Season', 'Team'])['Salary'].mean()

    # 4b


    ## save
    # 4a
    salary_mean.to_csv("../data/avg_salary_team_season.csv")


    ## print
    print("4a. ")
    print(salary_mean)
    print('-------------------------')


    
    return;

if __name__ == '__main__':
    # count_data_2()
    # count_data_3()
    count_data_4()