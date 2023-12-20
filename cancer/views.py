#用python manage.py inspectdb > cancer/models.py 產生model.py 記得先把 view.py admin.py 註解起來
#後python manage.py makemigrations 再 python manage.py migrate
import os
import json
import sys
import numbers
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from web_tool.models import Gene
from django.http import JsonResponse
from django.db import connection
from operator import itemgetter
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt #用這個就不用在javascript 加token了
from django.core.serializers import serialize
from django.db import models
from . import models
from flask import Flask, render_template
import base64
import shutil
import csv
from io import StringIO
import mysql.connector
from tqdm import tqdm
from multiprocessing import Pool
from function_list.pvalue import PValue
import math 
def cancer_web(request,id):
    return render(request, 'cancer.html', locals())

@csrf_exempt  
def gene_name_data(request):
    # 查询数据库获取 gene_name 数据
    gene_names = models.TcgaAccGenesFpkmCufflinks.objects.values_list('gene_name', flat=True)

    # 将 QuerySet 转换为列表
    gene_names_list = list(gene_names)
    # 返回 JSON 响应
    return JsonResponse({'gene_names': gene_names_list})

@csrf_exempt  
def cancer_data(request):
    gene_name = request.POST['gene_name']
    survival_input_low = request.POST['survival_input_low']
    survival_input_high = request.POST['survival_input_high']
    survival_input_days = request.POST['survival_input_days']
    stage = request.POST['stage']

    result = models.TcgaAccGenesFpkmCufflinks.objects.all()
    result = result.filter(gene_name=gene_name)

    analysis_images_path = '/home/cosbi/forme/survival_analysisv3/plot_result/'
    files1 = os.listdir(analysis_images_path)

    for file in files1:
        file_path = os.path.join(analysis_images_path, file)
        os.remove(file_path)

    static_images_path = '/home/cosbi/forme/jieweb/static/images/'
    files2 = os.listdir(static_images_path)
    for file in files2:
        file_path = os.path.join(static_images_path, file)
        os.remove(file_path)

    analysis_csv_path = '/home/cosbi/forme/survival_analysisv3/csv_result/'
    files3 = os.listdir(analysis_csv_path)
    for file in files3:
        file_path = os.path.join(analysis_csv_path, file)
        os.remove(file_path)

    static_csv_path = '/home/cosbi/forme/jieweb/static/csv/'
    files4 = os.listdir(static_csv_path)
    for file in files4:
        file_path = os.path.join(static_csv_path, file)
        os.remove(file_path)


    current_working_directory = os.getcwd() #紀錄目前做資料夾
    os.chdir('/home/cosbi/forme/survival_analysisv3') # 換資料夾
    os.system('python survival_analysis.py -p TCGA-ACC --primary_site Adrenal_Gland_Adrenocortical_Carcinoma -t genes -n'+ gene_name +' --Low_Percentile '+survival_input_low +' --High_Percentile '+ survival_input_high +' --High_Percentile '+ survival_input_high +' --survival_days '+ survival_input_days +' --survival_select '+stage+'') 
    os.chdir(current_working_directory) #換回原本的資料夾

    os.system('cp /home/cosbi/forme/survival_analysisv3/plot_result/* /home/cosbi/forme/jieweb/static/images')     
    os.system('cp /home/cosbi/forme/survival_analysisv3/csv_result/* /home/cosbi/forme/jieweb/static/csv')         


    # 讀取 PNG 圖片文件
    folder_path = '/home/cosbi/forme/jieweb/static/images/'

    # 列举文件夹内所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查文件是否是文件而不是子文件夹
        if os.path.isfile(file_path):
            # 使用 with 语句打开文件
            with open(file_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    #csv 下載資料
    csv_data = pd.read_csv('/home/cosbi/forme/survival_analysisv3/csv_result/Survival_Profile_Adrenal Gland Adrenocortical Carcinoma_'+survival_input_low+'_'+survival_input_high+'.csv', delimiter='\t')

    csv_data_dict = csv_data.to_dict(orient='records')
    # 创建 CSV 字符串
    csv_string = StringIO()
    csv_writer = csv.writer(csv_string)

    # 写入数据
    for row in csv_data_dict:
        csv_writer.writerow(row.values())

    # 获取 CSV 字符串
    csv_result = csv_string.getvalue()
    response ={
        'gene_name':gene_name,
        'image_data':encoded_image,
        'csv_data':csv_result,
     }
    return JsonResponse(response)

@csrf_exempt  
def cancer_plot_data(request):
    gene_name = request.POST['gene_name']
    # cancer_kind = request.POST['cancer_kind']
    survival_input_low = request.POST['survival_input_low']
    survival_input_high = request.POST['survival_input_high']
    survival_input_days = request.POST['survival_input_days']
    stage = request.POST['stage']
    analysis_images_path = '/home/cosbi/forme/survival_analysisv3/plot_result/'
    files1 = os.listdir(analysis_images_path)
    for file in files1:
        file_path = os.path.join(analysis_images_path, file)
        os.remove(file_path)

    static_images_path = '/home/cosbi/forme/jieweb/static/images/'
    files2 = os.listdir(static_images_path)
    for file in files2:
        file_path = os.path.join(static_images_path, file)
        os.remove(file_path)

    analysis_csv_path = '/home/cosbi/forme/survival_analysisv3/csv_result/'
    files3 = os.listdir(analysis_csv_path)
    for file in files3:
        file_path = os.path.join(analysis_csv_path, file)
        os.remove(file_path)

    static_csv_path = '/home/cosbi/forme/jieweb/static/csv/'
    files4 = os.listdir(static_csv_path)
    for file in files4:
        file_path = os.path.join(static_csv_path, file)
        os.remove(file_path)

    current_working_directory = os.getcwd() #紀錄目前做資料夾
    os.chdir('/home/cosbi/forme/survival_analysisv3') # 換資料夾
    os.system('python survival_analysis.py -p TCGA-ACC --primary_site Adrenal_Gland_Adrenocortical_Carcinoma -t genes -n'+ gene_name +' --Low_Percentile '+survival_input_low +' --High_Percentile '+ survival_input_high +' --High_Percentile '+ survival_input_high +' --survival_days '+ survival_input_days +' --survival_select '+stage+'') 
    os.chdir(current_working_directory) #換回原本的資料夾

    os.system('cp /home/cosbi/forme/survival_analysisv3/plot_result/* /home/cosbi/forme/jieweb/static/images')     
    os.system('cp /home/cosbi/forme/survival_analysisv3/csv_result/* /home/cosbi/forme/jieweb/static/csv')         


    # 讀取 PNG 圖片文件
    folder_path = '/home/cosbi/forme/jieweb/static/images/'

    # 列举文件夹内所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 检查文件是否是文件而不是子文件夹
        if os.path.isfile(file_path):
            # 使用 with 语句打开文件
            with open(file_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    #csv 下載資料
    csv_data = pd.read_csv('/home/cosbi/forme/survival_analysisv3/csv_result/Survival_Profile_Adrenal Gland Adrenocortical Carcinoma_'+survival_input_low+'_'+survival_input_high+'.csv', delimiter='\t')

    csv_data_dict = csv_data.to_dict(orient='records')
    # 创建 CSV 字符串
    csv_string = StringIO()
    csv_writer = csv.writer(csv_string)

    # 写入数据
    for row in csv_data_dict:
        csv_writer.writerow(row.values())

    # 获取 CSV 字符串
    csv_result = csv_string.getvalue()
    response ={
        'gene_name':gene_name,
        'image_data':encoded_image,
        'csv_data':csv_result,
     }
    return JsonResponse(response)

@csrf_exempt  
def cancer_screener_web(request):
    return render(request, 'cancer_screener.html', locals())

@csrf_exempt  
def cancer_screener_data(request):

    cancer_kind = request.POST['cancer_kind']
    select_cancer = request.POST['select_cancer']
    select_stage = request.POST['select_stage']
    High_Percentile_input = request.POST['High_Percentile_input']
    Low_Percentile_input = request.POST['Low_Percentile_input']
    Pvalue_input = request.POST['Pvalue_input']

    if 'DE Gene' in cancer_kind :
        result = models.TcgaAccGenesFpkmCufflinks.objects.all()
        result = list(result.values())

    else:
        result = models.TcgaAccIsoformsFpkmCufflinks.objects.all().values()
        result = list(result.values())

    # result = [[value for value in element.values()] for element in result]
    result = [[value.strip("'") for value in element.values()] for element in result]

    pvalue_analysis = PValue()





    import multiprocessing


 
    with multiprocessing.Manager() as manager:
        # manager.list() 用於創建一個可以在多個進程之間共享的列表
        result_list_m = manager.list()
        # 創建一個 multiprocessing.Pool, 這是一個進程池，用於管理並行執行的進程。processes=4 的參數指定要使用 4 個處理器，預設是全部使用
        pool = multiprocessing.Pool(processes=4)
        # 使用 map 函數來平行處理數據
        # 注意: 如果 all_cancer_data 很大，可以考慮使用 imap 或者 imap_unordered 來節省記憶體
        pool.starmap(pvalue_analysis.process_data, [(data, Low_Percentile_input, High_Percentile_input, Pvalue_input, result_list_m) for data in tqdm(result)])
        # 關閉進程池，這表示不再接受新的任務(沒有其他資料與任務需要加到佇列) 
        pool.close()
        # 等待所有的工作完成，然後恢復執行主進程
        pool.join()
        result_list = list(result_list_m)

    # result_list = []
    #len(result)
    # for i in tqdm(range(len(result))):
    #     p_value, max_time = pvalue_analysis.organize_and_cal_pvalue(result[i], Low_Percentile_input, High_Percentile_input)
    #     if p_value <= float(Pvalue_input):
    #         result_list.append({"name":result[i][0], "logrank_p_value":"{:e}".format(p_value), "max_time":max_time})


    response ={
        'result_list':result_list,
     }
    return JsonResponse(response)

@csrf_exempt  
def liver_screener_web(request):
    return render(request, 'liver_screener.html', locals())

@csrf_exempt  
def liver_screener_data(request):
    cancer_kind = request.POST['cancer_kind']
    select_cancer = request.POST['select_cancer']
    select_conditon2_Value = request.POST['select_conditon2_Value']
    select_conditon1_Value = request.POST['select_conditon1_Value']
    select_type1_Value = request.POST['select_type1_Value']
    type1_input = request.POST['type1_input']
    select_test_Value = request.POST['select_test_Value']
    select_type2_Value = request.POST['select_type2_Value']
    qvalue_input = request.POST['qvalue_input']

    type1_input = math.log2(float(type1_input))

    def filter_and_transform_result_gt(result, filter_field, qvalue_input):
        result = result.filter(log2_fold_change_field__gte=type1_input)
        result = result.filter(**{filter_field + "__lte": float(qvalue_input)})

        table_list = []
        for row in result:
            table_list.append({
                'gene': row.gene,
                'value_1': row.value_1,
                'value_2': row.value_2,
                'fold_change': round(2 ** float(row.log2_fold_change_field), 3),
                'q_value': getattr(row, filter_field),
            })
        return table_list
    def filter_and_transform_result_lt(result, filter_field, qvalue_input):
        result = result.filter(log2_fold_change_field__lte=type1_input)

        result = result.filter(**{filter_field + "__gte": qvalue_input})
        table_list = []
        for row in result:
            table_list.append({
                'gene': row.gene,
                'value_1': row.value_1,
                'value_2': row.value_2,
                'fold_change': round(2 ** float(row.log2_fold_change_field), 3),
                'q_value': getattr(row, filter_field),
            })
        return table_list
    
    if 'DE Gene' in cancer_kind :
        if select_conditon1_Value == 'N' :
            class_name = f'TcgaLihcN{select_conditon2_Value}Genes'
            model_class = getattr(models, class_name, None)
            result = model_class.objects.all() if model_class else []
        else:
            class_name = f'TcgaLihc{select_conditon1_Value}{select_conditon2_Value}Genes'
            model_class = getattr(models, class_name, None)
            result = model_class.objects.all() if model_class else []
    if select_type1_Value == 'bigthan':
        if select_test_Value == 'Utest':
            table_list = filter_and_transform_result_gt(result, 'u_test_greater', qvalue_input)
        elif select_test_Value == 'Ttest':
            table_list = filter_and_transform_result_gt(result, 't_test_greater', qvalue_input)

        elif select_test_Value == 'KStest':
            result = result.filter(log2_fold_change_field__gte=type1_input)
            result = result.filter(ks_test_greater__gte=qvalue_input)   
            table_list = filter_and_transform_result_gt(result, 'ks_test_greater', qvalue_input)         
    else:
        if select_test_Value == 'Utest':
            table_list = filter_and_transform_result_lt(result, 'u_test_less', qvalue_input)
        elif select_test_Value == 'Ttest':
            table_list = filter_and_transform_result_lt(result, 't_test_less', qvalue_input)
        elif select_test_Value == 'KStest':
            table_list = filter_and_transform_result_lt(result, 'ks_test_less', qvalue_input)

 
    response ={
        'table_list':table_list,
     }
    return JsonResponse(response)