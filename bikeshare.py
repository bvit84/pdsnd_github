import time
import random
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

DATA_year = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

WEEK = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']

# one time message about program
def intro():
    print_slow("This program explores data related to bike share systems "
               "for three major cities in the United States: ")
    print_slow("Chicago, New York City and Washington.")
    print_slow("NOTE: Pressing [ENTER] key without selecting any "
               "choice will pick a random choice for you!")


# prints a string and pauses
def print_slow(s):
    time.sleep(1)
    print(s)


# checks validity of list, retries if failed
def check_validity(choice_list, valid_options):
    if type(choice_list) == list:
        for choice in choice_list:
            print_slow(choice)
    else:
        print_slow(choice_list)
    input_string = input().lower()
    while True:
        if input_string in valid_options:
            return input_string
        # random choice for [ENTER] only
        elif input_string == "":
            choice = random.choice(valid_options)
            print_slow(f"You opted random selection: {choice}")
            return choice
        else:
            print_slow("Please try again.")
            input_string = input().lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nLet\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs.
    city = check_validity(
        "Select Chicago, New York city or Washington:"
        , list((CITY_DATA).keys()))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = check_validity(
        "Select month (January - June) or all:"
        , DATA_year)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_validity(
        "Select day (Monday - Sunday) or all:"
        , WEEK)

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
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = DATA_year.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:\n', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:\n', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('Most frequent route:\n', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time:", df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print("Mean/average travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].median()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# option for game to start again or end
def end():
    if check_validity("\nWould you like to restart? Enter yes or no.\n",
                      ["y", "n"]) == "y":
        body()
    else:
        print_slow("Goodbye!")

        
def body():
    city, month, day = get_filters()
    df = load_data(city, month, day)
    print(df)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    end()


def main():
    intro()
    body()    


if __name__ == "__main__":
	main()
