

import pandas as pd
import os
import shutil
import datetime
import time

def camel_case(x) :
    x = x.lower()
    x = x[0].upper() + x[1:]
    length = len(x)
    for counter in range(length) :
        if x[counter] == ' ' :
            x = x[:counter] + ' ' + x[counter+1].upper() + x[counter+2:]

    return(x)

def path_code_mapping(y) :
    if y == 'B' :
        return('BENELUX\\')
    elif y == 'I' :
        return('')
    elif y == 'F' :
        return('FRANCHISE\\')
    else :
        print("there has been a problem with the code mapping. Check the 'hotel list' file in ZZZAsh")

def path(x, y) :
    '''takes in a hotel name and its path code, returning the code'''
    path = "Z:\\2.Departments\\RevenueMgt\\05. BI Team\\IDeaS Daily Reports\\" +  path_code_mapping(y) + x
    return(path)

hotel_list_df = pd.read_excel("Z:\\2.Departments\\BusinessInsights\\BI team\\ZZZ Ash\\Hotel List.xlsx", header = None, usecols = [0,1])
already_done = []
today = datetime.datetime.today()
today_day = today.strftime('%d')
today = today.strftime('%d%m%Y')


dangerous = []
while True :
    for a, b in hotel_list_df.iterrows() :
        x = b[0]
        if x in already_done :
            continue
        y = b[1]
        copy_index = 0
        open_report = 0
        if os.path.exists(path(x, y)) :
            if os.path.exists(path(x,y) + "\\Daily Report\\Daily Report " + camel_case(x) + "_" + today + ".xlsb") :
                name_camel = 1
                try :
                    os.rename(path(x,y) + "\\Daily Report\\Daily Report " + camel_case(x) + "_" + today + ".xlsb", path(x,y) + "\\Daily Report\\Daily Report " + x + "_" + today + ".xlsb")
                    name_camel = 0
                except :
                    name_camel = 1
                copy_index = 1
                if os.path.exists(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb") :
                    time_stamp = os.path.getmtime(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb")
                    if datetime.datetime.fromtimestamp(time_stamp).strftime('%d') == today_day :
                        already_done.append(x)
                        continue

                    try :
                        os.remove(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb")
                    except :
                        open_report = 1
                elif os.path.exists(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb") :
                    time_stamp = os.path.getmtime(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb")
                    if datetime.datetime.fromtimestamp(time_stamp).strftime('%d') == today_day :
                        already_done.append(x)
                        continue

                    try :
                        os.remove(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb")
                    except :
                        open_report = 1
                    

            if os.path.exists(path(x,y) + "\\Daily Report\\Daily Report " + x + "_" + today + ".xlsb") :
                name_camel = 0
                copy_index = 1
                if os.path.exists(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb") :
                    time_stamp = os.path.getmtime(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb")
                    if datetime.datetime.fromtimestamp(time_stamp).strftime('%d') == today_day :
                        already_done.append(x)
                        continue

                    try :
                        os.remove(path(x,y) + "\\Daily Report " + x + "_NEW.xlsb")
                    except :
                        open_report = 1
                
                elif os.path.exists(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb") :
                    time_stamp = os.path.getmtime(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb")
                    if datetime.datetime.fromtimestamp(time_stamp).strftime('%d') == today_day :
                        already_done.append(x)
                        continue

                    try :
                        os.remove(path(x,y) + "\\Daily Report " + camel_case(x) + "_NEW.xlsb")
                    except :
                        open_report = 1

            if copy_index == 1 :
                dangerous.append(x)
                if open_report != 1 :
                    if name_camel == 1 :
                        shutil.copyfile(path(x,y) + "\\Daily Report\\Daily Report " + camel_case(x) + "_" + today + ".xlsb", path(x,y) + "\\Daily Report " + x + "_NEW.xlsb")
                    elif name_camel == 0 :
                        shutil.copyfile(path(x,y) + "\\Daily Report\\Daily Report " + x + "_" + today + ".xlsb", path(x,y) + "\\Daily Report " + x + "_NEW.xlsb") 
                elif open_report == 1 :
                    if name_camel == 1 :
                        shutil.copyfile(path(x,y) + "\\Daily Report\\Daily Report " + camel_case(x) + "_" + today + ".xlsb", path(x,y) + "\\Daily Report " + x + "_" + today + ".xlsb")
                    elif name_camel == 0 :
                        shutil.copyfile(path(x,y) + "\\Daily Report\\Daily Report " + x + "_" + today + ".xlsb", path(x,y) + "\\Daily Report " + x + "_" + today + ".xlsb")   

        else :
            print(x + "'s path directory is not found. Investigate")
        
    print(dangerous)
    already_done = already_done + dangerous
    time.sleep(60*5)