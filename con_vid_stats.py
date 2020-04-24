import requests
from bs4 import BeautifulSoup
import argparse
import sys
# from termcolor import colored

def get_arguments(parser):
    # parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dashboard", choices=["india", "world"], help="Show quick overview of stats")
    parser.add_argument("-s", "--state", help="Show detail for given Indian state")
    options = parser.parse_args()
    return options

def dashboard_india():
    active = soup.find(
        'div', class_='field-name-field-total-active-case').find(
            'div', class_='field-item even').get_text()

    cured = soup.find(
        'div', class_='field-name-field-total-cured-discharged').find(
            'div', class_='field-item even').get_text()

    migrated = soup.find(
        'div', class_='field-name-field-migrated-counts').find(
            'div', class_='field-item even').get_text()

    deaths = soup.find(
        'div', class_='field-name-field-total-death-case').find(
            'div', class_='field-item even').get_text()

    updated = soup.find(
        'div', class_='field-name-field-covid-india-as-on').find(
            'div', class_='field-item even').get_text()
     
    print(f"Total Confirmed: {int(active) + int(cured) + int(migrated) + int(deaths)}")
    print(f"Total Deceased:\t {deaths}")
    print(f"Total Active:\t {active}")
    print(f"Total Recovered: {cured}")
    print(f"Migrated:\t {migrated}")
    print(f"Last updated:\t {updated}")
    

def dashboard_world():
    stats = soup.find_all('div', class_='container--wrap')[1].find_all("p")
    # print(stats)
    print(f"Total Confirmed: {stats[2].get_text().strip()}")
    print(f"Total Critical:\t {stats[4].get_text().strip()}")
    print(f"Total Deceased:\t {stats[6].get_text().strip()}")
    print(f"Total Active:\t {stats[8].get_text().strip()}")
    print(f"Total Recovered: {stats[10].get_text().strip()}")




def state_details(search_state):
    table = soup.find('div', class_='field-name-field-covid-statewise-data').find_all('div', class_='content')
    states = []
    for row in table:
        fields = row.find_all('div', class_='field-items')
        new_state = {}
        new_state['state'] = fields[0].get_text()
        new_state['total_confirmed'] = fields[1].get_text()
        new_state['cured'] = fields[2].get_text()
        new_state['deaths'] = fields[3].get_text()
        states.append(new_state)

    for state in states:
        if (search_state.lower() in state['state'].lower()):
            print('State:\t' + state['state'])
            print('Total:\t' + state['total_confirmed'])
            print('Cured:\t' + state['cured'])
            print('Deaths:\t' + state['deaths'])
            break

parser = argparse.ArgumentParser()
args = get_arguments(parser)

if (args.dashboard == "india"):
    response = requests.get("https://www.mygov.in/corona-data/covid19-statewise-status")
    soup = BeautifulSoup(response.text, "html.parser")
    dashboard_india()
elif (args.dashboard == "world"):
    response = requests.get("https://ncov2019.live/")
    soup = BeautifulSoup(response.text, "html.parser")
    dashboard_world()

if (args.state):
    response = requests.get("https://www.mygov.in/corona-data/covid19-statewise-status")
    soup = BeautifulSoup(response.text, "html.parser")
    state_details(args.state)

if(len(sys.argv)<2):
    parser.print_help()