#!/usr/bin/python
import urllib2
import simplejson as json
import smtplib
import datetime 
from optparse import OptionParser 
import subprocess

def test(abc):
	SMTP_SERVER = 'smtp.gmail.com'
	SMTP_PORT = 587
	 
	sender = 'tehn.yit.chin@gmail.com'
	recipient = 'tehn.yit.chin@gmail.com'
	subject = 'Gmail SMTP Test'
	body = 'blah blah blah'
	 
	"Sends an e-mail to the specified recipient."
	 
	body = "" + body + abc + ""
	 
	headers = ["From: " + sender,
		   "Subject: " + subject,
		   "To: " + recipient,
		   "MIME-Version: 1.0",
		   "Content-Type: text/html"]
	headers = "\r\n".join(headers)
	 
	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	 
	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(sender, 'chillout123')
	 
	session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
	session.quit()
	return None

parser = OptionParser()
parser.add_option("-l", "--limits", dest="limits", help="max number of queries to get")

(options, args)=parser.parse_args()

if options.limits != None:
	limit = int(options.limits)
else:
	limit = 30
print "Getting " + str(limit) + " number of articles"

search_base_url = 'http://api.thriftdb.com/api.hnsearch.com/items/_search?limit='
start = 0
sort_by = 'create_ts+desc'

base_url_orig = "http://api.thriftdb.com/api.hnsearch.com/items/_search?limit=30&sortby=create_ts+desc&q=%22Show+HN%22&weights[title]=1.1&weights[text]=0.7&weights[domain]=2.0&weights[username]=0.1&weights[type]=0.0&boosts[fields][points]=0.15&boosts[fields][num_comments]=0.15&boosts[functions][pow(2,div(div(ms(create_ts,NOW),3600000),72))]=200.0&pretty_print=true"

prefix_url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?limit="
post_url = "&sortby=create_ts+desc&q=%22Show+HN%22&weights[title]=1.1&weights[text]=0.7&weights[domain]=2.0&weights[username]=0.1&weights[type]=0.0&boosts[fields][points]=0.15&boosts[fields][num_comments]=0.15&boosts[functions][pow(2,div(div(ms(create_ts,NOW),3600000),72))]=200.0&pretty_print=true"  

base_url = prefix_url + repr(limit) 
base_url = base_url + "&start=" + repr(start) + post_url

req = urllib2.Request(base_url)
opener = urllib2.build_opener()
f = opener.open(req)
json_obj = json.load(f)

# get the filename
filename = datetime.datetime.now().strftime("%Y%m%d")
filename = str(filename) + "_from_hnsearch.csv"
output_file = open(filename, "w")

# print out each line that is not in the file
output_file.write("create_ts,title,url,id,hn_discussion\n")
for title in json_obj["results"]:
	string = title["item"]["create_ts"]
	string = string + ","
	
	if title["item"]["title"] != "":
		string = string + "\""
		string += repr(title["item"]["title"] )
		string = string + "\""
	else:
		string += repr("") 
	string = string + ","

	if title["item"]["url"] != "":
		string = string + "\""
		string += repr(title["item"]["url"] )
		url_string = str(title["item"]["url"])
		string = string + "\""
	else:
		string += repr("")
	string = string + ","
	
	string += repr(title["item"]["id"]) 
	string += ","
	
	string = string + "\""
	string += "http://news.ycombinator.com/item?id="
	string += repr(title["item"]["id"]) 
	string = string + "\""
 
	output_file.write(string+"\n")
	if url_string != "":
		itemid_string=repr(title["item"]["id"])
		params = ["./get_shot.py", "--url="+url_string]
		exitcode = subprocess.call("./get_shot.py --id="+itemid_string+" --url="+url_string, shell=True)

output_file.close()

#title_abc = "fatdog"
#url = "google.com"
#url_text = "google.com"
#id_abc=repr(123)
#html_message =  "<p><font face='Arial, Helvetica, sans-serif'><b>Project :</b>" + title_abc + "</font></p>";
#html_message += "<p><font face='Arial, Helvetica, sans-serif'><b>Where:</b>&nbsp;</font>" ;
#html_message += "<a href=" + url + " style='color: #1155cc;' target=''><font face='Arial, Helvetica, sans-serif'>" + url_text + "</font></a></p>";
#html_message += "<p><font face='Arial, Helvetica, sans-serif'><b>Tagline :</b>" + title_abc + "</font></p>";
#html_message += "<p><p><a href=http://news.ycombinator.com/item?id=" + id_abc + " style='color: #1155cc;' target='_blank'><font face='Arial, Helvetica, sans-serif'>HN Discussions</font></a></p>";  
#test(html_message)
