import sys

import numpy as np
import pandas as pd


def print_line_separator():
    # Line separator to use between each segment
    print('-' * 40)


def print_continue_message():
    input('\nPress Enter to continue...\n')


# Display raw data
##########################################################################

def raw_data(df):
    """
    Displays raw data to the user upon their request.

    Prints:
        The raw data, five lines at a time, until the user specifies
        to stop, or until the end of the dataframe is reached.
    """
    show_data = input('\nWould you like to see the raw data?'
                      ' Enter yes or no.\n').lower()
    i = 0
    while show_data.startswith('y'):
        if i + 5 < df.shape[0]:
            print(df.iloc[i:i+5])
            i = i + 5
        else:
            print(df.iloc[i:])
            break

        show_data = input('\nWould you like to see more of the data?'
                          ' Enter yes or no.\n').lower()

    print_line_separator()


# Display statistics
##########################################################################

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Prints:
        Breakdown of users - total number of subscribers, customers, and dependents
        Breakdown of gender - total number of males and females
        Breakdown of birth years - oldest, youngest, and most popular birth year

    Note:
        Not all datasets contain gender and birth year data. In this case, the user
        will be alerted that no gender/birth year data is available for this city.
    """
    print("\nCalculating User Stats...\n")

    print("Breakdown of users:")
    user_breakdown = df['User Type'].value_counts()
    print(user_breakdown.to_string(), '\n')

    print("Breakdown of gender:")
    if 'Gender' in df:
        gender_breakdown = df['Gender'].value_counts()
        print(gender_breakdown.to_string(), '\n')
    else:
        print("No gender data available for this city.\n")

    print("Breakdown of birth years:")
    if 'Birth Year' in df:
        oldest_birth_year = int(df['Birth Year'].min())
        youngest_birth_year = int(df['Birth Year'].max())
        popular_birth_year = english_list(df['Birth Year'].mode().apply(int))

        birth_year_data = pd.Series([oldest_birth_year,
                                     youngest_birth_year,
                                     popular_birth_year],
                                     index=['Oldest', 'Youngest', 'Most popular'])

        print(birth_year_data.to_string(), '\n')
    else:
        print("No birth year data available for this city.\n")

    print_continue_message()
    print_line_separator()


def human_readable_time(duration_in_seconds):
    # Input time in seconds and convert to days, hours, minutes, and seconds
    time = []

    days, remainder = divmod(int(duration_in_seconds), 86400)
    if days == 1: time.append(str(days) + ' day')
    elif days > 0: time.append(str(days) + ' days')

    if remainder > 0:
        hours, remainder = divmod(remainder, 3600)
        if hours == 1: time.append(str(hours) + ' hour')
        elif hours > 0: time.append(str(hours) + ' hours')

        if remainder > 0:
            minutes, seconds = divmod(remainder, 60)
            if minutes == 1: time.append(str(minutes) + ' minute')
            elif minutes > 0: time.append(str(minutes) + ' minutes')
            if seconds == 1: time.append(str(seconds) + ' second')
            elif seconds > 0: time.append(str(seconds) + ' seconds')

    return english_list(time)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Prints:
        Total - total amount of time traveled
        Average - average time spent on each trip
    """
    print('\nCalculating Trip Duration...\n')

    total_trip_seconds = df['Trip Duration'].sum()
    total_trip_duration = human_readable_time(total_trip_seconds)
    average_trip_seconds = df['Trip Duration'].mean()
    average_trip_duration = human_readable_time(average_trip_seconds)

    print("The total traveling done during this period was {}.\n"
          .format(total_trip_duration))

    print("The average time spent on each trip was {}.\n"
          .format(average_trip_duration))

    print_continue_message()
    print_line_separator()


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Prints:
        Start station - most popular start station
        End station - most popular end station
        Trip - most popular start/end station combination
    """
    print("\nCalculating The Most Popular Stations and Trip...\n")

    popular_start_station = english_list(df['Start Station'].mode())
    popular_end_station = english_list(df['End Station'].mode())
    popular_trip = pd.Series(df.groupby(['Start Station', 'End Station']).size().idxmax(),
                             index=['Start station', 'End station'])

    print("The most popular start station is " + popular_start_station + ".\n")

    print("The most popular end station is " + popular_end_station + ".\n")

    print("The most popular trip:")
    print(popular_trip.to_string(), '\n')

    print_continue_message()
    print_line_separator()


def twelve_hour_time(hour, minutes=0):
    # Input military hours (and optionally minutes)
    # Return time as string, e.g., "2:00 AM"

    def is_midnight(hour):
        return hour == 0

    def is_pm(hour):
        return hour > 12

    twelve_hour = 12 if is_midnight(hour) else ((hour - 12)
                     if is_pm(hour) else hour)

    suffix = 'PM' if is_pm(hour) else 'AM'

    formatted_time = '{}:{:02d} {}'
    return formatted_time.format(twelve_hour, minutes, suffix)


def english_list(series):
    # Return a series as a comma-delimited list. E.g., "A, B, C".
    return  ', '.join(map(str, series))


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Prints:
        Month name - most popular month for traveling
        Day of week - most popular day for traveling
        Hour - most popular hour of day to start a trip
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # Omit displaying day or month statistics for columns which are
    # filtered to a single value, as it's not meaningful information.
    if df['month name'].nunique() > 1:
        popular_month = english_list(df['month name'].mode())
        print("The most popular month for traveling is " + popular_month + ".\n")

    if df['day of week'].nunique() > 1:
        popular_day = english_list(df['day of week'].mode())
        print("The most popular day for traveling is " + popular_day + ".\n")


    popular_start_hour = english_list(df['start hour'].mode().apply(twelve_hour_time))
    print("The most popular hour of the day to start your travels is "
          + popular_start_hour + ".\n")

    print_continue_message()
    print_line_separator()


# Load data
##########################################################################

def add_date_columns(df):
    # Add month name, day of week, and start hour columns to dataframe
    start_time = pd.to_datetime(df['Start Time'])

    month_names = ['January', 'February', 'March',
                   'April',   'May',      'June',
                   'July',    'August',   'September',
                   'October', 'November', 'December']

    month_name_column = start_time.dt.month.apply(lambda x: month_names[x - 1])
    day_of_week_column = start_time.dt.weekday_name
    start_hour_column = start_time.dt.hour

    return (month_name_column,
            day_of_week_column,
            start_hour_column)


def city_data(city):
    # Specified city data to load
    data_directory = 'bikeshare_data/'
    city_data = {'Chicago': 'chicago.csv',
                 'New York': 'new_york_city.csv',
                 'Washington': 'washington.csv'}
    try:
        return pd.read_csv(data_directory + city_data[city])
    except FileNotFoundError:
        # Gracefully quit program when file is not found
        sys.exit("\nError: File '{}' not found. Exiting program.\n"
                 .format(city_data[city]))

def load_data(city, month_filter=None, day_filter=None):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = city_data(city)

    # Add additional date columns to assist with later analysis
    (df['month name'],
     df['day of week'],
     df['start hour']) = add_date_columns(df)

     # Filter data down to month and day supecified by user if applicable
    if month_filter:
        df = df[df['month name'] == month_filter]
    if day_filter:
        df = df[df['day of week'] == day_filter]

    return df


# Get filters
##########################################################################

def valid_input(items, message):
    # constrain input to items in provided list
    item = None
    error_message = "That is not a valid input.\n" + message
    while item not in items:
        item = input('\n' + message + '\n').lower()
        message = error_message
    return item


def get_day_of_week():
    # Day to filter
    days = ('monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday')
    message = ("Which day - Monday, Tuesday, Wednesday,"
               " Thursday, Friday, Saturday, or Sunday?")
    day = valid_input(days, message)
    return day.title()


def get_month():
    # Month to filter
    month_names = ('january', 'february', 'march', 'april', 'may', 'june')
    message = "Which month? - January, February, March, April, May, or June?"
    month_name = valid_input(month_names, message)
    return month_name.title()


def get_time_filters():
    # Optional time filters for month and/or day
    filter_options = ('month', 'day', 'both', 'neither', '')
    message = "Would you like to filter the data by month, day, both, or neither?"

    time_filters = valid_input(filter_options, message)
    if time_filters == 'both':
        time_filters = ('month', 'day')

    # Initialize variables as unfiltered and only set them if required
    month_name, day = None, None

    if 'month' in time_filters:
        month_name = get_month()
    if 'day' in time_filters:
        day = get_day_of_week()

    return month_name, day


def get_city():
    # City to filter
    cities = ('chicago', 'new york', 'washington')
    message = "Would you like to see data for Chicago, New York, or Washington?"
    city = valid_input(cities, message)
    return city.title()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    """
    print_line_separator()
    print("\nHello! Let's explore some US bikeshare data during 2017!")

    city = get_city()
    month_name, day = get_time_filters()

    # Print a confirmation of all filters that have been applied.
    # E.g., "Filtering data to Saturdays in Chicago during March."
    month_info = ' ' + month_name if month_name else ''
    day_info = day + 's in ' if day else ''

    print("\nRestricting data to {0}{1} during{2} 2017.\n".
          format(day_info, city, month_info))

    print_line_separator()

    return city, month_name, day


# Main
##########################################################################

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart?'
                        ' Enter yes or no.\n').lower()
        print()

        if not restart.startswith('y'):
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Print goodbye message rather than error code if user force quits program.
        print("\nKeyboard interrupt detected. Goodbye.\n")
