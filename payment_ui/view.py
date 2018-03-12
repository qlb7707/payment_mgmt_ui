#coding=utf-8
#================================================================
#   Copyright (C) 2018 All rights reserved.
#   
#   filename     :view.py
#   author       :qinlibin
#   create date  :2018/02/02
#   mail         :qin_libin@foxmail.com
#
#================================================================
import time as tm
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import request
import json
from payment_mgmt.models import PriTypeTbl as pri_type_tbl
from payment_mgmt.models import SecTypeTbl as sec_type_tbl
from payment_mgmt.models import PeriodTbl as period_tbl
from payment_mgmt.models import Payment
import MySQLdb as mysql
from utils import *
import pdb

select_field = "year,mon,day,cost,cost_name,seller "
sum_cost = "round(sum(cost),2) total "
item_count = "count(*) number "
concat = " and "
where = " where "
time_filter_b = "time >= %s "
time_filter_t = "time <= %s "
name_filter = "cost_name like '%%%s%%' "
pri_filter = "pri_type_tbl.value = %s "
sec_filter = "sec_type_tbl.value = %s "
period_filter = "period_tbl.value = %s "
seller_filter = "seller like '%%%s%%' "

search_result_format = "共%d条记录，花费%.2f元"

context = {}
lookup_context = {}
def get_ymd(str):
    ta = tm.strptime(str,'%Y-%m-%d')
    return ta.tm_year,ta.tm_mon,ta.tm_mday
def clear_context():
    global context
    context={}

def delete_item(request):
    index = request.GET['id']
    Payment.objects.filter(id=index).delete()
    return HttpResponseRedirect('/')

def retSecData(request):
    pri = request.GET['Pri']
    sec_list = []
    rows = sec_type_tbl.objects.filter(pri_type=pri)
    for row in rows:
        sec_list.append({'value':row.value,'description':row.description})
    sec_list_json = json.dumps(sec_list)
#    print sec_list_json
    return HttpResponse(sec_list_json)


def retDateItems(request):
    item_list = []
    date1 = request.GET['date1']
    y,m,d = get_ymd(date1)
    rows = Payment.objects.filter(year=y,mon=m,day=d)
    for row in rows:
        item_list.append({'id':row.id,'year':row.year,'mon':row.mon,'day':row.day,'cost':row.cost,'cost_name':row.cost_name,\
                'seller':row.seller,'pri_type':row.pri_type,'sec_type':row.sec_type,'period':row.period})
    date_items_json = json.dumps(item_list)
#    print date_items_json
    return HttpResponse(date_items_json)

    
    

    
def recordPayment(request):
    tarray = tm.strptime(request.POST['date'],"%Y-%m-%d")
    Payment.objects.create(cost=request.POST['cost'],
            cost_name=request.POST['name'],
            seller=request.POST['seller'],
            pri_type=request.POST['pri'],
            sec_type=request.POST['sec'],
            period=request.POST['per'],
            user_id=1,
            time = int(tm.mktime(tarray)),
            year=tarray.tm_year,mon=tarray.tm_mon,day=tarray.tm_mday)
    #return HttpResponseRedirect('/')

def lookup(request):
    date_array = tm.localtime()
    records = Payment.objects.filter(year=date_array.tm_year,mon=date_array.tm_mon,day=date_array.tm_mday)
    return records

def hello(request):
    if request.POST != {}:
        recordPayment(request)
    context['records'] = lookup(request)
    context['hello'] = 'Payment record'
    context['pri'] = pri_type_tbl.objects.all()
    context['sec'] = sec_type_tbl.objects.all()
    context['per'] = period_tbl.objects.all()
    return render(request,'hello.html',context)

def get_record_by_filter(filters):
    item_count = 0
    total_cost = 0
    SQL = "select " + select_field + "from payment join pri_type_tbl on pri_type = pri_type_tbl.value join sec_type_tbl on sec_type_tbl.value = sec_type join period_tbl on period_tbl.value=period" + where
    db = mysql.connect('192.168.1.121','root','123456','payment_mgmt')
    cursor = db.cursor()
    is_first = True
    paras = ()
    if filters['date1']:
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + time_filter_b
        paras = paras + (time_str_to_int(filters['date1']),)

    if filters['date2']:
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + time_filter_t
        paras = paras + (time_str_to_int(filters['date2']),)

    if filters['name']:
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + name_filter
        paras = paras + (filters['name'],)

    if filters['seller']:
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + seller_filter
        paras = paras + (filters['seller'],)

    if filters['pri'] != "Not_data1":
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + pri_filter
        paras = paras + (filters['pri'],)

    if filters['sec'] != "Not_data2":
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + sec_filter
        paras = paras + (filters['sec'],)

    if filters['per'] != "Not_data3":
        if not is_first:
            SQL = SQL + concat
        else:
            is_first = False
        SQL = SQL + period_filter
        paras = paras + (filters['per'],)

    if is_first:
        return [],0,0
    #pdb.set_trace()
    SQL_F = SQL%paras + ' order by time'
    #print SQL_F
    cursor.execute(SQL_F)
    rows = cursor.fetchall()
    db.close()
    item_count = len(rows)
    item_list = []
    field_list = select_field.strip(' ').split(',')
    for row in rows:
        record = {}
        for i in range(len(field_list)):
            record[field_list[i]] = row[i]
        item_list.append(record)
        total_cost = total_cost + record['cost']
    return item_list,item_count,total_cost


    


    


        



def lookupitems(request):
    data = {}
    if request.GET != {}:
        records,cnt,cost = get_record_by_filter(request.GET)
        data['search_result'] = search_result_format%(cnt,cost)
        data['records'] = records
    data['pri'] = pri_type_tbl.objects.all()
    data['per'] = period_tbl.objects.all()

    return render(request,'lookup.html',data)
