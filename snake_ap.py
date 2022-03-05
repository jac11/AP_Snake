#!/usr/bin/env python3

import os 
import sys
import time
import subprocess
from subprocess import PIPE
import argparse


if os.geteuid() != 0 :
   print("\n[+] Run as root or sudo ")
   exit()
else:
    pass
Curent_dir  = os.path.abspath(os.getcwd())
user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]

class Fake_access_point:
     
      def __init__(self):
          self.args_Control()
          self.Show_ap_all()
          self.Clean_IP_Table()
          self.Create_Fake()
          self.Create_File_hostapd()     
          self.Create_dns_masq()        
          self.Start_InterFace()
          self.call_tremmial()

      def Show_ap_all(self):
          if self.args.show:
              from Snake_Package.Show_AP import  Show_AP_all
              run = Show_AP_all()
              exit()    
      def Clean_IP_Table(self):
          Table_Flush = [
           
                            "sudo iptables -D FORWARD --in-interface wlan0mon -j ACCEPT"
                       ]
          for _ in Table_Flush :
              call_termminal = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
              time.sleep(0.30)      
      def Create_Fake (self):
         
          ifconfig_command  = [   
                                  
                              # "sudo service NetworkManager stop" ,
                               #"sudo service NetworkManager start ",
                               #"sudo ifconfig wlan0 down",
                               #"sudo iwconfig wlan0mon mode Monitor"
                               #"sudo ifconfig wlan0 up ",
                               "sudo airmon-ng start "
                                #"sudo ifconfig wlan0 down",
                                #"sudo iwconfig wlan0 mode Monitor ",
                                #"sudo ifconfig wlan0 up"
                                                           
                              ]
          for _ in  ifconfig_command :
             call_termminal = subprocess.call( _ +f'{self.args.Interface}',shell=True,stderr=subprocess.PIPE,stdout=PIPE) 
             time.sleep(2)
          print("[+] Interface is in monitor Mode")
      def Create_File_hostapd(self):
              if os.path.exists(Curent_dir+"/Snake_config/") :
                 pass
              else:                 
                   os.mkdir(Curent_dir+"/Snake_config/") 
                   group  = "chown "+ user_name+ ":"+user_name +" *" 
                   os.system(group)             
                   print("access dir config is create " )                   
                   with open ('/etc/hostapd/hostapd.conf','w') as pathconfig :
                       pathconfig.write("DAEMON_CONF="+Curent_dir+"/Snake_config/hostapd.conf")               
              os.chdir(os.path.dirname(__file__)+"/Snake_config/")              
              with open("./hostapd.conf",'w') as config_hostapd :
                    if self.args.APName :
                       ssid_AP = self.args.APName
                    else:
                        ssid_AP = 'Free-Wifi'
                    config_hostapd.write(
                                          'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                          "driver=nl80211"+'\n'\
                                          "ssid="+ssid_AP+'\n'\
                                          "hw_mode=g"+'\n'\
                                          "channel=11"+'\n'\
                                          "macaddr_acl=0"+'\n'\
                                          "ignore_broadcast_ssid=0"+"\n"\
                                         )  
              group  = "chown "+ user_name+ ":"+user_name +" ./hostapd.conf" 
              os.system(group)           
      def Create_dns_masq(self):
              with open(os.path.dirname(__file__)+"/Snake_config/dnsmasq.conf",'w') as dnsmasq:
                   dnsmasq.write(
                                   'interface='+f'{self.args.Interface}'+'mon'+'\n'\
                                   "dhcp-range=192.168.1.2, 192.168.1.30,255.255.255.0, 12h"+'\n'\
                                   "dhcp-option=3, 192.168.1.1"+'\n'\
                                   "dhcp-option=6, 192.168.1.1"+'\n'\
                                   "server= 208.67.220.220"+'\n'\
                                   "log-queries"+'\n'\
                                   "log-dhcp"+"\n"\
                                   "listen-address= 127.0.0.1"+'\n'                                
                                )  
              group  = "chown "+ user_name+ ":"+user_name +" "+ os.path.dirname(__file__)+"/Snake_config/dnsmasq.conf" 
              os.system(group) 
      def Start_InterFace(self):
          all_Interface = os.listdir('/sys/class/net/') 
          for interface in all_Interface :
              try:  
                 command = 'ping -I '+f'{interface}'+' -w1 www.google.com  >/dev/null 2>&1 '   
                 communicate = os.system(command) 
                 if communicate  == 0 :
                    break          
              except Exception  :
                continue                      
          Set_Up_access_point = [
                                  "ifconfig "+f'{self.args.Interface}'+'mon'+" up 192.168.1.1 netmask 255.255.255.0",
                                  "route add -net 192.168.1.0 netmask 255.255.255.0 gw\
                                   192.168.1.1",
                                  "iptables --table nat --append POSTROUTING\
                                   --out-interface "+interface+" -j MASQUERADE",
                                  "iptables --append FORWARD --in-interface "+f'{self.args.Interface}'+"mon\
                                   -j ACCEPT",
                                  "echo 1 > /proc/sys/net/ipv4/ip_forward",
                                ]
                                         
          for _ in Set_Up_access_point :
              call_termminal = subprocess.call( _ ,shell=True,stderr=subprocess.PIPE,stdout=PIPE)
      def call_tremmial(self):
             subprocess.call(["chmod +x "+Curent_dir+"/Snake_Package/Host_apd.py"],shell=True)
             order = Curent_dir+"/Snake_Package/Host_apd.py"             
             command_proc = ' gnome-terminal  -e ' +'"' + order  +'"'                  
             call_termminal = subprocess.call(command_proc,shell=True,stderr=subprocess.PIPE)              
     
             order2 = "dnsmasq -C dnsmasq.conf -d"
             command_proc2 = ' gnome-terminal  -e ' +'"' + order2 +'"'               
             call_termminal = subprocess.call(command_proc2,shell=True,stderr=subprocess.PIPE)

      def args_Control(self):
            parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
            parser.add_argument( '-I',"--Interface" ,metavar='' , action=None,required = True  )               
            parser.add_argument(  "--show", action='store_true'  )
            parser.add_argument( '-AP',"--APName" ,metavar='' , action=None )
            self.args = parser.parse_args()
            if len(sys.argv)> 1 :
                 pass
            else:
                 parser.print_help()
                 exit()                   
           
   
if __name__=='__main__':
     Fake_access_point()

