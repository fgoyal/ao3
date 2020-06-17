from abc import ABC
from bs4 import BeautifulSoup
import requests
import re
from sys import exc_info

from .searchValues import Sort_By
from .workList import WorkList, WorkIterator

"""
	Used for looking at search results, collecting works, & looking through all pages in result

	for bugs please mention: lambricm
"""

class SearchResult(ABC, object):

	base_site = "https://www.archiveofourown.org"

	def __init__(self, search, sess=None):
		self.search = search
		
		if sess == None:
			sess = requests.Session()
			
		self.sess = sess
		
		self._change_page(self.search.get_url())
		self._page_type()
	
	def __rep__(self):
		return "Search Result for search: " + print(self.search)
		
	def __eq__(self, comp):
		#should be in same state if we have the same url
		return (not (comp == None)) and (self.search.get_url() == comp.search.get_url())
		
	def __ne__(self, comp):
		return not (self == comp)
		
	def __hash__(self):
		return hash(repr(self))
	
	#change the page url & the soup
	def _change_page(self, url):
		self.current_url = url
	
		sess = self.sess
		req = sess.get(url)
		
		self._check_page(req)
				
		self._html = req.text
		self._soup = BeautifulSoup(self._html, 'html.parser')
	
	#check page for errors
	def _check_page(self, req):
		if (req.status_code == 400):
			raise RuntimeError("Search had no results or unexpected error occurred")
		if not (req.status_code == 200):
			raise RuntimeError('Unexpected error from AO3 API: %r (%r)' % (
                req.text, req.statuscode))
		
	#determine page type
	def _page_type(self):
		#there are two types of search (and 3 page types, but one is a 404 error, so we can ignore it
		# because it's already been handled) result we can get from our 'search' class:
		#	Major Tag Search - probably the most common/sought after result
		#	Additional Tag Search - still a search, but shows different results
		#to account for this, I use subclasses with different properties
		#this function is meant to determine the subclass by checking if the tag is minor/additional
		
		if type(self) is SearchResult: #only check if still generic type
		
			tp = self._soup.find("div",{"class":"tag home profile"}) #only exists for additional tags
		
			if tp == None:
				#primary tag
				temp = PrimaryTag(self.search, self.sess)
				self = temp
			else:
				temp = AdditionalTag(self.search, self.sess)
				self = temp
				
		return self
		
	#get all the works on the page
	def get_page_works(self):
		#each work is held in a "work blurb group" item inside of the "work index group" class
		
		#	<ol class="work index group"> == $0
		#		<li class="work blurb group" id="work_[WORK ID]" role="article">
		#			[work info]
		#		</li>
		#		... [more work list items]
		#	<ol>
		
		soup = self._soup.find_all("li", {"class":"work blurb group", "role":"article"})
		
		#we can extract all of the work numbers via regex on the element ids
		arr = []
		for li in soup:
			id = li['id']
			
			id = int(re.sub(r'work_', "", id))
			
			arr.append(id)
		
		return arr
		
	#PAGE STATS
	
	#helper function used for getting the head of the page
	def get_heading(self):
		#found under 'main' element in 'heading':
		
		#	<div id="main" class="works-index filtered region" role="main">
		#		<h2 class="heading>
		#			[text we want]
		#		</h2>
		#	</div>
		
		soup = self._soup.find("div", {"id":"main"})
		soup = soup.find("h2", {"class":"heading"})
		
		return soup
		
	#helper function for retrieving pagination
	def get_pages(self):
		#tricky - no specific ID, uses class type 'pagination actions', but that could also refer to the 
		# paginator at the bottom of the screen. In this case I think there are only two elements with
		# those classes. I am going to just grab the first 
		
		#	<ol class="gatination actions" role="navigation" title="pagination"> == $0
		#		<li> [page_number ___] </li>
		#		... [more page number list items]
		#	</ol>
		
		try:
			soup = self._soup.find("ol", \
				{"class":"pagination actions", \
				"role":"navigation", \
				"title":"pagination"})

		except:
			return None
		
		return soup
		
	#returns what the current page is
	@property
	def current_page(self):
		#current page is within the pagination list, but also has the class 'current'
		soup = self.get_pages()
		
		if soup == None:
			return 1
		else:
			soup = soup.find("span",{"class":"current"})
			return int(soup.decode_contents())
		
	#returns how many pages there are
	@property
	def num_pages(self):
		#the last page has no differentiating class but, if the contents of the list is returned in an
		# ordered list, we should be able to  get it as the second from the last button (behind next)
		
		#WARNING - for some reason beautiful soup is getting a lower of number of pages than I do when I go
		#			to the exact same URL via my web browser. I have no idea why, but I know that I -am-
		#			getting the highest numbered page available in the html. It's just strange.
		
		soup = self.get_pages()
		
		if (soup == None):
			return 1
		else:
			soup = soup.find_all("li")
			return int(soup[len(soup)-2].contents[0].decode_contents())

	#checks whether we are on the first page
	@property
	def is_first_page(self):
		return (self.current_page == 1)
		
	#checks whether we are on the last page
	@property
	def is_last_page(self):	
		return (self.current_page == self.num_pages)
		
	#PAGE MOVEMENT
	#changes what page we're on. Important for parsing through all results
		
	#go to next page
	def next_page(self):
		if not self.is_last_page:
			soup = self.get_pages()
			soup = soup.find("li",{"class":"next", "title":"next"})
			soup = soup.a
		
			if not (soup == None):
				soup = soup['href']
				url = self.base_site + soup

				self._change_page(url)
			
				return True
		return False
		
	#go to previous page
	def prev_page(self):
		if not self.is_first_page:
			soup = self.get_pages()
			soup = soup.find("li",{"class":"previous", "title":"previous"})
			soup = soup.a
		
			if not (soup == None):
				soup = soup['href']
				url = self.base_site + soup
				
				self._change_page(url)
				
				return True
		return False
		
	#go to first page
	def first_page(self):
		if not (self.is_first_page):
			soup = self.get_pages()
			soup = soup.find_all("li")
				
			for li in soup:
				if not (li.a == None):
					try:
						if int(li.a.decode_contents()) == 1:
							url = self.base_site + li.a["href"]
						
							self._change_page(url)
						
							break
					except:
						print("ERROR: could not go to last page. Exception text:\n")
						print(exc_info()[0])
	
	#go to last page
	def last_page(self):
		if not (self.is_last_page):
			soup = self.get_pages()
			soup = soup.find_all("li")
				
			for li in soup:
				if not (li.a == None):
					try:
						if int(li.a.decode_contents()) == self.num_pages:
							url = self.base_site + li.a["href"]
				
							self._change_page(url)
						
							break
					except:
						print("ERROR: could not go to last page. Excepion text:\n")
						print(exc_info()[0])
						
						
	#refresh current page
	def refresh(self):
		self._change_page(self.current_url)
			
	#WORKS COLLECTION CREATION
	
	#aids in getting user all of the works. For this, I have elected to change the way sorting happens
	# to use 'date posted'
	
	def get_all_works(self, search_page=None, worklist=None, check_hash=None):
	
		if not (search_page == None):
			
			works = search_page.get_page_works() #get this page's works
			work_hash = hash(tuple(works))
		
			if check_hash == None: #means we have nothing to check
			
				temp_worklist = WorkList(search_page.get_page_works())
				
				return self.get_all_works(search_page, (temp_worklist + worklist), work_hash)
				
			else: #need to compare to make sure no new works were suddenly added
				
				if (check_hash == work_hash):
				
					if search_page.is_first_page:
						return worklist
					else:
						#the works are the same, so we increment the page
						search_page.prev_page()
						return self.get_all_works(search_page, worklist, None)
					
				else:
					#there has been a new work added! need to re-add all works
					#NOTE: worklist has a set, so re-adding the same works will be fine
					
					return self.get_all_works(search_page, worklist, None)
		else:
			#if our search page is none, we need to create one
			
			new_search = self.search
			new_search.set_sort_by(Sort_By.DATE_POSTED) #want to sort by date posted
			search_page = new_search.get_result()
			search_page.last_page() #start at the last page
			
			return self.get_all_works(search_page, worklist, check_hash)
			
	def get_work_iterator(self):
		return WorkIterator(self)
	
	def get_work(self):
		id = None
	
		try:
			id = next(self.work_iter)
		except:
			if not self.is_last_page:
				if self.next_page():
					id = self.get_work()
		
		return id
		
class PrimaryTag(SearchResult):
	
	def __rep__(self):
		"Result type: Primary Search Tag, " + super().__rep__()
			
	#PAGE STATS
	
	@property
	def main_tag(self):
		header = self.get_heading()
		return header.a.decode_contents()
	
	@property
	def number_fics(self):
		header = self.get_heading().decode_contents()
		num = header.split(" of ")[1]
		num = re.match(r"^([0-9]+)", num).group(0)
		return num
		
	def get_range(self):
		header = self.get_heading().decode_contents()
		nums = header.split(" of ")[0]
		nums = nums.split(" - ")
		
		return nums
	
	@property
	def page_range_start(self):
		return int(self.get_range()[0])
		
	@property
	def page_range_end(self):
		return int(self.get_range()[1])

	#SIDEBAR RESULTS
	#only present for primary tag result pages
	
	#the sidebar contains counts for things like warnings/fandoms/tags
	#it only provides the top 10 for larger groups like characters/relationships, etc though
		
	#gets elements from the side panel
	#one function is used because the side panel elemeents basically have the same format
	def get_side_elements(self,x):
	
		#found in the tag_category_x element:
		
		#	<dd id="tag_category_x" class="tags toggled" style="display:block;"> == $0
		#		<ul>
		#			<li> 
		#				[wanted info]
		#			</li>
		#			... [more list items]
		#		</ul>
		#	</dd>
	
		ret = {}
		
		soup = self._soup.find("dd", {"id":"tag_category_" + x})
		
		for li in soup.find_all('li'):
			contents = li.label.decode_contents()
			
			if not (contents == None):
				temp = contents.split("(")
			
				x = temp[0]
				x = re.sub(r'\s*$', '', x) #take away space @ end of word
				
				num = temp[1]
				num = re.sub(r"\)", '', num)
				
				ret[x] = num
			
		return ret
	
	@property
	def ratings(self):
		get_side_elements('rating')
	
	@property
	def warnings(self):
		get_side_elements('warning')
		
	@property
	def categories(self):
		get_side_elements('category')
		
	@property
	def fandoms(self):
		get_side_elements('fandom')
	
	@property
	def characters(self):
		get_side_elements('character')
		
	@property
	def relationships(self):
		get_side_elements('relationship')
		
	@property
	def additional_tags(self):
		get_side_elements('freeform')
	
class AdditionalTag(SearchResult):
	
	def __rep__(self):
		"Result type: Additional Search Tag, " + super().__rep__()
		
	#PAGE STATS
	
	@property
	def main_tag(self):
		return self.get_heading().decode_contents()
		
	@property
	def parent_tags(self):
		tags = []
		
		soup = self._soup.find("div", {"class":"parent listbox group"})
		soup = soup.find("ul", {"class":"tags commas index group"})
		soup = soup.find_all("li")
		
		for li in soup:
			tags.append(li.a.decode_contents())
			
		return tags