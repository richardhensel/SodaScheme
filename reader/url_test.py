
import requests
import os

def get_registered_cards():
    query_string = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":8080/getregisteredcards"
    response = requests.get(query_string)
    if response.status_code == 200:
        cards = str (response.text)
        cards = cards.replace("[", "").replace("]", "").replace('\n', "").replace('"', "").replace(" ", "").split(",")
    return cards

def log_card_touch(card_hash):
    card_data = {"data" : card_hash}
    queryString = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":8080/logcardtouch"
    response = requests.put(queryString, data=card_data)
    print response.text


print get_registered_cards()

log_card_touch("t4gR6XhiGEwgCgYxn0HN5RCWUCIvYoKtCWxxH9AhIU8ndq0YehM7/P3oYHbK3dNJPJ3b9i2ig8YfTzUcqioxo1")        

