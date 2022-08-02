# IMPORTING LIBRARIES
import statistics
from datetime import datetime
import pandas as pd
# testing my code
def freqClass(df, siku):
    # output list
    output = [[], [], [], []]
    # groupby week and user ID
    freqUser = df.groupby(["user ID", pd.Grouper(key="Day", freq="W-SUN")])["type"].count().reset_index()
    # place unique values of user ID in list
    userUniq = freqUser["user ID"].unique()
    for user in userUniq:
        # change datatype from string to datetime
        sikuDT = datetime.strptime(siku, "%d/%m/%Y")
        userDF = pd.DataFrame(freqUser.loc[freqUser["user ID"] == user])
        # reset index
        userDF.reset_index(drop=True, inplace=True)
        # INDEX OF DATE in Day column
        idx = userDF.index[userDF["Day"] == sikuDT].tolist()
        #---modified code-----
        if len(idx) == 0:
            freqVal = -1
            did = userDF.index[userDF["Day"] < sikuDT].tolist()
            if len(did) > 0:
                valst = userDF["type"].loc[did].tolist()
                b4mean = statistics.mean(valst)
            else:
                b4mean = 0
            if b4mean >= 5:
                output[1].append(user)
            elif b4mean < 5:
                output[2].append(user)
        else:
            freqVal = userDF["type"].loc[idx[0]]
            try:
                preVal = userDF["type"].loc[idx[0] - 1]
            except KeyError:
                preVal = 0
            # look at activity of user
            if freqVal >= 5 and freqVal < 10:
                output[0].append(user)
            elif freqVal < 5 and  preVal >= 5:
                output[1].append(user)
            elif freqVal < 5 and preVal < 5:
                output[2].append(user)
            elif freqVal >= 10:
                output[3].append(user)
    #----end of modified code-----
    return output

# analysis main function
def analysisPipe(dates):
    # READ EXCEL FILE
    dating = pd.read_excel("Engineer Dommie.xlsx", sheet_name="Dates Scheduled", engine="openpyxl")
    # implement freqClass function
    ziggy = freqClass(dating, dates)
    zigDict = {"Active": ziggy[0], "Bored": ziggy[1], "Inactive": ziggy[2], "SuperActive": ziggy[3]}
    for zig in list(zigDict.keys()):
        print(f"{zig} users: {zigDict[zig]}")

job = input("Choose week whose Sunday date is (format{day/month(num)/year})")
analysisPipe(job)