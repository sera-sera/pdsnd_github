import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'argentine' : 'argentine.csv',
              'brazil' : 'brazil.csv'
              }
months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','october','november','september','december']

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter city name : ").lower()
        if city in CITY_DATA :
            print ('File to analyze : ' + CITY_DATA.get(city))
            break    
        else:
            print('City not recognized')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month : ").lower()
        if month not in months and month != 'all':
            print('mont not recognized')
        if month == 'all':
            print('Analyze for all months')
            break
        else:
            print('Month to analyze : ' + month)
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day : ").lower()
        if day not in days and day != 'all':
            print('day not recognized')
        if day == 'all':
            print('Analyze for all day')
            break
        else:
            print('Day to analyze : ' + day)
            break
 
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name 
      # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    while True:
        ask_user = input('Would you like to view 5 rows of individual trip data, yes or no ? : ').lower()
        if ask_user == 'yes':
            #print (df.head(5))
            start_loc = 0
            while (True):
                print(df.iloc[start_loc:start_loc+5])
                view_display = input("Do you wish to continue?: ").lower()
                if(view_display=='yes'):
                    start_loc += 5
                if(view_display=='no'):
                    break
        if ask_user == 'no':
            break
        break       
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    #if month is given then we don't need to display the most common month
    df['Month'] = df['Start Time'].dt.month
    common_month=df['Month'].mode()[0]
    print('The Most Common Month: {}'.format(common_month))
    
    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common day_of_week :', popular_day_of_week)
    
    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most Commonly used Start Station : {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('Most commonly used end station : {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df_start_end=(df['Start Station']+ ' => ' +df['End Station'])
    print('most frequent combination of start station and end station trip: {}'.format(df_start_end.mode()[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_seconds=df['Trip Duration'].sum()
    hours = total_travel_seconds // 3600
    minutes = hours % 60
    secondes = minutes % 60
    print ('total travel time : {} hours {} minutes {} secondes'.format(hours, minutes, secondes ))
    
    # TO DO: display mean travel time
    mean_time_seconds=df['Trip Duration'].mean()
    print ('Mean travel time : {} secondes'.format(mean_time_seconds ))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nDisplay counts of user types : \n {}'.format(user_types))

    # TO DO: Display counts of gender
    #Exception WASHINGTON
    if 'Gender' in df:
        print('\nDisplay counts of gender : \n{}'.format(df['Gender'].value_counts()))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe\n')
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest=df['Birth Year'].min()
        recent=df['Birth Year'].max()
        mode=df['Birth Year'].mode()[0]
        print('\nThe earliest year of birth is {}'.format(int(earliest)))
        print('The most recent year of birth is {}'.format(int(recent)))
        print('The most common year of birth is {}'.format(int(mode)))
    else:
        print('Birth Year cannot be calculated because Birth Year does not appear in the dataframe\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
