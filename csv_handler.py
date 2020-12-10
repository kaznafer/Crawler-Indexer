import pandas
import os


# at first we create a csv if doesn't exist after we overwrited with all the words  we found in the websites follow it
# by their frequency in every url.
from Index import Index


def write_a_csv(obj):
    val = list()
    if not os.path.exists('Inverted Index.csv'):
        open('Inverted Index.csv', 'wb')
    with open('Inverted Index.csv', 'wb'):
        for x, y in Index.the_dict.items():  # we scan the dictionary that we handle at the Index class
            val.append(Index.the_dict[x])
        df = pandas.DataFrame(data={"WORDS": list(Index.the_dict.keys()), "FREQ, URL, URL'S#": val})  # inform the dataframe
        # using pandas
        df.to_csv('Inverted Index.csv', header=True, index=False)  # inform the csv with the above dataframe.


# read a csv using pandas module.
def read_a_csv(csv_name):
    df = pandas.read_csv(csv_name)
    return df


# delete a csv using os module
def delete_a_csv(csv_name):
    os.remove(csv_name)
