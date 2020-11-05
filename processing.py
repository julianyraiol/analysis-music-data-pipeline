import requests
import pandas as pd

def create_csv():
    csv_list = []
    cont = 1

    with open('data/data4.txt', 'r') as filehandle:
        for line in filehandle:
            try:
                spotify_url = requests.get(line).url

                print(cont, " ", spotify_url)

                if "https://open.spotify.com/track/" in spotify_url:
                    type_link = "track"
                
                elif "https://open.spotify.com/album/" in spotify_url:
                    type_link = "album"
                
                elif "https://open.spotify.com/playlist/" in spotify_url:
                    type_link = "playlist"
                
                elif "https://open.spotify.com/artist/" in spotify_url:
                    type_link = "artist"
                else:
                    type_link = "other"

                csv_list.append({"SINCE_DATE": "MARCH", "UNITIL_DATE": "MARCH", "SPOTIFY_URL": spotify_url, "TYPE_URL": type_link})
                cont+=1
            except:
                continue
           

    df = pd.DataFrame(csv_list)
    df.to_csv("data/data_4" + ".csv", index=False)


if __name__ == "__main__":
    create_csv()
