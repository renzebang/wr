from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import time
import re
import urllib.error import URLError,HTTPError

page_container=[]
paragraph_container=[]
information_to_sql=[[x for x in range(11)]  for j in range(2500)]

f_m_set=["furnished"]
l_m_set=["laundry in bldg","laundry on site","w/d in unit","w/d hookups"]
p_m_set=["street parking","off-street parking","attached garage","carport","detached garage","valet parking"]
pr_m_set=["private room","no private room"]
pb_m_set=["private bath","no private bath"]

def match(a,b):
   for i in a:
      if i in b:
         return a.index(i)
   return -1


for i in range(25):
   
   req = Request("http://vancouver.craigslist.ca/search/roo?s="+str(100*(i)))
   try:
      response = urlopen(req)
   
   except HTTPError as e:
      print("The server cannot fulfill the request.")
      print("Error code: ",e.code)
      continue
   except URLError as e:
      print("We failed to reach a server")
      print("Reason: ",e.reason)
      continue
   else:
      html = urlopen("http://vancouver.craigslist.ca/search/roo?s="+str(100*(i)))
   
   bsobj = BeautifulSoup(html)
   page_container.append(bsobj)
   i+=1
   
   if i%10 == 0:
      time.sleep(1)
      print("Gaining pages"+str(4*i)+"%\n")

print("Finished!\n")

for p in page_container:
   for i in p.findAll("p"):
      paragraph_container.append(i)

for p in paragraph_container:
   if paragraph_container.index(p)%10==0:
      time.sleep(1)
      print(str(paragraph_container.index(p)/25)+"%\n")  
   lk = p.findAll("a",{"class":"hdrlnk"})[0].attrs['href']
   
   req = Request("http://vancouver.craigslist.ca" + lk)
   try:
      response = urlopen(req)

   except HTTPError as e:
      print("The server cannot fulfill the request.")
      print("Error code: ",e.code)
      continue
   except URLError as e:
      print("We failed to reach a server")
      print("Reason: ",e.reason)
      continue
   else:
      html = urlopen("http://vancouver.craigslist.ca" + lk)

   bsobj = BeautifulSoup(html)

   information_to_sql[paragraph_container.index(p)][0] = lk  

   information_to_sql[paragraph_container.index(p)][1] = p.findAll("a",{"class":"hdrlnk"})[0].next
   
   a = p.findAll("span",{"class":"price"})
   if len(a)==0:
      information_to_sql[paragraph_container.index(p)][2] = None
   else:
      a=a[0].next
      b = a[(a.index('$')+1):]
      information_to_sql[paragraph_container.index(p)][2] = int(b)

   a = p.findAll("span",{"class":"housing"})
   if (len(a)==0):
      information_to_sql[paragraph_container.index(p)][3] = None
   else:    
      b = a[0].next
      m =re.search('[0-9]+',b)
      if type(m) is None:
         information_to_sql[paragraph_container.index(p)][3] = None
      else:
         information_to_sql[paragraph_container.index(p)][3] = int(m.group(0))
  
   a = bsobj.findAll("div",{"class":"viewposting"})
   
   if (len(a)==0):
      information_to_sql[paragraph_container.index(p)][4] = None
      information_to_sql[paragraph_container.index(p)][5] = None

   else:
      information_to_sql[paragraph_container.index(p)][4] = a[0].attrs['data-latitude']
      information_to_sql[paragraph_container.index(p)][5] = a[0].attrs['data-longitude']
   
   list = []
  
   a = bsobj.findAll("p",{"class":"attrgroup"})
   if(len(a)==0): 
      information_to_sql[paragraph_container.index(p)][6] = None
      information_to_sql[paragraph_container.index(p)][7] = None
      information_to_sql[paragraph_container.index(p)][8] = None
      information_to_sql[paragraph_container.index(p)][9] = None
      information_to_sql[paragraph_container.index(p)][10] = None   

   else:
      a = a[1].findAll("span")
      for i in range(len(a)):
         list.append(a[i].next)
   
      information_to_sql[paragraph_container.index(p)][6] = match(f_m_set,list)
      information_to_sql[paragraph_container.index(p)][7] = match(l_m_set,list)
      information_to_sql[paragraph_container.index(p)][8] = match(p_m_set,list)
      information_to_sql[paragraph_container.index(p)][9] = match(pr_m_set,list)
      information_to_sql[paragraph_container.index(p)][10] = match(pb_m_set,list)