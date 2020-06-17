from .searchResult import SearchResult
from .searchValues import *

"""
	class that allows user to search with current Ao3 interface
	
	for bugs please mention: lambricm
"""

#object to actually bring all the search options together
class search(object):

	def __init__(self, tag, sess=None, sort_by=Sort_By.DATE_UPDATED, rating=None, complete=False, warnings=[], categories=[], tags=[], query="", page_number=1, date_from="", date_to=""):
		self.set_tag(tag)
		self.set_sort_by(sort_by)
		self.set_rating(rating)
		self.set_complete(complete)
		self.set_warnings(warnings)
		self.set_categories(categories)
		self.set_query(query)
		self.set_tags(tags)
		self.set_page_number(page_number)
		self.set_date_from(date_from)
		self.set_date_to(date_to)
		self.sess = sess
		
	def __repr__(self):
		return str({	"Main tag":self.tag, \
						"Sort by":self.sort_by, \
						"Rating":("Any" if self.rating == None else self.rating),\
						"Complete Only":self.complete, \
						"Warnings":self.warnings, \
						"Categories":self.categories, \
						"Tags":self.tags, \
						"Query":self.query \
					})
			
	#SEARCH CHANGE METHODS
			
	def set_tag(self, tag):
		self.tag = tag
			
	def set_sort_by(self, sort_by):
		self.sort_by = sort_by
		
	def set_rating(self, rating):
		self.rating = rating
		
	def set_complete(self, type):
		self.complete = type
		
	def set_query(self, query):
		self.query = query
		
	def remove_query(self):
		self.query = ""
		
	def set_warnings(self, warnings):
		self.warnings = warnings
		
	def add_warning(self, warning):
		add_val(self.warnings, warning)
			
	def remove_warning(self, warning):
		remove_val(self.wrnings, warning)
		
	def set_categories(self, categories):
		self.categories = categories
		
	def add_categories(self, categories):
		add_val(self.categories, categories)
			
	def remove_categories(self, categories):
		remove_val(self.categories, categories)
		
	def set_tags(self, tags):
		self.tags = tags
		
	def add_tag(self, tag):
		add_val(self.tags, tag)
			
	def remove_tag(self, tag):
		remove_val(self.tags, tag)
		
	def add_val(lst, to_add):
		lst.append(to_add)
	
	def remove_val(lst, to_rm):
		if to_rm in lst:
			lst.remove(to_rm)
			
	def set_page_number(self, num):
		self.page_number = num
		
	#use date format "YYYY-MM-DD" or "" to clear
	def set_date_from(self, date_from):
		self.date_from = date_from
	
	#use date format "YYYY-MM-DD" or "" to clear
	def set_date_to(self, date_to):
		self.date_to = date_to
		
	#retrieves the URL for the search
	def get_url(self):
		url = 	"https://archiveofourown.org/works?utf8=%E2%9C%93&commit=Sort+and+Filter" \
			+	PageNumber.toString(self.page_number) \
			+	Sort_By.toString(self.sort_by) \
			+	Ratings.toString(self.rating) \
			+	Complete.toString(self.complete) \
			+	Warnings.toString(self.warnings) \
			+	Categories.toString(self.categories) \
			+	Date_To.toString(self.date_to) \
			+	Date_From.toString(self.date_from) \
			+ 	Tags.toString(self.tags) \
			+ 	Query.toString(self.query)\
			+	Tag.toString(self.tag)
			
		return url
		
	#returns a SearchResult object so that we can actually investigate the search
	def get_result(self):
		return SearchResult(self, self.sess)._page_type()