from django.template import context
#from django.template import content
from django.shortcuts import render
import pandas as pd
import json
#movies/management/commands/import_movies_from_xls.py
# -*- coding: UTF-8 -*-
#import xlrd
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils.encoding import smart_str


#class Command(BaseCommand):
    #args = "<file_path...C:\Users\imman\Desktop\Project_Covid\International_vaccine>"

# Create your views here.
df_json=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
def index(request):
    df_vaccine_data = pd.read_csv('https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/vaccine_data_global.csv', sep=',', error_bad_lines = False, encoding='latin-1')
#usecols= ['Country_Region','Date', 'Doses_admin','People_partially_vaccinated','People_fully_vaccinated','Report_Date_String','UID'])
    totalCount = df_vaccine_data[df_vaccine_data.columns[-3]].sum()
    djangoData=df_vaccine_data[['Country_Region',df_vaccine_data.columns[-3]]].groupby('Country_Region').sum()
    djangoData=djangoData.reset_index()
    djangoData.columns=['Country_Region','values']
    djangoData=djangoData.sort_values(by='values',ascending=False)
    djangoDataVals=djangoData['values'].values.tolist()
    country_name=djangoData['Country_Region'].values.tolist()
    data_to_load_map=data_to_load_calc(djangoData, country_name)
    context ={'totalCount':totalCount,'country_name': country_name,'djangoDataVals':djangoDataVals,'data_to_load_map':data_to_load_map}
    return render(request,'index.html',context)


def data_to_load_calc(djangoData,country_name):
    data_to_load_map = []
    for i in country_name:
        try:
           tempdf=df_json[df_json['name']==i]
           temp={}
           temp["code3"]=list(tempdf['code3'].values)[0]
           temp["name"]=i
           temp["value"]=djangoData[djangoData['Country_Region']==i]['values'].sum()
           temp["code3"]=list(tempdf['code'].values)[0]
           data_to_load_map.append(temp)
        except:
           pass
    return data_to_load_map