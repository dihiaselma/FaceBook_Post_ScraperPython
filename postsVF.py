#I have download this code from https://nocodewebscraping.com/facebook-scraper/
# And I have ameliorated it according to my needs 
import urllib2
import json
import datetime
import csv
import time

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Specify the name of the FAcebook page
page_id = "Page_Name"

#Give your access_token = app_id|app_secret
access_token = "pp_id|app_secret"

#This function get a result from a given url
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
            print "Retrying to connect..."

    return response.read()


#This function return the data of facebook page posts 
def getFacebookPageData(page_id, access_token, num_statuses):

    base = "https://graph.facebook.com/v2.6"
    node = "/%s/posts" % page_id 
    fields = "?fields=message,link,permalink_url,created_time,type,id,application,caption,"+ \
		"description,age_max,age_min,genders,interested_in,interests,relationship_statuses,"+ \
		"from,icon,instagram_eligibility,is_hidden,is_instagram_eligible,is_published,name,object_id,"+ \
		"parent_id,picture,place,source,status_type,story,story_tags,comments.limit(0)."+ \
		"summary(true),shares,reactions.limit(0).summary(true),message_tags,targeting,countries."+ \
		"limit(0).summary(true),locales.limit(0).summary(true),regions.limit(0)."+ \
		"summary(true),cities.limit(0).summary(true),to,updated_time"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters  #the facebook url page posts

    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data

#This function return the diffrent reaction of a post
def getReactionsForStatus(status_id, access_token):   

    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
	    ",reactions.type(NONE).limit(0).summary(total_count).as(none)" \
            ",reactions.type(THANKFUL).limit(0).summary(total_count).as(thankful)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))
     
    return data

#This function get the differents fields of a post(status)
def processFacebookPagePosts(status, access_token):

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else \
            status['message']
    link_name = '' if 'name' not in status.keys() else \
            status['name']
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else \
            status['link']
    status_permalink_url = '' if 'permalink_url' not in status.keys() else \
            status['permalink_url']
    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')    
    status_published = status_published + \
            datetime.timedelta(hours=0) # EST
    status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

    status_update = datetime.datetime.strptime(
            status['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')    
    status_update = status_update + \
            datetime.timedelta(hours=0) # EST
    status_update  = status_update.strftime(
            '%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
##################################################################################
    status_application = '' if 'application' not in status.keys() else \
            status['application']
    status_caption = '' if 'caption' not in status.keys() else \
            status['caption']
    status_description = '' if 'description' not in status.keys() else \
            status['description']
    status_age_max = '' if 'age_max' not in status.keys() else \
            status['age_max']
    status_age_min = '' if 'age_min' not in status.keys() else \
            status['age_min']
    status_genders = '' if 'genders' not in status.keys() else \
            status['genders']
    status_interested_in = '' if 'interested_in' not in status.keys() else \
            status['interested_in']
    status_interests = '' if 'interests' not in status.keys() else \
            status['interests']
    status_relationship_statuses = '' if 'relationship_statuses' not in status.keys() else \
            status['relationship_statuses']
    status_from = '' if 'from' not in status.keys() else \
            status['from']
    status_icon = '' if 'icon' not in status.keys() else \
            status['icon']
    status_instagram_eligibility = '' if 'instagram_eligibility' not in status.keys() else \
            status['instagram_eligibility']
    status_is_hidden = '' if 'is_hidden' not in status.keys() else \
            status['is_hidden']
    status_is_instagram_eligible = '' if 'is_instagram_eligible' not in status.keys() else \
            status['is_instagram_eligible']
    status_is_published = '' if 'is_published' not in status.keys() else \
            status['is_published']
    status_object_id = '' if 'object_id' not in status.keys() else \
            status['object_id']
    status_parent_id = '' if 'parent_id' not in status.keys() else \
            status['parent_id']
    status_picture = '' if 'picture' not in status.keys() else \
            status['picture']
    status_place = '' if 'place' not in status.keys() else \
            status['place']
    status_source = '' if 'source' not in status.keys() else \
            status['source']
    status_status_type = '' if 'status_type' not in status.keys() else \
            status['status_type']
    status_story = '' if 'story' not in status.keys() else \
            status['story']
    status_story_tags = '' if 'story_tags' not in status.keys() else \
            status['story_tags']
    status_message_tags = '' if 'message_tags' not in status.keys() else \
            status['message_tags']
    status_targeting = '' if 'targeting' not in status.keys() else \
            status['targeting']

################################################################################""
    num_countries = 0 if 'countries' not in status else \
            status['countries']['summary']['total_count']
    num_locales = 0 if 'locales' not in status.keys() else \
            status['locales']['summary']['total_count']
    num_regions = 0 if 'regions' not in status.keys() else \
            status['regions']['summary']['total_count']
    num_cities = 0 if 'cities' not in status.keys() else \
            status['cities']['summary']['total_count']
    status_to = '' if 'to' not in status.keys() else \
            status['to']

    num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    
    reactions = getReactionsForStatus(status_id, access_token) if \
            status_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

    num_likes = num_reactions if status_published < '2016-02-24 00:00:00' \
            else num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)
    num_none = get_num_total_reactions('none', reactions)
    num_thankful = get_num_total_reactions('thankful', reactions)

    # Return a tuple of all processed data
    return (status_id, status_message, link_name, status_type,
            status_link, status_permalink_url, status_published,status_update, status_application,
            status_caption,status_description,status_age_max, status_age_min,status_genders,
            status_interested_in, status_interests, status_relationship_statuses, status_from,
            status_icon, status_instagram_eligibility, status_is_hidden, status_is_instagram_eligible,
            status_is_published, status_object_id, status_parent_id, status_picture, status_place,
            status_source, status_status_type, status_story, status_story_tags, status_message_tags,
            status_targeting, num_countries, num_locales, num_regions, num_cities, status_to,
            num_reactions,num_comments, num_shares, num_likes, num_loves, 
            num_wows, num_hahas, num_sads, num_angrys,num_none,num_thankful)

#This fucntion read the results and writes them in a csv file,
def scrapeFacebookPagePosts(page_id, access_token):
    with open('%s_facebook_posts.csv' % page_id, 'wb') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", "status_type",
            "status_link", "status_permalink_url", "status_published","status_update", "status_application",
            "status_caption","status_description","status_age_max", "status_age_min","status_genders",
            "status_interested_in", "status_interests", "status_relationship_statuses", "status_from",
            "status_icon", "status_instagram_eligibility", "status_is_hidden", "status_is_instagram_eligible",
            "status_is_published", "status_object_id", "status_parent_id", "status_picture", "status_place",
            "status_source", "status_status_type", "status_story", "status_story_tags", "status_message_tags",
            "status_targeting", "num_countries", "num_locales","num_regions", "num_cities", "status_to",
            "num_reactions","num_comments", "num_shares", "num_likes", "num_loves", 
            "num_wows", "num_hahas", "num_sads", "num_angrys","num_none","num_thankful"])

        has_next_page = True        
        scrape_starttime = datetime.datetime.now()

        print "Scraping %s Facebook posts of the page: %s\n" % (page_id, scrape_starttime)

        statuses = getFacebookPageData(page_id, access_token, 100)

        while has_next_page:
            for status in statuses['data']:               
                if 'reactions' in status:
                    w.writerow(processFacebookPagePosts(status,access_token))               
                

            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(statuses['paging']['next']))
            else:
                has_next_page = False


        print "\nDone!\n%s Posts Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime)


if __name__ == '__main__':
    scrapeFacebookPagePosts(page_id, access_token)
