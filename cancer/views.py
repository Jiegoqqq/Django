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
from pvalue import PValue

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

# Assuming organize_and_cal_pvalue is a function you have defined
# def process_result(args):
#     i, result, Low_Percentile_input, High_Percentile_input, Pvalue_input = args
#     p_value, max_time = organize_and_cal_pvalue(result[i], Low_Percentile_input, High_Percentile_input)
#     if p_value <= float(Pvalue_input):
#         return {"name": result[i][0], "logrank_p_value": "{:e}".format(p_value), "max_time": max_time}
#     else:
#         return None
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
    # result_list = []
    # for i in tqdm(range(len(result))):
    #     p_value, max_time = pvalue_analysis.organize_and_cal_pvalue(result[i], Low_Percentile_input, High_Percentile_input)
    #     if p_value <= float(Pvalue_input):
    #         result_list.append({"name":result[i][0], "logrank_p_value":"{:e}".format(p_value), "max_time":max_time})




    # # Create a list of arguments for the pool
    pool_args = [(i, result, Low_Percentile_input, High_Percentile_input, Pvalue_input) for i in range(len(result))]
    # pool_size = 4
    # with Pool(pool_size) as pool:
    #     result_list = list(tqdm(pool.imap(pvalue_analysis.parallelprocessing_result, pool_args), total=len(pool_args)))

    # # Remove None results
    # result_list = [item for item in result_list if item is not None]

    from concurrent.futures import ThreadPoolExecutor


    def process_result(i):
        p_value, max_time = pvalue_analysis.organize_and_cal_pvalue(result[i], Low_Percentile_input, High_Percentile_input)
        if p_value <= float(Pvalue_input):
            return {"name": result[i][0], "logrank_p_value": "{:e}".format(p_value), "max_time": max_time}
        else:
            return None

    result_list = []

    # 设置线程池的大小，可以根据需要进行调整
    max_workers = 4

    # 使用ThreadPoolExecutor来并行处理for循环
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_result, i) for i in range(len(result))]

        # 使用tqdm显示进度条
        for future in tqdm(futures, total=len(result), desc="Processing"):
            result_item = future.result()
            if result_item is not None:
                result_list.append(result_item)




    response ={
        'result_list':result_list,
     }
    return JsonResponse(response)
