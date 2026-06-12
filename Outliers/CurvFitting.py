import types
from numpy.core.arrayprint import printoptions
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import sys
# define the true objective function
def model_5_degree(x, a, b, c, d, e, f):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

# define the true objective function
def model_3_degree(x, a, b, c,d):
	return (a * x) + (b * x**2) + (c * x**3) + d


#define the linear regression model
def linear_model1(x, a, b):
	return a * x + b

def data_preprocessing(df):
   for col in df.columns:
      df[col] = pd.to_numeric(df[col], errors='coerce')
      df[col] = df[col].replace(np.nan, 99999999)

   df.insert(0, 'SN', range(1, 1 + len(df)))

def remove_outliers(df):
      
   # Find Quantile
   Q1 = df.quantile(0.25)
   Q3 = df.quantile(0.75)
   IQR = Q3 - Q1

   # building ture - false table
   df_bol_map = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))

   # detecting outlier and removing outliers
   good_data = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]

   return (df_bol_map,good_data)

def curvefit(inputfile,outputfile):
   
   # Read Input Excel File
   df = pd.read_excel(inputfile)

   #df pre-processing
   for col in df.columns:
      df[col] = pd.to_numeric(df[col], errors='coerce')
      df[col] = df[col].replace(np.nan, 99999999)

   df.insert(0, 'SN', range(1, 1 + len(df)))

   result = remove_outliers(df)
   df_bol_map = result[0]
   good_data  = result[1]

   df_out =  pd.DataFrame()


   #Iterating through all columns 
   colFlag = False
   x_col = ""
   i =  1

   #####################################
   #### Predicting Linear curve ########
   #####################################

   
   # Create linear regression object
   regr = linear_model.LinearRegression()
   array = good_data.to_numpy()
   sample_x = array[:,np.newaxis,0]
   sample_y = array[:,np.newaxis,1]


   x_train  = sample_x[:-5]
   x_test   = sample_x[:5]

   y_train  = sample_y[:-5]
   y_test   = sample_y[:5]


   # Train the model using the training sets
   regr.fit(x_train, y_train)

   # Make predictions using the testing set
   y_pred = regr.predict(x_test)

   
   for col in df.columns:
      #skiping independent variable i.e x variable
   
      if colFlag == False:
         x_col = col# Independent column
         colFlag = True
         df_out[col] = df[col]
         
         x_line = good_data[x_col].values
         i = i+1
         continue

      y_col = col
      x_line = good_data[x_col].values

      y_line = good_data[y_col].values
     
      df[x_col] = df[x_col].fillna(0)
      x_ori  = df[x_col].values   
         
      
      if i == 2:
           
         temp_array = df.to_numpy()
         sample_x_1 = temp_array[:,np.newaxis,0]   
         y_pred = regr.predict(sample_x_1)

         # df_out.insert(1, 'Predict_344', y_pred)
         i = i+1
         df_out[col] = y_pred

         continue




      # finding coefficient and covarience
      popt, pcov = curve_fit(model_5_degree, x_line, y_line)

      #3rd degree model
      popt_3, pcov_3 = curve_fit(model_3_degree, x_line, y_line)

      lpopt,lpov = curve_fit(linear_model1, x_line, y_line)


      predict_3degree = model_3_degree(x_ori, *popt_3)
      r2_pre_3 = model_3_degree(x_line, *popt_3)

      l_predict = linear_model1(x_ori, *lpopt)

      r2_pre_5 = model_5_degree(x_line,*popt)

      r2_score_5th_degree =  r2_score(r2_pre_5,y_line)
      r2_score_3rd_degree = r2_score(r2_pre_3,y_line)
      if r2_score_5th_degree < r2_score_3rd_degree:
         predict = model_3_degree(x_ori, *popt_3)
      else:
         predict = model_5_degree(x_ori, *popt)

      df[f"{col}_predict"] = predict
      #NaN array
      nafil = [np.NAN]

      #replacing outlier with NaN
      new_col = df[col].where(~(df_bol_map[col]), nafil, axis=0) 
      df[col] = new_col

      #Filling NaN with predicted values
      df[col].fillna(df[f"{col}_predict"], inplace=True)
      df_out[col] = df[col]
      i = i + 1

   del df_out['SN']   
   df_out.to_excel(outputfile,index=False)     

   types_a = df_out.dtypes

   print(types_a) 

   df_out.round(2)
   pd.options.display.float_format = '{:.2f}'.format
  
   df_out.to_excel(outputfile,index=False)


if __name__ == "__main__":
   #84_original.xlsx 
   curvefit(sys.argv[1],sys.argv[2])
   #curvefit("E:\ProofOfConcepts\Softomotive\SM\InputFiles\Hydrostatic\Process1\\NEW1PAD.xlsx" , "E:\ProofOfConcepts\Softomotive\SM\OutputFiles\\new1pad_3.xlsx")
