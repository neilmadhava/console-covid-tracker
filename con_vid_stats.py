import requests
from bs4 import BeautifulSoup
import argparse
import sys
from termcolor import colored, cprint

def get_arguments(parser):
    # parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dashboard", choices=["india", "world"], help="Show quick overview of stats")
    parser.add_argument("-s", "--state", help="Show detail for given Indian state")
    parser.add_argument("-c", "--colored", action="store_true", help="Print colored output")
    options = parser.parse_args()
    return options


def dashboard_india(color):
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
    text = '''
         -----------------
        |    DASHBOARD    |
         -----------------
    '''
    if(not color):
        # printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
        print(text)
        print(f"Total Confirmed: {int(active) + int(cured) + int(migrated) + int(deaths)}")
        print(f"Total Deceased:\t {deaths}")
        print(f"Total Active:\t {active}")
        print(f"Total Recovered: {cured}")
        print(f"Migrated:\t {migrated}")
        print(f"Last updated:\t {updated}\n")
    else:
        print_yellow = lambda x: cprint(x, 'yellow', end=" ")
        printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
        printBoldBlink = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
        printBold(text, "white")
        print_yellow(f"Total Confirmed:") 
        printBoldBlink(f"{int(active) + int(cured) + int(migrated) + int(deaths)}", "magenta")
        
        print_yellow(f"Total Deceased:\t") 
        printBold(f"{deaths}", "red")
        
        print_yellow(f"Total Active:\t") 
        printBold(f"{active}", "yellow")
        
        print_yellow(f"Total Recovered:") 
        printBold(f"{cured}", "green")
        
        print_yellow(f"Migrated:\t") 
        printBold(f"{migrated}", "cyan")
        
        print_yellow(f"Last updated:\t") 
        printBold(f"{updated}\n", "white")


def dashboard_world(color):
    stats = soup.find_all('div', class_='container--wrap')[1].find_all("p")
    text = '''
         -----------------
        |    DASHBOARD    |
         -----------------
    '''
    if(not color):
        print(text)
        print(f"Total Confirmed: {stats[2].get_text().strip()}")
        print(f"Total Critical:\t {stats[4].get_text().strip()}")
        print(f"Total Deceased:\t {stats[6].get_text().strip()}")
        print(f"Total Active:\t {stats[8].get_text().strip()}")
        print(f"Total Recovered: {stats[10].get_text().strip()}")
    else:
        print_yellow = lambda x: cprint(x, 'yellow', end=" ")
        printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
        printBoldBlink = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
        printBold(text, "white")

        print_yellow(f"Total Confirmed:")
        printBoldBlink(f"{stats[2].get_text().strip()}", "magenta")

        print_yellow(f"Total Critical:\t")
        printBold(f"{stats[4].get_text().strip()}", "cyan")

        print_yellow(f"Total Deceased:\t")
        printBold(f"{stats[6].get_text().strip()}", "red")

        print_yellow(f"Total Active:\t")
        printBold(f"{stats[8].get_text().strip()}", "yellow")

        print_yellow(f"Total Recovered:")
        printBold(f"{stats[10].get_text().strip()}\n", "green")


def state_details(search_state, color):
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
            if(color):
                print_yellow = lambda x: cprint(x, 'yellow', end=" ")
                printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
                printBoldBlink = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
                
                print_yellow('\nState:\t')
                printBoldBlink(state['state'], "yellow")

                print_yellow('Total:\t')
                printBold(state['total_confirmed'], "magenta")
        
                print_yellow('Cured:\t')
                printBold(state['cured'], "green")
        
                print_yellow('Deaths:\t')
                printBold(f"{state['deaths']}\n", "red")
            else:
                print('\nState:\t' + state['state'])
                print('Total:\t' + state['total_confirmed'])
                print('Cured:\t' + state['cured'])
                print('Deaths:\t' + state['deaths'] + "\n")
            break

parser = argparse.ArgumentParser()
args = get_arguments(parser)

if (args.dashboard == "india"):
    response = requests.get("https://www.mygov.in/corona-data/covid19-statewise-status")
    soup = BeautifulSoup(response.text, "html.parser")
    dashboard_india(args.colored)
elif (args.dashboard == "world"):
    response = requests.get("https://ncov2019.live/")
    soup = BeautifulSoup(response.text, "html.parser")
    dashboard_world(args.colored)

if (args.state):
    response = requests.get("https://www.mygov.in/corona-data/covid19-statewise-status")
    soup = BeautifulSoup(response.text, "html.parser")
    state_details(args.state, args.colored)

if(len(sys.argv)<2):
    parser.print_help()