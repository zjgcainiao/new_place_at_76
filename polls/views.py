from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from .models import Choice, Question, RepairOrderReport
# repairOrder model was added on 11/5/2022

from django.urls import reverse
from django.views import generic

import os
# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
from dotenv import load_dotenv
import pyodbc 
#import pymssql 

class IndexView(generic.ListView):
    
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#  def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list':latest_question_list}
#     return render(request,'polls/index.html',context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
#   template_name = 'polls/slides-deck.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def detail(request, question_id):
    
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request, 'polls/detail.html',{'question':question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# try to list all repair ordes 2022-11-05
# model repairOrder
def all_repair_orders(request):
    # load the environment
    load_dotenv()  # take environment variables from .env.
    server=os.getenv("DB_SERVER")
    user=os.getenv("DB_USER")
    password=os.getenv("DB_PASSWORD")
    databaseName=os.getenv("DB_HOST")
    # how to use pymssql, visit https://pymssql.readthedocs.io/en/stable/ref/pymssql.html#module-level-symbols
    # pymssql.connect(server='.', user=None, password=None, database='', timeout=0, login_timeout=60, charset='UTF-8', as_dict=False, host='', appname=None, port='1433', conn_properties=None, autocommit=False, tds_version=None)
    conn=pyodbc.connect(server, user,password,databaseName)
    c1=conn.cursor()
    c1.execute("""
        SELECT TOP (50) 
       a.[RepairOrderId]
      -- ,a.[RepairOrderPhaseId]
      ,f.[Phase] as ' Repair Order Phase'
      ,concat(b.[FirstName], ' ', b.[LastName]) as 'Customer Name'
      ,b.[LastVisited]
      ,b.[FirstVisited]
      ,b.[NewCustFollowUpDate]
      ,[TimeIn] as 'Repair Order TimeIn'
      ,[TimeOut] as 'Repair Order TimeOut'
      ,[DatePosted] as 'Repair Order Posted Date'
      ,[OdometerIn]
      ,[OdometerOut]
      ,[StatusDescription]
      ,[ScheduleDate]
      ,[ScheduledHours]
      ,[PromiseDate]
      ,[ReasonForVisitId]    
      ,[Location]
      ,a.[CustId]
      ,a.[VehicleId]
      ,c.year 'manuf year'
      ,c.[Vin]
      ,c.[License]
      ,c.[LicenseState]
      ,c.EngineId
      ,d.[NumberOfCylinders]
      ,d.[ValvesPerCylinder]
      ,d.[FuelDeliveryMethodType]
      ,c.[MakeId]
      ,c.[SubModelId]
      ,e.[Name] as 'model Name'
      ,[CategoryId]
      ,[RoPrinted]
      ,[InvoicePrinted]
      ,a.[LastChangeDate]
      ,a.[AppointmentRequestUid]
      ,a.[Notes]
      ,a.[OrderTotal]
      ,a.[ShopSuppliesAmt]
      ,a.[TotalTaxAmt]
      ,a.[LaborSale]
      ,a.[PartsSale]
      ,a.[DiscountAmt]
      ,a.[Observations]
      ,a.[CreatedAsEstimate]
      ,[TaxAmtHazMat]
      ,[TaxAmtShopSupplies]
      ,[PrintedDate]
      ,[PartDiscountDescriptionId]
      ,a.[TaxExempt]
      ,[LaborRateDescriptionId]
      ,[RateVersionDate]
      ,[FromQuickEst]
      ,[HazWasteAmt]
      ,[BalanceDueAdjustment]
      ,a.[timestamp]
      ,[MarginPct]
      ,[TireFeeSale]
      ,a.[EngineHoursIn]
      ,a.[EngineHoursOut]
      ,a.[RecordVersion]
  FROM [ShopMgt].[SM].[RepairOrder] as a
  left join [ShopMgt].[SM].[Customers] as b  on a.[CustId]=b.[custID]
  left join  [ShopMgt].[SM].[Vehicle] as c on c.[VehicleId]=a.[vehicleID]
  left join [ShopMgt].[DMV].[Engine] as d on d.EngineId=c.[engineid]
  left join  [ShopMgt].[SM].[RepairOrderPhase] as f on f.[RepairOrderPhaseId]=a.[RepairOrderPhaseId]
  left join [ShopMgt].[DMV].[Make] as e on e.MakeId=c.MakeId
  where f.[Phase] not in ('DELETED')
  order by [TimeIn] desc
    """)
    all_repair_orders=[]
    data=c1.fetchall()
        
    for row in data:
        repair_id=row[0]    # repair ID
        customer_name=row[2] # getting the customer name. column number may change due to the sql script
        repair_status=row[1]  # get the status of the repair order; EST/RO/INV/DELETED/SCHEDULED
        vin=row[20]         # vin number
        make=row[29]         # make of the vehicle
        time_out=row[7]      # repair_order_time_out 
        last_visit_date=row[2]  # last date visted
        vehicle_year=row[19]    # vehicle year
        repair_total_amount=row[36]  # total repair amount
        RO={'repair_id':repair_id, 'repair_status':repair_status, 'time_out':time_out,'repair_total_amount':repair_total_amount, 'customer_name':customer_name,'make':make,'vehicle_year':vehicle_year,'vin':vin,'last_visit_date':last_visit_date}
        
        all_repair_orders.append(RO)
    return render(request,'polls/repair_order_dashboard.html',{'all_repair_orders':all_repair_orders})

    



