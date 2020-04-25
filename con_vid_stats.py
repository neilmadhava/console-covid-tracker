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

def dash_world(color, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    stats = soup.find_all('div', class_='container--wrap')[1].find_all("p")
    text = '''
         -----------------------
        |    WORLD DASHBOARD    |
         -----------------------
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
        printBoldBlink(f"{stats[2].get_text().strip()}", "red")

        print_yellow(f"Total Critical:\t")
        printBold(f"{stats[4].get_text().strip()}", "cyan")

        print_yellow(f"Total Deceased:\t")
        printBold(f"{stats[6].get_text().strip()}", "blue")

        print_yellow(f"Total Active:\t")
        printBold(f"{stats[8].get_text().strip()}", "yellow")

        print_yellow(f"Total Recovered:")
        printBold(f"{stats[10].get_text().strip()}\n", "green")

def dash_india(color, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    total = soup.find(id="total_counter").get_text()
    active = soup.find(id="activecases").find(class_="card-title").get_text()
    recovered = soup.find(id="recoveredcases").find(class_="card-title").get_text().replace("\n", "").replace("\t", "").replace("[", " [")
    deaths = soup.find(id="deaths").find(class_="card-title").get_text().replace("\n", "").replace("\t", "").replace("[", " [")
    text = '''
         -----------------------
        |    INDIA DASHBOARD    |
         -----------------------
    '''
    if (not color):
        print(text)
        print(f"\tTotal Confirmed: {total}")
        print(f"\tTotal Deceased:\t {deaths}")
        print(f"\tTotal Active:\t {active}")
        print(f"\tTotal Recovered: {recovered}")
    else:
        print_yellow = lambda x: cprint(x, 'yellow', end=" ")
        printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
        printBoldUnderline = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
        printBold(text, "white")
        print_yellow(f"Total Confirmed:") 
        printBoldUnderline(f"{total}", "red")
        
        print_yellow(f"Total Deceased:\t") 
        printBold(f"{deaths}", "blue")
        
        print_yellow(f"Total Active:\t") 
        printBold(f"{active}", "yellow")
        
        print_yellow(f"Total Recovered:") 
        printBold(f"{recovered}", "green")
        
        # print_yellow(f"Last updated:\t") 
        # printBold(f"{updated}\n", "white")

def state_details(search_state, color, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find(id="table_id").find_all("tr")[1:]
    states = []
    for row in table:
        new_state = {}
        
        # State Name
        new_state['state'] = row.find_all("td")[0].get_text()
        
        # total cases
        total = row.find_all("td")[1].get_text().strip().split("\n")
        if len(total) > 1 :
            inc = total[0]
            curr = total[2]
        else:
            inc = 0
            curr = total[0]
        new_state['total'] = f"[+{inc}] {curr}"
        
        # active cases
        new_state['active'] = row.find_all("td")[2].get_text()
        
        # recovered cases
        recovered = row.find_all("td")[3].get_text().strip().split("\n")
        if len(recovered) > 1 :
            inc = recovered[0]
            curr = recovered[2]
        else:
            inc = 0
            curr = recovered[0]
        new_state['recovered'] = f"[+{inc}] {curr}"
        
        # total deaths
        deaths = row.find_all("td")[4].get_text().strip().split("\n")
        if len(deaths) > 1 :
            inc = deaths[0]
            curr = deaths[2]
        else:
            inc = 0
            curr = deaths[0]
        new_state['deaths'] = f"[+{inc}] {curr}"

        new_state['rec_perc'] = row.find_all("td")[5].get_text()
        new_state['death_perc'] = row.find_all("td")[6].get_text()
        new_state['case_perc'] = row.find_all("td")[7].get_text()
        states.append(new_state)
    
    for state in states:
        if (search_state.lower() in state['state'].lower()):
            if(color):
                print_yellow = lambda x: cprint(x, 'yellow', end=" ")
                printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
                printBoldUnderline = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
                
                printBoldUnderline(f"\n\t{state['state']}\n", "white")

                print_yellow('Total cases:\t')
                printBold(state['total'], "blue")

                print_yellow('Total deaths:\t')
                printBold(state['deaths'], "red")

                print_yellow('Total active:\t')
                printBold(state['active'], "yellow")

                print_yellow('Total cured:\t')
                printBold(state['recovered'], "green")

                print_yellow('Cured percent:\t')
                printBold(state['rec_perc'], "green")

                print_yellow('Death percent:\t')
                printBold(state['death_perc'], "red")

                print_yellow('Case percent:\t')
                printBold(state['case_perc'] + "\n", "blue")
            else:
                print(f"\nState:\t\t {state['state']}")
                print(f"Total cases:\t {state['total']}")
                print(f"Total active:\t {state['active']}")
                print(f"Total deaths:\t {state['deaths']}")
                print(f"Total cured:\t {state['recovered']}")
                print(f"Cured percent:\t {state['rec_perc']}")
                print(f"Death percent:\t {state['death_perc']}")
                print(f"Case percent:\t {state['case_perc']}\n")
            break

parser = argparse.ArgumentParser()
args = get_arguments(parser)

if (args.dashboard == "india"):
    url = "https://tcovid19.herokuapp.com/"
    dash_india(args.colored, url)
elif (args.dashboard == "world"):
    url = "https://ncov2019.live/"
    dash_world(args.colored, url)

if (args.state):
    url = "https://tcovid19.herokuapp.com/"
    state_details(args.state, args.colored, url)

if(len(sys.argv)<2):
    parser.print_help()