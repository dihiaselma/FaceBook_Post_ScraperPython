import urllib2
import json
import datetime
import csv
import time

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


page_id = "your page id"

#access_token = page access token
access_token = "the page access token"



def request_until_succeed(url):

    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            print "Error for URL %s: %s" % (url, datetime.datetime.now())
            print "Retrying."

    return response.read()



# Needed to write tricky unicode correctly to csv

def unicode_normalize(text):    
    return text.encode('utf-8')



def getFacebookPageFeedData(page_id, access_token):

    base = "https://graph.facebook.com/"
    node = str(page_id)
    fields = "/threads/?fields=messages{created_time,from,to,message,id}"
    parameters = "&access_token=%s" %access_token

    url = base + node + fields + parameters   

    data = json.loads(request_until_succeed(url))    

    return data



def processFacebookPageFeedStatus(message, access_token,conversation_key):

    conversation_id = conversation_key

    message_body =message['message']
    message_id=message['id']

    message_fromName=message['from']['name']
    message_fromEmail=message['from']['email']
    message_fromId=message['from']['id']
    
    message_toName=message['to']['data'][0]['name']
    message_toEmail=message['to']['data'][0]['email']
    message_toId=message['to']['data'][0]['id']

    message_created_date= datetime.datetime.strptime(message['created_time'],'%Y-%m-%dT%H:%M:%S+0000')   
    message_created_date = message_created_date + datetime.timedelta(hours=0) # EST
    message_created_date = message_created_date.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs


    return (conversation_id,message_id, message_fromName,message_fromEmail,message_fromId, message_created_date, message_body,message_toName,message_toEmail,message_toId)



def scrapeFacebookPageFeedStatus(page_id, access_token):

    with open('Brandt.dz_facebook_messages.csv', 'wb') as file:

        w = csv.writer(file)
        w.writerow(["conversation_id","message_id", "message_fromName","message_fromEmail","message_fromId", "message_created_date", "message_body","message_toName","message_toEmail","message_toId"])


        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()
        print "Scraping %s Facebook massage : %s\n" % (page_id, scrape_starttime)

        statuses = getFacebookPageFeedData(page_id, access_token)

        while has_next_page:
            for status in statuses['data']:
				for message in status['messages']['data']:
               		w.writerow(processFacebookPageFeedStatus(message,access_token,status['id']))                

                num_processed += 1
                if num_processed % 100 == 0:
                    print "%s Statuses Processed: %s" % (num_processed, datetime.datetime.now())

            # if there is no next page, we're done.

            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(statuses['paging']['next']))

            else:
                has_next_page = False


        print "\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token)




