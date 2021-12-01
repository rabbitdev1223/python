# import pandas as pd
# df = pd.read_excel ('book1.xlsx')
# #print(df)
# # show it in html file
# html = df.to_html()
# #write html to file
# text_file = open("source.html", "w")
# text_file.write(html)
# text_file.close()
#
# #define function to find out the outlier
# def find_outlier(val):
#     temp=[]
#     for i in range(3):
#         temp.append(val[i])
#  3 G1,G2=(0,0)
#     temp.sort()
#     if temp[0]<temp[1]/1.5:
#         G1 = temp[1]/1.5 - temp[0]
#     if temp[2]>temp[1]*1.5:
#         G2 = temp[2]-temp[1]*1.5
#     else:
#
#     if G1>G2 and G1>1:
#         ot = temp[0]
#     elif G2>G1 and G2>1:
#         ot = temp[2]
#
#     # for i in range(3):
#     #     if ot==val[i]:
#     #         return i

#
# # create a function to return the average of outlying set
# def Find_Avg(val,pos):
#     #print(sum(val))
#  #   return (sum(val) - val[pos])/2
# # to find new total grades after removing outliers
# def Set_Total(val):
#     return int(sum(val)/3)
#
# #create a blank dataframe
#
# i = 0
# col_header = ['Ans_ID','CR11','CR12','CR13','CR14','CR15','CR21','CR22','CR23','CR24','CR25','CR31','CR32','CR33','CR34','CR35','TOTAL']
# NewData = pd.DataFrame()
# for i in col_header:
#     NewData[i]=[]
# start=0
# record=[]
# ans_code=''
# i=0
# counter = 0
# Data_with_outlier = pd.DataFrame(NewData)
#
# for start in range(start,len(df),3):
#     temp1=[]
#     ans_code=df.iloc[start][0]
#     temp = pd.DataFrame(df.iloc[start:start+3,2:7])
#     i=0
#     #copy 3 records/rows in 1 row
#     total = 0
#     for i in range(0,3):
#         for j in range(0,5):
#             temp1.append(temp.iloc[i][j])
#             total = total + temp.iloc[i][j]
#     temp1.insert(0,ans_code)
#     total = int(total/3)
#     temp1.insert(len(temp1), total)
# #    print(temp1)
#     NewData_len = len(NewData)
#     NewData.loc[NewData_len] = temp1
#     temp1=[]
# #print(NewData)
# # Write this data to html file source.html
# #write html to file
# html = NewData.to_html()
# text_file = open("source_New.html", "w")
# text_file.write(html)
# text_file.close()
# #print the CR groups
# i=1
# temp1=[]
# j=1
#
# for row_count in range(NewData_len):
#     for i in range(1,6):
#         #print("Set "+str(i))
#         counter = i
#         test_data = []
#         testdata_index = []
#         for j in range(0,3):
#             test_data.append(NewData.iloc[row_count,counter])
#             testdata_index.append(counter)
#             counter = counter +5
#     #call function outlier
#         #print(testdata_index)
#         #print(test_data)
#         ot = find_outlier(test_data)
#         #print("Outlier position: " + str(ot))
#         if ot<3:
#             #print("The original value:")
#             #print(NewData.iloc[row_count,testdata_index[ot]])
#             NewVal = Find_Avg(test_data,ot)
#             #print("New Value:", str(NewVal))
#             NewData.iloc[row_count,testdata_index[ot]] = NewVal
#             #NewData.iloc[row_count,testdata_index[ot]] = str(NewVal) + "*"
#             #print("The value with outlier:")
#             #print(NewData.iloc[row_count,testdata_index[ot]])
#     New_Total = Set_Total(NewData.iloc[row_count,1:15])
#     #print("New Total:" + str(New_Total))
#     NewData.iloc[row_count,16] = New_Total
# print(NewData)
# html = NewData.to_html()
# text_file = open("source_Outlier.html", "w")
# text_file.write(html)
# text_file.close()
#
# # This function is to find out the outlier
#
#
#
#
#
#
