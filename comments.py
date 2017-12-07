#I have download this code from https://nocodewebscraping.com/facebook-scraper/
# And I have ameliorated it according to my needs 

import urllib2
import json
import datetime
import csv
import time


file_id ="page_name"

#access_token = app_id + "|" + app_secret
access_token = "app_id|app_secret"

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

            if '400' in str(e):
                return None;

    return response.read()

#This function returns the result on a json format
def getFacebookCommentFeedData(status_id, access_token, num_comments):

    # Construct the URL string
        base = "https://graph.facebook.com/v2.6"
        node = "/%s/comments" % status_id 
        fields = "?fields=id,message,like_count,created_time,comments,from,attachment"
        parameters = "&order=chronological&limit=%s&access_token=%s" % \
                (num_comments, access_token)
        url = base + node + fields + parameters

        # retrieve data
        data = request_until_succeed(url)
        if data is None:
            return None
        else:   
            return json.loads(data)

#this function returns the differnt fiels of a given comment 
def processFacebookComment(comment, status_id, parent_id = ''):    

    comment_id = comment['id']
    comment_message = '' if 'message' not in comment else \
            unicode_normalize(comment['message'])
    comment_author = unicode_normalize(comment['from']['name'])
    comment_likes = 0 if 'like_count' not in comment else \
            comment['like_count']

    if 'attachment' in comment:
        attach_tag = "[[%s]]" % comment['attachment']['type'].upper()
        comment_message = attach_tag if comment_message is '' else \
                (comment_message.decode("utf-8") + " " + \
                        attach_tag).encode("utf-8")

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    comment_published = datetime.datetime.strptime(comment['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    comment_published = comment_published + datetime.timedelta(hours=0) # EST
    comment_published = comment_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

    # Return a tuple of all processed data

    return (comment_id, status_id, parent_id, comment_message, comment_author,
            comment_published, comment_likes)

#This function browse the result and decorticate it into comments then stores them in a csv file
def scrapeFacebookPageFeedComments(page_id, access_token):
    with open('facebook_comments.csv', 'wb') as file:
        w = csv.writer(file)
        w.writerow(["comment_id", "status_id", "parent_id", "comment_message", 
            "comment_author", "comment_published", "comment_likes"])

        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        print "Scraping Comments From Posts"

        with open('facebook_statuses.csv' % file_id, 'rb') as csvfile:  #specify the name of the file containing the posts (give the url of the file)
            reader = csv.DictReader(csvfile)         

            for status in reader:
                has_next_page = True

                comments = getFacebookCommentFeedData(status['status_id'], 
                        access_token, 100)

                while has_next_page and comments is not None:				
                    for comment in comments['data']:
                        w.writerow(processFacebookComment(comment, 
                            status['status_id']))

                        if 'comments' in comment:
                            has_next_subpage = True

                            subcomments = getFacebookCommentFeedData(
                                    comment['id'], access_token, 100)

                            while has_next_subpage:
                                for subcomment in subcomments['data']:                                    
                                    w.writerow(processFacebookComment(
                                            subcomment, 
                                            status['status_id'], 
                                            comment['id']))

                                    num_processed += 1
                                    if num_processed % 1000 == 0:
                                        print "%s Comments Processed: %s" % \
                                                (num_processed, 
                                                    datetime.datetime.now())

                                if 'paging' in subcomments:
                                    if 'next' in subcomments['paging']:
                                        subcomments = json.loads(
                                                request_until_succeed(
                                                    subcomments['paging']\
                                                               ['next']))
                                    else:
                                        has_next_subpage = False
                                else:
                                    has_next_subpage = False

                        # output progress occasionally to make sure code is not
                        # stalling
                        num_processed += 1
                        if num_processed % 1000 == 0:
                            print "%s Comments Processed: %s" % \
                                    (num_processed, datetime.datetime.now())

                    if 'paging' in comments:		
                        if 'next' in comments['paging']:
                            comments = json.loads(request_until_succeed(
                                        comments['paging']['next']))
                        else:
                            has_next_page = False
                    else:
                        has_next_page = False


        print "\nDone!"

if __name__ == '__main__':
    scrapeFacebookPageFeedComments(file_id, access_token)
