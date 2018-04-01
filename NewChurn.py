import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sbn
import numpy as np
import dateutil
from dateutil import parser

ChurnData=pd.read_csv("latest.csv")

#coverting string to datetime
ChurnData["InvoiceDate"]=pd.to_datetime(ChurnData["InvoiceDate"])

#checking null values
#ChurnData.dropna(how="any",inplace=True)

#initializing new features

#ChurnData["Days bw Events"]=1000 #default value of last unique date
#ChurnData["No of Diff Dates"]=0
#ChurnData["Monthly Regular"]=1
#ChurnData["DiffMonths"]=0

#remove time and making index to Invoice Data
ChurnData["InvoiceDate"]=ChurnData["InvoiceDate"].apply(lambda ChurnData : datetime.datetime(day=ChurnData.day,month=ChurnData.month,year=ChurnData.year))

#making a new feature
ChurnData["quan*price"]=ChurnData["Quantity"]*ChurnData["UnitPrice"]

#using grouper and analyse total amount spent in a month for each customer ID
ChurnData['MonthlyAmt']=ChurnData.groupby(['CustomerID',pd.Grouper(key="InvoiceDate",freq="M")])["quan*price"].transform('sum')

#analyse average value of a feature in a month for each customer
AvgFeatCust=ChurnData.groupby(['CustomerID','Description',pd.Grouper(key="InvoiceDate",freq="M")])["Quantity"].mean()

#geting avg value of feature in each month
AvgFeatTot=ChurnData.groupby(['Description',pd.Grouper(key="InvoiceDate",freq="M")])["Quantity"].mean()

#calculating no of events of a customer id per month
ChurnData['MonthlyEvents']=ChurnData.groupby(['CustomerID',pd.Grouper(key="InvoiceDate",freq="M")])["CustomerID"].transform('count')

#getting unique Customer IDs
uCustomerID=ChurnData["CustomerID"].unique()

#after creating new csv analyzation

#FUNCTIONS

#fuction to increment month
def MoYr(d):
    d= d + datetime.timedelta(days=31)
    return d


#calculating difference between dates

def DateDifference(uCustomerID):

    for i in range(len(uCustomerID)-1):
        uDates = ChurnData.groupby('CustomerID')
        ugrp=uDates["InvoiceDate"].get_group(uCustomerID[i]).unique()
        print("Count: "+str(i) +" ID: "+str(uCustomerID[i]))
        print(ugrp)
        j=uCustomerID[i]
        while j == uCustomerID[i]:
            Date=ChurnData.loc[ChurnData["CustomerID"]==uCustomerID[i],"InvoiceDate"]
            print(uCustomerID[i])
            for key,values in Date.iteritems(): #loop for iterating through all dates of particular id
                for dates in range(len(ugrp)-1):     #loop for iterating through unique dates of particular id
                    pDate=pd.to_datetime(ugrp[dates])
                    fDate=pd.to_datetime(ugrp[dates+1])
                    if values == pDate:
                        delta=fDate-pDate
                        ChurnData.at[key,'Days bw Events']=delta.days
                        print("present Date: "+str(pDate))
                        print("future Date: "+ str(fDate))
                        print("Date diff: "+str(delta.days))
            i+=1

# different no of dates customer came overall
def allComingDates(uCustomerID):
    for i in range(len(uCustomerID)-1):
        uDates=ChurnData.groupby('CustomerID')
        ugrp=uDates["InvoiceDate"].get_group(uCustomerID[i]).unique()
        j=uCustomerID[i]
        print("---------------- "+str(uCustomerID[i])+" -----------------")
        while j == uCustomerID[i]:
            index = ChurnData.loc[ChurnData["CustomerID"] == uCustomerID[i],"InvoiceDate"]
            for key,value in index.iteritems():
                ChurnData.at[key,"No of Diff Dates"]= len(ugrp)
            i+=1

#different months per id
def DiffMonths(uCustomerID):
    for i in range(len(uCustomerID) - 1):
        uDates = ChurnData.groupby('CustomerID')
        tMonths=[]
        uMonths=[]
        ugrp = uDates["InvoiceDate"].get_group(uCustomerID[i]).unique()
        print(ugrp)
        for x in ugrp:
            x=pd.to_datetime(x)
            moYr=str(x.month)+","+str(x.year)
            tMonths.append(moYr)
        for y in tMonths:
            if y not in uMonths:
                uMonths.append(y)
        j = uCustomerID[i]
        print("---------------- " + str(uCustomerID[i]) + " -----------------")
        while j == uCustomerID[i]:
            index = ChurnData.loc[ChurnData["CustomerID"] == uCustomerID[i], "InvoiceDate"]
            for key, value in index.iteritems():
                ChurnData.at[key, "DiffMonths"] = len(uMonths)
                print("Diff Dates: "+str(len(ugrp))+"Diff Month length is: "+str(len(uMonths)))
            i += 1
