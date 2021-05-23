import time
import logging
import tkinter
from tkinter import messagebox
from app import printing, grafic_sygn_connection, grafic_out_connection



error_counter = 0
error_names_sygn = []
error_names_out = []
sn_zespol = 0


############## Adresacja modułów ####################
MODULE = {
    'IO2': 202,
    'IO3': 302,
    'IO4': 402,
    'IO5': 502,
    'IO6': 602
}

################# Baza sygnalow sterownikow 3p i 4p###########################
EOP_4P = {
    "none": ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    "switch": ".. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    0: "## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    1: ".. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    2: ".. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. ..",
    3: ".. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ..",
    4: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. ..",
    5: ".. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ..",
    6: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. ..",
    7: "## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    8: ".. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    9: ".. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. ..",
    10: ".. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ..",
    11: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. ..",
    12: ".. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ..",
    13: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. ..",
    14: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. ..",
    15: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. ..",
    16: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. ..",
    17: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. ..",
    18: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. ..",
    19: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. ..",
    20: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. ..",
    21: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## ..",
    22: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ##",
    23: "## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    24: ".. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    25: ".. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    26: ".. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    27: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    28: ".. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    29: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    30: ".. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    31: ".. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    32: ".. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    33: ".. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    34: ".. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    35: ".. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. ..",#3P
    36: ".. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ..",
    37: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. ..",
    38: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ..",
    39: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. ..",
    40: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. ..",
    41: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. ..",
    42: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. ..",
    43: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. ..",
    44: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. ..",#4p
}


######################## dodatkowa baza sygnalow sterownika 5p#####################
EOP_5P = {
    23: "## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    24: ".. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    25: ".. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    26: ".. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    27: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    28: ".. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    29: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## ..",
    30: ".. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ##",
    31: ".. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    32: ".. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    33: ".. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    34: ".. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    35: ".. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. ..",#3P
    36: ".. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. ..",
    37: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. ..",
    38: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. ..",
    39: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. ..",
    40: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. ..",
    41: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. ..",
    42: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. ..",
    43: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. .. ..",
    44: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. .. ..",#4p
    45: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. .. ..",
    46: ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## .. ..",
    47: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ## ..",
    48: ".. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ##",
    49: "## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    50: ".. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    51: ".. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    52: ".. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    53: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .."
}


########### Baza nazw sygnaliacji############
SYGN_NAME = {
    "switch": "x",
    0: "x",
    1: "x",
    2: "x",
    3: "x",
    4: "x",
    5: "x",
    6: "x",
    7: "x",
    8: "x",
    9: "x",
    10: "x",
    11: "x",
    12: "x",
    13: "x",
    14: "x",
    15: "x",
    16: "x",
    17: "x",
    18: "x",
    19: "x",
    20: "x",
    21: "x",
    22: "x",
    23: "x",
    24: "x",
    25: "x",
    26: "x",
    27: "x",
    28: "x",
    29: "x",
    30: "x",
    31: "x",
    32: "x",
    33: "x",
    34: "x",
    35: "x",
    36: "x",
    37: "x",
    38: "x",
    39: "x",
    40: "x",
    41: "x",
    42: "x",
    43: "x",
    44: "x",
    45: "x",
    46: "x",
    47: "x",
    48: "x",
    49: "x",
    50: "x",
    51: "x",
    52: "x",
    53: "x"
}

############# Baza sygnalizac#ji sprawdzajaca wyjscia sterownikow ################
EOP_OUT = {
    0: "## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    1: ".. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    2: ".. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    3: ".. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    4: ".. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    5: ".. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    6: ".. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    7: ".. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    8: ".. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    9: ".. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    10: ".. .. .. .. .. .. .. .. .. .. ## .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
}


############ Baza nazw sterowan ###############################
OUT_NAME = {
    0: "x",
    1: "x",
    2: "x",
    3: "x",
    4: "x",
    5: "x",
    6: "x",
    7: "x",
    8: "x",
    9: "x",
    10: "x",
}


####### polaczenie i logowanie do aplikacji ##########
def log_in(console):
        console.write(str.encode("x" + '\r\n'))
        time.sleep(0.5)
        console.write(str.encode("x" + '\r\n'))
        time.sleep(0.5)


######### Odczyt numeru seryjnego #####
def sn(console):
    console.write(str.encode('sn' + '\r\n'))
    time.sleep(0.1)
    data = console.read(console.in_waiting)
    data = str(data, "UTF-8")
    d = data.split('\r\n')
    c = d[-2].strip()
    number = c[14:21]
    return number


######## Stworzenie pliku logów ######
def loger(sn, sn_zespol):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(filename=f'log\\log_{sn}.log', mode='w')
    fh.setLevel(logging.INFO)
    format = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S'
    )
    fh.setFormatter(format)
    log.addHandler(fh)
    log.info("------------------Test sterowań i sygnalizacji---------------------")
    log.info(f"Zespół sterownika o numerze: {sn_zespol} i sterownikiem o numerze seryjnym {sn}")


########### Ustawienie sterowan ##################
def set_bo(console, module, bo, txt_frame):
    console.write(str.encode('x' + '\r\n'))
    time.sleep(0.15)
    for key, value in MODULE.items():
        if module == key:
            printing(txt_frame, f'Zalaczenie sterowania {bo}')
            print(f'Zalaczenie sterowania {bo}')
            logging.info(f'Zalaczenie sterowania {bo}')
            console.write(str.encode(f'x({value})x {bo}x' + '\r\n'))
            time.sleep(0.3)

########### Ustawienie sterowan ##################
def set_signal(console, bo, txt_frame):
    printing(txt_frame, f'Zalaczenie sterowania {bo}')
    logging.info(f'Zalaczenie sterowania {bo}')
    console.write(str.encode(f'x {bo} x' + '\r\n'))
    time.sleep(0.3)

########### Kasowanie sterowan ##################
def del_bo(console, module, bo):
    for key, value in MODULE.items():
        if module == key:
            console.write(str.encode(f'x({value}) x {bo} x' + '\r\n'))


########### Odczyt sygnalizacji ##################
def read_bi(console, module):
    console.write(str.encode("\r\n"))
    time.sleep(0.1)
    console.write(str.encode(f"d /dev/bi/{module}x" + "\r\n"))
    time.sleep(0.25)
    data = console.read(console.in_waiting)
    data = str(data, "UTF-8")
    ans = data.split('\r\n')
    sygn = ans[-2].strip()
    return sygn


########## Sprawdzenie sygnalizacji ###############
def check_sygn(sygn, db, nr_sygn, txt_frame, grafic_frame):
    if sygn == db[nr_sygn]:
        if db == EOP_4P or db == EOP_5P:
            printing(txt_frame, f"Numer sygnalizacji {nr_sygn} : {sygn} OK")
            grafic_sygn_connection(grafic_frame, nr_sygn, 1)
            print(f"Numer sygnalizacji {nr_sygn} : {sygn} OK")
            logging.info(f"Numer sygnalizacji {nr_sygn} : {sygn} OK")
        if db == EOP_OUT:
            printing(txt_frame, f"Numer sterowania {nr_sygn} : {sygn} OK")
            grafic_out_connection(grafic_frame, nr_sygn, 1)
            print(f"Numer sterowania {nr_sygn} : {sygn} OK")
            logging.info(f"Numer sterowania {nr_sygn} : {sygn} OK")

    else:
        global error_counter
        if db == EOP_4P or db == EOP_5P:
            printing(txt_frame, f"Numer sygnalizacji {nr_sygn} : {sygn} ZLE")
            grafic_sygn_connection(grafic_frame, nr_sygn, 0)
            print(f"Numer sygnalizacji {nr_sygn} : {sygn} ZLE")
            logging.info(f"Numer sygnalizacji {nr_sygn} : {sygn} ZLE")
            global error_names_sygn
            error_counter += 1
            error_names_sygn.append((nr_sygn, SYGN_NAME[nr_sygn]))
        if db == EOP_OUT:
            global error_names_out
            printing(txt_frame, f"Numer sterowania {nr_sygn} : {sygn} ZLE")
            grafic_out_connection(grafic_frame, nr_sygn, 0)
            print(f"Numer sterowania {nr_sygn} : {sygn} ZLE")
            logging.info(f"Numer sterownia {nr_sygn} : {sygn} ZLE")
            error_counter += 1
            error_names_out.append((nr_sygn, OUT_NAME[nr_sygn]))



########### Podsumowanie #########################
def result(serial_number, txt_frame, sn_zespol):
    if error_counter == 0:
        print(f"Zespół SN:{sn_zespol} ze sterownikiem {serial_number} przeszedł POZYTYWNIE test sterowan i sygnalizacji\nLiczba bledow {error_counter}")
        logging.info(f"Zespół SN:{sn_zespol} ze sterownikiem {serial_number} przeszedł POZYTYWNIE test sterowan i sygnalizacji\nLiczba bledow {error_counter}")
        printing(txt_frame, f"Zespół SN:{sn_zespol} ze sterownikiem {serial_number} przeszedł POZYTYWNIE test sterowan i sygnalizacji\nLiczba bledow {error_counter}")
    else:
        printing(txt_frame, f"Zespół SN:{sn_zespol} ze sterownikiem {serial_number} wynik testu NEGATYWNY\nLiczba bledow {error_counter}")
        print(f"Zespół SN:{sn_zespol} ze sterownikiem {serial_number} wynik testu NEGATYWNY\nLiczba bledow {error_counter}")
        logging.info(f"Sterownik Zespół SN:{sn_zespol} ze sterownikiem {serial_number} wynik testu NEGATYWNY\nLiczba bledow {error_counter}")
        for x in error_names_sygn:
            printing(txt_frame, f"AWARIA Sygnalizacji {x[0]} - ({x[1]})")
            print(f"AWARIA Sygnalizacji {x[0]} - ({x[1]})")
            logging.info(f"AWARIA Sygnalizacji {x[0]} - ({x[1]})")
        for error in error_names_out:
            printing(txt_frame, f"AWARIA sterowania {error[0]} - ({error[1]})")
            print(f"AWARIA sterowania {error[0]} - ({error[1]})")
            logging.info(f"AWARIA sterowania {error[0]} - ({error[1]})")


########### Test przelacznika w pozycji odstawionej ######################
def test_switcha_odst(con_s, txt_frame, grafic_frame, typ):
    if typ == "5P":
        tkinter.messagebox.showinfo(title='Test przełącznika - odstawiony', message='Ustaw przełącznik w pozycji odstawionej')
        ans = read_bi(con_s, "IO5")
        check_sygn(ans, EOP_4P, "switch", txt_frame, grafic_frame)
    else:
        tkinter.messagebox.showinfo(title='Test przełącznika - odstawiony', message= 'Ustaw przełącznik w pozycji odstawionej')
        ans = read_bi(con_s, "IO4")
        check_sygn(ans, EOP_4P, "switch",txt_frame, grafic_frame)


########### Test przelacznika w pozycji zdalnej ######################
def test_switcha_zdal(con_s, typ):
    if typ == "5P":
        tkinter.messagebox.showinfo(title='Test przełącznika - zdalny', message='Ustaw przełącznik w pozycji zdalnej')
        ans = read_bi(con_s, "IO5")
        if ans == EOP_4P["none"]:
            logging.info(f"Przelacznik w pozycji zdalnej {ans} OK")
    else:
        tkinter.messagebox.showinfo(title='Test przełącznika - zdalny', message='Ustaw przełącznik w pozycji zdalnej')
        ans = read_bi(con_s, "IO4")
        if ans == EOP_4P["none"]:
            logging.info(f"Przelacznik w pozycji zdalnej {ans} OK")


####################### Test sterowan 3p###################################
def test_bi_3p(con_m, con_s, txt_frame, grafic_frame):
    printing(txt_frame, "**********TEST SYGNALIZACJI**********")
    logging.info("**********TEST SYGNALIZACJI**********")
    counter = 0
    for i in range(0, 36):
        if counter == 8:
            counter = 0
        if i < 6:
            set_bo(con_m, "IO2", i,txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO2", i)
            check_sygn(ans, EOP_4P, i,txt_frame, grafic_frame)
        elif i == 6:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
        elif i < 15:
            set_bo(con_m, "IO2", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO2", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 23:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 31:
            set_bo(con_m, "IO4", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO4", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 37:
            set_bo(con_m, "IO5", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO5", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1


########################Test sygnalizacji sterownika 4p####################
def test_bi_4p(con_m, con_s, txt_frame, grafic_frame):
    printing(txt_frame, "**********TEST SYGNALIZACJI**********")
    logging.info("**********TEST SYGNALIZACJI**********")
    counter = 0
    for i in range(0, 45):
        if counter == 8:
            counter = 0
        if i < 6:
            set_bo(con_m, "IO2", i, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO2", i)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
        elif i == 6:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
        elif i < 15:
            set_bo(con_m, "IO2", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO2", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 23:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io4")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 31:
            set_bo(con_m, "IO4", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO4", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 39:
            set_bo(con_m, "IO5", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO5", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 45:
            set_bo(con_m, "IO6", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO6", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1

#######################Test sygnalizacji sterownika 5p#######################
def test_bi_5p(con_m, con_s, txt_frame, grafic_frame):
    logging.info("**********TEST SYGNALIZACJI**********")
    printing(txt_frame, "**********TEST SYGNALIZACJI**********")
    counter = 0
    for i in range(0, 54):
        if counter == 8:
            counter = 0
        if i < 6:
            set_bo(con_m, "IO2", i, txt_frame)
            ans = read_bi(con_s, "Io5")
            del_bo(con_m, "IO2", i)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
        elif i == 6:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io5")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
        elif i < 15:
            set_bo(con_m, "IO2", counter, txt_frame)
            ans = read_bi(con_s, "Io5")
            del_bo(con_m, "IO2", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 23:
            set_bo(con_m, "IO3", counter, txt_frame)
            ans = read_bi(con_s, "Io5")
            del_bo(con_m, "IO3", counter)
            check_sygn(ans, EOP_4P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 31:
            set_bo(con_m, "IO4", counter, txt_frame)
            ans = read_bi(con_s, "Io6")
            del_bo(con_m, "IO4", counter)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 39:
            set_bo(con_m, "IO5", counter, txt_frame)
            ans = read_bi(con_s, "Io6")
            del_bo(con_m, "IO5", counter)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
            counter += 1
        elif i < 47:
            set_bo(con_m, "IO6", counter, txt_frame)
            ans = read_bi(con_s, "Io6")
            del_bo(con_m, "IO6", counter)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
            counter += 1
        elif i == 47:
            set_bo(con_m, "IO4", 6, txt_frame)
            ans = read_bi(con_s, "Io6")
            del_bo(con_m, "IO4", 6)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
        elif i == 48:
            set_bo(con_m, "IO4", 7, txt_frame)
            ans = read_bi(con_s, "Io6")
            del_bo(con_m, "IO4", 7)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
        elif i < 54:
            set_bo(con_m, "IO5", counter, txt_frame)
            ans = read_bi(con_s, "Io7")
            del_bo(con_m, "IO5", counter)
            check_sygn(ans, EOP_5P, i, txt_frame, grafic_frame)
            counter += 1


################### Test sterowan 3p#######################
def test_sterowan_3p(con_m, con_s, txt_frame, grafic_frame):
    printing(txt_frame, "**********TEST STEROWAN**********")
    logging.info("**********TEST STEROWAN**********")
    con_s.write(str.encode('x' + '\r\n'))
    time.sleep(0.1)
    con_s.write(str.encode('x ' + '\r\n')) #Ustawienie sterownika w tryb testowy
    time.sleep(0.1)
    con_s.write(str.encode('x' + '\r\n'))#Ustawienie sterowania w tryb testowy
    time.sleep(0.1)
    read_bi(con_m, "Io7")
    time.sleep(0.1)
    for i in range(0, 7):
        set_bo(con_s, "IO3", i, txt_frame)
        ans = read_bi(con_m, "Io7")
        del_bo(con_s, "IO3", i)
        check_sygn(ans, EOP_OUT, i, txt_frame, grafic_frame)


################### Test sterowan 4p#######################
def test_sterowan_4p(con_m, con_s, txt_frame, grafic_frame):
    printing(txt_frame, "**********TEST STEROWAN**********")
    logging.info("**********TEST STEROWAN**********")
    con_s.write(str.encode('x' + '\r\n'))
    time.sleep(0.1)
    con_s.write(str.encode('x' + '\r\n')) #Ustawienie sterownika w tryb testowy
    time.sleep(0.1)
    con_s.write(str.encode('x' + '\r\n'))#Ustawienie sterowania w tryb testowy
    time.sleep(0.1)
    con_s.write(str.encode('x' + '\r\n'))  # Ustawienie sterowania w tryb testowy
    time.sleep(0.1)
    read_bi(con_m, "Io7")
    time.sleep(0.1)
    counter = 0
    for i in range(0, 9):
        if i < 7:
            set_bo(con_s, "IO3", i, txt_frame)
            ans = read_bi(con_m, "Io7")
            del_bo(con_s, "IO3", i)
            check_sygn(ans, EOP_OUT, i, txt_frame, grafic_frame)
        else:
            set_bo(con_s, "IO6", counter, txt_frame)
            ans = read_bi(con_m, "Io7")
            del_bo(con_s, "IO6", counter)
            check_sygn(ans, EOP_OUT, i, txt_frame, grafic_frame)
            counter += 1


################### Test sterowan 5p                                DO UZUPELNIENIA WARTOSCI SYGNALOWE PAKIETOW I W DB#######################
def test_sterowan_5p(con_m, con_s, txt_frame, grafic_frame):
    printing(txt_frame, "**********TEST STEROWAN**********")
    logging.info("**********TEST STEROWAN**********")
    time.sleep(0.1)
    read_bi(con_m, "Io7")
    time.sleep(0.1)
    control = 1
    for i in range(1, 12):
        if i >= 8:
            set_signal(con_s, control+1, txt_frame)
            ans = read_bi(con_m, "Io7")
            check_sygn(ans, EOP_OUT, control - 1, txt_frame, grafic_frame)
            control += 1
            time.sleep(0.8)
        else:
            set_signal(con_s, control, txt_frame)
            ans = read_bi(con_m, "Io7")
            check_sygn(ans, EOP_OUT, control-1, txt_frame, grafic_frame)
            control += 1
            time.sleep(0.8)


def SN_zespol(sn_zesp):
    global sn_zespol
    sn_zespol = f"A{sn_zesp}"


def clear_variables():
   global error_counter
   error_counter= 0
   global error_names_sygn
   error_names_sygn = []
   global error_names_out
   error_names_out = []


def end_logging(sn):
    logging.getLogger().handlers.clear()
    logging.getLogger().removeHandler(logging.FileHandler(filename=f'log\\log_{sn}.log'))


def test_3p(con_s, con_m, txt_frame, grafic_frame):
    log_in(con_s)
    serial_number = sn(con_s)
    loger(serial_number, sn_zespol)
    test_switcha_odst(con_s, txt_frame, grafic_frame, "3P")
    test_switcha_zdal(con_s, "3P")
    test_bi_3p(con_m, con_s, txt_frame, grafic_frame)
    test_sterowan_3p(con_m, con_s, txt_frame, grafic_frame)
    result(serial_number, txt_frame, sn_zespol)
    clear_variables()
    end_logging(serial_number)


def test_4p(con_s, con_m, txt_frame, grafic_frame):
    log_in(con_s)
    serial_number = sn(con_s)
    loger(serial_number, sn_zespol)
    test_switcha_odst(con_s, txt_frame, grafic_frame, "4P")
    test_switcha_zdal(con_s, "4P")
    test_bi_4p(con_m, con_s, txt_frame, grafic_frame)
    test_sterowan_4p(con_m, con_s, txt_frame, grafic_frame)
    result(serial_number, txt_frame, sn_zespol)
    clear_variables()
    end_logging(serial_number)

def test_5p(con_s, con_m, txt_frame, grafic_frame):
    log_in(con_s)
    serial_number = sn(con_s)
    loger(serial_number, sn_zespol)
    test_switcha_odst(con_s, txt_frame, grafic_frame, "5P")
    test_switcha_zdal(con_s, "5P")
    test_bi_5p(con_m, con_s, txt_frame, grafic_frame)
    test_sterowan_5p(con_m, con_s, txt_frame, grafic_frame)
    result(serial_number, txt_frame, sn_zespol)
    clear_variables()
    end_logging(serial_number)


if __name__ == "__main__":
    pass