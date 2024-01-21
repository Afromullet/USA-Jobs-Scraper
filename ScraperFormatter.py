# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:33:43 2024

@author: Afromullet
"""
import requests
import pandas as pd



api_key = None
email_address= None

def read_config_file():
    

    global api_key,email_address
    '''
    A simple reader to read the email and api key from the config.txt
    '''
    with open("config.txt") as config:
        
        email_address = next(config).split(":")[1].strip()
        api_key = next(config).split(":")[1].strip()

def write_occupational_series_to_file():
    
    '''
    Gets all occupational series and writes them to a file.
    
    '''

    url = 'https://data.usajobs.gov/api/codelist/occupationalseries'

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        data = data["CodeList"][0]["ValidValue"] #Index 1 is "DateGenerated", which doesn't seem useful at the moment
        
        keys_to_remove = ["IsDisabled","JobFamily","LastModified"] #These keys don't add anything useful 
        [ser.pop(k) for ser in data for k in keys_to_remove]
        pd.DataFrame.from_dict(data).to_csv("Occupational_Series.csv")
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    return data


def write_pay_plans_to_file():
    
    '''
    Gets all occupational series and writes them to a file.
    
    '''

    url = 'https://data.usajobs.gov/api/codelist/payplans'

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        data = data["CodeList"][0]["ValidValue"] #Index 1 is "DateGenerated", which doesn't seem useful at the moment
        
        #keys_to_remove = ["IsDisabled","JobFamily","LastModified"] #These keys don't add anything useful 
        #[ser.pop(k) for ser in data for k in keys_to_remove]
        pd.DataFrame.from_dict(data).to_csv("Pay_plans.csv")
        
    else:
        print(f"Request failed with status code {response.status_code}")
    
    return data  
    
    
def targetted_search(positionTitle="",jobCategoryCode="",keyword="",location=""):
    
    
    global email_address, api_key
    

    url = 'https://data.usajobs.gov/api/search'
      
    host = 'data.usajobs.gov'

    
    headers = {
        'Host': host,
        'User-Agent': email_address,
        'Authorization-Key': api_key
    }
    
    params = {
        'ResultsPerPage': 5,
        "PositionTitle" : positionTitle,
        'Keyword': keyword,
        'JobCategoryCode': jobCategoryCode,
        'LocationName' : location
    }
    

    df = pd.DataFrame() #Concatenating the results of each page to this dataframe
    number_of_pages = get_number_of_pages(url,headers,params)
    if number_of_pages > 0:
        
        for page in range(number_of_pages):
            
            params['Page'] = page
       
            response = requests.get(url, headers=headers,params=params)
            
            if response.status_code == 200:
                
                data = response.json()
                
                search_result_items = data['SearchResult']['SearchResultItems']
                if len(search_result_items) > 0:
                    search_results = search_result_items[0]['MatchedObjectDescriptor']
                    search_results = [item['MatchedObjectDescriptor'] for item in search_result_items]        
                    search_results = pd.DataFrame(search_results)
                    df = pd.concat([df, search_results], ignore_index=True)
                    
                else:
                    search_results = None   #todo handle errors differently
        else:
            print("No search results")
                    
    return df   
    
def get_number_of_pages(url,headers,params):
    
    '''
    Returns the number of pages of a search query. 
    We use the number of pages for further requests
    '''
    
    response = requests.get(url, headers=headers,params=params)
    
    number_of_pages = 0
    if response.status_code == 200:
        data = response.json()
        number_of_pages = int(data["SearchResult"]["UserArea"]["NumberOfPages"])
    else:
        print("Request failed")
        
    return number_of_pages
       
        
def drop_unecessary_data(df):
    
   if df is not None:
       #columns_to_drop = ["PositionLocation","PositionFormattedDescription","UserArea","QualificationSummary"]
       columns_to_drop = ["PositionFormattedDescription","UserArea","QualificationSummary",
                          "PositionRemuneration","PositionLocation",
                          "JobCategory","JobGrade","Longitude",
                          "Latitude","PositionOfferingType",
                          "PositionSchedule","PositionID"]
       locations_to_excluse = ['Anywhere', 'Multiple']
       
       df = df.drop(columns=columns_to_drop)
       #df = df[~df['PositionLocationDisplay'].str.contains('|'.join(locations_to_excluse))] #todo figure out why this breaks
   
   return df
   

def write_job_search_to_file(df,fname):
    
    df = drop_unecessary_data(df)
    if df is not None:
        df.to_csv(fname)
    else:
        print("No jobs found")

def format_series(df,key_to_format,keys_to_drop=[]):
    
    '''
    Key to format is the key in the response that  we're reformatting. 
    The key we're formatting is a list of dicts
    Where only index[0] contains the data we need and it's a list of keys
    
    keys_to_drop are the keys we don't need
    '''
    temp_df =  pd.DataFrame([data[0] for data in df[key_to_format]]).drop(keys_to_drop,axis=1)   

    return pd.concat([df,temp_df],axis=1)

def reformat_data(df):
    
    
    '''
    Several of the series contain data in the form of a dictionary.
    We take the dictionary and create separate columns for each key 
    '''
    df = format_series(df,"PositionRemuneration",["RateIntervalCode","Description"])
    df = format_series(df,"PositionLocation",["CountryCode","CountrySubDivisionCode"])
    df = format_series(df,"JobCategory")
    df = format_series(df,"JobGrade")

    return df
    
read_config_file()


#write_occupational_series_to_file()
#write_pay_plans_to_file()