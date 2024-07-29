import csv
import io

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


import pandas as pd

def parse_100_heats(fname, event, round):

    with open(fname, 'r') as file:
        content = file.readlines()

    # Split the content into records
    # every record is 11 lines long

    # Splitting the content into records, each record is 11 lines long
    records = [content[i:i + 11] for i in range(0, len(content), 11)]

    results = []

    for rec in records:
        place = rec[0].strip().split()[0]
        country = rec[1].strip()
        country = country[0:3]
        name = rec[2].strip()

        age_rt_status_points = rec[5].strip()
        age,rt,status_time = age_rt_status_points.split()[0:3]
        status = status_time[0:9]
        time = status_time[9::]

        fifty_split = rec[-3].split('\t')[0]

        one_hundred_split = rec[-1].split('\t')[0]

        res = [place, country, name, age, rt, status, time, fifty_split, one_hundred_split, event, round]
        results.append(res)

    df = pd.DataFrame(results, columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time', '50 Split', '100 Split', 'Event', 'Round'])

    return df

def parse_200_heats(fname, event, round):
    
        with open(fname, 'r') as file:
            content = file.readlines()
    
        # Split the content into records
        # every record is 11 lines long
    
        # Splitting the content into records, each record is 11 lines long
        records = [content[i:i + 15] for i in range(0, len(content), 15)]
    
        results = []
    
        for rec in records:
            place = rec[0].strip().split()[0]
            country = rec[1].strip()
            country = country[0:3]
            name = rec[2].strip()
    
            age_rt_status_points = rec[5].strip()
            age,rt,status_time = age_rt_status_points.split()[0:3]
            status = status_time[0:9]
            time = status_time[9::]
    
            
    
            #res = [place, country, name, age, rt, status, time, fifty_split, one_hundred_split, one_fifty_split, event, round]
            #results.append(res)
    
        #df = pd.DataFrame(results, columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time', '50 Split', '100 Split', '150 Split', 'Event', 'Round'])
    
        #return df

def parse_400_heats (fname, event, round='Heats'):
    with open(fname, 'r') as file:
        content = file.readlines()
    records = [content[i:i + 23] for i in range(0, len(content), 23)]
    results = []
    for rec in records:
        #print (rec[0])
        place = rec[0].strip().split()[0]
        country = rec[1].strip()
        country = country[0:3]
        name = rec[2].strip()
        #print (rec[5])
        age_rt_status_points = rec[5].strip()

        
        age,rt,status_time = age_rt_status_points.split()[0:3]
        

        status = status_time[0:9]
        time = status_time[9::]

        splits = rec[7::]
        splits_times= splits[1::2]
        distances = splits[0::2]
        distances = [dist.strip() for dist in distances]

        split_times = [split.split('\t')[0] for split in splits_times]
        res = [place, country, name, age, rt, status, time]
        res.extend(split_times)
        res.extend([event, round])
        results.append(res)

        
        
    columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time']
    columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time']
    columns.extend(distances)
    columns.extend(['Event', 'Round'])
    df = pd.DataFrame(results, columns=columns)

    return df


def parse_200_heats (fname, event, round='Heats'):
    with open(fname, 'r') as file:
        content = file.readlines()
    records = [content[i:i + 15] for i in range(0, len(content), 15)]
    results = []
    for rec in records:
        #print (rec[0])
        place = rec[0].strip().split()[0]
        country = rec[1].strip()
        country = country[0:3]
        name = rec[2].strip()
        
        age_rt_status_points = rec[5].strip()
        
        age,rt,status_time = age_rt_status_points.split()[0:3]
        

        status = status_time[0:9]
        time = status_time[9::]

        splits = rec[7::]
        splits_times= splits[1::2]
        distances = splits[0::2]
        distances = [dist.strip() for dist in distances]

        split_times = [split.split('\t')[0] for split in splits_times]
        res = [place, country, name, age, rt, status, time]
        res.extend(split_times)
        res.extend([event, 'Heats'])
        results.append(res)

        
        
    columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time']
    columns=['Place', 'Country', 'Name', 'Age', 'RT', 'Status', 'Time']
    columns.extend(distances)
    columns.extend(['Event', 'Round'])
    df = pd.DataFrame(results, columns=columns)

    return df



def sort_heats(df):

    # if status is not equal QUALIFIED, then copy the value in the status column to the time column
    df.loc[df['Status']!='QUALIFIED', 'Time'] = df['Status']

    # if status is not equal QUALIFIED, then set the value in the status column to ELIMINATED
    df.loc[df['Status']!='QUALIFIED', 'Status'] = 'ELIMINATED'


    # convert the time column to a datetime object, if there is a : in the time string, then use the format %M:%S.%f else use the format %S.%f
    df['Time'] = df['Time'].apply(lambda x: datetime.strptime(x, '%M:%S.%f') if ':' in x else datetime.strptime(x, '%S.%f'))

    # sort the dataframe by the time column in ascending order
    df = df.sort_values(by='Time').reset_index(drop=True)

    #reset the place column to be the row index + 1
    df['Place'] = df.index + 1

    return df


        
    




def parse_heats( filename, output_filename, event_name):
    with open(filename, 'r') as file:
        content = file.read()

    # Split the content into records
    records = content.split('-\t-\t')

    # Prepare CSV output
    output = io.StringIO()
    csv_writer = csv.writer(output)

    # Write header
    csv_writer.writerow(['Country Code', 'Full Name', 'First Name', 'Last Name', 'Age', 'Event'])

    # Process each record
    for record in records:
        if record.strip():  # Skip empty records
            lines = record.strip().split('\n')
            if len(lines) >= 5:
                country_code = lines[0].strip()
                #country code is repeated, so take only the first 3 characters
                country_code = country_code[0:3]
                full_name = lines[1].strip()
                first_name = lines[2].strip()
                last_name = lines[3].strip()
                age = lines[4].strip()

                csv_writer.writerow([country_code, full_name, first_name, last_name, age, event_name])

    # Write to file
    with open(output_filename, 'w', newline='') as file:
        file.write(output.getvalue())

    print(f"CSV {output_filename} has been created.")




def boxplot_ages_by_event(data: pd.DataFrame, fname: str):
    # Calculate the median age for each event
    event_medians = data.groupby('Event')['Age'].median().sort_values()
    
    # Create a new order of events based on the sorted medians
    event_order = event_medians.index.tolist()
    
    plt.figure(figsize=(12, 8))
    
    # Use the order parameter in sns.boxplot to specify the custom order
    sns.boxplot(x='Event', y='Age', data=data, palette='Set2', order=event_order)
    
    plt.title('How does the distribution of athlete ages vary by event?', wrap=True)
    plt.xlabel('Event')
    plt.xticks(rotation=90)
    plt.ylabel('Age')

    #save to file
    path='Plots/'+fname
    plt.savefig(path)
    print(f"Boxplot saved to {path}")


def events_per_swimmer(data: pd.DataFrame, fname: str):
    # Group by the Full Name and count the number of unique events
    events_per_swimmer = data.groupby('Full Name')['Event'].nunique()
    
    plt.figure(figsize=(12, 8))
    
    # Plot the histogram of events per swimmer
    sns.histplot(events_per_swimmer, kde=True, legend=True)
    
    plt.title('How many events does each swimmer participate in?', wrap=True)
    plt.xlabel('Number of Events')
    plt.ylabel('Number of Swimmers')

    #save to file
    path='Plots/'+fname
    plt.savefig(path)
    print(f"Histogram saved to {path}")




def histogram_ages(data: pd.DataFrame):
    sns.histplot(data=data, x='Age', kde=True, legend=True)
    plt.title('What is the distribution of athlete ages?', wrap=True)
    
    #save to file
    path='Plots/histogram_ages.png'
    plt.savefig(path)
    print(f"Histogram saved to {path}")


