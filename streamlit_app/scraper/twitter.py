import twint
import nest_asyncio
import pandas as pd

# nest_asyncio.apply()

# print("Download Conte's followers? y/n")
# val = str(input())


def config(username="GiuseppeConteIT", store=True, output="./data/conte_followers.csv"):
    """
    Configure Twint settings for scraping
    """
    c = twint.Config()
    c.Username = username
    c.Store_csv = store
    c.Output = output

    print(f"Configuration set: {c}")

    return c


def download(config, output_path, level=1):
    """
    Download new tweets using configuration
    """
    if level == 1:
        print("Downloading level 1")
        try:
            twint.run.Followers(config)
            return True
        except Exception as message:
            print(f"Impossibile download new tweets: {message} ")
            return False
    elif level == 2:
        print(f"Downloading level 2")
        conte_df = pd.read_csv(output_path).iloc[1950:2000]
        error_list = []
        c = twint.Config()
        for user in conte_df["username"]:
            try:
                c.Username = user
                c.Store_csv = True
                c.Output = "./conte_followers/" + user + "_followers.csv"
                twint.run.Followers(c)
                print(f"{user} downloaded")
                return True
            except Exception as message:
                print(f"Error downloading: {user}, {message}")
                error_list.append(user)
                return False
    else:
        print(f"Please specify a graph level: 1 or 2 in the function")
        return False
