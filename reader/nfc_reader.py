#! /usr/bin/python

import subprocess

from gpiozero import LED
from time import sleep
import datetime
import crypt
import requests
import os

# list of registered cards
registered_cards = []

# gpio pins for leds
buzzer = LED(15)
ready_light = LED(18) # green
touch_light = LED(17) # blue

# log output direction
log_to_file = True
log_to_screen = True

def run():
    alert_startup()
    registered_cards = get_registered_cards()
    while True:
        process = subprocess.Popen(['/usr/bin/stdbuf', '-o0', '/usr/bin/nfc-poll'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = process.stdout.readline()
            if not output == '':
                if 'NFC device will poll' in output:
                    print_stamped('NFC reader ready.')
                    display_ready()

                elif 'UID' in output:
                    card_id = output.split(':')[1].replace('\n', '').replace(' ', '')
                    id_hash = get_hash(card_id)
                    double_hash = get_hash(id_hash)
                    print_stamped("double hash: " + double_hash)

                    # registered cards is a double hash
                    if double_hash in registered_cards:
                        display_card_detected()
                        print_stamped('Registered card logged: ' + id_hash)
                        log_card_touch(id_hash)
                    else:
                        display_card_not_recognised()
                        print_stamped('Unregistered card logged: ' + id_hash)
                    break

                elif 'error   libnfc.bus.i2c  Error: wrote only -1 bytes (10 expected).' in output:
                    print_stamped( output)
                    display_error()
                    break

                elif 'error' in output:
                    print_stamped(output)
                    display_error()

                #else:
                    #do nothing
                    
            else:
                print_stamped('NFC reader restarting.')
                display_not_ready()
                break
    
def get_registered_cards():
    query_string = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":8080/getregisteredcards"
    print_stamped(query_string)
    response = requests.get(query_string)
    cards = []
    if response.status_code == 200:
        cards = str(response.text)
        cards = cards.replace("[", "").replace("]", "").replace('\n', "").replace('"', "").replace(" ", "").split(",")
        print_stamped(cards)
    return cards

def log_card_touch(card_hash):
    card_data = {"data" : card_hash}
    query_string = "http://" + os.environ["SCHEME_SERVER_HOST"] + ":8080/logcardtouch"
    response = requests.put(query_string, data=card_data)
    print_stamped(response.text)

def print_stamped(message):
    log_message ="[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + str(message)
    if log_to_screen == True:
        print log_message
    if log_to_file == True:
        f= open("/home/pi/nfc_reader_log.txt","a+")
        f.write(log_message + '\n')
        f.close()

def get_hash(raw_id):
    return str(crypt.crypt(raw_id, "$6$").replace("$6$$","").replace(" ",""))


def display_ready():
    ready_light.on()
    touch_light.off()

def display_not_ready():
    ready_light.off()
    touch_light.off()
    buzzer.off()

def display_error():
    ready_light.on()
    touch_light.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    buzzer.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    buzzer.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.off()
    touch_light.off()
    buzzer.off()

def display_error():
    ready_light.on()
    touch_light.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    sleep(0.2)
    ready_light.off()
    touch_light.off()

def display_card_not_recognised():
    ready_light.on()
    touch_light.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    buzzer.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.on()
    touch_light.off()
    buzzer.off()
    sleep(0.2)
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.2)
    ready_light.off()
    touch_light.off()
    buzzer.off()

def display_card_detected():
    ready_light.off()
    touch_light.on()
    buzzer.on()
    sleep(0.1)
    touch_light.off()
    sleep(0.1)
    touch_light.on()
    sleep(0.1)
    touch_light.off()
    sleep(0.1)
    touch_light.on()
    sleep(0.1)
    touch_light.off()
    sleep(0.1)
    touch_light.on()
    buzzer.off()

def alert_startup():
    buzzer.on()
    sleep(0.2)
    buzzer.off()



if __name__ == "__main__":
    run()

