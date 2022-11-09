from numpy import percentile
import csv
import re
import pandas as pd

WRANGLEPATH = 'wrangled/'

SESDATAPATH = 'datasets/Socio-economic level.csv'
CRIMEDATAPATH = 'datasets/Recorded_offences_'
FILENAMES = [WRANGLEPATH + 'prepost_div.csv', WRANGLEPATH + 'during_div.csv']
DATAPATH_4_CLASS = 'four_class.csv'

def wrangle():
    wrangle_ses()
    wrangle_crime_general()
    wrangle_crime_type()

# SES Rankings

def wrangle_ses():
    with open(SESDATAPATH) as f:
        reader = csv.reader(f)
        data = list(reader)
        SUBURB = 1
        PERCENTILE = 9
        SES_SCORE = 3
        victoria_data = data[137:216]
        ses_rankings = []
        
        for line in victoria_data:
            pattern = r' \(.*'
            suburb_name = line[SUBURB]  
            revised_suburb = re.sub(pattern, '', suburb_name)[2:]     
            suburb_rank = [revised_suburb, int(line[PERCENTILE]), int(line[SES_SCORE])]
            ses_rankings.append(suburb_rank)
        
        ses_rankings.sort(key=lambda pr:pr[1] , reverse=True)
        four_class = {'low':[], 'medium low':[], 'medium':[], 'high':[]}
        
        for line in ses_rankings:
            if 99 >= line[1] >= 76:
                line.append('high')  
                four_class['high'].append(line[0])
            elif 75 >= line[1] >= 51:
                line.append('medium')   
                four_class['medium'].append(line[0])
            elif 50 >= line[1] >= 26:
                line.append('medium low')  
                four_class['medium low'].append(line[0])
            elif 25 >= line[1] >= 1:
                line.append('low') 
                four_class['low'].append(line[0])

    with open(WRANGLEPATH + 'ses_ranking.csv', 'w', newline='') as f2:
        writer = csv.writer(f2)
        headings = ['LGA', 'Percentile', 'Score', 'Class' ]
        writer.writerow(headings)
        for row in ses_rankings:
            writer.writerow(row)
            
    with open(WRANGLEPATH + 'four_class.csv', 'w', newline='') as f3:
        writer = csv.writer(f3)
        headings = ['Low', 'Medium low', 'Medium', 'High']
        writer.writerow(headings)
        four_class_values = list(four_class.values())
        four_class_column = list(zip(*four_class_values))
        four_class_column.append([four_class_values[0][-1], '', four_class_values[2][-1], four_class_values[3][-1]])
        for row in four_class_column:
            writer.writerow(row)

# Crime Count

def wrangle_crime_general():
    ses=pd.read_csv(WRANGLEPATH + 'ses_ranking.csv',encoding = 'ISO-8859-1')
    ses=ses.drop(columns=['Percentile','Class'])
    ses=ses.sort_values(by=['LGA'],ascending=True)
    ses=ses.set_index('LGA')
    ses.to_csv(WRANGLEPATH + 'ses.csv',index=True)

    periods = [["March", "December" ], ["June","September"]]
    status = ["prepost", "during"]

    i = 0
    while i < 2:
        generate_total_count(periods[i], status[i], ses)
        i += 1

def month_count(month):
    crimes = pd.read_csv(CRIMEDATAPATH + month + '_2020.csv',encoding = 'ISO-8859-1', low_memory=False)
    years = crimes['ï»¿Year']

    index = 0
    for year in years:
        if year != 2020:
            break
        index += 1

    lgas = crimes['Local Government Area'][:index]
    offence_div = crimes['Offence Division'][:index]
    offence_count = crimes['Offence Count'][:index]

    count_index = 0
    for count in offence_count:
        if type(count) is str:
            offence_count[count_index] = int(count.replace(',', ''))
        count_index += 1

    div_index = 0
    for div in offence_div:
        offence_div[div_index] = div.strip()
        div_index += 1

    data_dict = {'LGA': lgas, 'offence_div': offence_div, 'offence_count': offence_count}
    df = pd.DataFrame(data = data_dict)

    lgas_unique = set(lgas)
    offence_div_unique = set(offence_div)

    # Creates offence division in case of no occurences
    for lga in lgas_unique:
        for div in offence_div_unique:
            if len(df.loc[(df['LGA'] == lga) & (df['offence_div'] == div)]) == 0:
                df2 = pd.DataFrame({'LGA': [lga], 'offence_div': [div], 'offence_count': [0]})
                df.append(df2)

    grouped = df.groupby(['LGA', 'offence_div']).sum().unstack(fill_value=0).stack()
    grouped['offence_count'].to_csv(WRANGLEPATH + month + '_crime_count.csv')

def generate_total_count (months, status, ses):
    month_count(months[0])
    month_count(months[1])
    total_crimes_1=pd.read_csv(WRANGLEPATH + months[0] + '_crime_count.csv',encoding = 'ISO-8859-1')
    total_crimes_2=pd.read_csv(WRANGLEPATH + months[1] + '_crime_count.csv',encoding = 'ISO-8859-1')

    
    final = total_crimes_2.merge(total_crimes_1,on=['LGA', 'offence_div']).merge(ses,on='LGA')
    final['total_div_count'] = final['offence_count_x'] + final['offence_count_y']
    final=final.drop(columns=['offence_count_x','offence_count_y'])
    final.to_csv(WRANGLEPATH + status + '_div.csv', index = False)

# Specific Crime Counts for Four SES Class

def wrangle_crime_type():
    ses_division = pd.read_csv(WRANGLEPATH + DATAPATH_4_CLASS, encoding='ISO-8859-1', low_memory=False)
    for filename in FILENAMES:
        produce_four_class_off_counts(filename, ses_division)

def produce_four_class_off_counts(filename, ses_division):
    dataset_df = pd.read_csv(filename, encoding='ISO-8859-1', low_memory=False)

    # index 0 = crime type A
    off_division_crimes = {}
    ses_division_lst = {'Low':0,'Medium low':1,'Medium':2,'High':3}
    off_div_lst = []

    for off_div in dataset_df['offence_div'][:6]:
        off_div_lst.append(off_div)
        off_division_crimes[off_div] = [0,0,0,0]

    index = 0
    for name in dataset_df['LGA']:
        offence_type = str(dataset_df.loc[index, :]['offence_div'])
        off_count = int(dataset_df.loc[index, ['total_div_count']])

        for division in ses_division_lst:
            if name in list(ses_division[division]):
                ses_div_index = ses_division_lst[division]
                off_division_crimes[offence_type][ses_div_index] += off_count
                index += 1
                break

    revised_filename = filename[:-8]
    with open(f'{revised_filename}_four_class.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        headings = ['Crime Type', 'Low', 'Medium low', 'Medium', 'High']
        writer.writerow(headings)
        crime_type = 0
        offence_counts = 1
        for item in off_division_crimes.items():
            item[offence_counts].insert(0,item[crime_type])
            writer.writerow(item[offence_counts])