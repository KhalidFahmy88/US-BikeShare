import time
import pandas as pd
import numpy as np

month_list = ['january','february','march','april','may','june','all']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or Enter to apply no month filter
        (str) day - name of the day of week to filter by, or Enter to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA:
        city = input('Which city would you like to filter? Chicago, New York City or Washington:\n').lower()
        if city not in CITY_DATA:
            print('\nData for {} is not available!. Please choose from the following cities: Chicago, New York City or Washington'.format(city.title()))
        else:    
            print('Data for {} is being accessed now!.'.format(city.title()))


    # TO DO: get user input for month (all, january, february, ... , june)
    month_input=''
    
    while month_input not in month_list:
        month_input = input("\nThere are so many data available for {}, would you like to filter by month?. Enter required month or press enter to skip this!".format(city.title())).lower()
        month = month_input
        if month_input == 'all':
            month = None
            break
       
        if month_input not in month_list:
            print('\n{} is not a valid month!. Please enter full month name. (e.g. June).'.format(month_input.title()))
            con = input('Do you want to skip month filtering? Y/N:').lower()
            if con == "n" or con == "no":
                month = month_input
                continue
            else:
                month = None
                print("\nMonth filtering has been skipped")
        break
     
    
    if month != None:
        month = month_list.index(month_input)+1
   

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    day_input=''
    
    while day_input.lower() not in day_list:
        day_input = input("\nEnter required day of week or press enter to skip this!:\n")
        day = day_input.title()
        if day_input.lower() == 'all':
            day = None
            break
        elif day_input.lower() not in day_list:
            print('\n{} is not a valid day!. Please enter full day name. (e.g. Monday).'.format(day_input.title()))
            con = input('Do you want to skip day filtering? Y/N:').lower()
            if con == "n" or con == "no":
                day = day_input.title()
                continue
            else:
                day = None
                print("\nDay filtering has been skipped")
        break
    print('filter by month: ',month)
    print('filter by day: ',day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or Enter to apply no month filter
        (str) day - name of the day of week to filter by, or Enter to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df= pd.read_csv(CITY_DATA[city])
    
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday_name
    
    if month != None:
        df = df[df['Month'] == month]
        
    if day != None:
        df = df[df['Day'] == day]
        
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == None:
        if day == None:
            print('The most common month is', month_list[df['Month'].mode()[0]-1])
            print('The most common day of week is', df['Day'].mode()[0])
           
        else:
            print('For {}\'s, the most common month is'.format(day.title()), month_list[df['Month'].mode()[0]-1])
        
    # TO DO: display the most common day of week
    elif day == None:
        print('During {}:'.format(month_list[month-1].title()))
        print('The most common day of week is', df['Day'].mode()[0])
     
    # TO DO: display the most common start hour
    else:
        print('During {}\'s of {}:'.format(day.title(),month_list[month-1].title()))

    
    print('The most common start hour of a day is', df['Start Time'].dt.hour.mode()[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    if month == None:
        if day == None:
            print('Among all months and days,')
            
        else:
            print('For {}\'s,'.format(day.title()))
            
     
    elif day == None:
        print('During {}:'.format(month_list[month-1].title()))
        
        
    else:
        print('During {}\'s of {}:'.format(day.title(),month_list[month-1].title()))

    # TO DO: display most commonly used start station
    print('The most commonly used start station is "', df['Start Station'].mode()[0],'"')
    


    # TO DO: display most commonly used end station
    print('The most commonly used end station is "', df['End Station'].mode()[0],'"')


    # TO DO: display most frequent combination of start station and end station trip
    strt_end_st = df.groupby(['Start Station', 'End Station']).count()
    st_max = strt_end_st.max()[0]
    strt_end_st_name = strt_end_st[strt_end_st['Start Time'] == st_max].index[0] 
    print('The most frequent combination of start station and end station trip are "{}" and "{}" respictively'.format(strt_end_st_name[0], strt_end_st_name[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    if month == None:
        if day == None:
            print('Among all months and days,')
            
        else:
            print('For {}\'s,'.format(day.title()))
            
     
    elif day == None:
        print('During {}:'.format(month_list[month-1].title()))
        
        
    else:
        print('During {}\'s of {}:'.format(day.title(),month_list[month-1].title()))

    # TO DO: display total travel time
    ttl_trp_tim = df['Trip Duration'].sum()//360
    print('Users travelled a total time of {} hours'.format(ttl_trp_tim))


    # TO DO: display mean travel time
    avg_trp_tim = df['Trip Duration'].mean()//60
    print('on avarage, a trip took {} minutes'.format(avg_trp_tim))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    if month == None:
        if day == None:
            print('Among all months and days,')
            
        else:
            print('For {}\'s,'.format(day.title()))
            
     
    elif day == None:
        print('During {}:'.format(month_list[month-1].title()))
        
        
    else:
        print('During {}\'s of {}:'.format(day.title(),month_list[month-1].title()))

    
    # TO DO: Display counts of user types
    print("The following are the counts of each user type:\n",df['User Type'].value_counts())
    


    # TO DO: Display counts of gender
    if city != 'washington':
        print('\nThe following are the counts of gender:\n', df['Gender'].value_counts())    
    
    # TO DO: Display earliest, most recent, and most common year of birth
        print('\nThe oldest user was born in', int(df['Birth Year'].min()))
        print('The youngest user was born in', int(df['Birth Year'].max()))
        print('The most common users\' year of birth is', int(df['Birth Year'].mode().max()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def raw_data(df):
    """Displays indvidual user trip data."""
    df.head()
    i=0
    j=5
    while True:
        show_data = input('\nWould you like to show more indvidual trips data? Enter yes or no.\n')
        if show_data.lower() not in ('yes', 'y'):
            break
        else:
            print(df.iloc[i:j,])
            i+=5
            j+=5
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df, month, day)
        user_stats(df, city, month, day)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
	main()
