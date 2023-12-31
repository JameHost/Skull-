from scapy.all import sniff, IP, TCP, UDP , Ether 
from Poto import extract_source_ip, extract_destination_ip, is_tcp_packet, is_udp_packet, is_http_packet, is_icmp_packet , is_dns_packet , extract_source_mac , extract_destination_mac 
from scapy.layers.http import HTTP  
from scapy.layers.inet6 import IPv6 
from scapy.layers.dns import DNS 
from Mylogo import logo
import time
import sys
from prettytable import PrettyTable
import colorama  # เพิ่ม import สำหรับ ANSI escape codes
from colorama import Fore , Style 



GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

table = PrettyTable()
table.field_names = [f"{BOLD}ประเภท{RESET}", f"{BOLD}ผลลัพธ์{RESET}"]

def process_packets(payload):
    # ทำสิ่งที่คุณต้องการกับ payload ที่รับมาที่นี่
    # ตัวอย่าง: แสดง payload ในรูปแบบข้อความและ hex
    payload_text = payload.decode("utf-8", "ignore")
    print(f"Processed Payload (Text):\n{payload_text}")
    payload_hex = ":".join("{:02x}".format(c) for c in payload)
    print(f"Processed Payload (Hex):\n{payload_hex}")
    time.sleep(0.5) 
     
print(logo)  # แสดงโลโก้

# ANSI escape codes for text colors
GREEN = '\033[92m' 
YELLOW = '\033[93m'
RED = '\033[91m'  
RESET = '\033[0m'
MAGENTA = '\033[95m'
BLUE = '\u001b[34m'  
BLACK = '\033[30m' 
BROWN = '\033[90m'


# คำสั่งบอกว่า logo ถูกปริ้นมาเเล้ว 
logo_printed = False

# ฟังก์ชันสำหรับรับแพ็คเก็ต
def packet_callback(packet):
    global logo_printed     # คำสั่งในการขึ้น logo 
    if not logo_printed:  
        print(logo)
        logo_printed = True
    # บอกวันเวลา
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{GREEN}\nDetails Packet :{RESET}")
    print(f"{YELLOW}Time: {current_time}{RESET}")
    print(f"Summary: {packet.summary()}")
    
    # เตรียมข้อมูลสำหรับ table
    data = []

    if IP in packet:
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        data.append([f"{BOLD}Source IP{RESET}", f"{GREEN}{source_ip}{RESET}"])
        data.append([f"{BOLD}Destination IP{RESET}", f"{YELLOW}{destination_ip}{RESET}"])
    elif IPv6 in packet:
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        data.append([f"{BOLD}Source IPv6{RESET}", f"{GREEN}{source_ip}{RESET}"])
        data.append([f"{BOLD}Destination IPv6{RESET}", f"{YELLOW}{destination_ip}{RESET}"])
    else:
        data.append([f"{BOLD}No IP find?{RESET}"])

    if Ether in packet:
        source_mac = extract_source_mac(packet)
        destination_mac = extract_destination_mac(packet)
        data.append([f"{BOLD}Source MAC Address{RESET}", f"{GREEN}{source_mac}{RESET}"])
        data.append([f"{BOLD}Destination MAC Address{RESET}", f"{YELLOW}{destination_mac}{RESET}"])
        
    # เพิ่มข้อมูลอื่น ๆ ตามต้องการ
    
    # แสดงข้อมูลในรูปแบบตาราง
    table.clear_rows()
    for entry in data:
        table.add_row(entry)
    
    print(table)
    time.sleep(0.5)


    if is_tcp_packet(packet):
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        print(f"{YELLOW}TCP packet from {source_ip} to {destination_ip}{RESET}")
        print(f"{MAGENTA}Source Port: {packet[TCP].sport}{RESET}")
        print(f"{MAGENTA}Destination Port: {packet[TCP].dport}{RESET}\n")
        if is_tcp_packet(packet):
           tcp_payload = bytes(packet[TCP].payload)
        print(f"{RED}TCP Payload (Text):\n{tcp_payload[:300].decode('utf-8', 'ignore')}{RESET}")  # แสดงเฉพาะ 300  ไบต์แรกในรูปแบบข้อความ
        # หรือถ้าคุณต้องการแสดงเป็น hex
        payload_hex = ":".join("{:02x}".format(c) for c in tcp_payload)
        print(f"{BROWN}TCP Payload (Hex):\n{payload_hex[:300]}{RESET}")  # แสดงเฉพาะ 300 ตัวแรกในรูปแบบ hex
    
    elif is_udp_packet(packet):
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        print(f"{BLUE}UDP packet from {source_ip} to {destination_ip}{RESET}")   
        if is_udp_packet(packet):
          udp_payload = bytes(packet[UDP].payload)
        print(f"{RED}UDP Payload (Text):\n{udp_payload[:300].decode('utf-8', 'ignore')}{RESET}")  # แสดงเฉพาะ 300 ไบต์แรกในรูปแบบข้อความ
        # หรือถ้าคุณต้องการแสดงเป็น hex
        payload_hex = ":".join("{:02x}".format(c) for c in udp_payload)
        print(f"{BROWN}UDP Payload (Hex):\n{payload_hex[:300 ]}{RESET}")  # แสดงเฉพาะ 300 ตัวแรกในรูปแบบ hex
        
    elif is_http_packet(packet):
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        print(f"{RED}HTTP packet from {source_ip} to {destination_ip}{RESET}")
        if is_http_packet(packet):
           http_payload = bytes(packet[HTTP].payload)
        print(f"{GREEN}HTTP Payload (Text):\n{http_payload[:300].decode('utf-8', 'ignore')}{RESET}")  # แสดงเฉพาะ 300 ไบต์แรกในรูปแบบข้อความ
        # หรือถ้าคุณต้องการแสดงเป็น hex
        payload_hex = ":".join("{:02x}".format(c) for c in http_payload)
        print(f"{GREEN}HTTP Payload (Hex):\n{payload_hex[:300 ]}{RESET}")  # แสดงเฉพาะ 300 ตัวแรกในรูปแบบ hex
    
    elif is_icmp_packet(packet):
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        print(f"{GREEN}ICMP packet from {source_ip} to {destination_ip}{RESET}")
        
    elif is_dns_packet(packet):
        source_ip = extract_source_ip(packet)
        destination_ip = extract_destination_ip(packet)
        print(f"{RED}DNS packet from {source_ip} to {destination_ip}{RESET}")
        if is_dns_packet(packet):
         dns_payload = bytes(packet[DNS].payload)
        print (f"{GREEN}DNS Payload (Text):\n{dns_payload[:300].decode('utf-8', 'ignore')}{RESET}")
        payload_hex = ":".join("{:02x}".format(c) for c in dns_payload)
        print(f"{GREEN}DNS Payload (Hex):\n{payload_hex[:300]}{RESET}")  
        
        
    time.sleep(0.5)
        
# ฟังก์ชันเริ่มหรือหยุดการจับแพ็คเก็ตขึ้นอยู่กับการป้อนข้อมูลของผู้ใช้ ด้วย 1 เเละ 2 ในการใช้คำสั่งใช้งาน
def start_stop_capture():
    while True:
        user_input = input("\033[92mEnter '1.start' to begin packet capture or '2.stop(): \033[0m")
        if user_input.lower() == 'start' or user_input == '1':
            # เริ่มการจับแพ็คเก็ตในโหมดลูปโดยไม่จำกัดจำนวนแพ็คเก็ต
            print("\033[92mStarting packet capture...\033[0m")
            sniff(filter="(tcp or udp or icmp or dns) and host src or (http and port 80)", prn=packet_callback) # fillter ในการsniff ข้อมูล มี tcp udp icmp ตัว host เเละ http 
        elif user_input.lower() == 'stop' or user_input == '2':
            print("\033[92mStopping packet capture.\033[0m")
            break #คำสั่งหยุดเมื่อผู้ใช้ กดออก ด้วย ctrl+c 
        else:
            print("\033[92mInvalid input. Please enter 'start' to begin or 'stop' to stop.\033[0m")
    time.sleep(0.5)

# ขอให้ผู้ใช้เริ่มการจับแพ็คเก็ต
try:
    user_input = input("\033[92mDo you want to start packet capture? (1: yes / 2: no): \033[0m")
    if user_input.lower() == '1'or user_input == 'yes' or user_input == 'y':
        start_stop_capture()
    elif user_input.lower() == '2' or user_input == 'no' or user_input == 'n':
        print("\033[92mPacket capture is not started. You can start it later again'.\033[0m")
except KeyboardInterrupt:
    print("\033[92mExiting the program \nThank you for useing .\033[0m")
    sys.exit(0) 
 

