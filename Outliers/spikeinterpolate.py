# import load_workbook
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np
from openpyxl.utils.dataframe import dataframe_to_rows
import sys, getopt
import os
import win32com.client as com
import pywintypes
from win32com.client import Dispatch
import win32com.client as win32

numtimes = 4

def spikeinterpolate(inputfile,interpolate,cyclenumm):
# set file path
     filepath=inputfile
     interpolateType=interpolate
     spikePresent=0
     global numtimes
     global cyclenum
     #interpolateCount=0
     # load demo.xlsx 
     wb=load_workbook(filepath,data_only=True)
     wb1=load_workbook(filepath,data_only=False)
     # select demo.xlsx
     wb.active=1
     sheet=wb.active

     # get max row count
     max_row=sheet.max_row
     #print(max_row)
     # get max column count
     max_column=sheet.max_column
     #print(max_column)
     # iterate over all cells 
     # iterate over all rows
     for i in range(1,max_row+1):
     
          # iterate over all columns
          for j in range(1,max_column+1):
               wb.active=1
               sheet=wb.active
               # get particular cell value    
               cell_obj=sheet.cell(row=i,column=j)
               #print(cell_obj.internal_value)
               if cell_obj.internal_value=="Y":
                    spikePresent = spikePresent + 1
                    cyclenum = 1
                    #print(cell_obj.internal_value)
                    wb1.active=0
                    sheet=wb1.active
                    #print(i)
                    #print(j)
                    s=get_column_letter(j)
                    sheet.cell(row=i, column=j).value = ''
                    #print('\n')
     wb1.save(filepath)
     wb1.close()
     wb.close()
     #data = pd.read_excel(filepath)
     xls = pd.ExcelFile(filepath)
     data = pd.read_excel(xls, 0)
     df2 = pd.read_excel(xls, 1)
     cdata = data.replace('', np.nan)
        #print(cdata)
     cdata = cdata.interpolate(mehtod='+interpolate+')
        #print("Interpolated Data: \n",cdata)

     wb1=load_workbook(filepath,data_only=False)
     wb1.active = 0

     ws= wb1.active
     max_row=sheet.max_row
     ws.delete_rows(1,max_row+1)

     for r in dataframe_to_rows(cdata, index=False, header=True):
         ws.append(r)
    

     wb1.save(filepath)
     wb1.close()
     excel = win32.gencache.EnsureDispatch('Excel.Application')
     wb = excel.Workbooks.Open(filepath)
     wb.Save()
     wb.Close()
     excel.Quit()

               
     if spikePresent > 0 and numtimes > 0:
          numtimes = numtimes -1
          spikeinterpolate(filepath,interpolateType,numtimes)
     
     if spikePresent == 0:
          cyclenum = 0
     #print(cyclenum)
     

if __name__ == "__main__":
   spikeinterpolate(sys.argv[1],sys.argv[2],sys.argv[3])
   global cyclenum
   print(cyclenum)
      
