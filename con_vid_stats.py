import requests
from bs4 import BeautifulSoup
import argparse
import sys
from termcolor import colored, cprint

def get_arguments(parser):
    # parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dashboard", choices=["india", "world"], help="Show quick overview of stats")
    parser.add_argument("-s", "--state", help="Show detail for given Indian state")
    parser.add_argument("-dis", "--district", help="Show detail for given district")
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
    newcases = soup.find(id="newcases").find(class_="card-title").get_text()
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
        print(f"\tNew cases today: {newcases}\n")
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
        
        print_yellow(f"New cases today:") 
        printBold(f"{newcases}\n", "cyan")

def states(search_state, color, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find(id="table_id").find_all("tr")[1:]
    for row in table:
        new_state = {}
        
        # State Name
        new_state['state'] = row.find_all("td")[0].get_text()
        if(search_state.lower() not in new_state['state'].lower()):
            continue
        
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
        if(search_state.lower() in new_state['state'].lower()):
            if(color):
                print_yellow = lambda x: cprint(x, 'yellow', end=" ")
                printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
                printBoldUnderline = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
                
                printBoldUnderline(f"\n\t{new_state['state']}\n", "white")

                print_yellow('\tTotal cases:\t')
                printBold(new_state['total'], "blue")

                print_yellow('\tTotal deaths:\t')
                printBold(new_state['deaths'], "red")

                print_yellow('\tTotal active:\t')
                printBold(new_state['active'], "yellow")

                print_yellow('\tTotal cured:\t')
                printBold(new_state['recovered'], "green")

                print_yellow('\tCured percent:\t')
                printBold(new_state['rec_perc'], "green")

                print_yellow('\tDeath percent:\t')
                printBold(new_state['death_perc'], "red")

                print_yellow('\tCase percent:\t')
                printBold(new_state['case_perc'] + "\n", "blue")
            else:
                print(f"\n\tState:\t\t {new_state['state']}")
                print(f"\tTotal cases:\t {new_state['total']}")
                print(f"\tTotal active:\t {new_state['active']}")
                print(f"\tTotal deaths:\t {new_state['deaths']}")
                print(f"\tTotal cured:\t {new_state['recovered']}")
                print(f"\tCured percent:\t {new_state['rec_perc']}")
                print(f"\tDeath percent:\t {new_state['death_perc']}")
                print(f"\tCase percent:\t {new_state['case_perc']}\n")
            return
    print("[-] No matching state found! Try a different state.")

def district_details(color, url, district_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    districts_list = soup.find(id="district_table").find_all("tbody")
    for districts in districts_list:
        district = districts.find_all("tr")
        for element in district:
            d_name = element.find(id="district_name").get_text()
            if (district_name.lower() not in d_name.lower()):
                continue
            cases = element.find(class_="text-right")
            if(cases.find(id="up_newcases") == None):
                new_case = 0
                curr_case = element.find_all("span")[-1].get_text()
            else:
                new_case = cases.find(id="up_newcases").get_text().strip()
                curr_case = element.find_all("span")[-1].get_text()
            
            if(color):
                print_yellow = lambda x: cprint(x, 'yellow', end=" ")
                printBold = lambda x, color: print(colored(x, color, attrs=['bold']))
                printBoldUnderline = lambda x, color: print(colored(x, color, attrs=['bold', 'underline']))
                
                printBoldUnderline(f"\n\t{d_name}\n", "white")

                print_yellow('Cases:\t')
                printBold(f"[+{new_case}] {curr_case}\n", "red")
            else:
                print(f"\nDistrict:\t {d_name}")
                print(f"Cases:\t\t [+{new_case}] {curr_case}\n")

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
    states(args.state, args.colored, url)
elif (args.district):
    url = "https://tcovid19.herokuapp.com/"
    district_details(args.colored, url, args.district)

if(len(sys.argv)<2):
    parser.print_help()

# print(args.dashboard)