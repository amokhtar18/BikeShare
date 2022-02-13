import time
import pandas as pd
import numpy as np

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    # prompt the user to select a city if needed
    while True:
        try:
            entered_city = str(input("Which city would you like to explore (all - chicago-new york city- washington): ")).lower()
            if entered_city not in ['all', 'chicago', 'new york city', 'washington']:
                print('Choose a city from the list or type all if you want all cities!')
                continue
        except:
            print('Choose a city from the list or type all if you want all cities!')
        else:
            if entered_city == 'all':
                city = ['all', 'chicago', 'new york city', 'washington']
            else:
                city = [entered_city]
            print("-" * 100)
            break

    # prompt the user to select a month if needed
    while True:
        month_list = ['January', 'February', 'March', 'April', 'May', 'June']
        try:
            entered_month = int(input("Which Month of the year (type which month no. from 1-6 or 0 for all months): "))
            if entered_month not in [0, 1, 2, 3, 4, 5, 6]:
                print('Choose available Month!')
                continue
        except:
            print('Choose available Month!')
        else:
            if entered_month == 0:
                month = month_list
            else:
                month = [month_list[entered_month - 1]]
            print("-" * 100)
            break

    # prompt the user to select a week_day if needed
    while True:
        week_days = ['All', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday']
        try:
            entered_week_day = str(input("Which day of the week or all for no filter: ")).title()
            if entered_week_day not in week_days:
                print('enter a valid week day!')
                continue
        except:
            print('enter a valid week day!')
        else:
            if entered_week_day == 'All':
                day = week_days
            else:
                day = [entered_week_day]
            print("-" * 100)
            break
    return city, month, day

#define the function that loads the data based on the user selection
def load_data(city, month, day):
    print('Loading Data......')
    """read CSV Files"""
    df = pd.read_csv('new_york_city.csv')
    df2 = pd.read_csv('chicago.csv')
    df3 = pd.read_csv('washington.csv')
    """add a city column to dataframe"""
    df['city'] = 'new york city'
    df2['city'] = 'chicago'
    df3['city'] = 'washington'
    """combine files in one dataframe"""
    df4 = df.append(df2)
    df4 = df4.append(df3)
    """change start & End Time to Datetime"""
    df4['Start Time'] = pd.to_datetime(df4['Start Time'])
    df4['End Time'] = pd.to_datetime(df4['End Time'])
    """add hour,month,week_day columns to the dataframe from start time column"""
    df4['hour'] = df4['Start Time'].dt.hour.astype(int)
    df4['month'] = df4['Start Time'].dt.month_name().astype(str)
    df4['week_day'] = df4['Start Time'].dt.day_name().astype(str)
    df4['trip'] = df4['Start Station']+"--"+df4['End Station']
    Data = df4[(df4['city'].isin(city)) & (df4['month'].isin(month)) & (df4['week_day'].isin(day))]
    return Data

city,month,day = get_filters()
print('You Selected the following :- city:{}  month:{}  day:{}'.format(city,month,day))
print('-'*100)
filtered_data = load_data(city,month,day)

def time_stats(dataframe):
    start_time = time.time()
    """"Displays statistics on the most frequent times of travel."""
    x = dataframe.groupby(['city', 'month', 'week_day'])['hour'].apply(lambda x: x.mode().iloc[0])
    y = dataframe.groupby(['city', 'month'])['week_day'].apply(lambda x: x.mode().iloc[0])
    most_common_hour = pd.DataFrame(x)
    most_common_week_day = pd.DataFrame(y)
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    return most_common_hour ,most_common_week_day


def station_stats(dataframe):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    a = dataframe.groupby(['city'])['Start Station'].apply(lambda x: x.mode().iloc[0])
    b = dataframe.groupby(['city'])['End Station'].apply(lambda x: x.mode().iloc[0])
    c = dataframe.groupby(['city'])['trip'].apply(lambda x: x.mode().iloc[0])
    most_common_start_station = pd.DataFrame(a)
    most_common_end_station = pd.DataFrame(b)
    most_common_trip = pd.DataFrame(c)
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    return most_common_start_station ,most_common_end_station,most_common_trip


def trip_duration_stats(dataframe):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    e = dataframe.groupby(['city'])['Trip Duration'].sum()
    f = dataframe.groupby(['city'])['Trip Duration'].mean()
    total_trips_duration = pd.DataFrame(e)
    average_trip_duration = pd.DataFrame(f)
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    return total_trips_duration ,average_trip_duration


def user_stats(dataframe):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    g = dataframe.groupby(['city','User Type'])['trip'].count()
    h = dataframe.groupby(['city','Gender'])['trip'].count()
    i = dataframe.groupby(['city', 'Gender'])['Birth Year'].min()
    j = dataframe.groupby(['city', 'Gender'])['Birth Year'].max()
    k = dataframe.groupby(['city', 'Gender'])['Birth Year'].apply(lambda x: x.mode().iloc[0])
    count_of_user_types = pd.DataFrame(g).dropna()
    count_of_gender = pd.DataFrame(h).dropna()
    max_age = pd.DataFrame(i).dropna()
    min_age = pd.DataFrame(j).dropna()
    common_age = pd.DataFrame(k).dropna()
    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    return count_of_user_types,count_of_gender,max_age,min_age,common_age



def user_select_stats():
    """prompt the user to select information required using his selection"""
    print('select the required information to extract')
    while True:
        try:
            selection = str(input('("T" for Time Stats - "S" for Stations Stats - "TR" for Trips Stats - "D" for Demographics ): ')).lower()
            if selection not in ['t','s','tr','d']:
                print('Choose a valid selection')
                continue
        except:
            print('Choose a valid selection')
        else:
            if selection == 't':
                print("\nA- most frequent times of travel")
                print('~' * 50)
                print('Most Common Hour of travel as follows :')
                most_common_hour, most_common_week_day = time_stats(filtered_data)
                print(most_common_hour)
                print('\n')
                print('Most Common week_day of travel as follows :')
                print(most_common_week_day)
                print('-' * 100)
            elif selection == 's':
                print("\nB- most common stations")
                print('~' * 50)
                print('Most Common start stations :')
                most_common_start_station, most_common_end_station, most_common_trip = station_stats(filtered_data)
                print(most_common_start_station)
                print('\n')
                print('Most Common end station :')
                print(most_common_end_station)
                print('\n')
                print('Most Common trip :')
                print(most_common_trip)
                print('-' * 100)
            elif selection == 'tr':
                print("\nC- trips durations")
                print('~' * 50)
                print('Total Trips Durations in Seconds :')
                total_trips_duration, average_trip_duration = trip_duration_stats(filtered_data)
                print(total_trips_duration)
                print('\n')
                print('Average Trip Duration in seconds :')
                print(average_trip_duration)
                print("-" * 100)
            elif selection == 'd':
                print("\nD- Demographics")
                print('~' * 50)
                print('No of trips by user type :')
                count_of_user_types, count_of_gender, max_age, min_age, common_age = user_stats(filtered_data)
                print(count_of_user_types)
                print('\n')
                print('No of Trips by User Gender :')
                print(count_of_gender)
                print('age_ranges :')
                print("max_age\n:", max_age)
                print("\nmin_age\n:", min_age)
                print("\ncommon_age\n:", common_age)
                print("-"*100)
            break
user_select_stats()