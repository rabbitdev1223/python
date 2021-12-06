from requests import get
from json import dumps
from typing import Iterable, Dict, Union, List

AREA_TYPE_NATION = "nation" #this is nation
AREA_TYPE_REGION = "region" #this is region
AREA_NAME = "england" #ignore

filtersNation = [
    f"areaType={ AREA_TYPE_NATION }",
    # f"areaName={ AREA_NAME }"
]  #this is the nation filter 

filtersRegion = [
    f"areaType={ AREA_TYPE_REGION }",
    # f"areaName={ AREA_NAME }"
]#this is the region filter

structure = {
    "date": "date",
    "name": "areaName",
    "code": "areaCode",
    "dailyCases": "newCasesBySpecimenDate",
    "cumulativeCases": "cumCasesBySpecimenDate",
    "dailyDeaths": "newDeaths28DaysByPublishDate",
    "cumulativeDeaths": "cumDeaths28DaysByPublishDate",
    "cumulativeVaccinated": "cumPeopleVaccinatedCompleteByVaccinationDate",
    "vaccinationAge":"vaccinationsAgeDemographics"
} #this is structure


def get_API_data(filters,structure):

    #this is the url for endpoint
    ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"

    page_number = 1; #this is the page number       
    api_params = {
        "filters": str.join(";", filters), 
        "structure": dumps(structure, separators=(",", ":")), 
        
    } #the url parms which can be used in url
    

    data = list() #target result dict array
    while True:
        api_params['page'] = page_number #add page number to url params
        response = get(ENDPOINT, params=api_params, timeout=100) #get response from the url
        # here url means = "https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nation&structure={"date":"date","name":"areaName",...}
        # or "https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=region&structure={"date":"date","name":"areaName",...}
        
        if response.status_code >= 400: 
            raise RuntimeError(f'Request failed: { response.text }')
        current_data = response.json() 
        #current_data['data] is the array of data
        data.extend(current_data['data'])  #attach the current page array to the target result dict 
        page_number += 1 #increment page number by 1
        if current_data["pagination"]["next"] is None:# if next page is not availble
            break
    return data #array on all pages

results_json_national = get_API_data(filtersNation,structure) #get nation results
#here results_json_national is the array
print(results_json_national[0]) #get the first index;you can change the index
print(len(results_json_national)) #get the size of array
# print(results_json_national[1]);

results_json_regional = get_API_data(filtersRegion,structure)#get region results
print(len(results_json_regional))#get the size of array
print(results_json_regional[0])#get the first index;you can change the index