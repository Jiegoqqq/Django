
import pandas as pd
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

#json 靜態爬
    #transcript_name =request.POST['transcript_id'] #由transcript.js回傳
#B0001.4c.1  B0001.4a.1

#Y40B10A.2a.1
#F54H12.1c.3
transcript_name='Y40B10A.2a.1'
response = requests.get(
        "https://wormbase.org/rest/widget/transcript/" + transcript_name + "/sequences",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })

soup = BeautifulSoup(response.text, "html.parser")
data= json.loads(str(soup))

start = []
stop = []
#處理變成dict
strand = data["fields"]['unspliced_sequence_context']['data']['strand']
#check + -
if strand == "+" :
    data1 = data["fields"]['unspliced_sequence_context']['data']['positive_strand']['sequence']
    data2 = data["fields"]['spliced_sequence_context']['data']['positive_strand']['sequence']
    for i in range(0,len(data2)-1):
        if (data2[i].islower() & data2[i+1].isupper()):
            start.append(i+2)
        elif (data2[i].isupper() & data2[i+1].islower()):
            stop.append(i+1)
    if (stop == []):
        stop.append(len(data2))
    elif (start == []):
        start.append(1)
else:
    data1 = data["fields"]['unspliced_sequence_context']['data']['negative_strand']['sequence']
    data2 = data["fields"]['spliced_sequence_context']['data']['negative_strand']['sequence']
    for i in range(0,len(data2)-1):
        if (data2[i].islower() & data2[i+1].isupper()):
            start.append(i+2)
        elif (data2[i].isupper() & data2[i+1].islower()):
            stop.append(i+1)
    if (stop == []):
        stop.append(len(data2))
    elif (start == []):
        start.append(1)

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


CDS = {
'type': 'CDS',
'start':start[len(start)-1],
'stop':stop[len(stop)-1]}

CDS = pd.DataFrame([CDS])
spliced = pd.concat([spliced, CDS], ignore_index=True)

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

translation = data['fields']['protein_sequence']['data']['sequence']
#用return 才能使用function內的變數
#return unspliced,spliced,translation,data1,data2
print(data2)


