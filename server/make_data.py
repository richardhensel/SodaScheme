#data = {}
#data["E.u2CiZrZ137BI.RTR8jsApZCHWYhVcTfhmJ9SOZFidDDMUb6DuRK8beKByrP7mmzXvIpvCvmy3YOFwD66Mny."] = {"Name": "hans", "Mobile": "1234", "Num_Purchases": 0}
#data["t4gR6XhiGEwgCgYxn0HN5RCWUCIvYoKtCWxxH9AhIU8ndq0YehM7/P3oYHbK3dNJPJ3b9i2ig8YfTzUcqioxo1"] = {"Name": "smiff", "Mobile": "1234", "Num_Purchases": 0}
#data["yTK/bUXq4Op638C8yvEaUQr4MYjSov7Sy52DUscptaN77yPNYdh4rE1.Gk7gRrs4Ow7ZXW.bkl56fki6tR9V21"] = {"Name": "wozzy", "Mobile": "1234", "Num_Purchases": 0}
#data["rxin6MDrBt5MffsXhyLhtkI1EUXCajWIHXw6wqTt65VJrQy2nCniBlRkW37YXHXdadhM/PCSZ9defHBAkUNBg0"] = {"Name": "dontmess", "Mobile": "1234", "Num_Purchases": 0}

from __init__ import Databaser 
import os
import time
# db = Databaser(os.environ["SCHEME_SERVER_DB_PATH"])
db = Databaser("/var/www/Flask/Scheme/data/database.db")

time_stamp = str(int(time.time()))  


return_val = db.add_user("t4gR6XhiGEwgCgYxn0HN5RCWUCIvYoKtCWxxH9AhIU8ndq0YehM7/P3oYHbK3dNJPJ3b9i2ig8YfTzUcqioxo1", "smiffy", "Smifff", "lon", "1234", "0")
print return_val
return_val = db.add_user("yTK/bUXq4Op638C8yvEaUQr4MYjSov7Sy52DUscptaN77yPNYdh4rE1.Gk7gRrs4Ow7ZXW.bkl56fki6tR9V21", "rozzy", "woz", "nof", "1234", "0")
print return_val
return_val = db.add_user("rxin6MDrBt5MffsXhyLhtkI1EUXCajWIHXw6wqTt65VJrQy2nCniBlRkW37YXHXdadhM/PCSZ9defHBAkUNBg0", "dont", "mess", "nte", "1234", "0")
print return_val
