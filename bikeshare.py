import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("\nWhich city would you like to see data for New York City, Washington or Chicago?\n") .lower()
        if city in CITY_DATA:
            break
        else:
            print("\nInvalid input. Please choose within a city of New York City, Washington or Chicago.\n")

    # user's choice filter type
    choice=input("\nchoose which filter of data would you like to add: Month, Day, or not at all.\n Type None for no time filter: ").lower()
    while choice not in(['month', 'day', 'both','none']):
        print('please enter a valid filter choice such as: Day, Month, Both or None.')
        choice = input('\nchoose which filter of data would you like to add: Month, Day, or not at all.\n Type None for no time filter:' ).lower()


    #  get user input for day of week (all, monday, tuesday, ... sunday)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if choice == 'month' or choice == 'both':
        month = input("\nPlease enter a month name from January to June.\n").lower()
        while month not in months:
            print("\nPlease enter a valid month input\n")
            month = input("\nPlease enter a month name from January to June.\n").lower()
    else:
        month='all'
    days= ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
    if choice == 'day' or choice == 'both':
        day = input("\nPlease enter a day name , or type all for no day filter\n").lower()
        while day not in days:
            print("\nPlease enter a valid day input\n")
            day = input("\nPlease enter a day name , or type all for no day filter\n").lower()
    else:
        day='all'


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

    df = pd.read_csv(CITY_DATA[city])   #load city data file to a dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time'])  #convert from a start to data time

    df['month'] = df['Start Time'].dt.month     #create month column from exatracting its data from Start Time
    df['day_of_week'] = df['Start Time'].dt.day_name()  #create day column from exatracting its data from Start Time

    #filtering month input
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #filtering day input
    if day != 'all' :
        df = df[df['day_of_week'] == day.title()]    #sentence case to match how written in the data set

    return df

def fiv_row_disp(df):
    """
    display rows of data depending on user answer "load 5 rows"

    Args:
         df - filitered city dataframe that returned from load_data function

    """
    row_display = input("\nDo you want to see the first five raws of data? Yes or No:\n").lower()
    if  row_display == 'yes':
        r = 0
        while True:
            print(df.iloc[r: r+5])
            r += 5
            more_row = input("\nDo you want to see more? Yes or No:\n").lower()
            if more_row != 'yes':
                break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    cmn_month = df['month'].mode()[0]
    print("The most common month is:",months[cmn_month-1],".")

    # display the most common day of week
    cmn_day = df['day_of_week'].mode()[0]
    print("The most common day is:",cmn_day,".")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour  #create hour column through extracting it from start time
    cmn_hour = df['hour'].mode()[0]
    print("The most common hour is:",cmn_hour,".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    cmn_start = df['Start Station'].mode()[0]
    print("The most common start station is: ",cmn_start,".")

    # display most commonly used end station
    cmn_end = df['End Station'].mode()[0]
    print("The most common end station is: ",cmn_end,".")


    #  display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    cmn_combin = df['combination'].mode()[0]
    print("The most frequent combination of start station and end station trip is: ",cmn_combin,".")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    def cvrt_to_hour(x):
        """convert from second to hours.
        Args:
         x - number of second
        """

        result= x/(60*60)

        return result

    # display total travel time
    trvl_time = df['Trip Duration'].sum()
    print("The total travel time is:",trvl_time, " Second. Or ", cvrt_to_hour(trvl_time)," Hour. or",int(cvrt_to_hour(trvl_time)//24)," days.")

    #  display mean travel time
    trvl_avg = df['Trip Duration'].mean()
    print("The average travel time is:",trvl_avg, " Second. Or ",cvrt_to_hour(trvl_avg)*60 ," min. or",cvrt_to_hour(trvl_avg) ," Hour.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("\nThe counts of each user type: \n",user_type)

    # Display counts of gender
    if 'Gender' in df:
        gndr = df['Gender'].value_counts()
        print("\ncounts of each gender :\n",gndr)
    else:
        print("Gender information not available in this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        early = df['Birth Year'].min()
        print("The most earliest year of birth is: ",early,".")
        rcnt = df['Birth Year'].max()
        print("The most recent year of birth is: ",rcnt,".")
        cmn_birth = df['Birth Year'].mode()[0]
        print("The most common year of birth is: ",cmn_birth,".")
    else:
        print("Birth year information not available in this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city,month,day= get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        fiv_row_disp(df)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
