import random
import calendar
import pandas as pd
import numpy as np
import timeit
import csv
import os
import warnings

warnings.filterwarnings("ignore")

if not os.path.isfile('std.csv') :
    tosave = ['a', 'b', 'c', 'd', 'e']
    with open('std.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(tosave)

# #### Create month table
def get_score(weekday_name):
#     print(weekday_name)
    day_score = []
    for name in weekday_name:
        if name == 'Saturday' :
            day_score.append(5)
        elif name == 'Friday':
            day_score.append(4)
        elif name == 'Sunday':
            day_score.append(3)
        elif name == 'Tuesday' or name =='Thursday' :
            day_score.append(2)
        else:
            day_score.append(1)
    return day_score

def create_table(start, end):
    df = pd.DataFrame({'Date': pd.date_range(start, end)})
    df['Day'] = df.Date.dt.weekday_name
    df['Score'] = get_score(df.Date.dt.weekday_name)
    df['Blue'] = 'NA'
    df['Red'] = 'NA'
    df['Silver'] = 'NA'
    df['Gold'] = 'NA'
    return df

def employee_schedule(start, end, empl_list):
    df = pd.DataFrame({'Date': pd.date_range(start, end)})
    for emp in empl_list:
        df[emp[0]] = 0
    return df

def update_df_emp(teams, empl_choice, loc, score, df_emp):

    for empl in empl_list:
        if empl == empl_choice:
            df_emp.loc[loc,empl[0]] += score*teams

    return df_emp

start = timeit.default_timer()
for run_times in range(100000):
    # #### Random year & month
    year = random.randint(1970,2100)
    month = random.randint(1,12)

    #no of days
    start_day, no_of_days = calendar.monthrange(year, month)
    start_day = (calendar.day_name[start_day])

    start_date = str(year) + '-' + str(month) +'-01'
    end_date = str(year) + '-' + str(month) +'-'+str(no_of_days)
    df_teams = create_table(start_date, end_date)

    # #### List of random no. of employees
    # #### Also select last 2 weekend's work randomly
    no_of_empl = random.randint(25,50)

    # 6 random employees worked 2 weekends back
    weekend_1 = random.sample(range(1,no_of_empl+1), 6)
    weekend_2 = random.sample(range(1,no_of_empl+1), 6)

    empl_list = []
    for i in range(1,no_of_empl+1):
        one_weekend_back = 0
        two_weekend_back = 0
        if i in weekend_1:
            one_weekend_back = 1
        if i in weekend_2:
            two_weekend_back = 1
        if(i<10):
            empl_list.append(['emp_0' + str(i), 0, two_weekend_back, one_weekend_back, 0])
        else:
            empl_list.append(['emp_' + str(i), 0, two_weekend_back, one_weekend_back, 0])


    # #### Random no. of employee on holiday for random amount of days
    #5-10 employees taking a leave
    no_of_empl_leave = random.randint(5,10)

    #selecting random employees who are takeing a leave
    empl_list_leave = random.sample(range(0,no_of_empl+1), no_of_empl_leave)

    #assiging random amount of leave days (max 10)
    for loc,empl in enumerate(empl_list):
        if loc in empl_list_leave:
            empl[4] = random.randint(1,10)

    for num,empl in enumerate(empl_list):
        days_leave = random.sample(list(df_teams['Date']), empl[4])
        empl.append(days_leave)

    df_emp = employee_schedule(start_date, end_date, empl_list)


    for loc,date in enumerate(df_teams['Date']):

        score = df_teams.loc[loc,'Score']
        #weekend
        if(date.weekday_name == 'Saturday' or date.weekday_name == 'Sunday'):

            free_list = []
            for i in empl_list:
                if ((i[2] == 0 or i[3] == 0) and i[1] == 0) and (date not in empl_list[5]):
                    free_list.append(i)

            gold_choice = random.choice(free_list)
            df_teams.at[loc, 'Gold'] = gold_choice[0]

            #assign same to one of the other three team (red,blue,silver)
            with_gold = random.choice(['Red','Blue','Silver'])
            df_teams.at[loc, with_gold] = gold_choice[0]
            update_df_emp(2, gold_choice, loc, score, df_emp)

            #assign different employees to remaining 2 team
            other_choice_1 = random.choice([x for x in free_list if x != gold_choice])
            other_choice_2 = random.choice([x for x in free_list if x != gold_choice and x != other_choice_1])

            if with_gold == 'Blue':
                df_teams.at[loc, 'Red'] = other_choice_1[0]
                df_teams.at[loc, 'Silver'] = other_choice_2[0]
                update_df_emp(1,other_choice_1,loc, score, df_emp)
                update_df_emp(1,other_choice_2,loc, score, df_emp)
            elif with_gold == 'Red':
                df_teams.at[loc, 'Blue'] = other_choice_1[0]
                df_teams.at[loc, 'Silver'] = other_choice_2[0]
                update_df_emp(1,other_choice_1,loc, score, df_emp)
                update_df_emp(1,other_choice_2,loc, score, df_emp)
            else:
                df_teams.at[loc, 'Blue'] = other_choice_1[0]
                df_teams.at[loc, 'Red'] = other_choice_2[0]
                update_df_emp(1,other_choice_1,loc, score, df_emp)
                update_df_emp(1,other_choice_2,loc, score, df_emp)

            #update weekend work status
            for i in range(len(empl_list)):
                if(empl_list[i]==gold_choice or empl_list[i]==other_choice_1 or empl_list[i]==other_choice_2):
                    empl_list[i][1] = 1

            if(date.weekday_name == 'Sunday'):
                for i in range(len(empl_list)):
                    empl_list[i][3] = empl_list[i][2]
                    empl_list[i][2] = empl_list[i][1]
                    empl_list[i][1] = 0


    #   Weekday
        else:
            #Get random choice for Gold
            gold_choice = random.choice(empl_list)
            df_teams.at[loc, 'Gold'] = gold_choice[0]

            #assign same to one of the other three team (red,blue,silver)
            with_gold = random.choice(['Red','Blue','Silver'])
            df_teams.at[loc, with_gold] = gold_choice[0]

            update_df_emp(2, gold_choice, loc, score, df_emp)

            #assign different employee to remaining 2 team
            other_choice = random.choice([x for x in empl_list if x != gold_choice])
            if with_gold == 'Blue':
                df_teams.at[loc, 'Red'] = other_choice[0]
                df_teams.at[loc, 'Silver'] = other_choice[0]
                update_df_emp(2,other_choice,loc, score, df_emp)
            elif with_gold == 'Red':
                df_teams.at[loc, 'Blue'] = other_choice[0]
                df_teams.at[loc, 'Silver'] = other_choice[0]
                update_df_emp(2,other_choice,loc, score, df_emp)
            else:
                df_teams.at[loc, 'Blue'] = other_choice[0]
                df_teams.at[loc, 'Red'] = other_choice[0]
                update_df_emp(2,other_choice,loc, score, df_emp)


    df_emp.loc['Total'] = df_emp.sum()


    workload_array = df_emp.loc['Total','emp_01':]
    for num,workload in enumerate(workload_array):
        workload *= no_of_days / (no_of_days-empl_list[num][4])
        workload_array[num] = workload
    wordload_std = np.std(workload_array)
    std_no_of_empl = wordload_std * np.sqrt(no_of_empl)
    score_to_minimize = wordload_std * np.sqrt(no_of_empl) / np.sqrt(no_of_days)


    tosave = [no_of_empl, no_of_days, wordload_std, std_no_of_empl, score_to_minimize]
    with open('std.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow(tosave)

    if run_times % 10000 == 0 :
        print(run_times)
        stop = timeit.default_timer()
        print('Time: ', stop - start)

stop = timeit.default_timer()

print('Time: ', stop - start)
