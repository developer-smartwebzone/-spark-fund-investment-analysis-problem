
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


rounds2 = pd.read_csv ('rounds2.csv',encoding = "ISO-8859-1")
#print(rounds2.shape)  # 114949,6



#calculating average funding amount of Ventures
ventures = rounds2.iloc[:,5]

df_filtered_ventures = rounds2[(rounds2.funding_round_type == "venture")]
#print(df_filtered_ventures)


#df_filtered_ventures.to_csv('ventures.csv')
ven = pd.read_csv('ventures.csv',encoding = "ISO-8859-1")
avg_ventures1 = ven.iloc[:,6].mean()
#print(avg_ventures1)



# calculating average funding amount of seed

df_filtered_seed = rounds2[(rounds2.funding_round_type == "seed")]
#print(df_filtered_seed)
df_filtered_seed.to_csv('seed.csv')
sed = pd.read_csv('seed.csv',encoding = "ISO-8859-1")
avg_seed = sed.iloc[:,6].mean()
#print("average of seed type : : ",avg_seed)   #719817.9969071728



# calculating average funding amount of angel

df_filtered_angel = rounds2[(rounds2.funding_round_type == "angel")]
#print(df_filtered_angel)
df_filtered_angel.to_csv('angel.csv')
angl = pd.read_csv('angel.csv',encoding = "ISO-8859-1")
avg_angl = angl.iloc[:,6].mean()
#print("average of angel type : : ",avg_angl)   #958694.4697530865 



# calculating average funding amount of private equity

df_filtered_prvt = rounds2[(rounds2.funding_round_type == "private_equity")]
#print(df_filtered_prvt)
df_filtered_prvt.to_csv('private_equity.csv')
prvt = pd.read_csv('private_equity.csv',encoding = "ISO-8859-1")
avg_prvt = prvt.iloc[:,6].mean()
#print("average of private_equity type : : ",avg_prvt)    #73308593.02944215





# pie chart for which investment type is the most suitable (venture, seed, angel, private_equity)
slices = [avg_ventures1,avg_seed,avg_angl,avg_prvt]
activities = ['venture','seed','angel','private_equity']
cols = ['c','m','r','b']
outside = (0, 0, 0, 0) 
#plt.pie(slices,
       # labels=activities,
      #  colors=cols,
     #   startangle=90,
	#	explode=outside,
	#	shadow=True,
 #      )

#plt.title('Best Investment Type')
#plt.show()



# Countries heavily invested in the past


companies = pd.read_csv ('Companies_d.csv',encoding = "ISO-8859-1")
#print(companies.shape)  # 18334,10



# top nine countries which have received the highest total funding
sorted_countries_count = companies.groupby('country_code')['name'].count()
#print(sorted_countries_count)  # count the number of companies in every country



sorted_countries_count1 = sorted_countries_count.sort_values(ascending=False)
#print(sorted_countries_count1)  # USA is heavily invested country and then GBR, CAN, CHN, IND, DEu, FRA




# 3.Sector analysis- understanding the distribution of investments across the eight main sectors

sorted_main_sectors = companies.groupby('category_list')['name'].count()
#print(sorted_main_sectors)

sorted_main_sectors1 = sorted_main_sectors.sort_values(ascending=False)
#print(sorted_main_sectors1) 




# unique companies are present in companies
#print("total companies:")
f=companies['name'].count()
#print(f)   #total companies in company csv files - 18334

ggg=companies['name'].str.lower()

unicoms = ggg.unique()

#np.savetxt('unique_companies_in_companies.csv', list(zip(unicoms)), delimiter=',', fmt='%5s')
#print("unique companies in companies file")
comp = pd.read_csv('unique_companies_in_companies.csv', encoding = "ISO-8859-1")
unicom1=comp.count()
#print(unicom1)  #420 unique companies


print("################################################################")



# unique companies are present in round file
#print("total companies in rounds2:")
g=rounds2['company_permalink'].count()
#print(g)

gg=rounds2['company_permalink'].str.lower()
#print(gg)   #total companies in round csv files

unicom = gg.unique()
#print(unicom)

#np.savetxt('unique_companies_in_rounds.csv', list(zip(unicom)), delimiter=',', fmt='%5s')

comp1 = pd.read_csv('unique_companies_in_rounds.csv', encoding = "ISO-8859-1")
unicom11=comp1.count()
#print(unicom11)  #425 unique companies


#creating 1 dataframe which contains merged file of rounds and company
master_frame_pre = pd.merge(rounds2, companies, on='company_permalink', how='inner')
#master_frame.to_csv("joineddata.csv")
#print("Done")
master_frame=pd.read_csv('joineddata.csv')
 
 
 
spark_investment_amount = master_frame[(master_frame.raised_amount_usd >= 5000000) & (master_frame.raised_amount_usd <= 15000000)]
#print(spark_investment_amount) 
#spark_investment_amount.to_csv('spark_investment_amount.csv')

 
spark_master_frame =  pd.read_csv('spark_investment_amount.csv')
j=spark_master_frame['funding_round_type'].value_counts()          # How many entries are there for each investment type
#print(j)
 

 
 

top_9 = sorted_countries_count1.head(9)
#print(top_9)  # USA is heavily invested country and then GBR, CAN, CHN, IND, DEu, FRA, Isr, ESP

top_9_countries= spark_master_frame[(spark_master_frame.country_code == "USA") | (spark_master_frame.country_code == "GBR") |  (spark_master_frame.country_code == "CAN") |  (spark_master_frame.country_code == "CHN") | (spark_master_frame.country_code == "IND") | (spark_master_frame.country_code == "DEU") | (spark_master_frame.country_code == "FRA") | (spark_master_frame.country_code == "ISR") | (spark_master_frame.country_code == "ESP")]
#print(top_9_countries) 
#top_9_countries.to_csv('top_9.csv')
 
 
 
####################################################################
# sector analysis

spark_master_frame['category_list'] = spark_master_frame['category_list'].str.split('|').str.get(0)
print(spark_master_frame['category_list'])


D1= spark_master_frame[(spark_master_frame.country_code == "USA")]
#print(D1)
#D1.to_csv('usa.csv')
usa_frame =  pd.read_csv('usa.csv')
total_number_of_investments_usa=usa_frame['funding_round_type'].count() 
#print(total_number_of_investments_usa)  #4706

total_amount_of_investments_usa=usa_frame['raised_amount_usd'].sum() 
#print(total_amount_of_investments_usa)  #36851927875.0

top_sector_usa=usa_frame['category_list'].value_counts() 
print(top_sector_usa)  
#Biotechnology                            750
#Software                                 321
#Advertising                              209
#Health Care                              195
#Enterprise Software                      188

investment_in_first_top = usa_frame.groupby('category_list')['funding_round_type'].count()
#print(investment_in_first_top)





D2= spark_master_frame[(spark_master_frame.country_code == "GBR")]
#print(D2)
#D2.to_csv('gbr.csv')

gbr_frame = pd.read_csv('gbr.csv')
total_number_of_investments_gbr=gbr_frame['funding_round_type'].count() 
#print(total_number_of_investments_gbr)  # 222

total_amount_of_investments_gbr=gbr_frame['raised_amount_usd'].sum() 
#print(total_amount_of_investments_gbr) #1855273937.0
top_sector_gbr=gbr_frame['category_list'].value_counts() 
#print(top_sector_gbr)  
#Biotechnology             20
#Software                  18
#Clean Technology          14
#Curated Web               10
#Hardware + Software        9


D3= spark_master_frame[(spark_master_frame.country_code == "CAN")]
#print(D3)
#D3.to_csv('can.csv')
can_frame = pd.read_csv('can.csv')
total_number_of_investments_can=can_frame['funding_round_type'].count() 
#print(total_number_of_investments_can)  # 135

total_amount_of_investments_can=can_frame['raised_amount_usd'].sum() 
#print(total_amount_of_investments_can) #1173689728.0
top_sector_can=can_frame['category_list'].value_counts() 
#print(top_sector_can) 
#Software                     16
#Biotechnology                14
#Clean Technology              9
#Hardware + Software           7
#Cloud Computing               6











sorted_main_sectors = spark_master_frame.groupby('category_list')['name'].count()
#print(sorted_main_sectors)

sorted_main_sectors1 = sorted_main_sectors.sort_values(ascending=False)
#print(sorted_main_sectors1) 




 

