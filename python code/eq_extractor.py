#script to extract data from the NSE website for F&O and equity between a start and an end date
#all the data extarcted is saved as .csv files in the downloads folder 
#change the location of downloads folder of ur browser to save the files in a particular directory 
######################################################################################
from time import sleep 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import calendar 

path_of_driver='/usr/local/bin/chromedriver'
driver=webdriver.Chrome(path_of_driver)
path="https://www1.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date="
path1="&section=EQ"#change FO to EQ to get the equity data 


start_date_string = input("enter the start date in the format dd-mm-yyyy")
end_date_string=input("enter the end date in the format of dd-mm-yyyy")
format_string = "%d-%m-%Y"


x=datetime.strptime(start_date_string, format_string)
y=datetime.strptime(end_date_string, format_string)

while (x<=y):
    if (x.weekday()==6 or x.weekday()==5):
        x=x+timedelta(1)
        continue
    date=datetime.strftime(x,format_string)
    final_path=path+date+path1
    print(final_path)
    driver.get(final_path)
    sleep(0.5)
    try:
        result = WebDriverWait(driver,3).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr/td/a"))
        )
        
        
        result.click()
        
    except:
        x=x+timedelta(1)
        continue
   
    sleep(1)
    
    d_s='01-'+str(x.month)+'-'+str(x.year)
    print(d_s)
    x=datetime.strptime(d_s, format_string)
    x=x+relativedelta(months=+1)
    
    
driver.close()

