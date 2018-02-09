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
    global context
    tarray = tm.strptime(request.POST['date'],"%Y-%m-%d")
#    print request.POST['date']
#    print tm.mktime(tarray)

#    context['error_msg']='Last record insert Error: data = {cost:%s,name:%s,seller:%s,pri:%s,sec:%s,per:%s,date:%s}'%(request.POST['cost'],request.POST['name'],request.POST['seller'],request.POST['pri'],request.POST['sec'],request.POST['per'],request.POST['date'])
   # context['error_msg'] = json.dumps(request.POST)
    Payment.objects.create(cost=request.POST['cost'],
            cost_name=request.POST['name'],
            seller=request.POST['seller'],
            pri_type=request.POST['pri'],
            sec_type=request.POST['sec'],
            period=request.POST['per'],
            user_id=1,
            time = int(tm.mktime(tarray)),
            year=tarray.tm_year,mon=tarray.tm_mon,day=tarray.tm_mday)
#    context['error_msg'] = context['error_msg'].replace("Error","Success")
    return HttpResponseRedirect('/')

def lookup(request):
    date_array = tm.localtime()
    records = Payment.objects.filter(year=date_array.tm_year,mon=date_array.tm_mon,day=date_array.tm_mday)
    return records

def hello(request):
    context['records'] = lookup(request)
    context['hello'] = 'Payment record'
    context['pri'] = pri_type_tbl.objects.all()
    context['sec'] = sec_type_tbl.objects.all()
    context['per'] = period_tbl.objects.all()
    return render(request,'hello.html',context)
