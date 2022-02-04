from multiprocessing import AuthenticationError
import imaplib
import email
import test
import os
from utilities import load


__author__ = "Siddharth Achari Sharabu"


username = input("Enter the GmailAddress:\t")
password = input('Enter the App password of your Gmail Address :\t')
imap = imaplib.IMAP4_SSL("imap.gmail.com")

try :
   result = imap.login(username, password)
   select = int(input("Enter which Messages to select\n1.Inbox \n2.Unseen\nSelect any Option :\t"))
   num = int(input("Enter the Number of Messages to Classify\n"))
   os.mkdir("Output")
   if select == 1 :
      response, messages = imap.select('Inbox')
      messages = messages[0].split()
      f=open("Output/Inboxmails.txt",'w+')
      for i in range(1,num+1):
         res, msg = imap.fetch(str(i), "(RFC822)")         
         for response in msg :
            if isinstance(response, tuple):
               msg = email.message_from_bytes(response[1])
               classify = test.get_predictions(msg["Subject"])
               f.write("\n")
               f.write("From :\t"+str(msg["From"]))
               f.write("\n")
               f.write("Date :\t"+str(msg["date"]))
               f.write("\n")
               f.write("Sub :\t"+str(msg['Subject']))
               f.write("\n")
               f.write("Classification :\t"+str(classify))
               f.write("\n")
               f.write("**********************************************************")
               f.write("\n")
      load()

   elif select == 2 :
      imap.select('"[Gmail]/All Mail"', readonly = True)
      response, messages = imap.search(None,'Unseen')
      messages = messages[0].split()
      latest = int(messages[-1])
      oldest = int(messages[0])
      f =open("Output/Unseenmails.txt",'w+')
      for i in range(latest, latest-num, -1):
         res, msg = imap.fetch(str(i), "(RFC822)")         
         for response in msg :
            if isinstance(response, tuple):
               msg = email.message_from_bytes(response[1])
               classify = test.get_predictions(msg["Subject"])
               f.write("\n")
               f.write("From :\t"+str(msg["From"]))
               f.write("\n")
               f.write("Date :\t"+str(msg["date"]))
               f.write("\n")
               f.write("Sub :\t"+str(msg['Subject']))
               f.write("\n")
               f.write("Classification :\t"+str(classify))
               f.write("\n")
               f.write("*********************************************************")
               f.write("\n")
      load()
   else :
      print("please Select Valid Option")
except :
   AuthenticationError
