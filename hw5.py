import pandas as pd
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

#Y40B10A.2a.1
#F54H12.1c.3

#json 靜態爬
transcript_name =request.POST['transcript_id'] #由transcript.js回傳
response = requests.get(
        "https://wormbase.org/rest/widget/transcript/" + transcript_name + "/sequences",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })

soup = BeautifulSoup(response.text, "html.parser")
data= json.loads(str(soup))

#處理變成dict
strand = data["fields"]['unspliced_sequence_context']['data']['strand']
#check + -
if strand == "+" :
    data1 = data["fields"]['unspliced_sequence_context']['data']['positive_strand']['sequence']
    data2 = data["fields"]['spliced_sequence_context']['data']['positive_strand']['sequence']
else:
    data1 = data["fields"]['unspliced_sequence_context']['data']['negative_strand']['sequence']
    data2 = data["fields"]['spliced_sequence_context']['data']['negative_strand']['sequence']


def check(a,b):
    transcription = ''  # 空的list
    i = 0
    while i < len(a):
        # 找Exon
        if a[i].isupper():  # 判斷大寫
            transcription += a[i]  # 把該個字元加進去
            if i == len(a)-1:  # 用來停止while迴圈
                break
            elif a[i+1].islower():
                transcription += ','
        # 找Intron
        elif a[i].islower():  # 判斷小寫
            transcription += a[i]
            if i == len(a)-1:
                break
            elif a[i+1].isupper():
                transcription += ','
        i += 1  # 逐個檢查
    # 弄成DataFrame的形式
    df1 = pd.DataFrame(columns=['Exon&Intron'])  # 建立兩個column的DataFrame
    df1['Exon&Intron'] = transcription.split(',')
    transcription = '' #空的list
    i = 0 

    while i <len(b):
        #找Exon
        if b[i].isupper(): #判斷大寫
            transcription  += b[i] #把該個字元加進去
            if i == len(b)-1: #用來停止while迴圈
                break
            elif b[i+1].islower():
                transcription  += ','
        #找Intron
        elif b[i].islower(): #判斷小寫
            transcription  += b[i]
            if i == len(b)-1:
                break
            elif b[i+1].isupper():
                transcription  += ','
        i += 1 #逐個檢查
    #弄成DataFrame的形式
    df2 = pd.DataFrame(columns=['Exon&Intron']) #建立兩個column的DataFrame
    df2['Exon&Intron'] = transcription.split(',')

    global c
    if df1.at[0,'Exon&Intron'] == df2.at[0,'Exon&Intron']:
        c = 0
        print('easy')

    else:
        c = 1 
        print('hard')

check(data1,data2)

if c == 0:
    #print('easy')
    #把大小寫切出來
    
    #for unspliced
    transcription = '' #空的list
    upper_lower = ''  #空的list 用來記錄有幾次大小寫變化
    i = 0 

    while i <len(data1):
        #找Exon
        if data1[i].isupper(): #判斷大寫
            transcription  += data1[i] #把該個字元加進去
            if i == len(data1)-1: #用來停止while迴圈
                break
            elif data1[i+1].islower():
                transcription  += ','
                upper_lower += 'U,'
        #找Intron
        elif data1[i].islower(): #判斷小寫
            transcription  += data1[i]
            if i == len(data1)-1:
                break
            elif data1[i+1].isupper():
                transcription  += ','
                upper_lower += 'L,'
        i += 1 #逐個檢查
    #處理最後一個的大小寫
    if data1[len(data1)-2].isupper():
        upper_lower +='U'
    else:
        upper_lower +='L'

    #弄成DataFrame的形式
    df1 = pd.DataFrame(columns=['temp','Exon&Intron']) #建立兩個column的DataFrame
    df1['temp'] = upper_lower.split(',') #split 表示依照什麼東西來區別 因為是string
    df1['Exon&Intron'] = transcription.split(',')

    #處理5'UTR和3'UTR
    if df1.at[0,'temp'] == 'L': #開頭小寫表示有5'UTR
        df1.at[0,'temp'] = '5'
    if df1.at[len(df1)-1,'temp'] == 'L': #結尾小寫表示有3'UTR
        df1.at[len(df1)-1,'temp'] = '3'
    #print(df1)

    #判斷Intron(小寫的)跟Exon(大寫的)
    count_Intron= 1
    count_Exon = 1
    for k in range(0,len(df1)):
        if df1.at[k,'temp'] == 'L':
            df1.at[k,'Name'] = 'Intron' + str(count_Intron)
            count_Intron+= 1
        elif df1.at[k,'temp'] == 'U':
            df1.at[k,'Name'] = 'Exon' + str(count_Exon)
            count_Exon += 1
        elif df1.at[k,'temp'] == '5':
            df1.at[k,'Name'] = '5\'UTR'
        elif df1.at[k,'temp'] == '3':
            df1.at[k,'Name'] = '3\'UTR'


    #弄一個dataframe 給spliced 用
    df3 = pd.DataFrame()
    df3 = df1
    for k in range(0,len(df3)):
        if df3.at[k,'temp'] == 'L' :
            df3 = df3.drop(labels = k)
    df3 = df3.reset_index()  
    df3 = df3.drop(columns='index')


    #計算Length
    df1['Length'] = df1['Exon&Intron'].str.len()

    #計算起始與終點位置方便標顏色
    #處理頭
    if df1.at[0,'temp'] != 'U' and df1.at[0,'temp'] !='L': #計算5'UTR
        df1.at[0,'Start'] = 1 #新增column
        df1.at[0,'End'] = df1.at[0,'Start'] + df1.at[0,'Length'] -1
        #計算Exon1(因為要含5'utr所以比較特別)
        df1.at[1,'Start'] = 1 
        df1.at[1,'End'] = df1.at[0,'Length'] + df1.at[1,'Length'] 
        df1.at[1,'Length'] = df1.at[0,'Length'] + df1.at[1,'Length']
    #處理沒有5'UTR的
    if df1.at[0,'temp'] == 'U' :
        df1.at[0,'Start'] = 1
        df1.at[0,'End'] = df1.at[0,'Start'] +df1.at[0,'Length'] -1
    #處理中間    
    for l in range(0,len(df1)): #計算Exon & Intron
        if df1.at[l,'Start'] !=1:
            df1.at[l,'Start'] = df1.at[l-1,'End'] + 1 #第2個的開始由第1個的結尾
            df1.at[l,'End'] = df1.at[l,'Start'] +df1.at[l,'Length'] -1
    #處理尾         
    if df1.at[len(df1)-1,'temp'] != 'U' and df1.at[len(df1)-1,'temp'] !='L': #計算3'UTR
        df1.at[len(df1)-1,'End'] = df1.at[len(df1)-2,'End'] + df1.at[len(df1)-1,'Length']
        df1.at[len(df1)-2,'End'] = df1.at[len(df1)-2,'End'] + df1.at[len(df1)-1,'Length'] #特別處理Exon因為要包含3'UTR
        df1.at[len(df1)-2,'Length'] = df1.at[len(df1)-2,'Length'] + df1.at[len(df1)-1,'Length']

    #for spliced
    transcription_spliced = '' #空的list
    upper_lower = ''  #空的list 用來記錄有幾次大小寫變化
    i = 0 

    while i <len(data2):
        #找Exon
        if data2[i].isupper(): #判斷大寫
            transcription_spliced  += data2[i] #把該個字元加進去
            if i == len(data2)-1: #用來停止while迴圈
                break
            elif data2[i+1].islower():
                transcription_spliced  += ','
                upper_lower += 'U,'
        #找Intron
        elif data2[i].islower(): #判斷小寫
            transcription_spliced  += data2[i]
            if i == len(data2)-1:
                break
            elif data2[i+1].isupper():
                transcription_spliced  += ','
                upper_lower += 'L,'
        i += 1 #逐個檢查
    #處理最後一個的大小寫
    if data2[len(data2)-2].isupper():
        upper_lower +='U'
    else:
        upper_lower +='L'


    #弄成DataFrame的形式
    df2 = pd.DataFrame(columns=['temp','Exon&Intron']) #建立兩個column的DataFrame
    df2['temp'] = upper_lower.split(',') #split 表示依照什麼東西來區別 因為是string
    df2['Exon&Intron'] = transcription_spliced.split(',')

    #處理5'UTR和3'UTR
    if df2.at[0,'temp'] == 'L': #開頭小寫表示有5'UTR
        df2.at[0,'temp'] = '5'
    
    if df2.at[len(df2)-1,'temp'] == 'L': #結尾小寫表示有3'UTR
        df2.at[len(df2)-1,'temp'] = '3'
    
    #刪掉Intron

    df3['Length'] = df3['Exon&Intron'].str.len()

    #計算起始與終點位置方便標顏色
    #處理頭
    if df3.at[0,'temp'] != 'U' and df3.at[0,'temp'] !='L': #計算5'UTR
        df3.at[0,'Start'] = 1 #新增column
        df3.at[0,'End'] = df3.at[0,'Start'] + df3.at[0,'Length'] -1
        #計算Exon1(因為要含5'utr所以比較特別)
        df3.at[1,'Start'] = 1 
        df3.at[1,'End'] = df3.at[0,'Length'] + df3.at[1,'Length'] 
        df3.at[1,'Length'] = df3.at[0,'Length'] + df3.at[1,'Length']
    #處理沒有5'UTR的
    if df3.at[0,'temp'] == 'U' :
        df3.at[0,'Start'] = 1
        df3.at[0,'End'] = df3.at[0,'Start'] +df3.at[0,'Length'] -1
    #處理中間    
    for l in range(0,len(df3)): #計算Exon & Intron
        if df3.at[l,'Start'] !=1:
            df3.at[l,'Start'] = df3.at[l-1,'End'] + 1 #第2個的開始由第1個的結尾
            df3.at[l,'End'] = df3.at[l,'Start'] +df3.at[l,'Length'] -1
    #處理尾         
    if df3.at[len(df3)-1,'temp'] != 'U' and df3.at[len(df3)-1,'temp'] !='L': #計算3'UTR
        df3.at[len(df3)-1,'End'] = df3.at[len(df3)-2,'End'] + df3.at[len(df3)-1,'Length']
        df3.at[len(df3)-2,'End'] = df3.at[len(df3)-2,'End'] + df3.at[len(df3)-1,'Length'] #特別處理Exon因為要包含3'UTR
        df3.at[len(df3)-2,'Length'] = df3.at[len(df3)-2,'Length'] + df3.at[len(df3)-1,'Length']
    #CDS
    CDS = {
        'temp': 'CDS',
        'Exon&Intron': df2.at[1,'Exon&Intron'],
        'Name': 'CDS',
        'Length':len(df2.at[1,'Exon&Intron']),
        'Start':len(df1.at[0,'Exon&Intron'])+1,
        'End':len(df2.at[0,'Exon&Intron'])+len(df2.at[1,'Exon&Intron'])}
    
    CDS = pd.DataFrame([CDS])
    df3 = pd.concat([df3, CDS], ignore_index=True)

    #for answer
    #unspliced
    unspliced =['Name','Start','End','Length']
    unspliced = df1[unspliced]
    #print('unsoliced:\n',unspliced)
    #spliced
    spliced = ['Name','Start','End','Length']
    spliced = df3[spliced]
    #print('spliced:\n',spliced)
    
    #處理Codon
    a=df2.at[len(df2)-2,'Exon&Intron']
    i=0
    codon=''
    for k in range(0,len(a)):
        if a[k].isupper():
            codon += a[k]
            i += 1
            if (i%3) == 0 :
                codon += ','
            else:
                continue    
    #string to list
    codon = codon.split(',')
    del codon[len(codon)-1]
    
    #the dict of codon table1
    dict = {'TTT':'F', 'TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V',
    'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A','TAT':'Y','TAC':'Y','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D',
    'GAC':'D','GAA':'E','GAG':'E','TGT':'C','TGC':'C','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G','TAA':'','TGA':'','TAG':''}

    #output
    Stop = 0
    translation = []
    for values in codon :
        gene = dict.get(values)

        if Stop == 0:
            translation += gene        
        if gene == '' :
            Stop = 1         
        elif Stop == 1:
            print('end')
            Stop = 0
            break
    translation = ''.join(translation)
    #print('translation:',translation)
else:
    #靜態爬
    #check + -
    if strand == "+" :
        transcriptdata1 = data["fields"]['unspliced_sequence_context']['data']['positive_strand']['features']
        transcriptdata2 = data["fields"]['spliced_sequence_context']['data']['positive_strand']['features']
    else:
        transcriptdata1= data["fields"]['unspliced_sequence_context']['data']['negative_strand']['features']
        transcriptdata2= data["fields"]['spliced_sequence_context']['data']['negative_strand']['features']

    def count_len(start: int,end: int):
        return end-start +1

    unspliced = pd.DataFrame(columns = ['type','start','stop'])
    spliced = pd.DataFrame(columns = ['type','start','stop'])

    for i in range(len(transcriptdata1)):
        unspliced.loc[i] = transcriptdata1[i]
    
    for i in range(len(transcriptdata2)):
        spliced.loc[i] = transcriptdata2[i]


    unspliced['length'] = unspliced.apply(lambda x: count_len(x['start'],x['stop']),axis=1)
    spliced['length'] = spliced.apply(lambda x: count_len(x['start'],x['stop']),axis=1)
    
    #重新命名
    #unspliced 
    count_Intron_u= 1
    count_Exon_u = 1
    for k in range(0,len(unspliced)):
        if unspliced.at[k,'type'] == 'intron':
            unspliced.at[k,'type'] = 'Intron' + str(count_Intron_u)
            count_Intron_u+= 1
        elif unspliced.at[k,'type'] == 'exon':
            unspliced.at[k,'type'] = 'Exon' + str(count_Exon_u)
            count_Exon_u += 1
        elif unspliced.at[k,'type'] == 'five_prime_UTR':
            unspliced.at[k,'type'] = '5\'UTR'
        elif unspliced.at[k,'type'] == 'three_prime_UTR':
            unspliced.at[k,'type'] = '3\'UTR'
    #spliced
    count_Exon_s = 1
    for k in range(0,len(spliced)):
        if spliced.at[k,'type'] == 'exon':
            spliced.at[k,'type'] = 'Exon' + str(count_Exon_s)
            count_Exon_s += 1
        elif spliced.at[k,'type'] == 'five_prime_UTR':
            spliced.at[k,'type'] = '5\'UTR'
        elif spliced.at[k,'type'] == 'three_prime_UTR':
            spliced.at[k,'type'] = '3\'UTR'

    #for answer
    #unspliced       
    #print('unspliced:\n',unspliced)
    #spliced
    #print('spliced:\n',spliced)
    

    translation = data['fields']['protein_sequence']['data']['sequence']
    #print('translation:',translation)