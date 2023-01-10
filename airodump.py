#!/usr/bin/python3
import socket
import struct
import time
import curses
import sys

def main(stdscr):
    i = 1
    bssid_list = []
    beacon_val_list = [] # beacon 값 넣을 변수
    try:
        while True:
            # Color
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_WHITE,  curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_CYAN,   curses.COLOR_BLACK)
        
            # 윗 줄 Print
            stdscr.addstr(0, 0, "BSSID ", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(0, 15, "PWR", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(0, 25,"Beacons", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(0, 35,"CH", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(0, 45,"ESSID", curses.color_pair(3) | curses.A_BOLD)
            

            inter_name = sys.argv[1] # interface name 실행 시 넘겨주기

            # 패킷 받아오기
            rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            rawSocket.bind((inter_name,0))
            packet = rawSocket.recvfrom(2048)
            beacon_f = struct.unpack('!H', packet[0][24:26])
            
            #BSSID
            if (beacon_f[0]) == 32768:
                bssid_name = packet[0][40:46] #BSSID
                # stdscr.addstr(i,0,bssid_name.hex()) # BSSID 출력
                if bssid_name.hex() not in bssid_list:

                    bssid_list.append(bssid_name.hex())

                    a = bssid_name.hex() 
                    bssid_index = int(bssid_list.index(a)) # BSSID LIST Index 값

                    stdscr.addstr(bssid_index+1,0,bssid_name.hex()) # BSSID 출력

                    beacon_val_list.append(1)
                    stdscr.addstr(bssid_index+1, 25, str(beacon_val_list[bssid_index])) # beacon 출력 

                    #PWR
                    pwr_val = struct.unpack('b', packet[0][18:19])
                    stdscr.addstr(bssid_index+1,15,str(pwr_val[0]))  # PWR 출력

                    #ESSID
                    ssid_len = struct.unpack('!H', (b'\x00' + packet[0][61:62])) #ESSID 길이
                    ssid_name = packet[0][62:ssid_len[0] + 62]
                    if ssid_len[0] == 0:
                        stdscr.addstr(bssid_index+1,45,'length:   0')
                    if ssid_len[0] != 0:
                        stdscr.addstr(bssid_index+1,45,ssid_name.decode('utf-8')) # ESSID 출력

                    #CH
                    support_rate_len = struct.unpack('!H', (b'\x00' + (packet[0][(ssid_len[0] + 62+1):(ssid_len[0] + 62 + 2)])))
                    test = ssid_len[0] + 62 + 1 + support_rate_len[0]

                    ch_val_len = struct.unpack('!H', (b'\x00' + packet[0][test+2:test+3]))
                    ch_val = struct.unpack(ch_val_len[0]*'b',packet[0][test+3:ch_val_len[0] + test+3])
                    stdscr.addstr(bssid_index+1,35,str(ch_val[0]))  # ch 출력

                if bssid_name.hex() in bssid_list:
                    a = bssid_name.hex() 
                    bssid_index = int(bssid_list.index(a)) # BSSID LIST Index 값
                
                    # beacon 값 더해서 출력
                    stdscr.addstr(bssid_index+1, 25, str(beacon_val_list[bssid_index]))
                    beacon_val_list[bssid_index] = beacon_val_list[bssid_index]+1 # 

                    #PWR
                    pwr_val = struct.unpack('b', packet[0][18:19])
                    stdscr.addstr(bssid_index+1,15,str(pwr_val[0]))  # PWR 출력

                i = i + 1 
                
                stdscr.refresh()

    except KeyboardInterrupt: # Ctrl + C 종료
        print('End')
 
if __name__ == "__main__":
    curses.wrapper(main)
