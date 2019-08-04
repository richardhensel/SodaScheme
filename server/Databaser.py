import sqlite3


#Storage class for Card information before databasing.
class Card:
    def __init__(self):
        self.user_id    = ""
        self.card_hash          = ""


#Storage class for RP information before databasing.
class User:
    def __init__(self):
        self.user_id    = ""
        self.first_name          = ""
        self.last_name          = ""
        self.email          = ""
        self.phone_number          = ""

class Current_Balance:
    def __init__(self):
        self.user_id    = ""
        self.current_balance          = ""

#Storage class for Description information before databasing.
class Transaction:
    def __init__(self):
        self.user_id              = ""
        self.transaction_id       = ""
        self.time_unix         = ""
        self.transaction_type          = "" #purchase or repayment
        self.transaction_item          = ""
        self.transaction_value         = "" # dollars (-ve for purchase, +ve for repayment)
        self.method                    = "" # card_touch, manual repayment, automatic repayment
        self.current_balance             = "" # dollars (-ve for debit, +ve for credit)


class Databaser:
    def __init__(self, path):
        self.path = path


        # try:
        self.create_tables() 
        # except:
            # print 'error creating tables, maybe already exists...'

    def create_tables(self):

        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        # Create Card table.
        s  = 'CREATE TABLE IF NOT EXISTS Cards ('
        s += 'user_id            text,'
        s += 'card_hash          text'
        s += ')'
        cursor.execute(s)

        # Create User table.
        s  = 'CREATE TABLE IF NOT EXISTS Users ('
        s += 'user_id    text,'
        s += 'first_name          text,'
        s += 'last_name           text,'
        s += 'email               text,'
        s += 'phone_number        text'
        s += ')'
        cursor.execute(s)

        # Create Current_Balance table.
        s  = 'CREATE TABLE IF NOT EXISTS Current_Balances ('
        s += 'user_id             text,'
        s += 'current_balance     text'
        s += ')'
        cursor.execute(s)

        # Create Current_Balance table
        s  = 'CREATE TABLE IF NOT EXISTS Transacts ('
        s += 'user_id             text,'
        s += 'transaction_id      text,'
        s += 'time_unix           text,'
        s += 'transaction_type    text,'
        s += 'transaction_item    text,'
        s += 'transaction_value   text,'
        s += 'method              text,'
        s += 'current_balance     text'
        s += ')'
        cursor.execute(s)

        connection.close()


    def create_user_with_card(self, card_hash, first_name, last_name, email, phone_number, starting_balance):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        ## check that the user doesn't already exist. if so, exit
        query = "SELECT email from Users;"
        cursor.execute(query)
        query_result = cursor.fetchall()
        #get id list, converted to numbers
        for row in query_result:
            if email == str(row[0]):
                return "0. User with email {} already in database.".format(email)

        ## check that the user doesn't already exist. if so, exit
        query = "SELECT card_hash from Cards;"
        cursor.execute(query)
        query_result = cursor.fetchall()
        #get id list, converted to numbers
        for row in query_result:
            if card_hash == str(row[0]):
                return "0. User with card_hash {} already in database.".format(card_hash)
 
        connection.commit()
        connection.close()            

        ## create unique user_id for the user.
        user_id, status = self.create_user_id()
        if "0. " in status:
            return status

        # create the entry in cards table
        card = Card()
        card.user_id = user_id
        card.card_hash = card_hash
        self.add_card(card)

        # create the entry in Users table
        user = User()
        user.user_id = user_id
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        self.add_user(user)

        # add starting balance to transactions (if necessary)
        # if starting_balance is not "0":
        #     transaction = Transaction
        #     transaction.user_id = user_id
        #     transaction.transaction_id

        # initialise the balance in the Balance table to zero.

        current_balance = Current_Balance()
        current_balance.user_id = user_id
        current_balance.current_balance = starting_balance

        self.update_current_balance(current_balance)

        return "1. Successfully added user with email: {}, assigned user_id: {}".format(email, user_id)


    def add_purchase(self, card_hash, time_unix, item, price):

        user_id, status = self.get_user_id_from_card_hash(card_hash)
        if "0. " in status:
            return status

        # create unique transaction id.
        transaction_id, status = self.create_transaction_id()
        if "0. " in status:
            return status

        # calculate the current balance
        previous_balance, status = self.get_current_balance(user_id)
        if "0. " in status:
            return status

        # create transaction objct and add
        transaction = Transaction()
        transaction.user_id = user_id
        transaction.transaction_id = transaction_id
        transaction.transaction_item = item
        transaction.transaction_type = "purchase"
        transaction.method = "card touch"
        transaction.transaction_value = str(-1 * abs(float(price)))
        transaction.time_unix = time_unix
        transaction.current_balance = str(previous_balance + (-1 * abs(float(price))))
        self.add_transaction(transaction)

        # udpate the current balance by doing some math. 
        current_balance = Current_Balance
        current_balance.user_id = user_id
        current_balance.current_balance = transaction.current_balance
        self.update_current_balance(current_balance)

        return "1. purchase successfully registered. Current balance: {}".format(transaction.current_balance)



    def add_payment(self, email, time_unix, payment_amount):

        user_id, status = self.get_user_id_from_email(email)

        if "0. " in status:
            return status

        # create unique transaction id.
        transaction_id, status = self.create_transaction_id()
        if "0. " in status:
            return status

        # calculate the current balance
        previous_balance, status = self.get_current_balance(user_id)
        if "0. " in status:
            return status

        # create transaction objct and add
        transaction = Transaction()
        transaction.user_id = user_id
        transaction.transaction_id = transaction_id
        # transaction.transaction_item = "payment"
        transaction.transaction_type = "payment"
        transaction.transaction_value = str(abs(float(payment_amount)))
        transaction.time_unix = time_unix
        transaction.current_balance = str(previous_balance + (abs(float(payment_amount))))
        self.add_transaction(transaction)

        # udpate the current balance by doing some math. 
        current_balance = Current_Balance
        current_balance.user_id = user_id
        current_balance.current_balance = transaction.current_balance
        self.update_current_balance(current_balance)

        return "1. payment successfully registered. Current balance: {}".format(transaction.current_balance)


    def get_balance_for_user(self, email):

        user_id, status = self.get_user_id_from_email(email)
        current_balance, status = self.get_current_balance(user_id)

        if "0. " in status:
            return 0, status
        else:
            return current_balance, "1. successfully retrieved balance for email {}".format(email)

    def get_user_id_from_email(self, email):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        #get user id for email
        query = "SELECT user_id, email FROM Users;"
        cursor.execute(query)
        query_result = cursor.fetchall()

        id_list = []
        email_list = []
        for row in query_result:
            id_list.append(str(row[0]))
            email_list.append(str(row[1]))

        user_id = ""
        status = ""
        if len(email_list) == 0:
            status = "0. No emails in database."

        elif email not in email_list:
            status = "0. No database entry for email {}".format(email)
        else:
            user_id = id_list[email_list.index(email)]
            status = "1. Successfully retrieved user_id."

        connection.commit()
        connection.close()

        return user_id, status

    def get_user_id_from_card_hash(self, card_hash):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        # get user_id assigned to this hash
        query = "SELECT * FROM Cards;"
        cursor.execute(query)
        query_result = cursor.fetchall()

        id_list = []
        hash_list = []
        for row in query_result:
            id_list.append(str(row[0]))
            hash_list.append(str(row[1]))

        user_id = ""
        status = ""
        if len(hash_list) == 0:
            status = "0. No card hashes in database."

        elif card_hash not in hash_list:
            status = "0. No database entry for card hash {}".format(card_hash)

        else:
            user_id = id_list[hash_list.index(card_hash)]
            status = "1. Successfully retrieved user_id."
            
        connection.commit()
        connection.close()

        return user_id, status

    def create_user_id():
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        query = "SELECT user_id FROM Users;"
        cursor.execute(query)
        query_result = cursor.fetchall()
        id_list = []
        #get id list, converted to numbers
        for row in query_result:
            id_list.append(int(str(row[0])))

        #if empty, id = str(1)
        user_id = "1"
        #if not empty, id = str(max(list) +1)
        if len(id_list) is not 0:
            user_id = str(max(id_list)+1)

        connection.commit()
        connection.close()

        return user_id, "1. success generating user id"

    def create_transaction_id(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        query = "SELECT transaction_id FROM Transacts;"
        cursor.execute(query)
        query_result = cursor.fetchall()
        id_list = []
        #get id list, converted to numbers
        for row in query_result:
            id_list.append(int(str(row[0])))

        #if empty, id = str(1)
        transaction_id = "1"
        #if not empty, id = str(max(list) +1)
        if len(id_list) is not 0:
            transaction_id = str(max(id_list)+1)

        connection.commit()
        connection.close()

        return transaction_id, "1. success generating transaction id"

    def get_current_balance(self, user_id):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        query = "SELECT user_id, transaction_value FROM Transacts;"
        cursor.execute(query)
        query_result = cursor.fetchall()
        value_list = []
        for row in query_result:
            if user_id == str(row[0]):
                value_list.append(float(str(row[1])))

        current_balance = 0
        status = ""
        if len(value_list) == 0:
            status = "0. No transactions registered to this user."
        else:
            current_balance = sum(value_list)
            status = "1.successfully retrieved current balance."

        connection.commit()
        connection.close()

        return current_balance, status


    def add_user(self, data):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        # TODO check if this user id already exists. 
        if data.user_id != '':
            s  = 'INSERT INTO Users VALUES(' 
            s += '"' + data.user_id             + '"' + ','
            s += '"' + data.first_name      + '"' + ','
            s += '"' + data.last_name           + '"' + ','
            s += '"' + data.email    + '"' + ','
            s += '"' + data.phone_number    + '"'
            s += ')'
            cursor.execute(s)
        connection.commit()
        connection.close()

    def add_card(self, data):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        # TODO check if this user id already exists. 
        if data.user_id != '':
            s  = 'INSERT INTO Cards VALUES(' 
            s += '"' + data.user_id             + '"' + ','
            s += '"' + data.card_hash      + '"'
            s += ')'
            cursor.execute(s)
        connection.commit()
        connection.close()      


    def update_current_balance(self, data):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        # TODO replace instaed of add. 
        if data.user_id != '':
            s  = 'INSERT INTO Current_Balances VALUES(' 
            s += '"' + data.user_id             + '"' + ','
            s += '"' + data.current_balance      + '"'
            s += ')'
            cursor.execute(s)
        connection.commit()
        connection.close()

    def add_transaction(self, data):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        if data.user_id != '':
            s  = 'INSERT INTO Transacts VALUES(' 
            s += '"' + data.user_id             + '"' + ','
            s += '"' + data.transaction_id      + '"' + ','
            s += '"' + data.time_unix           + '"' + ','
            s += '"' + data.transaction_type    + '"' + ','
            s += '"' + data.transaction_item    + '"' + ','
            s += '"' + data.transaction_value   + '"' + ','
            s += '"' + data.method              + '"' + ','
            s += '"' + data.current_balance     + '"'
            s += ')'
            cursor.execute(s)
        connection.commit()
        connection.close()

if __name__ == "__main__":

    import time
    db = Databaser("./test_db.db")

    time_stamp = str(int(time.time()))  


    return_val = db.create_user_with_card("1234", "steve", "jones", "lol6@webz.com", "1234", "0")
    print return_val

    return_val = db.add_purchase("1234", time_stamp, "coke", "1.20")
    print return_val

    return_val = db.add_purchase("1234", time_stamp, "coke", "1.20")
    print return_val

    return_val = db.add_payment("lol6@webz.com", time_stamp, "2.5")
    print return_val

    return_val, status = db.get_balance_for_user("lol6@webz.com")
    print "balance: " + str(return_val) + " " + status
    
