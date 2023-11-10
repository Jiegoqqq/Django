#用python3 manage.py inspectdb > web_tool/models.py 產生model.py 記得先把 view.py admin.py 註解起來
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
from web_tool import models
from operator import itemgetter
from django.db.models import Q
#my function 
from crawler import crawler
from plot import plot
from django.db.models import Q


def hello_world(request):
    time = datetime.now()
    return render(request,'hello_world.html', locals())
    #return HttpResponse("Hello World!")

def index(request):

    genes = Gene.objects.all()

    '''
    df = pd.read_csv('data/hw1_output_WS289.csv')
    df = df.head(10)
    df = df.rename(columns={"Gene_ID": "id",
                            "transcript_ID": "transcript",
                            "# of transcripts": "number",
                            })
    json_string = df.to_json(orient='records')
    genes = json.loads(json_string)
    '''
    return render(request, 'index.html', locals())

# 將 SQL 指令回傳的 List 轉成 Dict
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def form(request):
    return render(request, 'form.html', locals())
#for ajax form
def ajax_data(request):
    
    get = request.POST['gene_id']
    

    try:
        gene = models.CElegans.objects.get(wormbase_id=get)
        id = gene.wormbase_id

        gene_sequence = gene.gene_sequence
        gene_name = gene.gene_name
        other_name = gene.other_name
        
        
    except:
        try:
            gene = models.CElegans.objects.get(gene_sequence=get)
            id = gene.wormbase_id

            gene_sequence = gene.gene_sequence
            gene_name = gene.gene_name
            other_name = gene.other_name
            
        except:
            try:
                gene = models.CElegans.objects.get(gene_name=get)
                id = gene.wormbase_id

                gene_sequence = gene.gene_sequence
                gene_name = gene.gene_name
                other_name = gene.other_name
                id = gene.wormbase_id
                
            except:
                try:
                    gene = models.CElegans.objects.get(other_name=get)
                    id = gene.wormbase_id

                    gene_sequence = gene.gene_sequence
                    gene_name = gene.gene_name
                    other_name = gene.other_name
                   
                except:
                        #加入__contains 來搜尋字串中特別的字串
                        transcriptid = models.Gene.objects.get(transcript_id__contains=get)
                        id = transcriptid.gene_id
                        gene = models.CElegans.objects.get(wormbase_id=id)
                        gene_sequence = gene.gene_sequence
                        gene_name = gene.gene_name
                        other_name = gene.other_name
    #for table two & code type
    matching_rows = models.W289All.objects.filter(gene_id=id) 
    transcript_and_type = []
    # 轉換成出來是字典的形式
    for row in matching_rows:
        transcript_and_type.append({
            'Gene_ID': row.gene_id,
            'Gene_name': row.gene_name,
            'Type': row.type,
            'Transcript_ID': row.transcript_id
        })
    #for numbers
    Gene = models.Gene.objects.get(gene_id=id)
    numbers = Gene.numbers

    response = {
        "data":[{

            'wormbase_id': id,
            'gene_sequence':gene_sequence,
            'gene_name':gene_name,
            'other_name':other_name,
            'numbers':numbers,
            
        }],

        'transcript_and_type':transcript_and_type, 

    }
    return JsonResponse(response)



def table(request,id):

    return render(request, 'transcript.html', locals())

def transcript(request):
    
    sys.path.append('D:/jieweb/')
    transcript_name =request.POST['transcript_id'] #由transcript.js回傳
    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)

    #for button&table
    unspliced = unspliced.values.tolist()
    spliced = spliced.values.tolist()
    spliced_sp = spliced_sp.values.tolist()  

    unspliced_list = []
    spliced_list = []
    translation_list = []

    for i in range(len(unspliced)):
        unspliced_list.append({"Name":unspliced[i][0]})
        unspliced_list[i]["Start"] = unspliced[i][1]
        unspliced_list[i]["End"] = unspliced[i][2]
        unspliced_list[i]["Length"] = unspliced[i][3]
        

    for i in range(len(spliced_sp)):
        spliced_list.append({"Name":spliced_sp[i][0]})
        spliced_list[i]["Start"] = spliced_sp[i][1]
        spliced_list[i]["End"] = spliced_sp[i][2]
        spliced_list[i]["Length"] = spliced_sp[i][3]
    
    transcript_get = models.W289All.objects.get(transcript_id=transcript_name)
    transcript_type = transcript_get.type
    if (transcript_type == 'Coding_transcript'):
        translation = data['fields']['protein_sequence']['data']['sequence']
        translation_list.append({"translation":translation})
        protein_title = list(range(1,len(translation),50))
    else:
        translation_list.append('stop')
        translation=''
        protein_title=''

    # for table title
    unspliced_title = list(range(1,len(data1),50))  #把unspliced sequence 切出 1,51,101
    spliced_title = list(range(1,len(data2),50))
    

    #for table color
    unspliced_index = []
    exon_type_u = 0
    if any('3\'UTR' in item for item in unspliced):
        if any('5\'UTR' in item for item in unspliced):
            for i in range(0,len(unspliced)):
                if (unspliced[i][0] == '5\'UTR'):
                    for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                        unspliced_index.append(1)
                elif('Exon' in unspliced[i][0]):
                        if(exon_type_u == 0 ) :
                            if(unspliced[i+1][0] == '3\'UTR'):
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1]-1)):
                                    unspliced_index.append(2)
                                    exon_type_u = 1 
                            else:
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                    unspliced_index.append(2)
                                    exon_type_u = 1
                        elif (exon_type_u == 1) :
                            if(unspliced[i+1][0] == '3\'UTR'):
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1]-1)):
                                    unspliced_index.append(3) 
                                    exon_type_u =0
                            else:
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                    unspliced_index.append(3)
                                    exon_type_u =0                
                elif('Intron' in unspliced[i][0]):
                        if(unspliced[i+1][0] == '3\'UTR'):
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1])):
                                unspliced_index.append(4) 
                        else:
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                unspliced_index.append(4)
                elif(unspliced[i][0] == '3\'UTR'):
                    for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                        unspliced_index.append(5)
        else:
            for i in range(0,len(unspliced)):
                if('Exon' in unspliced[i][0]):
                        if(exon_type_u == 0 ) :
                            if(unspliced[i+1][0] == '3\'UTR'):
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1]-1)):
                                    unspliced_index.append(2)
                                    exon_type_u = 1 
                            else:
                                for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                                    unspliced_index.append(2)
                                    exon_type_u = 1
                        elif (exon_type_u == 1) :
                            if(unspliced[i+1][0] == '3\'UTR'):
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1]-1)):
                                    unspliced_index.append(3) 
                                    exon_type_u =0
                            else:
                                for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                    unspliced_index.append(3)
                                    exon_type_u =0                
                elif('Intron' in unspliced[i][0]):
                        if(unspliced[i+1][0] == '3\'UTR'):
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i+1][1])):
                                unspliced_index.append(4) 
                        else:
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                unspliced_index.append(4)
                elif(unspliced[i][0] == '3\'UTR'):
                    for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                        unspliced_index.append(5)
    else:
        if any('5\'UTR' in item for item in unspliced):
            for i in range(0,len(unspliced)):
                if (unspliced[i][0] == '5\'UTR'):
                    for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                        unspliced_index.append(1)
                elif('Exon' in unspliced[i][0]):
                        if(exon_type_u == 0 ) :
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                unspliced_index.append(2)
                                exon_type_u = 1
                        elif (exon_type_u == 1) :
                            for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                                unspliced_index.append(3)
                                exon_type_u =0                
                elif('Intron' in unspliced[i][0]):
                        for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                            unspliced_index.append(4)
        else:
            for i in range(0,len(unspliced)):
                if('Exon' in unspliced[i][0]):
                    if(exon_type_u == 0 ) :
                        for j in range(int(unspliced[i][1]-1),int(unspliced[i][2])):
                            unspliced_index.append(2)
                            exon_type_u = 1
                    elif (exon_type_u == 1) :
                        for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                            unspliced_index.append(3)
                            exon_type_u =0                
                elif('Intron' in unspliced[i][0]):
                    for j in range(int(unspliced[i-1][2]),int(unspliced[i][2])):
                        unspliced_index.append(4)


    spliced_index = []
    exon_type_s = 0
    if any('3\'UTR' in item for item in unspliced):
        if any('5\'UTR' in item for item in unspliced):
            for i in range(0,len(spliced)):
                if (spliced[i][0] == '5\'UTR'):
                    for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                        spliced_index.append(1)
                elif('Exon' in spliced[i][0]):
                        if(exon_type_s == 0 ) :
                            if(spliced[i+1][0] == '3\'UTR'):
                                for j in range(int(spliced[i-1][2]),int(spliced[i+1][1]-1)):
                                    spliced_index.append(2)
                                    exon_type_s = 1 
                            else:
                                for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                                    spliced_index.append(2)
                                    exon_type_s = 1
                        elif (exon_type_s == 1) :
                            if(spliced[i+1][0] == '3\'UTR'):
                                for j in range(int(spliced[i-1][2]),int(spliced[i+1][1]-1)):
                                    spliced_index.append(3) 
                                    exon_type_s =0
                            else:
                                for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                                    spliced_index.append(3)
                                    exon_type_s =0                
                elif(spliced[i][0] == '3\'UTR'):
                    for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                        spliced_index.append(5)
        else:
            for i in range(0,len(spliced)):
                if('Exon' in spliced[i][0]):
                    if(exon_type_s == 0 ) :
                        if(spliced[i+1][0] == '3\'UTR'):
                            for j in range(int(spliced[i-1][2]),int(spliced[i+1][1]-1)):
                                spliced_index.append(2)
                                exon_type_s = 1 
                        else:
                            for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                                spliced_index.append(2)
                                exon_type_s = 1
                    elif (exon_type_s == 1) :
                        if(spliced[i+1][0] == '3\'UTR'):
                            for j in range(int(spliced[i-1][2]),int(spliced[i+1][1]-1)):
                                spliced_index.append(3) 
                                exon_type_s =0
                        else:
                            for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                                spliced_index.append(3)
                                exon_type_s =0                
                elif(spliced[i][0] == '3\'UTR'):
                    for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                        spliced_index.append(5)
    else:
        if any('5\'UTR' in item for item in unspliced):
            for i in range(0,len(spliced)):
                if (spliced[i][0] == '5\'UTR'):
                    for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                        spliced_index.append(1)
                elif('Exon' in spliced[i][0]):
                        if(exon_type_s == 0 ) :
                            for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                                spliced_index.append(2)
                                exon_type_s = 1
                        elif (exon_type_s == 1) :
                            for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                                spliced_index.append(3)
                                exon_type_s =0                
        else:
            for i in range(0,len(spliced)):
                if('Exon' in spliced[i][0]):
                    if(exon_type_s == 0 ) :
                        for j in range(int(spliced[i][1]-1),int(spliced[i][2])):
                            spliced_index.append(2)
                            exon_type_s = 1
                    elif (exon_type_s == 1) :
                        for j in range(int(spliced[i-1][2]),int(spliced[i][2])):
                            spliced_index.append(3)
                            exon_type_s =0     
    #for d3 line
    unspliced_d3 = []
    exon_type_d3_u = 0
    for i in range(0,len(unspliced)):
        if (unspliced[i][0] == '5\'UTR'):
            unspliced_d3.append({"Type":'5\'UTR'})
            unspliced_d3[i]["start"] = unspliced[i][1]
            unspliced_d3[i]["end"] = unspliced[i][2]
            unspliced_d3[i]["x1"] = (unspliced[i][1]-1)+10
            unspliced_d3[i]["y1"] = 65
            unspliced_d3[i]["x2"] = (unspliced[i][2])+10
            unspliced_d3[i]["y2"] = 65
            unspliced_d3[i]["color"] = "gray"
        elif('Exon' in unspliced[i][0]):
                if(exon_type_d3_u == 0 ) :
                    unspliced_d3.append({"Type":'Exon'})
                    unspliced_d3[i]["start"] = unspliced[i][1]
                    unspliced_d3[i]["end"] = unspliced[i][2]
                    unspliced_d3[i]["x1"] = (unspliced[i][1]-1)+10
                    unspliced_d3[i]["y1"] = 50
                    unspliced_d3[i]["x2"] = (unspliced[i][2])+10
                    unspliced_d3[i]["y2"] = 50
                    unspliced_d3[i]["color"] = "yellow"
                    exon_type_d3_u = 1
                elif (exon_type_d3_u == 1) :
                    unspliced_d3.append({"Type":'Exon'})
                    unspliced_d3[i]["start"] = unspliced[i][1]
                    unspliced_d3[i]["end"] = unspliced[i][2]
                    unspliced_d3[i]["x1"] = (unspliced[i][1]-1)+10
                    unspliced_d3[i]["y1"] = 50
                    unspliced_d3[i]["x2"] = (unspliced[i][2])+10
                    unspliced_d3[i]["y2"] = 50
                    unspliced_d3[i]["color"] = "orange" 
                    exon_type_d3_u = 0             
        elif('Intron' in unspliced[i][0]):
            unspliced_d3.append({"Type":'Intron'})
            unspliced_d3[i]["start"] = unspliced[i][1]
            unspliced_d3[i]["end"] = unspliced[i][2]
            unspliced_d3[i]["x1"] = (unspliced[i][1]-1)+10
            unspliced_d3[i]["y1"] = 50
            unspliced_d3[i]["x2"] = (unspliced[i][2])+10
            unspliced_d3[i]["y2"] = 50
            unspliced_d3[i]["color"] = "GhostWhite"          
        elif(unspliced[i][0] == '3\'UTR'):
            unspliced_d3.append({"Type":'3\'UTR'})
            unspliced_d3[i]["start"] = unspliced[i][1]
            unspliced_d3[i]["end"] = unspliced[i][2]
            unspliced_d3[i]["x1"] = (unspliced[i][1]-1)+10
            unspliced_d3[i]["y1"] = 65
            unspliced_d3[i]["x2"] = (unspliced[i][2])+10
            unspliced_d3[i]["y2"] = 65
            unspliced_d3[i]["color"] = "gray"          
     
    spliced_d3 = []
    exon_type_d3_s = 0
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 65
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 65
            spliced_d3[i]["color"] = "gray"
        elif('Exon' in spliced[i][0]):
                if(exon_type_d3_s == 0 ) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "yellow"
                    exon_type_d3_s = 1
                elif (exon_type_d3_s == 1) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "orange" 
                    exon_type_d3_s = 0               
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 65
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 65
            spliced_d3[i]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 65
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 65
            spliced_d3[i]["color"] = "blue"                
    response = {
            'unspliced_table':unspliced_list,  
            'spliced_table':spliced_list,
            'translation':translation_list,
            'unspliced_sequence':data1,
            'spliced_sequence':data2, 
            'protein_sequence':translation,
            'unspliced_title':unspliced_title,
            'spliced_title':spliced_title,
            'protein_title':protein_title,
            'unspliced_index':unspliced_index,
            'spliced_index':spliced_index,
            'unspliced_d3_line':unspliced_d3,
            'spliced_d3_line':spliced_d3,

        }
    #C:/Users/jiego/Downloads
    '''
    os.remove('/home/cosbi/Downloads/unspliced+UTRTranscriptSequence_' + transcript_name + '.fasta')
    os.remove('/home/cosbi/Downloads/spliced+UTRTranscriptSequence_' + transcript_name + '.fasta')
    '''
    return JsonResponse(response)




def pirScan(request,id):
    sys.path.append('D:/jieweb/')
    data = crawler(id)
    current_working_directory = os.getcwd() #紀錄目前做資料夾
    os.chdir('/home/cosbi/forme/pirScan') # 換資料夾#/home/jiego/forme/pirScan #/home/cosbi/forme/pirScan
    with open ('inputSeq.fa','w') as f:
        f.write('>{}\n'.format(id)+data[3])
    os.system('python3 piTarPrediction.py inputSeq.fa ce none [0,2,2,3,6]') #windows 用 python ; linux 用 python3
    os.chdir(current_working_directory) #換回原本的資料夾
    return render(request, 'pirscan.html', locals())
def pirScan_data(request):
    transcript_name =request.POST['transcript_id']
    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)
    #D:/HW/pirScan/output/piRNA_targeting_sites.json
    with open ('/home/cosbi/forme/pirScan/output/piRNA_targeting_sites.json','r') as file:#/home/cosbi/forme/jieweb/pirScan/output/piRNA_targeting_sites.json
        jsondata = json.load(file)

    table_data = jsondata['newout']
    table_dict = []
    # for i in range(0,len(table_data)):
    for item in table_data:
        index = item[10].find("5'")
        start_end =item[1].split('-')
        modify_string_2 = item[10].replace('mark',"span class='y'")
        dict = {"piRNA":item[0],
                'piRNA_target_score':item[14],
                "target_region":item[1],
                'mismatches':item[2],
                "position_in_piRNA":item[3],
                "non_GU_mismatches_in_seed_region":item[5],
                "GU_mismatches_in_seed_region":item[6],
                "non_GU_mismatches_in_non_seed_region":item[7],
                "Gu_mismatches_in_non_seed_region":item[8],
                'pairing (top:Input sequence, bottom:piRNA)':item[9]+'<br>'+modify_string_2,
                'start':int(start_end[0]),
                'end':int(start_end[1]),
                'y':135

                            }
        table_dict.append(dict)
    table_dict = sorted(table_dict, key=itemgetter('start')) #排序list


    #for d3 line
    spliced = spliced.values.tolist()
    spliced_d3 = []
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]-1+10
            spliced_d3[index]["y1"] = 150
            spliced_d3[index]["x2"] = spliced[i][2]+10
            spliced_d3[index]["y2"] = 150
            spliced_d3[index]["color"] = "gray"         
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]-1+10
            spliced_d3[index]["y1"] = 150
            spliced_d3[index]["x2"] = spliced[i][2]+10
            spliced_d3[index]["y2"] = 150
            spliced_d3[index]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]-1+10
            spliced_d3[index]["y1"] = 150
            spliced_d3[index]["x2"] = spliced[i][2]+10
            spliced_d3[index]["y2"] = 150
            spliced_d3[index]["color"] = "blue"   
        else:
            continue    

    #for pirScan d3
    y = 135
    start = 0
    end = 0
    first = 1
    for i in range(0,len(table_dict)):
            if first == 1:
                start = table_dict[i]['start']
                end = table_dict[i]['end']
                first = 0
            elif first == 0 :    
                if (table_dict[i]['start'] >= start) and (table_dict[i]['start'] <= end):
                    start = table_dict[i]['start']
                    end = table_dict[i]['end']
                    table_dict[i]['y'] = table_dict[i-1]['y'] - 12
                    # if (table_dict[i-1]['y'] == y):
                    #     table_dict[i]['y'] = table_dict[i-1]['y'] - 12
                    # else:
                        # if (table_dict[i-2]['end'] <= start):
                        #     table_dict[i]['y'] = y
                        # elif(table_dict[i-3]['end'] <= start):
                        #     table_dict[i]['y'] = y
                        # elif(table_dict[i-4]['end'] <= start):
                        #     table_dict[i]['y'] = y
                        # elif(table_dict[i-5]['end'] <= start):
                        #     table_dict[i]['y'] = y
                        # elif(table_dict[i-6]['end'] <= start):
                        #     table_dict[i]['y'] = y
                        # else:
                        #     table_dict[i]['y'] = table_dict[i-1]['y'] - 12
                        # for j in range(2, i):
                        #     if table_dict[i - j]['end'] <= start:
                        #         table_dict[i]['y'] = y
                        #         break
                        # else:
                        #     table_dict[i]['y'] = table_dict[i - 1]['y'] + 10
                else:
                    start = table_dict[i]['start']
                    end = table_dict[i]['end']  

    for i in range(0,len(table_dict)):
        spliced_d3.append({"Type":table_dict[i]['piRNA']})
        index = len(spliced_d3) - 1 
        spliced_d3[index]["start"] = table_dict[i]['start']
        spliced_d3[index]["end"] = table_dict[i]['end']
        spliced_d3[index]["x1"] = table_dict[i]['start']-1+10
        spliced_d3[index]["y1"] = table_dict[i]['y']
        spliced_d3[index]["x2"] = table_dict[i]['end']+10
        spliced_d3[index]["y2"] = table_dict[i]['y']
        spliced_d3[index]["color"] = "green"  
    response ={
        'pirScan_d3_line':spliced_d3,
        'table_dict':table_dict,

    }
    return JsonResponse(response)

def function_list(request):
    return render(request, 'function_list.html', locals())

def filter(request):
    return render(request, 'filter.html', locals())


def filter_data(request):

    #use post to get javascript data
    gene=request.POST['gene'] 
    miRNA=request.POST['miRNA']
    readcount_mode =request.POST['readcount_mode'] 
    readcount=request.POST['readcount']
    RNAup_score_mode=request.POST['RNAup_score_mode']
    RNAup_score=request.POST['RNAup_score']
    miranda_energy_mode=request.POST['miranda_energy_mode']
    miranda_energy=request.POST['miranda_energy']
    RNAup_max_score_mode=request.POST['RNAup_max_score_mode']
    RNAup_max_score=request.POST['RNAup_max_score']
    miranda_max_energy_mode=request.POST['miranda_max_energy_mode']
    miranda_max_energy=request.POST['miranda_max_energy']   

    #篩選
    result = models.Srr3882728HybRnaupRnaupMirandaMirandaMutation.objects.all()

    #gene
    if (gene != ''):
        gene_name_get = models.CElegans.objects.get(gene_name__contains=gene)
        gene_sequence = gene_name_get.gene_sequence
        id = gene_name_get.wormbase_id
        result = result.filter(targetrnaname__icontains=gene_sequence)
        

    #miRNA
    if (miRNA != ''):
        miRNA_list = miRNA.split('\n')
        for i in range(0,len(miRNA_list)):
            result = result.filter(smallrnaname=miRNA_list[i])
    
    #readcount_mode
    if readcount_mode == '1' :
        result = result.filter(readcount__gt=readcount)
    elif readcount_mode == '2' :
        result = result.filter(readcount__lt=readcount)
    elif readcount_mode == '3' :
        result = result.filter(readcount=readcount)
    #RNAup_score_mode
    if RNAup_score_mode == '1' :
        result = result.filter(rnaupscore__gt=RNAup_score)
    elif RNAup_score_mode == '2' :
        result = result.filter(rnaupscore__lt=RNAup_score)
    elif RNAup_score_mode == '3' :
        result = result.filter(rnaupscore=RNAup_score)
    #miranda_energy_mode
    if miranda_energy_mode == '1' :
        result = result.filter(mirandaenergy__gt=miranda_energy)
    elif miranda_energy_mode == '2' :
        result = result.filter(mirandaenergy__lt=miranda_energy)
    elif miranda_energy_mode == '3' :
        result = result.filter(mirandascore=miranda_energy)
    #RNAup_max_score_mode
    if RNAup_max_score_mode == '1' :
        result = result.filter(rnaupmaxscore__gt=RNAup_max_score)
    elif RNAup_max_score_mode == '2' :
        result = result.filter(rnaupmaxscore__lt=RNAup_max_score)
    elif RNAup_max_score_mode == '3' :
        result = result.filter(rnaupmaxscore=RNAup_max_score)
    #miranda_max_energy_mode
    if miranda_max_energy_mode == '1' :
        result = result.filter(mirandamaxenergy__gt=miranda_max_energy)
    elif miranda_max_energy_mode == '2' :
        result = result.filter(mirandamaxenergy__lt=miranda_max_energy)
    elif miranda_max_energy_mode == '3' :
        result = result.filter(mirandamaxenergy=miranda_max_energy)
    

    table_list = []
        # 轉換成出來是字典的形式
    for row in result:
        start_end_mirandamax = row.mirandamaxbindingsite.split('-')
        table_list.append({
            'clashread': row.clashread,
            'readcount': row.readcount,
            'smallrnaname': row.smallrnaname,
            'regiononclashreadidentifiedassmallrna': row.regiononclashreadidentifiedassmallrna,
            'smallrnaregionfoundinclashread': row.smallrnaregionfoundinclashread,
            'targetrnaname': row.targetrnaname,
            'targetrnaregionfoundinclashread': row.targetrnaregionfoundinclashread,
            'rnaupmaxregulatorsequence': row.rnaupmaxregulatorsequence,
            'rnaupmaxtargetsequence': row.rnaupmaxtargetsequence,
            'rnaupmaxbindingsite': row.rnaupmaxbindingsite,
            'rnaupmaxscore': row.rnaupmaxscore,
            'rnaupregulatorsequence': row.rnaupregulatorsequence,
            'rnauptargetsequence': row.rnauptargetsequence,
            'rnaupbindingsite': row.rnaupbindingsite,
            'rnaupscore': row.rnaupscore,
            'mirandaenergy': row.mirandaenergy,
            'mirandamaxenergy': row.mirandamaxenergy,
            'mirandascore': row.mirandascore,
            'mirandabindingsite': row.mirandabindingsite,
            'mirandatargetsequence': row.mirandatargetsequence,
            'mirandaregulatorsequence': row.mirandaregulatorsequence,
            'mirandamaxbindingsite': row.mirandamaxbindingsite,
            'mirandamaxtargetsequence': row.mirandamaxtargetsequence,
            'mirandamaxregulatorsequence': row.mirandamaxregulatorsequence,
            'm': row.m,
            'id':id,
            'start_mirandamax':int(start_end_mirandamax[0]),
            'end_mirandamax':int(start_end_mirandamax[1]),
            })
    #minimum pairing
    table_list = plot(table_list,'mirandatargetsequence','mirandaregulatorsequence','miRanda_minpairing')
    table_list = plot(table_list,'rnauptargetsequence','rnaupregulatorsequence','rnaup_minpairing')
    #maximum pairing
    table_list = plot(table_list,'mirandamaxtargetsequence','mirandamaxregulatorsequence','miRanda_maxpairing')
    table_list = plot(table_list,'rnaupmaxtargetsequence','rnaupmaxregulatorsequence','rnaup_maxpairing')
    response = {
        'table_list':table_list,
    }
    return JsonResponse(response)

def search(request,id):
    return render(request, 'search.html', locals())

def search_data2(request):
    transcript_name =request.POST['transcript_id']
    check_list_str = request.POST.get('check_list')  
    check_list = check_list_str.split(',')  
    result = models.Srr3882728HybRnaupRnaupMirandaMirandaMutation.objects.all()
    result = result.filter(targetrnaname=transcript_name)

    if 'all' not in check_list:
        # Create a Q object to combine multiple filters
        filters = Q()
        for smallrnaname in check_list:
            filters |= Q(smallrnaname=smallrnaname)
        # Apply the combined filter to the result
        result = result.filter(filters)
    table_list = []
        # 轉換成出來是字典的形式
    for row in result:
        start_end_mirandamax = row.mirandamaxbindingsite.split('-')
        start_end_d3 = row.targetrnaregionfoundinclashread.split('-')
        table_list.append({
            'clashread': row.clashread,
            'readcount': row.readcount,
            'smallrnaname': row.smallrnaname,
            'targetrnaname': row.targetrnaname, 
            'targetrnaregionfoundinclashread': row.targetrnaregionfoundinclashread,
            'mirandabindingsite': row.mirandabindingsite,
            'mirandaenergy': row.mirandaenergy,
            'mirandatargetsequence': row.mirandatargetsequence,
            'mirandaregulatorsequence': row.mirandaregulatorsequence,
            'rnaupbindingsite': row.rnaupbindingsite,
            'rnaupscore': row.rnaupscore,
            'rnauptargetsequence': row.rnauptargetsequence,
            'rnaupregulatorsequence': row.rnaupregulatorsequence,
            'm': row.m,
            'start_mirandamax':int(start_end_mirandamax[0]),
            'end_mirandamax':int(start_end_mirandamax[1]),
            'start_d3':int(start_end_d3[0]),
            'end_d3':int(start_end_d3[1]),
            })
    table_list = plot(table_list,'mirandatargetsequence','mirandaregulatorsequence','miRanda_pairing')
    table_list = plot(table_list,'rnauptargetsequence','rnaupregulatorsequence','rnaup_pairing')

    table_list = sorted(table_list, key=itemgetter('start_d3')) #排序list

    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)
    #for d3 line
    spliced = spliced.values.tolist()
    spliced_d3 = []
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "gray"         
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "blue"   
        else:
            continue    
    #for clash d3
    y = 5
    start = 0
    end = 0
    first = 1
    clash_d3 = []
    for i in range(0,len(table_list)):
            if first == 1:
                start = table_list[i]['start_d3']
                end = table_list[i]['end_d3']
                clash_d3.append({"start":start})
                index = len(clash_d3) - 1 
                clash_d3[index]["end"] = end
                clash_d3[index]["x1"] = start
                clash_d3[index]["y1"] = y
                clash_d3[index]["x2"] = end
                clash_d3[index]["y2"] = y
                clash_d3[index]["color"] = "green"  
                clash_d3[index]["y"] = y
                clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                clash_d3[index]["readcount"] = table_list[index]['readcount']
                clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing'] 
                clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']               
                first = 0
            elif first == 0 :  
                if (table_list[i]['start_d3'] > start) and (table_list[i]['start_d3'] < end):
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']
                    clash_d3.append({"start":start})
                    index = len(clash_d3) - 1 
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["x2"] = end
                    if (clash_d3[index - 1]['y'] == y):
                        clash_d3[index]["y1"] = y + 12
                        clash_d3[index]["y2"] = y + 12
                        clash_d3[index]["y"] = y + 12
                        clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                        clash_d3[index]["readcount"] = table_list[index]['readcount']
                        clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                        clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                        clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                        clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                        clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                        clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                        clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                        clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   
                    else:
                        clash_d3[index]["y1"] = y + 12
                        clash_d3[index]["y2"] = y + 12
                        clash_d3[index]["y"] = y + 12
                        clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                        clash_d3[index]["readcount"] = table_list[index]['readcount']
                        clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                        clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                        clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                        clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                        clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                        clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                        clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']    
                        clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']                       
                elif (table_list[i]['start_d3'] == start) and (table_list[i]['end_d3'] == end):
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']
                    clash_d3.append({"start": start})
                    index = len(clash_d3) - 1
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["x2"] = end
                    clash_d3[index]["y1"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["y2"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["y"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["color"] = "green"
                    clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                    clash_d3[index]["readcount"] = table_list[index]['readcount']
                    clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                    clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                    clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                    clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                    clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                    clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                    clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                    clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   
                    
                else:
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']  
                    clash_d3.append({"start":start})
                    index = len(clash_d3) - 1 
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["y1"] = y
                    clash_d3[index]["x2"] = end
                    clash_d3[index]["y2"] = y
                    clash_d3[index]["color"] = "green"  
                    clash_d3[index]["y"] = y
                    clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                    clash_d3[index]["readcount"] = table_list[index]['readcount']
                    clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                    clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                    clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                    clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                    clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                    clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                    clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                    clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   

    response = {
        'table_list':table_list,
        'search_d3_line':spliced_d3,
        'clash_d3_line':clash_d3,
    }
    return JsonResponse(response)

def search_data(request):
    transcript_name =request.POST['transcript_id']

    result = models.Srr3882728HybRnaupRnaupMirandaMirandaMutation.objects.all()
    result = result.filter(targetrnaname=transcript_name)
    target_list=[]
        # 轉換成出來是字典的形式
    for row in result:
        target_list.append({
            'smallrnaname': row.smallrnaname,
            })
    select_list=[]
    for i in range(0,len(target_list)):
        if target_list[i]['smallrnaname'] not in select_list :
            select_list.append(target_list[i]['smallrnaname'])
    
    temp = select_list[0]
    result2 = models.Srr3882728HybRnaupRnaupMirandaMirandaMutation.objects.all()
    result2 = result2.filter(targetrnaname=transcript_name)
    result2 = result2.filter(smallrnaname=temp)

    table_list = []
    for row in result2:
        start_end_mirandamax = row.mirandamaxbindingsite.split('-')
        start_end_d3 = row.targetrnaregionfoundinclashread.split('-')
        table_list.append({
            'clashread': row.clashread,
            'readcount': row.readcount,
            'smallrnaname': row.smallrnaname,
            'targetrnaname': row.targetrnaname, 
            'targetrnaregionfoundinclashread': row.targetrnaregionfoundinclashread,
            'mirandabindingsite': row.mirandabindingsite,
            'mirandaenergy': row.mirandaenergy,
            'mirandatargetsequence': row.mirandatargetsequence,
            'mirandaregulatorsequence': row.mirandaregulatorsequence,
            'rnaupbindingsite': row.rnaupbindingsite,
            'rnaupscore': row.rnaupscore,
            'rnauptargetsequence': row.rnauptargetsequence,
            'rnaupregulatorsequence': row.rnaupregulatorsequence,
            'm': row.m,
            'start_mirandamax':int(start_end_mirandamax[0]),
            'end_mirandamax':int(start_end_mirandamax[1]),
            'start_d3':int(start_end_d3[0]),
            'end_d3':int(start_end_d3[1]),
            })
    table_list = plot(table_list,'mirandatargetsequence','mirandaregulatorsequence','miRanda_pairing')
    table_list = plot(table_list,'rnauptargetsequence','rnaupregulatorsequence','rnaup_pairing')

    table_list = sorted(table_list, key=itemgetter('start_d3')) #排序list

    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)
    #for d3 line
    spliced = spliced.values.tolist()
    spliced_d3 = []
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "gray"         
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            index = len(spliced_d3) - 1 
            spliced_d3[index]["start"] = spliced[i][1]
            spliced_d3[index]["end"] = spliced[i][2]
            spliced_d3[index]["x1"] = spliced[i][1]
            spliced_d3[index]["y1"] = 100
            spliced_d3[index]["x2"] = spliced[i][2]
            spliced_d3[index]["y2"] = 100
            spliced_d3[index]["color"] = "blue"   
        else:
            continue    
    #for clash d3
    y = 5
    start = 0
    end = 0
    first = 1
    clash_d3 = []
    for i in range(0,len(table_list)):
            if first == 1:
                start = table_list[i]['start_d3']
                end = table_list[i]['end_d3']
                clash_d3.append({"start":start})
                index = len(clash_d3) - 1 
                clash_d3[index]["end"] = end
                clash_d3[index]["x1"] = start
                clash_d3[index]["y1"] = y
                clash_d3[index]["x2"] = end
                clash_d3[index]["y2"] = y
                clash_d3[index]["color"] = "green"  
                clash_d3[index]["y"] = y
                clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                clash_d3[index]["readcount"] = table_list[index]['readcount']
                clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing'] 
                clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']               
                first = 0
            elif first == 0 :  
                if (table_list[i]['start_d3'] > start) and (table_list[i]['start_d3'] < end):
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']
                    clash_d3.append({"start":start})
                    index = len(clash_d3) - 1 
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["x2"] = end
                    if (clash_d3[index - 1]['y'] == y):
                        clash_d3[index]["y1"] = y + 12
                        clash_d3[index]["y2"] = y + 12
                        clash_d3[index]["y"] = y + 12
                        clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                        clash_d3[index]["readcount"] = table_list[index]['readcount']
                        clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                        clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                        clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                        clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                        clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                        clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                        clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                        clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   
                    else:
                        clash_d3[index]["y1"] = y + 12
                        clash_d3[index]["y2"] = y + 12
                        clash_d3[index]["y"] = y + 12
                        clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                        clash_d3[index]["readcount"] = table_list[index]['readcount']
                        clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                        clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                        clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                        clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                        clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                        clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                        clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']    
                        clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']                       
                elif (table_list[i]['start_d3'] == start) and (table_list[i]['end_d3'] == end):
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']
                    clash_d3.append({"start": start})
                    index = len(clash_d3) - 1
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["x2"] = end
                    clash_d3[index]["y1"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["y2"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["y"] = clash_d3[index - 1]["y"] + 12
                    clash_d3[index]["color"] = "green"
                    clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                    clash_d3[index]["readcount"] = table_list[index]['readcount']
                    clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                    clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                    clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                    clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                    clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                    clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                    clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                    clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   
                    
                else:
                    start = table_list[i]['start_d3']
                    end = table_list[i]['end_d3']  
                    clash_d3.append({"start":start})
                    index = len(clash_d3) - 1 
                    clash_d3[index]["end"] = end
                    clash_d3[index]["x1"] = start
                    clash_d3[index]["y1"] = y
                    clash_d3[index]["x2"] = end
                    clash_d3[index]["y2"] = y
                    clash_d3[index]["color"] = "green"  
                    clash_d3[index]["y"] = y
                    clash_d3[index]["targetrnaname"] = table_list[index]['targetrnaname']
                    clash_d3[index]["readcount"] = table_list[index]['readcount']
                    clash_d3[index]["targetrnaregionfoundinclashread"] = table_list[index]['targetrnaregionfoundinclashread']
                    clash_d3[index]["mirandabindingsite"] = table_list[index]['mirandabindingsite']
                    clash_d3[index]["mirandaenergy"] = table_list[index]['mirandaenergy']
                    clash_d3[index]["miRanda_pairing"] = table_list[index]['miRanda_pairing']
                    clash_d3[index]["rnaupbindingsite"] = table_list[index]['rnaupbindingsite']
                    clash_d3[index]["rnaupscore"] = table_list[index]['rnaupscore']
                    clash_d3[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']
                    clash_d3[index]["smallrnaname"] = table_list[index]['smallrnaname']   

    response = {
        'select_list':select_list,
        'table_list':table_list,
        'search_d3_line':spliced_d3,
        'clash_d3_line':clash_d3,
    }
    return JsonResponse(response)

def read_count(request,id):
    return render(request, 'read_count.html', locals())
def read_count_data(request):
    transcript_name =request.POST['transcript_id']
 
    result = models.WtclashHybFinalWeb.objects.all()
    result = result.filter(target_rna_name=transcript_name)


    target_list=[]
    # 轉換成出來是字典的形式
    for row in result:
        target_list.append({
            'regulator_rna_name': row.regulator_rna_name,
            })
    # print(target_list)
    select_list=[]
    for i in range(0,len(target_list)):
        if target_list[i]['regulator_rna_name'] not in select_list :
            select_list.append(target_list[i]['regulator_rna_name'])
  
    check_box = []
    for i in range(0,len(select_list)) :
        check_box.append({'RNANAME':select_list[i]}) 

    temp = select_list[0]
    result2 = models.WtclashHybFinalWeb.objects.all()
    result2 = result2.filter(target_rna_name=transcript_name)
    result2 = result2.filter(regulator_rna_name=temp)

    table_list = []
    for row in result2:
        start_end_clash = row.target_rna_region_found_in_clash_read.split('-')
        table_list.append({
            'CLASH read ID': row.id,
            'CLASH read sequence': row.clash_read,
            'Region identified by piRNA': row.region_on_clash_read_identified_as_regulator_rna,
            'Region identified by target RNA': row.region_on_clash_read_identified_as_target_rna, 
            'hybrid Count': row.read_count,
            'Clash identified region': row.target_rna_region_found_in_clash_read,
            'predicted binding site from pirScan': row.pirscan_min_ex_binding_site,
            'pirScan targeting score': row.pirscan_min_ex_score,
            'WT_WAGO122G(pirScan)': row.wt_wago_pirscan_min_ex25_22g,
            'prg-1 mutant WAGO122G(pirScan)': row.prg1mut_wago1_22g_pirscan_min_ex25,
            '22G-RNA fold change(pirScan)': row.wago1_22g_pirscan_min_ex25_foldchange,
            'pirScan_min_ex_target_rna_sequence' :row.rnaup_min_ex_target_rna_sequence,
            'pirScan_min_ex_regulator_rna_sequence':row.rnaup_min_ex_regulator_rna_sequence,
            'rnaup_max_ex_target_rna_sequence' :row.rnaup_max_ex_target_rna_sequence,
            'rnaup_max_ex_regulator_rna_sequence':row.rnaup_max_ex_regulator_rna_sequence,
            'predicted binding site from RNAup': row.rnaup_min_ex_binding_site,
            'RNAup binding energy': row.rnaup_min_ex_score,
            'WT_WAGO122G(RNAup)': row.wt_wago_rnaup_min_ex25_22g,
            'prg-1 mutant WAGO122G(RNAup)': row.prg1mut_wago1_22g_rnaup_min_ex25,
            '22G-RNA fold change(RNAup)': row.wago1_22g_rnaup_min_ex25_foldchange,
            'start_clash':int(start_end_clash [0]),
            'end_clash':int(start_end_clash [1]),
            })
    table_list = plot(table_list,'pirScan_min_ex_target_rna_sequence','pirScan_min_ex_regulator_rna_sequence','pirScan_pairing')   
    table_list = plot(table_list,'rnaup_max_ex_target_rna_sequence','rnaup_max_ex_regulator_rna_sequence','rnaup_pairing')
    table_list = sorted(table_list, key=itemgetter('start_clash')) #排序list

    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)
    #for spliced d3 line
    spliced = spliced.values.tolist()

    spliced_d3 = []
    exon_type_d3_s = 0
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "gray"
        elif('Exon' in spliced[i][0]):
                if(exon_type_d3_s == 0 ) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "yellow"
                    exon_type_d3_s = 1
                elif (exon_type_d3_s == 1) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "orange" 
                    exon_type_d3_s = 0               
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "blue"    


    #for piRTarBase d3
    y = 5
    start = 0
    end = 0
    first = 1
    piRTarBase_list = []
    for i in range(0,len(table_list)):
            if first == 1:
                start = table_list[i]['start_clash']
                end = table_list[i]['end_clash']
                piRTarBase_list.append({"start":start})
                index = len(piRTarBase_list) - 1 
                piRTarBase_list[index]["end"] = end
                piRTarBase_list[index]["x1"] = start
                piRTarBase_list[index]["y1"] = y
                piRTarBase_list[index]["x2"] = end
                piRTarBase_list[index]["y2"] = y
                piRTarBase_list[index]["color"] = "#FF6464"  
                piRTarBase_list[index]["y"] = y
                piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
                piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
                piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
                piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
                piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
                piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
                piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
                piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
                piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

                piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
                piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
                piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']           
 
                first = 0
            # elif first == 0 :  
            #     if (table_list[i]['start_clash'] > start) and (table_list[i]['start_clash'] < end):
            #         start = table_list[i]['start_clash']
            #         end = table_list[i]['end_clash']
            #         piRTarBase_list.append({"start":start})
            #         index = len(piRTarBase_list) - 1 
            #         piRTarBase_list[index]["end"] = end
            #         piRTarBase_list[index]["x1"] = start
            #         piRTarBase_list[index]["x2"] = end
            #         if (piRTarBase_list[index - 1]['y'] == y):
            #             piRTarBase_list[index]["y1"] = y + 12
            #             piRTarBase_list[index]["y2"] = y + 12
            #             piRTarBase_list[index]["y"] = y + 12
            #             piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
            #             piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
            #             piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
            #             piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
            #             piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
            #             piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
            #             piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
            #             piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
            #             piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
            #             piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

            #             piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
            #             piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
            #             piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
            #             piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']     
            #         else:
            #             piRTarBase_list[index]["y1"] = y + 12
            #             piRTarBase_list[index]["y2"] = y + 12
            #             piRTarBase_list[index]["y"] = y + 12
            #             piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
            #             piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
            #             piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
            #             piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
            #             piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
            #             piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
            #             piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
            #             piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
            #             piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
            #             piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

            #             piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
            #             piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
            #             piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
            #             piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']                                                 
            #     elif (table_list[i]['start_clash'] == start) and (table_list[i]['end_clash'] == end):
            #         start = table_list[i]['start_clash']
            #         end = table_list[i]['end_clash']
            #         piRTarBase_list.append({"start": start})
            #         index = len(piRTarBase_list) - 1
            #         piRTarBase_list[index]["end"] = end
            #         piRTarBase_list[index]["x1"] = start
            #         piRTarBase_list[index]["x2"] = end
            #         piRTarBase_list[index]["y1"] = piRTarBase_list[index - 1]["y"] + 12
            #         piRTarBase_list[index]["y2"] = piRTarBase_list[index - 1]["y"] + 12
            #         piRTarBase_list[index]["y"] = piRTarBase_list[index - 1]["y"] + 12
            #         piRTarBase_list[index]["color"] = "green"
            #         piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
            #         piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
            #         piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
            #         piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
            #         piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
            #         piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
            #         piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
            #         piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
            #         piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
            #         piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

            #         piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
            #         piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
            #         piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
            #         piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']                       
                    
            else:
                start = table_list[i]['start_clash']
                end = table_list[i]['end_clash']  
                piRTarBase_list.append({"start":start})
                index = len(piRTarBase_list) - 1 
                piRTarBase_list[index]["end"] = end
                piRTarBase_list[index]["x1"] = start
                piRTarBase_list[index]["y1"] = piRTarBase_list[index-1]["y1"]+12
                piRTarBase_list[index]["x2"] = end
                piRTarBase_list[index]["y2"] = piRTarBase_list[index-1]["y2"]+12
                piRTarBase_list[index]["color"] = "#FF6464"  
                piRTarBase_list[index]["y"] = piRTarBase_list[index-1]["y"]+12
                piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
                piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
                piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
                piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
                piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
                piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
                piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
                piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
                piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

                piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
                piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
                piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']     

    result3 = models.WtCrisprWago1FlagIpSrnaSeqBedgraph.objects.all()
    result3 = result3.filter(ref_id=transcript_name)

    A22_list = []
    for row in result3:
        A22_list.append({
            'A22_start': row.init_pos,
            'A22_end': row.end_pos,
            'A22_value': row.evenly_rc,
            'color':'#001253',
            })
    # print(A22_list)
    response = {
        'check_box':check_box,
        'table_list':table_list,
        'search_d3_line':spliced_d3,
        'piRTarBase_list':piRTarBase_list,
        'A22_list':A22_list,
    }
    return JsonResponse(response)

def read_count_data2(request):
    transcript_name =request.POST['transcript_id']
    check_list_str = request.POST.get('check_list')  
    check_list = check_list_str.split(',')  

    result = models.WtclashHybFinalWeb.objects.all()
    result = result.filter(target_rna_name=transcript_name)

    if 'all' not in check_list:
    # Create a Q object to combine multiple filters
        filters = Q()
        for rna_name in check_list:
            filters |= Q(regulator_rna_name=rna_name)
        # Apply the combined filter to the result
        result = result.filter(filters)

    table_list = []
    for row in result:
        start_end_clash = row.target_rna_region_found_in_clash_read.split('-')
        table_list.append({
            'CLASH read ID': row.id,
            'CLASH read sequence': row.clash_read,
            'Region identified by piRNA': row.region_on_clash_read_identified_as_regulator_rna,
            'Region identified by target RNA': row.region_on_clash_read_identified_as_target_rna, 
            'hybrid Count': row.read_count,
            'Clash identified region': row.target_rna_region_found_in_clash_read,
            'predicted binding site from pirScan': row.pirscan_min_ex_binding_site,
            'pirScan targeting score': row.pirscan_min_ex_score,
            'WT_WAGO122G(pirScan)': row.wt_wago_pirscan_min_ex25_22g,
            'prg-1 mutant WAGO122G(pirScan)': row.prg1mut_wago1_22g_pirscan_min_ex25,
            '22G-RNA fold change(pirScan)': row.wago1_22g_pirscan_min_ex25_foldchange,
            'pirScan_min_ex_target_rna_sequence' :row.rnaup_min_ex_target_rna_sequence,
            'pirScan_min_ex_regulator_rna_sequence':row.rnaup_min_ex_regulator_rna_sequence,
            'rnaup_max_ex_target_rna_sequence' :row.rnaup_max_ex_target_rna_sequence,
            'rnaup_max_ex_regulator_rna_sequence':row.rnaup_max_ex_regulator_rna_sequence,
            'predicted binding site from RNAup': row.rnaup_min_ex_binding_site,
            'RNAup binding energy': row.rnaup_min_ex_score,
            'WT_WAGO122G(RNAup)': row.wt_wago_rnaup_min_ex25_22g,
            'prg-1 mutant WAGO122G(RNAup)': row.prg1mut_wago1_22g_rnaup_min_ex25,
            '22G-RNA fold change(RNAup)': row.wago1_22g_rnaup_min_ex25_foldchange,
            'start_clash':int(start_end_clash [0]),
            'end_clash':int(start_end_clash [1]),
            })
    table_list = plot(table_list,'pirScan_min_ex_target_rna_sequence','pirScan_min_ex_regulator_rna_sequence','pirScan_pairing')   
    table_list = plot(table_list,'rnaup_max_ex_target_rna_sequence','rnaup_max_ex_regulator_rna_sequence','rnaup_pairing')
    table_list = sorted(table_list, key=itemgetter('start_clash')) #排序list

    unspliced,spliced,data1,data2,data,spliced_sp  = crawler(transcript_name)
    #for spliced d3 line
    spliced = spliced.values.tolist()

    spliced_d3 = []
    exon_type_d3_s = 0
    for i in range(0,len(spliced)):
        if (spliced[i][0] == '5\'UTR'):
            spliced_d3.append({"Type":'5\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "gray"
        elif('Exon' in spliced[i][0]):
                if(exon_type_d3_s == 0 ) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "yellow"
                    exon_type_d3_s = 1
                elif (exon_type_d3_s == 1) :
                    spliced_d3.append({"Type":'Exon'})
                    spliced_d3[i]["start"] = spliced[i][1]
                    spliced_d3[i]["end"] = spliced[i][2]
                    spliced_d3[i]["x1"] = spliced[i][1]-1+10
                    spliced_d3[i]["y1"] = 50
                    spliced_d3[i]["x2"] = spliced[i][2]+10
                    spliced_d3[i]["y2"] = 50
                    spliced_d3[i]["color"] = "orange" 
                    exon_type_d3_s = 0               
        elif(spliced[i][0] == '3\'UTR'):
            spliced_d3.append({"Type":'3\'UTR'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "gray"
        elif(spliced[i][0] == 'CDS'):
            spliced_d3.append({"Type":'CDS'})
            spliced_d3[i]["start"] = spliced[i][1]
            spliced_d3[i]["end"] = spliced[i][2]
            spliced_d3[i]["x1"] = spliced[i][1]-1+10
            spliced_d3[i]["y1"] = 80
            spliced_d3[i]["x2"] = spliced[i][2]+10
            spliced_d3[i]["y2"] = 80
            spliced_d3[i]["color"] = "blue"    

    #for piRTarBase d3
    y = 5
    start = 0
    end = 0
    first = 1
    piRTarBase_list = []
    for i in range(0,len(table_list)):
            if first == 1:
                start = table_list[i]['start_clash']
                end = table_list[i]['end_clash']
                piRTarBase_list.append({"start":start})
                index = len(piRTarBase_list) - 1 
                piRTarBase_list[index]["end"] = end
                piRTarBase_list[index]["x1"] = start
                piRTarBase_list[index]["y1"] = y
                piRTarBase_list[index]["x2"] = end
                piRTarBase_list[index]["y2"] = y
                piRTarBase_list[index]["color"] = "#FF6464"  
                piRTarBase_list[index]["y"] = y
                piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
                piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
                piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
                piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
                piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
                piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
                piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
                piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
                piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

                piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
                piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
                piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']           
 
                first = 0
            else:
                start = table_list[i]['start_clash']
                end = table_list[i]['end_clash']  
                piRTarBase_list.append({"start":start})
                index = len(piRTarBase_list) - 1 
                piRTarBase_list[index]["end"] = end
                piRTarBase_list[index]["x1"] = start
                piRTarBase_list[index]["y1"] = piRTarBase_list[index-1]["y1"]+12
                piRTarBase_list[index]["x2"] = end
                piRTarBase_list[index]["y2"] = piRTarBase_list[index-1]["y2"]+12
                piRTarBase_list[index]["color"] = "#FF6464"  
                piRTarBase_list[index]["y"] = piRTarBase_list[index-1]["y"]+12
                piRTarBase_list[index]["CLASH_read_ID"] = table_list[index]['CLASH read ID']
                piRTarBase_list[index]["hybrid_Count"] = table_list[index]['hybrid Count']
                piRTarBase_list[index]["predicted_binding_site_from_pirScan"] = table_list[index]['predicted binding site from pirScan']
                piRTarBase_list[index]["pirScan_targeting_score"] = table_list[index]['pirScan targeting score']
                piRTarBase_list[index]["WT_WAGO122G_pirScan"] = table_list[index]['WT_WAGO122G(pirScan)']
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_pirScan"] = table_list[index]['prg-1 mutant WAGO122G(pirScan)']
                piRTarBase_list[index]["A22G_RNA_fold_change_pirScan"] = table_list[index]['22G-RNA fold change(pirScan)']
                piRTarBase_list[index]["pirScan_pairing"] = table_list[index]['pirScan_pairing']
                piRTarBase_list[index]["predicted_binding_site_from_RNAup"] = table_list[index]['predicted binding site from RNAup'] 
                piRTarBase_list[index]["RNAup_binding_energy"] = table_list[index]['RNAup binding energy']     

                piRTarBase_list[index]["WT_WAGO122G_RNAup"] = table_list[index]['WT_WAGO122G(RNAup)'] 
                piRTarBase_list[index]["prg_1_mutant_WAGO122G_RNAup"] = table_list[index]['prg-1 mutant WAGO122G(RNAup)'] 
                piRTarBase_list[index]["A22G_RNA_fold_change_RNAup"] = table_list[index]['22G-RNA fold change(RNAup)'] 
                piRTarBase_list[index]["rnaup_pairing"] = table_list[index]['rnaup_pairing']     

    result3 = models.WtCrisprWago1FlagIpSrnaSeqBedgraph.objects.all()
    result3 = result3.filter(ref_id=transcript_name)

    A22_list = []
    for row in result3:
        A22_list.append({
            'A22_start': row.init_pos,
            'A22_end': row.end_pos,
            'A22_value': row.evenly_rc,
            'color':'#001253',
            })
        

    response = {
        'table_list':table_list,
        'search_d3_line':spliced_d3,
        'piRTarBase_list':piRTarBase_list,
        'A22_list':A22_list,
    }
    return JsonResponse(response)