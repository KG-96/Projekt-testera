import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Backend.settings import set_master_ports, set_slave_ports, set_user_ports, get_user_ports
from Backend.tests import *
import time



SYGN_PLACES = {
    "switch": (189, 28),
    0: (74, 12),
    1: (96, 12),
    2: (117, 12),
    3: (139, 12),
    4: (64, 49),
    5: ((84, 49), (106, 49), (127, 49)),
    6: (148, 49),
    7: (135, 111),
    8: (105, 111),
    9: (179, 137),
    10: (150, 137),
    11: (120, 137),
    12: (90, 137),
    13: (59,137),
    14: (195, 164),
    15: (165, 164),
    16: (135, 164),
    17: (105, 164),
    18: (135, 210),
    19: (105, 210),
    20: (74, 210),
    21: (45, 210),
    22: (180, 237),
    23: (150, 237),
    24: (120, 237),
    25: (90, 237),
    26: (59, 237),
    27: (74, 264),
    28: (45, 264),
    29: (195, 310),
    30: (165, 310),
    31: (135, 310),
    32: (105, 310),
    33: (74, 310),
    34: (45, 310),
    35: (179, 336),
    36: (195, 363),
    37: (165, 363),
    38: (135, 363),
    39: (105, 363),
    40: (74, 363),
    41: (45, 363),
    42: (195, 410),
    43: (165, 410),
    44: (135, 410),
    45: (150, 436),
    46: (120, 436),
    47: (90, 436),
    48: (59, 436),
    49: (195, 462),
    50: (165, 462),
    51: (135, 462),
    52: (105, 462),
    53: (74, 462),
}

OUT_PLACES = {
    0: ((74, 111), (45, 111)),
    1: ((74, 163), (45, 163)),
    2: ((195, 210), (164, 210)),
    3: ((195, 263), (165, 263)),
    4: ((135, 263), (105, 263)),
    5: ((150, 336), (120, 336)),
    6: ((90, 336), (59, 336)),
    7: ((105, 409), (74, 409)),
    8: ((45, 409), (179, 436)),
    9: ((45, 462), (195, 508)),
    10: ((165, 508), (135, 508))
}


def home(consol_frame, test_menu_frame):
    for widget in consol_frame.winfo_children():
            widget.destroy()
    for widget in test_menu_frame.winfo_children():
            widget.destroy()
    home_frame = tk.Frame(consol_frame, bg='#ffffff')
    home_frame.place(x=0, y=0, height=620, width=1307)
    h1_label = tk.Label(home_frame, text='Narzędzia potrzebne do przeprowadzenia testu:', font=('Times new roman', 28, " bold"),
                        fg='#0b2540', bg='white')
    h1_label.place(x=0, y=65)
    h2_label = tk.Label(home_frame, text="""
1) Zasilacz 24V z wyprowadzeniem na dwa złącza wejściowe dwu pinowe
2) Multimetr
3) Urządzenie testowe wraz z wiązką testową
4) Dwa kable USB typu B
    """,
                        font=('Times new roman', 18, " bold"), justify="left", fg='#0b2540', bg='white')
    h2_label.place(x=0, y=120)

def test_menu(test_menu_frame, consol_frame):
    for widget in consol_frame.winfo_children():
            widget.destroy()
    test_frame = tk.Frame(consol_frame, bg='#ffffff')
    test_frame.place(x=0, y=0, height=620, width=1307)
    test_3p_button = tk.Button(test_menu_frame, text='Test sterownika 3P', command=lambda : SN_zesp(test_frame, "3P"), font=('Arial', 12, " bold"), fg='#0b2540',bg="white" , bd=3, padx=8,pady=8).place(x=15, y=8)
    test_4p_button = tk.Button(test_menu_frame, text='Test sterownika 4P', command=lambda : SN_zesp(test_frame, "4P"), font=('Arial', 12, " bold"), fg='#0b2540',bg="white" , bd=3, padx=8, pady=8).place(x=200, y=8)
    test_5p_button = tk.Button(test_menu_frame, text='Test sterownika 5P', command=lambda : SN_zesp(test_frame, "5P"), font=('Arial', 12, " bold"), fg='#0b2540',bg="white" , bd=3, padx=8, pady=8).place(x=386, y=8)
    h1_label = tk.Label(test_frame, text='Przed uruchomieniem testu wykonać:', font=('Times new roman', 28, " bold"),fg='#0b2540', bg='white')
    h1_label.place(x=0, y=65)
    h2_label = tk.Label(test_frame, text="""
1) Sprawdzenie porawności montażu w szczególności: polaryzacje złącz zasilających oraz oznaczniki
2) Multimetrem sprawdzić rozszycie przewodów pomiarowych na złącze
3) Połączyć zespół sterownika z urządzeniem testowy 
   (spiąć duże złącze pomiarowe, 4 pinowe złącze sygnałowe oraz obsadzić 10 pinowe złącze w zepole)
""",
font=('Times new roman', 17, " bold"),justify = "left",fg='#0b2540', bg='white')
    h2_label.place(x=0, y=120)

def settings(consol_frame, test_menu_frame):
    for widget in consol_frame.winfo_children():
            widget.destroy()
    for widget in test_menu_frame.winfo_children():
            widget.destroy()
    settings_frame = tk.Frame(consol_frame, bg="#ffffff", relief = 'groove', borderwidth=3)
    settings_frame.place(x=200, y=40, height=400, width=640)
    settings_label = tk.Label(settings_frame, text='Ustawienia portów:', font=('Times new roman', 36, " bold"),fg='#0b2540', bg='white')
    settings_label.place(x=120, y=15)
    master_connection_label = tk.Label(settings_frame,text=f'Aktualny COM dla sterownika testowego: {get_user_ports()[0][1]} ',font=('Arial', 16), fg='#12141a', bg='white')
    master_connection_label.place(x=80, y=95)
    master_new_label = tk.Label(settings_frame, text=f'Wprowadź nowy numer COM:', font=('Arial', 16), fg='#12141a',bg='white')
    master_new_label.place(x=80, y=155)
    var_master_new = tk.StringVar()
    txt_master_new = tk.Entry(settings_frame, font=('Arial', 14), fg='#12141a', bg='white', justify='center',textvariable=var_master_new)
    txt_master_new.place(x=360, y=156, width=40)
    button_master_new = tk.Button(settings_frame, text='Zapisz', command=lambda: save_port_master(var_master_new),font=('Arial', 12, " bold"), fg='#12141a', bd=3, padx=1, pady=1)
    button_master_new.place(x=405, y=150)

    master_connection_label = tk.Label(settings_frame,text=f'Aktualny COM dla sterownika Zespołu EOP: {get_user_ports()[1][1]} ',font=('Arial', 16), fg='#12141a', bg='white')
    master_connection_label.place(x=80, y=230)
    master_new_label = tk.Label(settings_frame, text=f'Wprowadź nowy numer COM:', font=('Arial', 16), fg='#12141a',bg='white')
    master_new_label.place(x=80, y=285)
    var_slave_new = tk.StringVar()
    txt_master_new = tk.Entry(settings_frame, font=('Arial', 14), fg='#12141a', bg='white', justify='center',textvariable=var_slave_new)
    txt_master_new.place(x=360, y=286, width=40)
    button_master_new = tk.Button(settings_frame, text='Zapisz', command= lambda: save_port_slave(var_slave_new), font=('Arial', 12, " bold"), fg='#12141a', bd=3, padx=1, pady=1)
    button_master_new.place(x=405, y=279)

def SN_zesp(central_frame, control):
    for widget in central_frame.winfo_children():
            widget.destroy()
    frame = tk.Frame(central_frame, bg="white", relief = 'groove', borderwidth=2)
    frame.place(x=340, y=100, height=220, width=340)

    label = tk.Label(frame, text=f'Wprowadz numer seryjny\n Zespołu sterownika\nA-',font=('Arial', 16), fg='#0b2540', bg='white')
    label.place(x=50, y=20)
    var_sn_zesp= tk.StringVar()
    txt_zesp = tk.Entry(frame, font=('Arial', 14), fg='#0b2540', bg='white', justify='center',textvariable=var_sn_zesp)
    txt_zesp.place(x=110, y=95, width=120)

    button_master_new = tk.Button(frame, text='Zapisz', command=lambda: save_sn_zespol(var_sn_zesp, frame, control, central_frame),font=('Arial', 12, " bold"), fg='#0b2540',bg='white', bd=3, padx=1, pady=1)
    button_master_new.place(x=130, y=130)

def save_sn_zespol(var_sn_zesp, frame, control, central_frame):
    try:
        sn_dev = int(var_sn_zesp.get())
    except ValueError:
        tk.messagebox.showwarning(title='Błąd', message='Podałeś zły numer seryjny zespołu')
    sn_dev = str(sn_dev)
    if len(sn_dev) == 6:
        frame.destroy()
        SN_zespol(sn_dev)
        if control == "5P":
            b_test_5p(central_frame)
        elif control == "4P":
            b_test_4p(central_frame)
        else:
            b_test_3p(central_frame)
    else:
        tk.messagebox.showwarning(title='Błąd', message='Podałeś zły numer seryjny zespołu')


def b_test_3p(test_frame):
    for widget in test_frame.winfo_children():
        widget.destroy()
    test_grafic_frame = tk.Frame(test_frame, bg='white')
    test_grafic_frame.place(x=755, y=10, height=600, width=250)
    text_frame = tk.Frame(test_frame, bg='white')
    text_frame.place(x=0, y=80, height=510, width=755)
    scroll = tk.Scrollbar(text_frame)
    scroll.pack(side='right', fill='y')
    text_box = tk.Text(text_frame, bg='white', padx=15, pady=15, wrap='word', yscrollcommand=scroll.set)
    text_box.place(x=0, y=0, height=510, width=740)
    scroll.config(command=text_box.yview)
    bg = Image.open('.\\images\\temple_1.png')
    bg = ImageTk.PhotoImage(bg)
    grafic_label = tk.Label(test_grafic_frame, image=bg)
    grafic_label.image = bg
    grafic_label.place(x=-2, y=-2)
    con_s = set_slave_ports()
    con_m = set_master_ports()
    try:
        con_s.open()
        con_m.open()
        if con_s.isOpen() and con_m.isOpen():
            test_3p(con_s, con_m, text_box, test_grafic_frame)
        con_s.close()
        con_m.close()
    except EnvironmentError:
        tk.messagebox.showwarning(title='Błąd', message='Nie można nawiązać połączenia\nSprawdź ustawnienia połączenia')




def b_test_4p(test_frame):
    for widget in test_frame.winfo_children():
        widget.destroy()
    test_grafic_frame = tk.Frame(test_frame, bg='white')
    test_grafic_frame.place(x=755, y=10, height=600, width=250)
    text_frame = tk.Frame(test_frame, bg='white')
    text_frame.place(x=0, y=80, height=510, width=755)
    scroll = tk.Scrollbar(text_frame)
    scroll.pack(side='right', fill='y')
    text_box = tk.Text(text_frame, bg='white', padx=15, pady=15, wrap='word', yscrollcommand=scroll.set)
    text_box.place(x=0, y=0, height=510, width=740)
    scroll.config(command=text_box.yview)
    bg = Image.open('.\\images\\temple_1.png')
    bg = ImageTk.PhotoImage(bg)
    grafic_label = tk.Label(test_grafic_frame, image=bg)
    grafic_label.image = bg
    grafic_label.place(x=-2, y=-2)
    con_s = set_slave_ports()
    con_m = set_master_ports()
    try:
        con_s.open()
        con_m.open()
        if con_s.isOpen() and con_m.isOpen():
            test_4p(con_s, con_m, text_box, test_grafic_frame)
        con_s.close()
        con_m.close()
    except EnvironmentError:
        tk.messagebox.showwarning(title='Błąd', message='Nie można nawiązać połączenia\nSprawdź ustawnienia połączenia')



def b_test_5p(test_frame):
    for widget in test_frame.winfo_children():
        widget.destroy()
    test_grafic_frame = tk.Frame(test_frame, bg='white')
    test_grafic_frame.place(x=755, y=10, height=600, width=250)
    text_frame = tk.Frame(test_frame, bg='white')
    text_frame.place(x=0, y=80, height=510, width=755)
    scroll = tk.Scrollbar(text_frame)
    scroll.pack(side='right', fill='y')
    text_box = tk.Text(text_frame, bg='white', padx=15, pady=15, wrap='word', yscrollcommand=scroll.set)
    text_box.place(x=0, y=0, height=510, width=740)
    scroll.config(command=text_box.yview)
    bg = Image.open('.\\images\\temple_1.png')
    bg = ImageTk.PhotoImage(bg)
    grafic_label = tk.Label(test_grafic_frame, image=bg)
    grafic_label.image = bg
    grafic_label.place(x=-2, y=-2)
    con_s = set_slave_ports()
    con_m = set_master_ports()
    start = time.time()
    try:
        con_s.open()
        con_m.open()
        if con_s.isOpen() and con_m.isOpen():
            test_5p(con_s, con_m, text_box, test_grafic_frame)
        con_s.close()
        con_m.close()
        print(f"{time.time()- start}")
    except EnvironmentError:
        tk.messagebox.showwarning(title='Błąd', message='Nie można nawiązać połączenia\nSprawdź ustawnienia połączenia')



def save_port_master(var_master_new):
    try:
        new_port = int(var_master_new.get())
    except ValueError:
        tk.messagebox.showwarning(title='Błąd', message='Wpisałeś złą liczbę')
    new_port = str(new_port)
    if new_port == "":
        tk.messagebox.showwarning(title='Błąd', message='Wpisałeś złą liczbę')
    else:
        set_user_ports("Urzadzenie_testowe", new_port)
        settings(consol_frame, test_menu_frame)


def save_port_slave(var_slave_new):
    try:
        new_port = int(var_slave_new.get())
    except ValueError:
        tk.messagebox.showwarning(title='Błąd', message='Wpisałeś złą liczbę')
    new_port = str(new_port)
    if new_port == "":
        tk.messagebox.showwarning(title='Błąd', message='Wpisałeś złą liczbę')
    else:
        set_user_ports("Zespol", new_port)
        settings(consol_frame, test_menu_frame)


def printing(box, text):
    box.insert('end', f'{text}\n')
    box.update()
    box.see("end")



def grafic_sygn_connection(frame, nr_sygn, ans):
    if nr_sygn != 5:
        if ans == 1:
            tk.Label(frame, bg="green").place(x=SYGN_PLACES[nr_sygn][0], y=SYGN_PLACES[nr_sygn][1], height=12, width=12)
        else:
            tk.Label(frame, bg="red").place(x=SYGN_PLACES[nr_sygn][0], y=SYGN_PLACES[nr_sygn][1], height=12, width=12)
    else:
        if ans == 1:
            tk.Label(frame, bg="green").place(x=SYGN_PLACES[nr_sygn][0][0], y=SYGN_PLACES[nr_sygn][0][1], height=12, width=12)
            tk.Label(frame, bg="green").place(x=SYGN_PLACES[nr_sygn][1][0], y=SYGN_PLACES[nr_sygn][1][1], height=12, width=12)
            tk.Label(frame, bg="green").place(x=SYGN_PLACES[nr_sygn][2][0], y=SYGN_PLACES[nr_sygn][2][1], height=12, width=12)
        else:
            tk.Label(frame, bg="red").place(x=SYGN_PLACES[nr_sygn][0][0], y=SYGN_PLACES[nr_sygn][0][1], height=12, width=12)
            tk.Label(frame, bg="red").place(x=SYGN_PLACES[nr_sygn][1][0], y=SYGN_PLACES[nr_sygn][1][1], height=12, width=12)
            tk.Label(frame, bg="red").place(x=SYGN_PLACES[nr_sygn][2][0], y=SYGN_PLACES[nr_sygn][2][1], height=12, width=12)


def grafic_out_connection(frame, nr_sygn, ans):
    if ans == 1:
        tk.Label(frame, bg="green").place(x=OUT_PLACES[nr_sygn][0][0], y=OUT_PLACES[nr_sygn][0][1], height=12, width=12)
        tk.Label(frame, bg="green").place(x=OUT_PLACES[nr_sygn][1][0], y=OUT_PLACES[nr_sygn][1][1], height=12, width=12)
    else:
        tk.Label(frame, bg="red").place(x=OUT_PLACES[nr_sygn][0][0], y=OUT_PLACES[nr_sygn][0][1], height=12, width=12)
        tk.Label(frame, bg="red").place(x=OUT_PLACES[nr_sygn][1][0], y=OUT_PLACES[nr_sygn][1][1], height=12, width=12)

if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("1300x880+0+0")
    root.title("Tester EOP")
    root.resizable(False, False)
                    # Background frame
    root.main_background = tk.PhotoImage(file=".\\images\\bg.png")
    root.image_panel = tk.Label(root, image =root.main_background)
    root.image_panel.place(x=-2, y=0)
    consol_frame = tk.Frame(root, bg="#ffffff")
    consol_frame.place(x=150, y=202, height=620, width=1000)
    test_menu_frame = tk.Frame(root, bg='#ffffff')
    test_menu_frame.place(x=396, y=124, height=65, width=565)




     #TEster frame
    menu_frame = tk.Frame(root, bg='#ffffff')
    menu_frame.place(x=25, y=30, height=75, width=900)
    home_button = tk.Button(menu_frame,  text='Informacje',command=lambda: home(consol_frame, test_menu_frame), font=('Arial', 12, " bold"), fg='#0b2540',bg="white", bd=3 , padx=10, pady=10).place(x=50, y=10)
    test_button = tk.Button(menu_frame, text='Testy zespołów', command=lambda: test_menu(test_menu_frame, consol_frame), font=('Arial', 12, " bold"), fg='#0b2540',bg="white", bd=3, padx=10, pady=10).place(x=185, y=10)
    settings_button = tk.Button(menu_frame, text='Ustawienia', command=lambda: settings(consol_frame, test_menu_frame),font=('Arial', 12, " bold"), fg='#0b2540', bg="white", bd=3, padx=10, pady=10).place(x=355, y=10)

    root.mainloop()