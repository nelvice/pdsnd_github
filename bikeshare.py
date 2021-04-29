import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday')
# choose function
def choose(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return choice

# get_filters function
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
        city = choose("\nFor what city(ies) do you want do select data, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>", CITY_DATA.keys())
        
    # TO DO: get user input for month (all, january, february, ... , june)
        month = choose("\nFrom January to June, for what month(s) do you "
                       "want do filter data? Use commas to list the names.\n>",
                       months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = choose("\nFor what weekday(s) do you want do filter bikeshare "
                     "data? Use commas to list the names.\n>", weekdays)
        
        confirmation = choose("\nPlease confirm that you would like to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        
        if confirmation == 'y':
            break
        else:
            print("\n try again!")
    

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
    if isinstance(city, list):
            
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)

        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])
     
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    
    print('\nthe most common month is: ' + str(months[common_month -1]))

    # TO DO: display the most common day of week

    common_day = str(df['weekday'].mode()[0])
    print('\nthe most common day is: ' + common_day)

    # TO DO: display the most common start hour
    
    common_hour = str(df['hour'].mode()[0])
    print('\nthe most common hour is: ' + common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_startstation = str(df['Start Station'].mode()[0])
    print('\nThe most common start station is:' + common_startstation)

    # TO DO: display most commonly used end station
    common_endstation = str(df['End Station'].mode()[0])
    print('\nThe most common end station is:' + common_endstation)

    # TO DO: display most frequent combination of start station and end station trip
    df['start end station'] = df['Start Station'] + '-' + df['End Station']
    
    common_start_end = str(df['start end station'].mode()[0])
    
    print('\nthe most common start and end station combination is:'+ common_start_end)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    total_travel = str(df['Trip Duration'].sum())
    
    print('\nTotal Travel Time is:' + total_travel)

    # TO DO: display mean travel time
    
    mean_travel = str(df['Trip Duration'].mean())
    
    print('\nMean Travel Time is:' + mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    try:
        
        gender_types = df['Gender'].value_counts()
        print(gender_types)   
    
    except KeyError:
        print("Sorry we don't have gender information for this city")
     

    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        
        earliest = str(int(df['Birth Year'].max()))
        print('\nThe youngest user was born in: ' + earliest)

        recent = str(int(df['Birth Year'].min()))
        print('\nThe most recent user was born in: ' + recent)

        common = str(int(df['Birth Year'].mode()[0]))
        print('\nThe most common user was born in: ' + common)
    except KeyError:
        print("we are sorry we don't have year information for this city")
    
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou opted to view raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = choose("\nWould you like to continue from where you "
                            "stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0


    # each loop displays 5 lines of raw data
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choose("Do you want to keep printing raw data?"
                      "\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place
    
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df,0)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
