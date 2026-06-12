import pandas as pd
import numpy as np
import sys, getopt


def interpolation(inputfile,outputfile,interpolate):
        data = pd.read_excel(inputfile)
        for col in data:
            #Check for Spikes in the column and convert data to numeric to prevent interpolation breaking
            count=data[col].astype(str).str.contains('^Y$|^\d+\,\d+$|^\d+\.\d+\/$|^\d+\_\d+$|^\d+\-\d+$|^\d+\$\d+$|^\d+\/\d+$|^\d+\(\d+$|^\d+\.\d+[a-zA-Z]$|^\d+[a-zA-Z0-9]+\d+$',regex=True).sum()
            if count>0:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        cdata = data.replace('Y', np.nan)
        #print(cdata)
        cdata = cdata.interpolate(method='+interpolate+')
        #print("Interpolated Data: \n",cdata)
        cdata.to_excel(outputfile,index=False) 

if __name__ == "__main__":
   interpolation(sys.argv[1],sys.argv[2],sys.argv[3])
