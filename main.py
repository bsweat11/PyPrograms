

from scapy.all import *
import socket
import netifaces as net
from queue import Queue
import threading
import wikipedia
import time
import subprocess
import re
from signal import signal, SIGINT
from sys import exit
import random



def home_screen(): ##### First loop initiation, runs once and then never again
    print('Toolbox copyright 2023')
    print('Author - Brandon Sweat')
    print('Toolbox is not to be resold or redistributed')
    print('Toolbox is not a means for crminial activity')
    print('\n\n')
    print('         _ ')
    print('Toolbox [_]\n\n')
    print()
    print(" Input [help] for command information, or read the README.TXT!")
    print()
    print()




#######################################################################
################This is the main loop##################################
#######################################################################

def main(): ###### Main loop, runs after home_screen endlessly
    while True:
        try:

            cmd = input('toolbox.cmd# ').lower() ##### cmd prompt type interface
            cmd = cmd.strip(" ") ##### Strips space from end of cmd if space is input
            cmd = re.split(' ', cmd)  ##### splits cmd input strings by space, each word will be an index

            if len(cmd) <= 2:
                pass

            if cmd[0] == 'exit': ###### program exit
                quit()

    ################################### Network Tools ###########################################

            if cmd[0] == 'show':
                if len(cmd) > 1:
                    if cmd[1] == 'ip':
                        get_ip()
                    elif cmd [1] == 'interfaces':
                        print('getting interfaces')
                    elif cmd [1] == 'dns':
                        print('getting DNS')
                    elif cmd[1] == 'dhcp':
                        print('getting dhcp')
                    elif cmd[1] == 'domain':
                        print('getting domain')
                    elif cmd[1] == 'help':
                        print('Show what?\n - ip\n - interfaces\n - dns\n - dhcp\n - domain')
                    else:
                        print('Invalid command - try "show help" for more information')
                else:
                    print('Incomplete command')

            if cmd[0] == 'port':
                if len(cmd) > 1:
                    if cmd[1] == 'scan': ##### Port scan branch
                        if len(cmd) > 2:
                            if cmd[2] == 'help':
                                print('Port Scanner command | Specify a target IP | You can add a port range to the end with a comma separator e.g. "1,1000", 1-1024 is the default\n*Please note, port scanning a range of IPs can take some time\nUse port scanner at your own risk!\n      port scan *target*\n e.g. port scan 192.168.1.1\n      port scan 192.168.1.1 1,250')
                            elif cmd[2] == ' ':
                                print('Please input a target host or network to perform a port scan, type "port scan help" for more information')
                            elif len(cmd) > 3 and cmd[3] != ' ': ########################## Adding in port range specification functionality
                                target = cmd[2]
                                portrange = cmd[3]
                                portrange = portrange.split(',')
                                port_scan(target, portrange)
                                pass
                            else: ################## No port range, will use default
                                target = cmd[2]
                                portrange = (1,1024)
                                port_scan(target, portrange)
                                pass
                        else:
                            print('Please input a target host or network to perform a port scan, type "port scan help" for more information')
                            pass
                else:
                    print('Syntax error !!! Incomplete command. Try "port scan..."')
                    pass



            if cmd[0] == 'net':
                if len(cmd) > 1:
                    if cmd[1] == 'scan': ###### Net scan branch
                        if len(cmd) > 2:
                            if cmd[2] == 'help':
                                print('Network Scanner command | Specify a target IP, or range of IPs by using a CIDR notation\n    net scan *target*\n e.g. net scan 192.168.1.1\n      net scan 192.168.1.1/24')
                            else:
                                target = cmd[2]
                                net_scan(target)
                                pass
                        else:
                            print('Please input a target network to scan, or add "help" for more information')
                else:
                    pass

    ################################### GAMES #######################################################

            if cmd[0] == 'play':
                if len(cmd) > 1:
                    if cmd[1] == 'slots':
                        play_slots()
                        pass
                    elif cmd[1] == 'hangman':
                        play_hangman()
                        pass
                else:
                    print("\nTrying to play a game? Here's a list of what's available")
                    print("  * Slots")
                    print('  * Hangman')
                    print('  * Checkers')
                    print('  * Oregon Trail')
                    print('  * Gangsters Paradise')
                    print()

    ################################## WIKI SEARCH ######################################################

            if cmd[0] == 'wiki':
                if len(cmd) > 1:
                    search = cmd[1:5]
                    wiki_search(search)
                    pass
                else:
                    print("\nPlease enter [wiki *search*] to perform a Wikipedia search, this will display a summary of the page you're searching for.\nYou can search up to 5 words after inputting wiki, for example if you needed to search a name that requires multiple inputs\nFor example: George W. Bush")


    ################################## HELP SECTION ##################################################

            if cmd[0] == 'help':   ####### Help command
                print("----------------------------------------------------------------------------------------------")
                print("Welcome to Toolbox! You can always read the README.TXT within the program folder for the")
                print(" same information displayed here. Toolbox works in a terminal format, there are quite a few")
                print(" tools to choose from, even some games as well! See list of commands below.")
                print('')
                print("    [help] -     You're already here! Please note, that [help] can be added to the end")
                print("                 of most commands in order to assist you")
                print("    [port scan *target* *range,range*] -   *target* must be a single IP address, you can add")
                print("                                            a range at the end, using a comma as a separator")
                print("                                            (e.g. 192.168.2.1 OR 192.168.2.1 1,5000)")
                print("    [net scan *target*] -    *target* can be a single IP address, or a network in CIDR")
                print("                             notation format (e.g. 192.168.2.1 OR 192.168.2.1/24)")
                print("    [play *game*] -      Play a game! Input play, followed by the game you want to play")
                print("                         If you input [play] only, will return a list of games available")
                print("    [ssh *target*] -     SSH into a target node, *target* must be a reachable IP address")
                print("    [show (ip, interfaces, dns, dhcp, domain)] -    Get information of the local computer")
                print("    [exit] -     Close program")
                print("----------------------------------------------------------------------------------------------")


                pass
            else:
                pass
        except KeyboardInterrupt:
            quit()

############## Network Tools ########################


#######################################################################
##################### Get My IP #######################################
#######################################################################

def get_ip():
    print('getting IP')



#######################################################################
################This is the port scanner###############################
#######################################################################

def port_scan(target, portrange):
    print('Scanning ports on', target, f" {portrange[0]}-{portrange[1]}","\n")
    def scan_ports(target, portrange):
        print_lock = threading.Lock()
        target_scan = target
        port_range = portrange
        global port_list
        port_list = []

        def portscan(port):
            #(port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                con = s.connect((target_scan, port))
                with print_lock:
                    port
                protocolname = 'tcp'
                service = socket.getservbyport(port, protocolname)
                state = 'open'
                port_list.append({'port': port, 'state': state.upper(), 'service': service.upper()})

                con.close()

            except:
                pass

        def threader():

            while True:
                worker = q.get()

                portscan(worker)
                q.task_done()

        q = Queue()

        for x in range(150):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()
            clock_start = time.time()

        for worker in range(int(port_range[0]),int(port_range[1])):
            q.put(worker)

        q.join()
        print("PORT" + " " * 3 + "STATE" + " " * 3 + "SERVICE")
        print("----   -----   -------")

        for client in port_list:
            print("{}     {:6}  {:10}".format(client['port'], client['state'], client['service']))


    scan_ports(target, portrange)
    print()


#######################################################################
################This is the net scanner################################
#######################################################################

def net_scan(target):
    print('Scanning network', target,"\n")

    target_net = target
    arp = ARP(pdst=target_net)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    start_time = time.time()

    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = '* * *'
            pass
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})
    print()
    print("IP" + " " * 18 + "MAC" + " " * 19 + "Hostname")
    print("---------------     -----------------     -------------------------")

    for client in clients:
        print("{:16}    {:18}    {:25}".format(client['ip'], client['mac'], client['hostname']))

    end_time = time.time()
    print()
    total_time = end_time - start_time
    print('Time taken: ', round(total_time, 2),'s')
    print()



################### Wiki search

def wiki_search(search):
    search_string = ' '.join(search)  ##### Joins multiple words into a string separated by spaces
    try:
        page_object = wikipedia.summary(search_string, sentences = 7, auto_suggest=False) ##### Inputs search string, number of sentences to display, and turns off the annoying auto-suggest feature that does nothing but change your input

        searching = wikipedia.search(search_string, results = 10, suggestion = True)
        print('Search Results:')
        print(searching)
        print(page_object)
    except wikipedia.exceptions.PageError as e: ##### Raises exception if page does not exist
        print(f"\n  {e}\n")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"\n  {e}\n")




############### GAMES ####################################


################ Slots Game ###################
def play_slots():
    print('\nPlaying slots!\n')

    MAX_LINES = 3
    MAX_BET = 1000
    MIN_BET = 5

    ROWS = 3
    COLS = 3

    ###### Creates a dictionary for symbols
    symbol_count = {
        "$": 4,
        "#": 6,
        "@": 8,
        "%": 10,
    }

    ###### "Multiplier" of symbol, how much more valuable it is
    symbol_value = {
        "$": 5,
        "#": 3,
        "@": 2,
        "%": 1,
    }

    def check_winnings(columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def get_slot_machine_spin(rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            for _ in range(symbol_count):
                all_symbols.append(symbol)
        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]  #### Creates a copy of all_symboles, so that it does not change it
            for _ in range(rows):
                value = random.choice(all_symbols)
                current_symbols.remove(value)
                column.append(value)

            columns.append(column)
        return columns

    def print_slot_machine(columns):  ##### Transposing: moves teh colums from left to right to up & down in the matrix
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns) - 1:
                    print(column[row], end=" | ")
                else:
                    print(column[row], end="")
            print()

    def deposit():
        while True:  #### waits until input is a valid integer greater than 0, then breaks out (see break)
            amount = input("How much would you like to deposit? $")
            if amount.isdigit():  #### Will determine if 'amount' is a valid number, and not a negative
                amount = int(amount)  #### Convert to input to int
                if amount > MIN_BET:
                    break  #### Breaks while loop
                else:
                    print(
                        "  Amount must be greater than $5, which is the minimum betting ammount.")  #### If amount is not greater than 0, print this error and loop
            else:
                print("  Please enter a dollar amount.")  ##### If input is not a digit, print this error and loop
        return amount

    def get_number_of_lines():
        while True:  #### waits until input is a valid integer greater than 0, then breaks out (see break)
            lines = input("Enter the number of lines to bet on [1-" + str(MAX_LINES) + "]? ")  ##### Uses max_lines var to display amt of lines 1-X
            if lines.isdigit():  #### Will determine if 'amount' is a valid number, and not a negative
                lines = int(lines)  #### Convert to input to int
                if 1 <= lines <= MAX_LINES:
                    break  #### Breaks while loop
                else:
                    print(
                        f"  Amount must be between 1 and {MAX_LINES}.")  #### If amount is not greater than 0, print this error and loop
            else:
                print("  Please enter a numerical value.")  ##### If input is not a digit, print this error and loop
        return lines

    def get_bet():
        while True:  #### waits until input is a valid integer greater than 0, then breaks out (see break)
            bet = input(
                "How much are you going to bet on each line? $")  ##### Uses max_lines var to display amt of lines 1-X
            if bet.isdigit():  #### Will determine if 'amount' is a valid number, and not a negative
                bet = int(bet)  #### Convert to input to int
                if MIN_BET <= bet <= MAX_BET:
                    break  #### Breaks while loop
                else:
                    print(
                        f"  Amount must be between {MIN_BET} and {MAX_BET}.")  #### If amount is not greater than 0, print this error and loop
            else:
                print("  Please enter a dollar amount.")  ##### If input is not a digit, print this error and loop
        return bet

    def play_slots(new_balance):  ##### Creates main function so that the program can re-run from here

        balance = deposit()
        balance = balance + new_balance
        lines = get_number_of_lines()
        while True:
            bet = get_bet()
            total_bet = bet * lines
            if total_bet > balance:
                print(f"You do not have enough funds to bet that amount, your current balance is ${balance}")
            else:
                break
        total_bet = bet * lines
        rem_balance = balance - total_bet
        print('\n')
        if lines >= 2:
            print(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}\n")
        else:
            print(f"You are betting ${bet} on {lines} line. Total bet is ${total_bet}\n")
        print('\n')
        print(f'Current account balance: ${balance}', f'\nLines on bet: {lines}')
        time.sleep(.5)
        print(f'Your remaining balance is ${rem_balance}')
        print()
        time.sleep(.5)
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        print_slot_machine(slots)
        winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
        print()
        time.sleep(.5)
        if winnings > 0:
            print(f'You won ${winnings}!!')
            print(f"You won on lines:", *winning_lines)
            new_balance = winnings + total_bet + rem_balance
            print(f'Your new account balance is:\n   ${new_balance}\n')
            print()

            for x in range(100):
                keep_playing = input('Do you want to [1] cash out, or [2] keep playing? [1/2]: ')
                if keep_playing == '1':
                    print(f"\nThanks for playing, congrats! Here's your ${new_balance}\n")
                    time.sleep(.5)
                    loop()
                elif keep_playing == '2':
                    print("\nFeeling lucky still? Let's spin again.\n")
                    play_slots(new_balance)
                else:
                    print("Please input 1 or 2.")
                    pass
        else:
            new_balance = rem_balance
            print(f'Your remaining account balance is:\n   ${new_balance}\n')
            print()
            for x in range(100):
                keep_playing = input('Do you want to [1] cash out, or [2] keep playing? [1/2]: ')
                if keep_playing == '1':
                    print(f"\nThanks for playing, sorry for your loss! Here's your ${new_balance}\n")
                    time.sleep(.5)
                    loop()
                elif keep_playing == '2':
                    print("\nDown.. but not out! Let's spin again.\n")
                    play_slots(new_balance)
                else:
                    print("\nPlease input 1 or 2.")
                    pass
            play_slots(new_balance)



    play_slots(new_balance=0)


################ Hangman Game #####################
def play_hangman():

    ans_list = ['WRENCH', 'TOOLBOX', 'COWBOY', 'COLT', 'CACTUS', 'IPHONE', 'ANDROID', 'PYTHON', 'FARZANA', 'HUMAN',
                'HAMMER', 'CAT', 'DOG', 'LIZARD', 'EARTH', 'MOON', 'SUN', 'SATURN', 'JUPITER', 'COMPUTER', 'DESIRE',
                'GHOST', 'TABLE', 'PIANO', 'GUITAR', 'TRUMPET', 'WATER', 'LASER', 'PLANT', 'TREE', 'OCEAN', 'FISH']

    def init_hangman():
        print("Welcome to Hangman!")
        print("\nReady to take your chances in the gallows?")
        print()
        print("Guess 1 letter at a time, or even a whole word, but be careful, you only have 6 chances to guess wrong!")

        playing_hangman()

    def loop_hangman():
        playing_hangman()
        loop_hangman()

    def playing_hangman():
        randomword = random.choice(ans_list)
        len_randomword = len(randomword)
        sign_board = []
        guessed_wrong = 0
        guessed_right = 0
        guessed = False
        num_of_guesses = 0
        guessed_letters = []
        randomwordnew = randomword
        r_word_string = randomword.replace(" ", "")
        r_word_len = len(r_word_string)
        while guessed == False:
            remaining_list = [x for x in randomword if x not in randomwordnew]  ########### Compares the originally generated word with the "remaining letters" of the correctly guessed letters
            listToStr = ' '.join(map(str, sign_board))

            if num_of_guesses == 0:
                for x in randomword:

                    if x != ' ':
                        # print('_')
                        sign_board.append('_')

                    else:
                        # print(' ')
                        sign_board.append(' ')
            else:
                pass

            if remaining_list == sign_board:
                guessed = True
                print("Congratulations! You've guessed the word correctly!\n")
                print()
                print("   ", randomword)
                for x in range(50):
                    play_again = input('Would you like to go another round, partner? [y/n]: ').lower()
                    if play_again == 'y':
                        print('\n Yee-haw!\n')
                        loop_hangman()  ########################################################################################################################### Do I need to change this?
                    elif play_again == 'n':
                        print("\n 'Nother time then, partner...\n")
                        main()  ################################################################################################################################################### Replace with main menu loop function

            display_signboard = (' '.join(map(str, sign_board)))

            scenery_list = [
                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |                              __     
                       | |                             /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |                             /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |    |                        /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |   /|                        /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |   /|\                       /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |   /|\                       /  \          /\\
                       | |    L                        \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",

                f"""\n
                        ________
                       |  _____|        
                       | |    |            {display_signboard}
                       | |    O                         __     
                       | |   /|\                       /  \          /\\
                       | |    LL                       \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .""",
            ]

            scene_index = scenery_list[guessed_wrong]
            print(scene_index)  ############################################ Prints scene
            print('\nGuessed letters:')
            print(' '.join(guessed_letters))
            guess = input("\nWhat's your guess? ").upper()
            guessed_letters = guessed_letters + [guess]

            if guessed_wrong == 5 and guess not in randomword:
                print(scenery_list[6])
                print(
                    f"\nYou've made too many wrong choices, partner! We were hoping you'd guess: {randomword}\n      GAME OVER!\n")
                print()
                for x in range(50):
                    play_again = input('Would you like to go another round, partner? [y/n]: ').lower()
                    if play_again == 'y':
                        print('\n Yee-haw!\n')
                        loop_hangman()
                    elif play_again == 'n':
                        print("\n 'Nother time then, partner...\n")
                        main()

            if guess == randomword or guess == randomwordnew or randomwordnew == '' or sign_board == remaining_list:
                guessed = True
                randomword_sign = (' '.join(randomword))
                print(f'''\n
                        ________
                       |  _____|        
                       | |    |            {randomword_sign}
                       | |                              __     
                       | |                             /  \          /\\
                       | |                             \__/       , | |/|
                       | |                                        \\\|  /
                  _____|_|___________                              \\\ |
                 |\-----------------/|                              | |
                _|||/|___________|\|||____o_____O__________##_______|_|
            .` , -~_  _-    o   .   ` .  .,  -__   _-     - .   ,.  .o  .
            ''')
                print()
                print("Congratulations! You've guessed the word correctly!\n")
                print("     ", randomword, "\n")
                for x in range(50):

                    play_again = input('Would you like to go another round, partner? [y/n]: ').lower()
                    if play_again == 'y':
                        print('\n Yee-haw!\n')
                        loop_hangman()
                    elif play_again == 'n':
                        print("\n 'Nother time then, partner...\n")
                        main()

            elif guess in sign_board:
                print("\nYou've already guessed that letter! You've wasted a guess :(\n")
                num_of_guesses += 1

            elif guess in randomword or guess in randomwordnew:
                print('You guessed correctly!\n')
                randomwordnew = randomwordnew.replace(guess, '')
                guessed_right = 1 + guessed_right
                remove_guess = randomword.count(guess)
                indices = [i for i, item in enumerate(randomword) if item == guess]
                num_of_guesses += 1

                for x in indices:

                    for i, item in enumerate(sign_board):
                        if x == i:
                            sign_board[i] = guess

            elif guess not in randomword:
                print('You guessed incorrectly.. 1 step closer to death.\n')
                guessed_wrong = 1 + guessed_wrong
                num_of_guesses += 1

    init_hangman()


#################################################################################
################## Initialize and Main loops ####################################
#################################################################################

def loop(): ##### Loops program
    main()
    loop()


def initialize(): ##### Init program
    home_screen()
    main()
    loop()



################ Program Run ##################

initialize()