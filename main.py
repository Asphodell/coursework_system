import numpy as np
import pandas as pd

class LongParser:
    #def univ func for needed file
    test_log = open("logs/test_log.txt")
    tfs_log = open("logs/tfs-log.txt")
    df_log = pd.DataFrame()
    df_log.rename(columns={0: 'Date', 1: 'Time', 2: 'Type', 3: 'Action'}, inplace=True)
    count_lines = 0


    while True:
        current_line = tfs_log.readline()
        count_lines += 1

        date_time_type = current_line.split(" ")[0:3]
        action_array = current_line.split(" ")[3:]
        action = " ".join(action_array)

        if len(date_time_type) == 3:
            date = np.array(date_time_type[0][:-1])
            timE = np.array(date_time_type[1])
            type = np.array(date_time_type[2][:-1])

        added_row = {'Date': date, 'Time': timE, 'Type': type, 'Action': action}
        df_log = df_log.append(added_row, ignore_index=True)

        if not current_line:
            break
    print(df_log)
    #df_log.to_excel("Test.xlsx")

class Statistics:
    """"Сбор статистики"""
    df_log = LongParser.df_log
    text_warning = '<warning>'
    text_new_ip = 'New connection from IP:'
    text_activated = 'Activated successfully.'
    text_deactivated = 'Deactivated successfully.'
    for i in range(0, LongParser.count_lines):
        checking_reason = df_log['Type'].loc[df_log.index[i]]

        if checking_reason == text_warning:
            print(i, df_log['Action'].loc[df_log.index[i]])

        checking_new_ip = df_log['Action'].loc[df_log.index[i]]

        if checking_new_ip[0:23] == text_new_ip:
            print(i, checking_new_ip[24:])

        #checking_activ_and_deactiv = df_log['Action'].loc[df_log.index[i]]
        #print(checking_activ_and_deactiv, checking_activ_and_deactiv == text_activated)
        #if (checking_activ_and_deactiv == text_activated) or (checking_activ_and_deactiv == text_deactivated):
        #    print(i, checking_activ_and_deactiv)

    #How much activated/deactivated around session/log --> find activated/deacticated --> count
