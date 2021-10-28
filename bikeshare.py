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
        (str) day_name - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while True:
        try:
            city = input("Please enter the name of the city you want to investigate(chicago, washington, new york city):\n").strip().lower()
            city = CITY_DATA[city] #checking if input is valid and assigning it to city
            print("-"*10)
            break
        except:
            print("\n","Invalid input. Please enter city name correctly as mentioned in the brackets".center(100))
        finally:
            print()
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["all","january","february","march","april","may","june"]
    month = None
    while True:
        try:
            month = input("Please enter the month you want to filter the data with(all,january february, .., june): \n").strip().lower()
            month = months.index(month) #checking if input is valid and assigning it to month
            print("-"*10)
            break
        except:
            print("\n","Invalid input. Please enter the month correctly as mentioned in the brackets".center(100))
        finally:
            print()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_names = ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day_name = None
    while True:
        try:
            day_name = input("Please enter the day of the week you want to filter the data with(all, monday, tuesday, .., sunday): \n").strip().lower()
            day_names.index(day_name) #checking if input is valid 
            print("-"*10)
            break
        except:
            print("\n","Invalid input. Please enter the day of the week correctly as mentioned in the brackets".center(100))
        finally:
            print()
        

    print('-'*40)
    return city, month, day_name




def load_data(city, month, day_name):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day_name - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["months"] = df["Start Time"].dt.month
    df["month_names"] = df["Start Time"].dt.month_name()
    df["day_names"] = df["Start Time"].dt.day_name()
    
    if month != 0: #checking if month doesn't equal all
        df = df[df["months"] == month] #filtering the dataframe according to month
    
    if day_name != "all": #checking if day_name doesn't equal all
        df = df[df["day_names"] == day_name.title()] #filtering the dataframe according to day_name

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if len(pd.unique(df["months"])) == 1:
        print("Please set month to 'all' to calculate the most common month!")
    else:
        print("The most common month is",df["month_names"].mode()[0])

    # TO DO: display the most common day of week
    if len(pd.unique(df["day_names"])) == 1:
        print("Please set day of the week to 'all' to calculate the most common weekday!")
    else:
        print("The most common day of the week is",df["day_names"].mode()[0])    

    # TO DO: display the most common start hour
    print("The most common start hour is",df["Start Time"].dt.hour.mode()[0]) 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is", df["Start Station"].mode()[0])

    # TO DO: display most commonly used end station
    print("The most commonly used end station is", df["End Station"].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df["combination"] = tuple(zip(df["Start Station"],df["End Station"]))
    most_frequent_combination = df["combination"].mode()[0]
    print("The most frequent combination of start & end stations is '{}' & '{}'".format(*most_frequent_combination))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    df["Trip Duration"]= pd.to_timedelta(pd.to_datetime(df["End Time"]) - pd.to_datetime(df["Start Time"]))
        
    # TO DO: display total travel time
    print("The total travel time equals:{} days, {} hours, {} minutes and {} seconds!".format(*df["Trip Duration"].sum().components[:4]))
    print("OR")
    print("{} seconds total!".format(df["Trip Duration"].sum().total_seconds()))
    print()
    # TO DO: display mean travel time
    print("The mean travel time equals:",df["Trip Duration"].mean().total_seconds()," seconds!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Subscriber counts:",df["User Type"].value_counts()["Subscriber"])
    print("Customer counts:",df["User Type"].value_counts()["Customer"])
    print()
    # TO DO: Display counts of gender
    if "Gender" in df:
        print("Male counts:",df["Gender"].value_counts()["Male"])
        print("Female counts:",df["Gender"].value_counts()["Female"])
        print() 
    else:
        print("Gender counts are not available for this city!")
        print()

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("Earliest year of birth:", int(df["Birth Year"].min()))
        print("Most recent year of birth:", int(df["Birth Year"].max()))
        print("Most common year of birth:", int(df["Birth Year"].mode()))
        print()
    else:
        print("Birth years are not available for this city!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw(df):
    i = 0
    more_raw = input("Please type yes if you would like to display raw data:\n").strip().lower()
    while True:
        if more_raw != "yes":
            print("-"*40)
            break
        if i + 5 > len(df.index): #check if end of dataframe has been reached
            print(df.iloc[i:len(df.index)+1])
            print("End of data!")
            break
        else:
            print(df.iloc[i:i+5])
            print()
            more_raw = input("Type yes to display more raw data\n").strip().lower()
        i += 5
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        
        if restart.lower() != 'yes':
            
            break
            

if __name__ == "__main__":
	main()
