from Drive import *

if __name__ == "__main__":
    address = "192.168.21.161"
    d = DriveClient(ip = address)
    # d = DriveClientPWM(ip = address)
    while(1):
        d.drive()
