import requests
import random
import time

def bot_defence():
    global result1
    while True:
        while True:
            response = requests.post('http://127.0.0.1:5000/can_defend', data={}).json()['otvet']
            if response == 'True' or response == 'End' or response == 'Win':
                break

        if response == 'End':

            result1 = 'Поражение'
            return 'lose'
            break
        if response == 'Win':

            result1 = 'Победа'
            return 'win'
            break

        response = requests.post('http://127.0.0.1:5000/centrality_info', data={}).json()['otvet']

        response = dict(sorted(response.items(), key=lambda item: item[1]))
        response = list(response)
        response = response[1:4]
        for i in range(len(response)):
            response[i] = int(response[i])

        response = requests.post('http://127.0.0.1:5000/add/' + str(response), data={}).json()['otvet']

        response = requests.post('http://127.0.0.1:5000/next_turn', data={}).json()['otvet']