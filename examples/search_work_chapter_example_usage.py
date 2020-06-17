from ao3.search import search
from ao3.chapter import Chapter
from ao3 import users, AO3

"""
	Originally for testing but can be used for an example how to use the new additions
"""

##
### api test
##

#api = AO3()
#api.login("username","password")	#needs username & password added

##
### searches
##

#test = search("Undertale (Video Game)") #, api.user.sess)	#searches for undertale w/our session
#test = search("Excel Saga")								#searches for excel saga
#test = search("Kustard")									#specific tag search
#test = search("AAAA")										#uncategorized tag search
#test = search("Ergo Proxy (Anime)")						#searches for ergo proxy

#res = test.get_result()									#the search result

##
### result testing - metrics & page movement
##

#print(res.current_page)
#res.last_page()
#print(res.current_page)
#print(res.num_pages)

##
### chapter testing
##

#ch = Chapter("5191202")					#retrieves a chapter - WORK ID should be given, starts on first chapter

##
### general chapter data
##

#print(ch.number)
#print(ch.title)
#print(ch.summary)						#note that this retrieves chapter & not the work summary

##
### obtaining chapter text
##

"""
print(ch.text)
while ch.next_chapter():
	print(ch.text)
"""
	
##
### work/worlist testing
##

#TRY NOT TO USE
#works = res.get_all_works()				#retrieves a work list DEPRECATED - TOO HEAVY, HIGH LOAD TIMES
#wrk = works.next_work						#retrieves a work from the work list 

#LESS LOAD TIMES, VERY SIMILAR USAGE
#works = res.get_work_iterator()
#wrk = works.next_work()


##
### obtaining information from all resulting works
##

"""
while (not (wrk is None)):
	print(wrk.id)
	wrk = works.next_work
"""