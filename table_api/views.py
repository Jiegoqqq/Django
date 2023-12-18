from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.db import connection
from django.db import models
import pandas as pd
import json
import pymysql
from . import models
from django.db import OperationalError
#Database管理及操作
class DatabaseManager(object):

    _instance = None
    db_cursor = None
    db_conn = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db_conn = pymysql.connect(
                                    host="localhost",
                                    database="WEB1",
                                    user="jienan",
                                    password="624001479",
                                    port=3306, #mysql default
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor
        )

        self.db_cursor = self.db_conn.cursor()
        print("SUCCESS: Connection to the database succeeded")
        
        
    
    def query_by_args(self, **kwargs):
        #接收DataTable傳來的參數
        print('----')
        #第幾次操作table, eg:0, 1, 2...
        draw = int(kwargs.get('draw', None)[0])
        #顯示的資料筆數, eg: 10, 25...
        length = int(kwargs.get('length', None)[0]) 
        #從第幾筆顯示, eg:0, 10, 20
        start = int(kwargs.get('start', None)[0]) 
         #輸入框內容: eg:search content
        search_value = kwargs.get('search[value]', None)[0]
        #由哪個column排序 eg:0, 1...
        order_column = kwargs.get('order[0][column]', None)[0] 
        #排序方式 eg: asc/desc 
        order = kwargs.get('order[0][dir]', None)[0] 
        #加一個dict讓拿回來的資料有東西對應
        name_dict = {0:'Library Name',1:'Gene ID',2:'Gene location',3:'Gene expression',4:'Accession number (Best hits in the GenBank)',5:'Annotation',6:'Species',7:'Blast Score',8:'Expect value',9:'Identities',10:'Frame',11:'KEGG pathway',12:'GO Term',13:'Interpro',14:'Pfam',15:'Swissprot',16:'TrEMBL',17:'TF_ath',18:'TF_osa'}
        order_column = name_dict[int(order_column)]
        
        #資料庫拿取資料
        sql = """
            SELECT * FROM `Lbarbarum`
            ORDER BY `%s` %s;
        """% (order_column, order)
        # print(sql)
        self.db_cursor.execute(sql)
        data = self.db_cursor.fetchall()
        #對資料篩選
        
        #選取包含search value的row
        if len(search_value) != 0:
            data = [dictionary for dictionary in data if any(search_value in value for value in dictionary.values())]
            
        #留下需要的資料筆數
        count = len(data)
        if count > length:
            data = data[start: start + length]

        
        #回傳以通過篩選的資料
        return {
            'query_data':data,
            'count':count,
            'total':count,
            'draw':draw
        }

#API
class UPDATEGENEANNOTATIONViewSet(viewsets.ModelViewSet):
    queryset = None
    # queryset = models.Lbarbarum.objects.all()
    response = None
    parser_classes = (JSONParser,)
    dbm = DatabaseManager()

    def list(self, request, **kwargs):
        try:
            #接收通過篩選的資料庫的值
            
            res = self.dbm.query_by_args(**request.query_params)
            result = dict()
            result['data'] = res['query_data']
            result['draw'] = res['draw']
            result['recordsTotal'] = res['total']
            result['recordsFiltered'] = res['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

def table_api_web(request):
    return render(request, 'table_api_web.html', locals())