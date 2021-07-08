import pandas as pd
import random
# from STTECHML.util.ScoreEventFunction import evaluateFaultScore, generateOnceEvent,generateEvent


def fixedScore(DeviceParameter,featureTH, resultDF, *args):
    #sensorID = resultDF['sensor'][0]
    #DeviceParameter = DeviceParameter[DeviceParameter['SensorID']==sensorID].reset_index(drop=True)
    threshold = DeviceParameter[featureTH][0]
    listScore = []
    for i in args:
        listScore.append((resultDF[i][0])/100)
    maxScore = max(listScore)
    if maxScore > threshold:
        return(random.randint(74,79))
    else:
        return(random.randint(85,95))



def commonScore(valueName,df,TH80,TH_a,TH_b,TH_c):
    value = df[valueName][0]
    if value < TH80:
        score = 80 + ((TH80-value)/TH80)*20
    else:
        score = TH_a * (value**TH_b) + TH_c
    return score



def fixed_WHQscore(ResultDF,DeviceParameter):
    Score = {}
    goodData = ResultDF['goodData'][0]
    if goodData == 100:
        Score['S1'] = -99     #转子不平衡
        Score['S2'] = -99   #转自不对中
        Score['S3_1'] = -99   #轴承外圈损伤
        Score['S3_2'] = -99   #轴承内圈损伤
        Score['S3_3'] = -99   #轴承滚动体损伤
        Score['S3_4'] = -99   #轴承保持架损伤
        Score['S3'] = -99   #轴承损伤
        Score['S4_1'] = -99
        Score['S4_2'] = -99
        Score['S4'] = -99     #碰磨

        Score['S5'] = -99
        Score['S6'] = -99
        Score['S7'] = -99
        Score['S8'] = -99
        Score['S9'] = -99

        Score['condition'] = 0
        Score['WkStatus'] = 0      #1是开机
        Score['PscoreMethod'] = 1  #0是动态阈值打分，1是固定阈值打分

    elif goodData == 1:

        sensorID = ResultDF['sensor'][0]
        DeviceParameter = DeviceParameter[DeviceParameter['SensorID']==sensorID].reset_index(drop=True)
        Trms_80 = DeviceParameter['Trms_80'][0]
        #Trms_60 = DeviceParameter['Trms_60'][0]
        Trms_a = DeviceParameter['Trms_a'][0]
        Trms_b = DeviceParameter['Trms_b'][0]
        Trms_c = DeviceParameter['Trms_c'][0]
        Tkurt_80 = DeviceParameter['Tkurt_80'][0]
        #Tkurt_60 = DeviceParameter['Tkurt_60'][0]
        Tkurt_a = DeviceParameter['Tkurt_a'][0]
        Tkurt_b = DeviceParameter['Tkurt_b'][0]
        Tkurt_c = DeviceParameter['Tkurt_c'][0]
        Tbias_80 = DeviceParameter['Tbias_80'][0]
        #Tbias_60 = DeviceParameter['Tbias_60'][0]
        Tbias_a = DeviceParameter['Tbias_a'][0]
        Tbias_b = DeviceParameter['Tbias_b'][0]
        Tbias_c = DeviceParameter['Tbias_c'][0]
        Tmargin_80 = DeviceParameter['Tmargin_80'][0]
        #Tmargin_60 = DeviceParameter['Tmargin_60'][0]
        Tmargin_a = DeviceParameter['Tmargin_a'][0]
        Tmargin_b = DeviceParameter['Tmargin_b'][0]
        Tmargin_c = DeviceParameter['Tmargin_c'][0]
        TF9_80 = DeviceParameter['TF9_80'][0]
        #TF9_60 = DeviceParameter['TF9_60'][0]
        TF9_a = DeviceParameter['TF9_a'][0]
        TF9_b = DeviceParameter['TF9_b'][0]
        TF9_c = DeviceParameter['TF9_c'][0]
        LX_F1_80 = DeviceParameter['LX_F1_80'][0]
        #LX_F1_60 = DeviceParameter['LX_F1_60'][0]
        LX_F1_a = DeviceParameter['LX_F1_a'][0]
        LX_F1_b = DeviceParameter['LX_F1_b'][0]
        LX_F1_c = DeviceParameter['LX_F1_c'][0]
        LX_F2_80 = DeviceParameter['LX_F2_80'][0]
        LX_F2_60 = DeviceParameter['LX_F2_60'][0]
        LX_F2_a = DeviceParameter['LX_F2_a'][0]
        LX_F2_b = DeviceParameter['LX_F2_b'][0]
        LX_F2_c = DeviceParameter['LX_F2_c'][0]
        #LX_F3_80 = DeviceParameter['LX_F3_80'][0]
        #LX_F3_60 = DeviceParameter['LX_F3_60'][0]
        LX_F3_a = DeviceParameter['LX_F3_a'][0]
        LX_F3_b = DeviceParameter['LX_F3_b'][0]
        LX_F3_c = DeviceParameter['LX_F3_c'][0]
        HZ_F2_80 = DeviceParameter['HZ_F2_80'][0]
        HZ_F2_60 = DeviceParameter['HZ_F2_60'][0]
        HZ_F2_a = DeviceParameter['HZ_F2_a'][0]
        #HZ_F2_b = DeviceParameter['HZ_F2_b'][0]
        HZ_F2_c = DeviceParameter['HZ_F2_c'][0]
        HZ_RMS3000_80 = DeviceParameter['HZ_RMS3000_80'][0]
        #HZ_RMS3000_60 = DeviceParameter['HZ_RMS3000_60'][0]
        HZ_RMS3000_a = DeviceParameter['HZ_RMS3000_a'][0]
        HZ_RMS3000_b = DeviceParameter['HZ_RMS3000_b'][0]
        HZ_RMS3000_c = DeviceParameter['HZ_RMS3000_c'][0]
        LX_F3_2_80 = DeviceParameter['LX_F3_2_80'][0]
        #LX_F3_2_60 = DeviceParameter['LX_F3_2_60'][0]
        LX_F3_2_a = DeviceParameter['LX_F3_2_a'][0]
        LX_F3_2_b = DeviceParameter['LX_F3_2_b'][0]
        LX_F3_2_c = DeviceParameter['LX_F3_2_c'][0]
        LX_F5_2_80 = DeviceParameter['LX_F5_2_80'][0]
        #LX_F5_2_60 = DeviceParameter['LX_F5_2_60'][0]
        LX_F5_2_a = DeviceParameter['LX_F5_2_a'][0]
        LX_F5_2_b = DeviceParameter['LX_F5_2_b'][0]
        LX_F5_2_c = DeviceParameter['LX_F5_2_c'][0]
        #HZ_F8_12_80 = DeviceParameter['HZ_F8_12_80'][0]
        #HZ_F8_12_60 = DeviceParameter['HZ_F8_12_60'][0]
        HZ_F8_12_a = DeviceParameter['HZ_F8_12_a'][0]
        HZ_F8_12_b = DeviceParameter['HZ_F8_12_b'][0]
        HZ_F8_12_c = DeviceParameter['HZ_F8_12_c'][0]


        LXF1 = ResultDF['LXF1'][0] / 100
        LXF2 = ResultDF['LXF2'][0] / 100
        LXF3 = ResultDF['LXF3'][0] / 100
        LXF4 = ResultDF['LXF4'][0] / 100
        LXF3_2 = ResultDF['LXF3_2'][0] / 100
        LXF5_2 = ResultDF['LXF5_2'][0] / 100
        F2 = ResultDF['F2'][0] / 100
        F8 = ResultDF['F8'][0] / 100
        F9 = ResultDF['F9'][0] / 100
        F10 = ResultDF['F10'][0] / 100
        F11 = ResultDF['F11'][0] / 100
        F12 = ResultDF['F12'][0] / 100
        RMS3000 = ResultDF['RMS3000'][0]
###############不平衡
        if LXF1 < LX_F1_80:
            Score['S1'] = 80+((LX_F1_80-LXF1)/LX_F1_80) * 20
        else:
            if (LXF2 < LX_F2_60)and(LXF3<0.8*LX_F2_60)and(LXF4<0.6*LX_F2_60):
                Score['S1'] = LX_F1_a*(LXF1**LX_F1_b)+LX_F1_c
            else:
                Score['S1'] = LX_F1_a*((0.9*LXF1)**LX_F1_a)+LX_F1_c
        if Score['S1'] > 98:
            Score['S1'] = 98
        elif Score['S1'] < 10:
            Score['S1'] = 10

##############不对中故障
        if LXF2 < LX_F2_80:
            Score['S2'] = 80 + ((LX_F2_80 - LXF2)/LX_F2_80)*20
        else:
            if (LXF2 > LXF1) and (F2 > HZ_F2_80):
                Score['S2'] = 0.6*(LX_F2_a*(LXF2**LX_F2_a)+LX_F2_c)+0.3*(HZ_F2_a*(F2**HZ_F2_a)+HZ_F2_c)+0.1*(LX_F3_a*(LXF3**LX_F3_b)+LX_F3_c)
            elif (LXF2 > LXF1) or ((F2>0.2*LXF2)and(F2<0.6*LXF2)):
                Score['S2'] = 0.8*(LX_F2_a*(LXF2**LX_F2_a)+LX_F2_c)+0.2*(HZ_F2_a*(F2**HZ_F2_a)+HZ_F2_c)
            elif (F2>HZ_F2_60) or (F2>0.6*LXF2):
                Score['S2'] = 0.5*(LX_F2_a*(LXF2**LX_F2_a)+LX_F2_c)+0.2*(LX_F3_a*(LXF3**LX_F3_b)+LX_F3_c)+0.3*(HZ_F2_a*(F2**HZ_F2_a)+HZ_F2_c)
            else:
                Score['S2'] = LX_F2_a * (LXF2 ** LX_F2_b) + LX_F2_c
        if Score['S2'] > 98:
            Score['S2'] = 98
        elif Score['S2'] < 10:
            Score['S2'] = 10
##############轴承打分，套用之前的逻辑
        ScoreS3_1 = fixedScore(DeviceParameter,'HFreOTH', ResultDF, 'HFreO1','HFreO2','HFreO3')
        Score['S3_1'] = ScoreS3_1
        #轴承内圈损伤
        ScoreS3_2 = fixedScore(DeviceParameter,'HFreITH', ResultDF, 'HFreI1','HFreI2','HFreI3')
        Score['S3_2'] = ScoreS3_2
        #轴承滚动体损伤
        ScoreS3_3 = fixedScore(DeviceParameter,'HFreRTH', ResultDF, 'HFreR1','HFreR2','HFreR3')
        Score['S3_3'] = ScoreS3_3
        #轴承保持架损伤
        ScoreS3_4 = fixedScore(DeviceParameter,'HFreCTH', ResultDF, 'HFreC1','HFreC2')
        Score['S3_4'] = ScoreS3_4
        Score['S3'] = min(ScoreS3_1,ScoreS3_2,ScoreS3_3,ScoreS3_4)

###################机械碰磨
        F812_mean = (F8+F9+F10+F11+F12) / 5
        if RMS3000 < HZ_RMS3000_80:
            Score['S4'] = 80+ ((HZ_RMS3000_80 - RMS3000)/HZ_RMS3000_80) * 20
        else:
            if LXF3_2 > LX_F3_2_80:
                Score['S4'] = 0.1*(LX_F1_a*(LXF1**LX_F1_b)+LX_F1_c)+0.7*(HZ_RMS3000_a*(RMS3000**HZ_RMS3000_b)+HZ_RMS3000_c)+0.2*(LX_F3_2_a*(LXF3_2**LX_F3_2_b)+LX_F3_2_c)
            elif LXF5_2 > LX_F5_2_80:
                Score['S4'] = 0.1*(LX_F1_a*(LXF1**LX_F1_b)+LX_F1_c)+0.7*(HZ_RMS3000_a*(RMS3000**HZ_RMS3000_b)+HZ_RMS3000_c)+0.2*(LX_F5_2_a*(LXF5_2**LX_F5_2_b)+LX_F5_2_c)
            else:
                ScoreS4_1 = 0.1*(LX_F1_a*(LXF1**LX_F1_b)+LX_F1_c)+0.9*(HZ_F8_12_a*(F812_mean**HZ_F8_12_b)+HZ_F8_12_c)
                ScoreS4_2 = 0.1*(LX_F1_a*(LXF1**LX_F1_b)+LX_F1_c)+0.9*(HZ_RMS3000_a*(RMS3000**HZ_RMS3000_b)+HZ_RMS3000_c)
                Score['S4'] = min(ScoreS4_1,ScoreS4_2)
        if Score['S4'] > 98:
            Score['S4'] = 98
        elif Score['S4'] < 10:
            Score['S4'] = 10

        Score['S5'] = commonScore('Trms',ResultDF,Trms_80,Trms_a,Trms_b,Trms_c)
        Score['S6'] = commonScore('Tkurt',ResultDF,Tkurt_80,Tkurt_a,Tkurt_b,Tkurt_c)
        Score['S7'] = commonScore('Tbias',ResultDF,Tbias_80,Tbias_a,Tbias_b,Tbias_c)
        Score['S8'] = commonScore('Tmargin',ResultDF,Tmargin_80,Tmargin_a,Tmargin_b,Tmargin_c)
        Score['S9'] = commonScore('TF9',ResultDF,TF9_80,TF9_a,TF9_b,TF9_c)

        Score['condition'] = 0
        Score['WkStatus'] = 1      #1是开机
        Score['PscoreMethod'] = 1  #0是动态阈值打分，1是固定阈值打分

    partsScore=pd.DataFrame(Score,index = [0])
    return partsScore


