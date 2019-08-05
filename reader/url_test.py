
import requests
import os

def get_registered_cards():
    query_string = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":" + os.environ["SCHEME_SERVER_API_PORT"] + "/getregisteredcards"
    response = requests.get(query_string)
    cards = ""
    if response.status_code == 200:
        cards = str (response.text)
        cards = cards.replace("[", "").replace("]", "").replace('\n', "").replace('"', "").replace(" ", "").split(",")
    return cards

def log_card_touch(card_hash):
    card_data = {"data" : card_hash}
    queryString = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":" + os.environ["SCHEME_SERVER_API_PORT"] + "/logcardtouch"
    response = requests.put(queryString, data=card_data)
    print response.text


print get_registered_cards()

log_card_touch("E.u2CiZrZ137BI.RTR8jsApZCHWYhVcTfhmJ9SOZFidDDMUb6DuRK8beKByrP7mmzXvIpvCvmy3YOFwD66Mny.")  
log_card_touch("t4gR6XhiGEwgCgYxn0HN5RCWUCIvYoKtCWxxH9AhIU8ndq0YehM7/P3oYHbK3dNJPJ3b9i2ig8YfTzUcqioxo1")
log_card_touch("yTK/bUXq4Op638C8yvEaUQr4MYjSov7Sy52DUscptaN77yPNYdh4rE1.Gk7gRrs4Ow7ZXW.bkl56fki6tR9V21")
log_card_touch("rxin6MDrBt5MffsXhyLhtkI1EUXCajWIHXw6wqTt65VJrQy2nCniBlRkW37YXHXdadhM/PCSZ9defHBAkUNBg0")

