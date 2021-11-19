import re
import json

import pandas as pd
df = pd.read_json('composer.json')
print(df)

def frequency_parser(in_string):

    pattern = re.compile(r"(\d+)\s*(x|times|x\s*times)\s*(/|per|a)\s*[a-zA-Z\-]*(week|month)\s*for[a-z\s]+(\d+)\-?\s*(weeks|months)", re.IGNORECASE)
    # sequence = "123x/week for 18-weeks & 1x/every-other-week for 7-weeks"
    results = pattern.findall(in_string)
    
    json_result = []
    for result in results:
        
        data = {
            "frequency":result[0],
            "frequency_unit":result[3],
            "duration":result[4],
            "duration_unit":result[5],
        }
        json_result.append(data)
    return json.dumps(json_result,indent=1)

sequence = "Moderate Frequency: 2 times per week for 25 Weeks Not to exceed 50 visits and re-evaluations as appropriate. Make-up visits may be completed within the certification period which may result in additional visits performed during a given week;\
Custom Frequency: 2x/week for 15-weeks and 1x/week for 10 weeks;\
Low Frequency: 1 times per week for 25 Weeks;\
Custom Frequency: 2x/week for 15-weeks and 1x/week for 10-weeks;\
Moderate Frequency: 2 times per week for 25 Weeks;\
Custom Frequency: 2x/week for 15-weeks & 1x/week for 10-weeks;\
Custom Frequency: 1x/week for 15 weeks decreasing to every other week for 10-weeks;\
Low Frequency: 1 times per week for 25 Weeks;\
Low Frequency: 1 times per week for 25 Weeks;\
Low Frequency: 1 times per week for 25 Weeks;"        
print(frequency_parser(sequence))