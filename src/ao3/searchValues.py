from abc import ABC, abstractmethod
from urllib.parse import quote_plus

"""
	Classes that are used to define searches and create a search url
	
	for bugs please mention: lambricm
"""

class Search_Values(ABC):

	def __init__():
		pass
		
	@abstractmethod
	def toString(data_in):
		return ""

class Sort_By(Search_Values):
	AUTHOR = 'authors_to_sort_on'
	TITLE = 'title_to_sort_on'
	DATE_POSTED = 'created_at'
	DATE_UPDATED = 'revised_at'
	WORD_COUNT = 'word_count'
	HITS = 'hits'
	KUDOS = 'kudos_count'
	COMMENTS = 'comments_count'
	BOOKMARKS = 'bookmarks_count'
	
	def toString(type):
		return "&work_search%5Bsort_column%5D=" + type
			
class Ratings(Search_Values):
	TEEN_AND_UP = 'Teen And Up Audiences'
	GENERAL_AUDIENCES = 'General Audiences'
	EXPLICIT = 'Explicit'
	MATURE = 'Mature'
	NOT_RATED = 'Not Rated'
	
	def to_id(type):
		if type == TEEN_AND_UP:
			return '11'
		elif type == GENERAL_AUDIENCES:
			return '10'
		elif type == EXPLICIT:
			return '13'
		elif type == MATURE:
			return '12'
		elif type == NOT_RATED:
			return '9'
		
	def toString(type):
		if type == None:
			return ""
		else:
			return "&work_search%5Brating_ids%5D%5B%5D=" + to_id(type)
			
class Complete(Search_Values):
	
	def toString(complete):
		if complete:
			return "&work_search%5Bcomplete%5D=1"
		else:
			return "&work_search%5Bcomplete%5D=0"
		
class Warnings(Search_Values):
	NO_WARNINGS = 'No Archive Warnings Apply'
	CREATOR_DIDNT_USE = 'Creator Chose Not To Use Archive Warnings'
	VIOLENCE = 'Graphic Depictions Of Violence'
	MAJOR_CHAR_DEATH = 'Major Character Death'
	RAPE_NON_CON = 'Rape/Non-Con'
	UNDERAGE = 'Underage'
	
	def to_id(type):
		if type == NO_WARNINGS:
			return '16'
		elif type == CREATER_DIDNT_USE:
			return '14'
		elif type == VIOLENCE:
			return '17'
		elif type == MAJOR_CHAR_DEATH:
			return '19'
		elif type == RAPE_NON_CON:
			return '20'
	
	def toString(warnings):
		ret = ""
		
		for warning in warnings:
			ret = ret + "&warning_ids%5D%5B%5D=" + to_id(warning)
			
		return ret

class Categories(Search_Values):
	GEN = 'Gen'
	FF = 'F/F'
	FM = 'F/M'
	MM = 'M/M'
	MULTI = 'Multi'
	OTHER = 'Other'
	
	def to_id(type):
		if type == GEN:
			return '21'
		elif type == FF:
			return '116'
		elif type == FM:
			return '16'
		elif type == MM:
			return '23'
		elif type == MULTI:
			return '2246'
		elif type == OTHER:
			return '24'
		
	def toString(categories):
		ret = ""
		
		for category in categories:
			ret = ret + "&work_search%5Bcategory_ids%5D%5B%5D=" + to_id(category)

		return ret
		
#used for fandom ids
class Fandoms(Search_Values):

	def toString(fandoms):
		ret = ""
		
		for fandom in fandoms:
			ret = ret + "&work_search%5Bfandom_ids%5D%5B%5D=" + fandom
		
		return ret

#used for character ids
class Characters(Search_Values):
	
	def toString(characters):
		ret = ""
		
		for character in characters:
			ret = ret + "&work_search%5Bcharacter_ids%5D%5B%5D=" + character
		
		return ret
		
#used for relationship ids
class Relationships(Search_Values):
	
	def toString(relationships):
		ret = ""
		
		for relationship in relationships:
			ret = ret + "&work_search%5Brelationship_ids%5D%5B%5D=" + relationship
		
		return ret
		
#should be used for any strings (character/fandom/relationship names along with other general tags)
class Tags(Search_Values):

	def toString(tags):
		ret = ""
	
		if len(tags) > 0:
			ret = "&work_search%5Bother_tag_names%5D=" + quote_plus(tags[0])
		
			for tag in tags.pop[0]:
				ret = ret + "%2C" + quote_plus(tag)
		
		return ret
		
#query string that user can type out
class Query(Search_Values):
	
	def toString(query):
		return "&work_search%5Bquery%5D=" + quote_plus(query)
		
class PageNumber(Search_Values):
	
	def toString(num):
		return "&page=" + str(num)
	
#currently not supporting - don't want to get all the ids manually	
class Language(Search_Values):
	
	def toString():
		return "&work_search%5Blanguage_id%5D="
		
class Date_From(Search_Values):
	
	def toString(date):
		return "&work_search%5Bdate_from%5D=" + date
		
class Date_To(Search_Values):
	
	def toString(date):
		return "&work_search%5Bdate_to%5D=" + date
		
class Tag(Search_Values):
	
	def toString(tag):
		return "&tag_id=" + quote_plus(tag)
	