import twint
import string
import emoji
import re
import pandas as pd
import numpy as np


def cleanTweets(text):
    text = re.sub("https*\S+", "", text)
    text = re.sub("@\S+", "", text)
    text = emoji.demojize(text)
    text = ''.join(text)
    return text


def tweetsExtractor(username_list):
    for username in username_list:
        # Configure
        c = twint.Config()
        c.Username = username
        c.Search = "exclude:replies"
        c.Store_csv = True
        c.Count = True
        c.Hide_output = True
        c.Output = username + "_tweets.csv"
        c.Custom["tweet"] = ["id", "user_id",
                            "created_at", "username", "name", "tweet"]

        # Run
        print("Downloading %s's tweets:" % username)
        twint.run.Search(c)
        df = pd.read_csv(username + "_tweets.csv")
        for row in df.itertuples():
            df.at[row.Index, 'tweet'] = cleanTweets(row.tweet)

        # Remove any rows with empty strings
        df.replace(r'^\s*$', np.nan, inplace=True, regex=True)
        df.dropna(how="any", axis=0, inplace=True)
        df.to_csv(username + "_tweets.csv", index=False)

usernames_list = [
    # 'syahmirastam',
    # 'apezzz_z',
    'MdAimanz'
]

tweetsExtractor(usernames_list)