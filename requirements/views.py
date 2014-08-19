from django.shortcuts import render
from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.db import transaction, connection
from django.db.models import Sum, Avg
from django.http import  HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rbmo.models import (Agency,
                         MonthlyReqSubmitted,
                         QuarterlyReq,
                         QuarterReqSubmission,
                         COSSubmission,
)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from helpers.helpers import (getMonthLookup, 
                             quarterofMonth,
                             dictfetchall)
from datetime import datetime, date
from decimal import *
import time
import sys

month_lookup = getMonthLookup()

def getSubmittedReqs(agency, year, month):
    #monthly requirements
    submitted_reqs = []
    if isMonthlyRepSubmitted(agency, year, month-1):
        submitted_reqs.append('Monthly Performance Report of Operation')
    #quarterly requirements
    quarter = quarterofMonth(month)
    if quarter==4:
        year-=1
    qrs = getQuarterReqSubmitted(agency, year, quarter)
    for qr in qrs:
        submitted_reqs.append(qr.requirement.name)
    
    return submitted_reqs

def getLackingReqs(agency, year, month):
    lacking_reqs = []
    if not isMonthlyRepSubmitted(agency, year, month-1):
        lacking_reqs.append('Monthly Performance Report of Operation')
    #quarter requirements
    quarter = quarterofMonth(month)
    if quarter==4:
        year-=1
    quarter_reqs = getLackingQuarterReqs(agency, year, quarter)
    for req in quarter_reqs:
        lacking_reqs.append(req['name'])
    return lacking_reqs
    

def isMonthlyRepSubmitted(agency, year, month):
    try:
        mrs = MonthlyReqSubmitted.objects.get(agency=agency, year=year, month=month)
        return True
    except MonthlyReqSubmitted.DoesNotExist:
        return False


def getQuarterReqSubmitted(agency, year, quarter):
    try:
        qrs = QuarterReqSubmission.objects.filter(agency=agency, year=year, quarter=quarter) 
        return qrs
    except QuarterReqSubmission.DoesNotExist:
        return None

def getLackingQuarterReqs(agency, year, quarter):
    cursor = connection.cursor()
    query = '''
            select * from quarterly_req 
              where id not in (select requirement_id from 
                               quarter_req_submitted 
                                 where agency_id=%s 
                                       and year=%s
                                       and quarter=%s)
            '''
    cursor.execute(query,[agency.id, year, quarter])
    return dictfetchall(cursor)
