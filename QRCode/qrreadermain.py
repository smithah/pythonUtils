import os
from typing_extensions import Self
from django.db import connection
from pdf2image import convert_from_path
import sys
import os
from cv2 import imread,resize,cvtColor,threshold,dilate,findContours,contourArea,boundingRect
from cv2 import COLOR_BGR2GRAY,THRESH_BINARY_INV,THRESH_OTSU,RETR_LIST,CHAIN_APPROX_SIMPLE
from numpy import ones,pi,uint8
import pyzbar
from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyzbar
import jwt
from blurdectect import blurDetect
from jose import jwt
import pandas as pd
from shutil import move
from re import search
import os
from os import listdir
from multiprocessing import Process
import threading
import traceback
from multiprocessing.pool import ThreadPool, Pool
import multiprocessing
from time import sleep
from datetime import datetime
import functools
from jproperties import Properties
from dbconnection import Database
import dbconnection

files="pdfinvtest"
fileinbox="inboxpdf"



def smap(f, *args):
    return f(*args)

def movefileProcessing(inboxDir):
    for filename in listdir(inboxDir):
        f = os.path.join("inboxpdf", filename)
        move(f,"pdfinvtest/")


def pdfToImage(file):
    successFlag = 1
    #directory = pdfpath
    #pdffile = 0
    try:
        for filename in listdir(file):
            #print("Here")
            f = os.path.join("pdfinvtest", filename)
    # checking if it is a file
            if os.path.isfile(f):
                print(f)
                print(filename)
        
                #f = os.path.join("pdfinvtest", filename)
                filen = filename.rsplit('.', 1)[0]
                print(filename)
                images = convert_from_path(f)
        #pdffile = pdffile + 1
                for i in range(len(images)):
   
                # Save pages as images in the pdf
                    #print("Here1")
                    stringList = ['invoiceimages\\page',str(i),'_',str(filen),'.jpg']                    
                    images[i].save(''.join(stringList), 'JPEG')   
                move(f,"pdfimagesgenerated/")             
    except Exception as e:
            print(e)
            traceback.print_exception(*sys.exc_info())
            successFlag = 0
    finally:
           return successFlag

def qrReader():
    successFlag = 1
    directory = 'invoiceimages'
    filetimestamp = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
    filestampstampstr = str(filetimestamp)
 
    found = 0
    scalelist = [0.3,1,2,3,4,5,6,7,8,9,10]
    i = 0
    j = -1
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df = pd.DataFrame(columns=['FileName', 'Blurry','Scale','Contrast','QRCode','QRCodeString','QRDecode','Remarks','DecodeError'])
# iterate over files in
# that directory
    break_out_flag = False
    try:
        for filename in listdir(directory):
            break_out_flag = False
            f = os.path.join(directory, filename)
            m = search('(?<=_)[0-9]+', filename)
            resultfilename = m.group(0)
            df1 = df1.append(df)
            df2 = df2.append(df)
            if not df.empty:
                #dfc = df
                df = df[df.QRCode.eq(1) & ~(df.duplicated(['FileName'])) & df.DecodeError.eq(0) ]
                #res = df.isin([resultfilename]).any
                #res = df2.isin([resultfilename, df.QRCode.eq(1)]).any().any()               
                #res = dfc["FileName"].isin([resultfilename])
                #res = dfc.isin([resultfilename]).any()
                found1 = df[df['FileName'].str.contains(resultfilename)]
                #print(found1)
                #print(found1.size)
                #print(found1.count())
                #print(res)
                #df1 = df.loc[(df['FileName'].str.contains(resultfilename)) & (df.QRCode.eq(1)) &  (df.DecodeError.eq(0))]
                #df1 = df2.isin([resultfilename]).any().any()
                #print(df1)
                #found1 = df[df['FileName'].str.contains(resultfilename) & df.QRCode.eq(1)]
                #print(found1.count())
            #print(found1.count())
                if(found1.size > 0):
                    #print("Here1")
                    #print(df1)
                    #print(filename)
                    move(f,"detectedQR/")
                    continue
                
            
        #resultfilename = re.sub('(?<=_)[0-9]+', '', filename)
            #print(resultfilename)
            found = 0
            i = 0
            j = j + 1
            df.loc[j, 'FileName'] = resultfilename
            blur = blurDetect(f)
            df.loc[j,'Blurry'] = blur
            df.loc[j, 'DecodeError']  = 0
            df.loc[j, 'QRCode']  = 0
    
    # checking if it is a file
            if os.path.isfile(f):
              
                #print(f)
        
        #image = cv2.imread(f)
              for k in range(0,len(scalelist)):
                if(found == 0 and i < len(scalelist) and break_out_flag == False):
                    scale =scalelist[i]
                    i = i + 1
                    image = imread(f)
                    width = int(image.shape[1] * scale)
                    height = int(image.shape[0] * scale)
                    image = resize(image, (width, height))
                #key3
                    public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwc00aZOc3Uqf4Wwy+OeF7QOduNtFqZzeo8VNcvH5Mo0Gs9kyoSwA+21MVLB3j34ioekU29USSkHcpdiNss00YcDzjrSGRld9IIF2MKowmV+Q/lZvcm9I1/P0OyBM7gSdZt7bDNfAF2+BSrgubHjwv5OVkYrwN8TexuqhoJAu3mSRev0yjgCS8ytldvG1LbftviEiC1h4CU1YpMwuZSja4c2V3nZEux+uTeQAd/vEQ+66b5ohMEwUqeb2h/M+Ztyn/Wlrb6Uf8ag7lZNo9k8WyWa97p0Ay/yP3Fvg4Om308gHdsCwBIUzQZI1wYhZYypY9LeGRMFYVGq3EIb+gOCR5QIDAQAB"
                #key1
                #public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7lJd64G3zd4WgfbiL26KTLjY5MuXjPsGSsfONmwX9Z1HbITKeFEaXKJYCe/2WLNvrcWefyk2sP3TitWmXFTRJrAvzlm/F9tKfGlHiEFzh65osolGE/KdOIvBvLXFwJ29ul3zSm17X1/clqxa6Moviys73hDxHbZZ/mpYLDatb66zzge/IzsOjfz4zyUE2Vus6sihUJZw2a7BpIPWOPoM0TGSkf9/dq9OPzKBakYfXZvL/hU8WYY9wOIS79GOqyTcMo7cAbstTp/dRZlsetmEP+f1Pyi8Cmm6ReKU0G3muTTPgWtM5r9Sz/tKf47xsFLAe69Q2WOmblFRYMi3tGIQHQIDAQAB"
                #key2
                #public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArxd93uLDs8HTPqcSPpxZrf0Dc29r3iPp0a8filjAyeX4RAH6lWm9qFt26CcE8ESYtmo1sVtswvs7VH4Bjg/FDlRpd+MnAlXuxChij8/vjyAwE71ucMrmZhxM8rOSfPML8fniZ8trr3I4R2o4xWh6no/xTUtZ02/yUEXbphw3DEuefzHEQnEF+quGji9pvGnPO6Krmnri9H4WPY0ysPQQQd82bUZCk9XdhSZcW/am8wBulYokITRMVHlbRXqu1pOFmQMO5oSpyZU3pXbsx+OxIOc4EDX0WMa9aH4+snt18WAXVGwF2B4fmBk7AtmkFzrTmbpmyVqA3KO2IjzMZPw0hQIDAQAB"
                    keyList = ['-----BEGIN PUBLIC KEY-----\n', public_key , '\n-----END PUBLIC KEY-----']
                    #key1 = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
                    key1 = ''.join(keyList)



                    gray = cvtColor(image, COLOR_BGR2GRAY)
                    _, thresh = threshold(gray, 120, 255, THRESH_BINARY_INV + THRESH_OTSU)

# The bigger the kernel, the more the white region increases.
# If the resizing step was ignored, then the kernel will have to be bigger
# than the one given here.
                    kernel = ones((3, 3), uint8)
                    thresh = dilate(thresh, kernel, iterations=1)
                    contours, _ = findContours(thresh, RETR_LIST, CHAIN_APPROX_SIMPLE)

                    bboxes = []
                    append = bboxes.append
                    for cnt in contours:
                        if break_out_flag:
                            break
                        area = contourArea(cnt)
                        xmin, ymin, width, height = boundingRect(cnt)
                        extent = area / (width * height)
  
  # filter non-rectangular objects and small objects
                        if (extent > (pi / 4)) and (area > 100):
                            append((xmin, ymin, xmin + width, ymin + height))

                    #qrs = []
                    info = set()
                    add = info.add
                    for xmin, ymin, xmax, ymax in bboxes:
                        if break_out_flag:
                            break
                        roi = image[ymin:ymax, xmin:xmax]
                        detections = decode(roi, symbols=[pyzbar.ZBarSymbol.QRCODE])
                    #print(detections)
                    
                        for barcode in detections:
                            if break_out_flag:
                                break
    
                            add(barcode.data)
                            if(len(info) == 0):
                                found = 0                        
                            else:
                                found = 1
                                df.loc[j, 'QRCode'] = 1
                                df.loc[j, 'Scale'] = scale
                                str1 = barcode.data.decode('UTF-8')
                                df.loc[j, 'QRCodeString'] = str1      
                               
                            try:
                                decoded = jwt.decode(str1,key=key1)
                                #print(decoded)
                            except Exception:
                                msg = 'Decode Error.' 
                                df.loc[j, 'Remarks']  = "Decode Error" 
                                df.loc[j, 'DecodeError']  = 1 
                                move(f,"decodeError/")
                                #print(msg)
                                break_out_flag = True 
                                break                                             
                           
                                 
                            data_items = decoded.items()                                                                          
                            df.loc[j, 'QRDecode'] = data_items
                            #print(data_items)
                            
                            n = 0
                            for i in list(data_items)[0]:
                               
                                n = n + 1
                                if(n == 2):
                                  res = i.split(',') 
                                  for i in res:                                    
                                    str1 = i.split(":")                                    
                                    df.loc[j, str1[0]] = str1[1] 
                            remarkList = [ "QR Code detected at ", str(ymin),str(ymax),str(xmin),str(xmax)," Co-ordinates."]                       
                            df.loc[j, 'Remarks'] = ''.join(remarkList)
                            move(f,"detectedQR/")
                            break_out_flag = True
                            break
              if(found == 0):   
                    df.loc[j, 'Remarks'] = "QR Code undected in image."                     
                    move(f,"undetectedQR/")
            
        #df.drop_duplicates(subset=['FileName', 'QRCode'], keep='first')
        
        df = df[df.QRCode.eq(1) & ~(df.duplicated(['FileName'])) & df.DecodeError.eq(0) ]
        #df = df[df.QRCode.eq(1)  & df.DecodeError.eq(0) ]
        df.to_excel('QRCode_'+filestampstampstr+'.xlsx', sheet_name='QRCodeData')
        db = Database()
        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = ("Steve", "Highway 21")
        db.execute(sql,val) 
        db.commit()
        df1 = df1[df1.QRCode.eq(1) & ~(df1.duplicated(['FileName'])) & df1.DecodeError.eq(1) ]
        df1.to_excel('QRCodeDecodeError_'+filestampstampstr+'.xlsx', sheet_name='QRCodeDecodeError')       
        df2 = df2[df2.QRCode.eq(0) & ~(df2.duplicated(['FileName'])) & df2.DecodeError.eq(0) ]
        common = df2.merge(df, on=["FileName"])
        result = df2[~df2.FileName.isin(common.FileName)]
        result.to_excel('QRCodeException_'+filestampstampstr+'.xlsx', sheet_name='QRCodeException')
        
    except Exception as e:
        print(e)
        traceback.print_exception(*sys.exc_info())
        successFlag = 0
    finally:
        return successFlag
    
 

if __name__ == "__main__":
    try:
      while True:  
        listdirect = ["decodeError", "detectedQR", "undetectedQR","pdfimagesgenerated","invoiceimages","pdfinvtest"]
        for dir in listdirect:
          for f in listdir(dir):
                os.remove(os.path.join(dir, f))
        configs = Properties()
  
        with open('qrutil.properties', 'rb') as read_prop:
                configs.load(read_prop)
        sleeptime = float(configs.get("SCRIPT_SLEEPSEC").data)
        #pdfDirectory = sys.argv[1]
        #get all the files of a directory
        #files=listdir(pdfDirectory)
        #conn = Database.connection
        #cursor = Database.cursor        
        
        if(len(listdir(fileinbox) ) != 0):
            func1 = functools.partial(movefileProcessing,fileinbox)
            func2 = functools.partial(pdfToImage, files)

            pool = Pool(processes=2)
            res = pool.map(smap, [func1, func2])
            pool.close()
            pool.join()
            print(res)
        
        #movefileProcessing(fileinbox)    
        #sucess = pdfToImage(files)    
        #pool=Pool(6)
            print("HEre")
        #pool=Pool(6)
        #pool.map(pdfToImage,files)        
        #pool.join()
            print("H")
        #sucess = pdfToImage(pdfDirectory)
        #print(sucess)
        
       
            sucess = qrReader() 
        #print(sucess)
            
            if(sucess == 1): 
                print("Process Completed successfully")    
            else:
                print("Error in Process")
        sleep(sleeptime)
                
    except Exception as e:
        print("Exception in the process") 
        print(e)
        traceback.print_exception(*sys.exc_info())
        sys.exit()

