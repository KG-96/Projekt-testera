import serial

FILE = 'Backend\\COMS.txt'

class Port:
    def __init__(self, port):
        self.port=port
        self.baudrate =921600
        self.bytesize=8
        self.parity='N'
        self.stopbits=1
        self.timeout =0
        self.xonxoff =1
        self.rtscts =1

    def __repr__(self):
        print(f"Otwarty {self.port}")

    def create_connection(self):
        con = serial.Serial()
        con.port = self.port
        con.baudrate = self.baudrate
        con.bytesize = self.bytesize
        con.parity = self.parity
        con.stopbits = self.stopbits
        con.timeout = self.timeout
        con.xonxoff = self.xonxoff
        con.rtscts = self.rtscts
        return con


def get_user_ports():
    with open(FILE, 'r') as file:
        ports = [line.strip().split(',') for line in file.readlines()]
        return ports

def set_user_ports(device, port):
    ports = get_user_ports()
    with open(FILE, 'w') as file:
        if device == 'Urzadzenie_testowe':
            file.write(f'{device},COM{port}\nZespol,{ports[1][1]}')
        else:
            file.write(f'Urzadzenie_testowe,{ports[0][1]}\n{device},COM{port}')

def set_slave_ports():
    slave = Port(get_user_ports()[1][1])
    con_s = slave.create_connection()
    return con_s


def set_master_ports():
    master = Port(get_user_ports()[0][1])
    con_m = master.create_connection()
    return con_m







