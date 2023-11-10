#用python3 manage.py inspectdb > web_tool/models.py 產生model.py 記得先把 view.py admin.py 註解起來
from django.contrib import admin
from web_tool.models import Gene
from web_tool.models import CElegans
# class GeneAdmin(admin.ModelAdmin): #設定Gene介面的外觀 客製化
#     list_display = ('gene_id','transcript_id','numbers')  #對應modles.py的gene
#     search_fields = ('gene_id',) #能夠被搜尋的欄位

# admin.site.register(Gene, GeneAdmin) #註冊Gene model

# class CElegansAdmin(admin.ModelAdmin): #設定Gene介面的外觀 客製化
#     list_display = ('wormbase_id','live','gene_sequence','gene_name','other_name')  #對應modles.py的gene
#     search_fields = ('wormbase_id',) #能夠被搜尋的欄位

# admin.site.register(CElegans, CElegansAdmin) #註冊Gene model