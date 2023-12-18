import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

class PValue:
    def __init__(self):
        pass

    def organize_and_cal_pvalue(self, survival_data: list, Low_Percentile: float, High_Percentile: float):
        survival_str = ""
        case_id_list = []
        survival_data = survival_data[1:-1]  #改這

        FPKM_list = [float(y.split("|")[0]) for x in survival_data for y in x.split(',')]
        low_quartile = np.percentile(FPKM_list, float(Low_Percentile))
        high_quartile = np.percentile(FPKM_list, 100-float(High_Percentile))
        T1 = []
        E1 = []
        T2 = []
        E2 = []
        high_case = []
        low_case = []
        high_FPKM = []
        low_FPKM = []
        survival_days = []
        ele = "".join(survival_data).split(",")
        survival_days = [float(x.split("|")[2]) for x in ele if x.split("|")[2] != 'None']
        # survival_days = [float(x.split("|")[2]) for x in ele if len(x.split("|")) >= 3 and x.split("|")[2] != 'None']

        max_survival_days = max(survival_days)

        for stage in survival_data:
            for info in stage.split(','):
                FPKM = float(info.split('|')[0])
                case_id = info.split('|')[1]
                survival_times = float(info.split('|')[2]) if info.split('|')[2] != 'None' else info.split('|')[2] #存活天數
                survival_events = False if info.split('|')[3] == 'alive' else True
                if FPKM >high_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(max_survival_days):
                    T1 += [survival_times]
                    E1 += [survival_events]
                    case_id_list += [case_id]
                    high_case += [case_id]
                    high_FPKM += [FPKM]
                elif FPKM < low_quartile and (survival_times != 0 and survival_times != 'None') and survival_times <= float(max_survival_days):
                    T2 += [survival_times]
                    E2 += [survival_events]
                    case_id_list += [case_id]
                    low_case += [case_id]
                    low_FPKM += [FPKM]
        if (T2 != [] and E2 != []) and (T1 != [] and E1 != []):
            logrank_result = logrank_test(T1, T2, E1, E2)
            logrank_p_value = logrank_result.p_value
        else:
            logrank_p_value =1 
            
        return logrank_p_value, max_survival_days

    def parallelprocessing_result(self, args):
        i, result, Low_Percentile_input, High_Percentile_input, Pvalue_input = args
        p_value, max_time = self.organize_and_cal_pvalue(result[i], Low_Percentile_input, High_Percentile_input)
        if p_value <= float(Pvalue_input):
            return {"name": result[i][0], "logrank_p_value": "{:e}".format(p_value), "max_time": max_time}
        else:
            return None

    def process_data(self,data, low_percent, high_percent, Pvalue_input, result_list):
        p_value, max_time = self.organize_and_cal_pvalue(data, low_percent, high_percent)
        if p_value <= float(Pvalue_input):
            result_list.append({"name": data[0], "logrank_p_value":"{:e}".format(p_value), "max_time": max_time})


    

