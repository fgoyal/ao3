from bs4 import BeautifulSoup
import requests
import re

"""
	class to obtain chapter information on chapters (including text!) as well as move through the chapter
	
	For bugs please mention: lambricm
"""

class Chapter(object):

	base_url = 'https://archiveofourown.org'
	
	def __init__(self, wrk_id, sess=None):
		self.wrk_id = wrk_id
	
		if sess == None:
			sess = requests.Session()
			
		self.sess = sess
		
		self._change_page("/works/" + str(self.wrk_id))
			
	def _change_page(self, url_add):
		self.url_add = url_add
	
		sess = self.sess
		req = sess.get(Chapter.base_url + url_add)
				
		self._check_page(req)
				
		self._html = req.text
		self._soup = BeautifulSoup(self._html, 'html.parser')	
	
	def _check_page(self, req):
		if req.status_code == 404:
			raise Exception('Cannot find chapter')
		elif req.status_code != 200:
			raise RuntimeError('Unexpected error from AO3 API: %r (%r)' % (req.text, req.statuscode))
	
	#gives user the id of the work (not the individual chapter)
	@property
	def work_id(self):
		return self.wrk_id
	
	#PAGE CHANGING AREA
	
	#checks if we're on the first page
	@property
	def first_chapter(self):
		#previous button is the only one with:
		#
		#	<li class="chapter previous>..</li>
	
		try:
			soup = self._soup.find("li", {"class":"chapter previous"})
			return (soup is None)
		except:
			#could not find button
			return True
			
	#checks if we're on the last page
	@property
	def last_chapter(self):
		#next button is the only one with:
		#
		#	<li class="chapter next>..</li>
		
		try:
			soup = self._soup.find("li", {"class":"chapter next"})
			return (soup is None)
		except:
			#could not find button
			return True
			
	#moves us to the next chapter
	#return - the success of the operation
	def next_chapter(self):
		#next button is the only one with:
		#
		#	<li class="chapter next>..</li>
		
		if not self.last_chapter:
			soup = self._soup.find("li", {"class":"chapter next"})
			url = soup.a["href"]
			self._change_page(url)
			return True
		return False
		
	#moves us to the previous chapter
	#return - the success of the operation
	def prev_chapter(self):
		#previous button is the only one with:
		#
		#	<li class="chapter previous>..</li>
		
		if not self.first_chapter:
			soup = self._soup.find("li", {"class":"chapter previous"})
			url = soup.a["href"]
			self._change_page(url)
			return True
		return False
	
	#PAGE CHANGING AREA
	
	#checks if we're on the first page
	@property
	def first_chapter(self):
		#previous button is the only one with:
		#
		#	<li class="chapter previous>..</li>
	
		try:
			soup = self._soup.find("li", {"class":"chapter previous"})
			return (soup is None)
		except:
			#could not find button
			return True
			
	#checks if we're on the last page
	@property
	def last_chapter(self):
		#next button is the only one with:
		#
		#	<li class="chapter next>..</li>
		
		try:
			soup = self._soup.find("li", {"class":"chapter next"})
			return (soup is None)
		except:
			#could not find button
			return True
			
	#moves us to the next chapter
	#return - the success of the operation
	def next_chapter(self):
		#next button is the only one with:
		#
		#	<li class="chapter next>..</li>
		
		if not self.last_chapter:
			soup = self._soup.find("li", {"class":"chapter next"})
			url = soup.a["href"]
			self._change_page(url)
			return True
		return False
		
	#moves us to the previous chapter
	#return - the success of the operation
	def prev_chapter(self):
		#previous button is the only one with:
		#
		#	<li class="chapter previous>..</li>
		
		if not self.first_chapter:
			soup = self._soup.find("li", {"class":"chapter previous"})
			url = soup.a["href"]
			self._change_page(url)
			return True
		return False
	
	#CHAPTER INFO AREA
	
	#helper function
	def _get_title_area(self):
		#title area can be defined as:
		#
		#	<div class="chapter preface group" role="complementary"
		#		<h3 class="title"> == $0
		#			<a href="title_url"Chapter #</a>: chapter_title
		#		</h3>
		#	</div>
		
		soup = self._soup.find("div",{"class":"chapter preface group"})
		soup = soup.find("h3",{"class":"title"})
		return soup
	
	#retrieves chapter number
	@property
	def number(self):
		#for this we use:
		#	<h3 class="title"> == $0
		#		<a href="title_url"Chapter #</a>: chapter_title
		#	</h3>
		# and extract #
	
		soup = self._get_title_area()
		ch_num = soup.a.decode_contents()
		ch_num = int(re.sub(r"Chapter ", "", ch_num))
		return ch_num
		
	#retrieves chapter title
	@property
	def title(self):
		#for this we use:
		#	<h3 class="title"> == $0
		#		<a href="title_url"Chapter #</a>: chapter_title
		#	</h3>
		# and extract chapter_title
	
		soup = self._get_title_area()
		soup = soup.decode_contents()
		soup = soup.split("</a>")[1]
		title = re.sub(r"^: ", "", soup)
		return title
		
	#retrieves chapter summary
	@property
	def summary(self):
		#found here:
		#
		#	<div id="chapters"> == $0
		#		<div class="chapter" id="chapter-#">
		#			<div class="chapter preface group" role="complementary">
		#				...
        #				<div id="summary" class="summary module">
        #					<h3 class="heading">
		#						Summary:
		#					</h3>
        #					<blockquote class="userstuff">
        #						summary (in many <p> blocks)
        #					</blockquote>
        #				</div>
		#				...
		#			</div>
		#		</div>
		#	</div>
	
		summ = ""
		
		try:
			soup = self._soup.find("div", {"id":"chapters"})
			soup = soup.find("div", {"id":"summary"})
			soup = soup.find("blockquote", {"class":"userstuff"})
			soup = soup.find_all("p")
			
			print(soup)
			
			for p in soup:
				summ = summ + p.decode_contents() + "\n"
				
		except:
			pass
			
		return summ
		
	@property
	def beg_note(self):
		#found here:
		#
		#	<div id="notes" class="notes module">
        #		<h3 class="heading">
		#			Notes:
		#		</h3>
        #		beginning_note (in multiple <p> tags)
		#	</div>
	
		note = ""
	
		try:
			soup = self._soup.find("div", {"class":"notes module","id":"notes"})
			soup = soup.find_all("p")
		
			for p in soup:
				note = note + p.decode_contents() + "\n"
				
		except:
			pass
			
		note = re.sub('\\n\\n            \(See the end of the chapter for  <a href=\"[^"]+\">more notes<\/a>\.\)\\n            \\n',"",note)
			
		return note
			
	@property
	def end_note(self):
		#found here:
		#
		#	<div class="end notes module" id="chapter_#_endnotes" role="complementary">
        #		<h3 class="heading">
		#			Notes:
		#		</h3>
        #		<blockquote class="userstuff">
		#			end_note (in multiple p tags)
		#		</blockquote>
		#	</div>
		
		note = ""
	
		try:
			soup = self._soup.find("div", {"class":"end notes module"})
			soup = soup.find("blockquote", {"class":"userstuff"})
			soup = soup.find_all("p")
		
			for p in soup:
				note = note + p.decode_contents() + "\n"
				
		except:
			pass
			
		return note
		
	@property
	def work_beg_note(self):
		#found here (FIRST CHAPTER):
		#
		#	<div class="preface group">
		#		...
		#		<div class = "notes module" role="complementary">
		#			...
		#			<blockquote class="userstuff">
		#				beginning note for work in <p> tags
		#			</blockquote>
		#		</div>
		#	</div>
	
		curr_url = self.url_add
		
		while not self.first_chapter:
			self.prev_chapter()
			
		note = ""
		
		try:
			soup = self._soup.find("div", {"class":"preface group"})
			soup = soup.find("div", {"class":"notes module"})
			soup = soup.find("blockquote", {"class":"userstuff"})
			soup = soup.find_all("p")
			
			for p in soup:
				note = note + p.decode_contents() + "\n"
		except:
			pass
			
		self._change_page(curr_url)
		
		return note
		
	@property
	def work_end_note(self):
		#found here (LAST CHAPTER):
		#
		#	<div id="work_endnotes" class="end notes module>
		#		...
		#		<blockquote class="userstuff">
		#			end note for work in <p> tags
		#		</blockquote>
		#		...
		#	</div>
	
		curr_url = self.url_add
		
		while not self.last_chapter:
			self.next_chapter()
			
		note = ""
		
		try:
			soup = self._soup.find("div", {"id":"work_endnotes","class":"end notes module"})
			soup = soup.find("blockquote", {"class":"userstuff"})
			soup = soup.find_all("p")
			
			for p in soup:
				note = note + p.decode_contents() + "\n"
		except:
			pass
			
		self._change_page(curr_url)
		
		return note
	
	#collects all text in soup
	def _chapter_piece(self, soup):
		ret = ""
		
		text = soup.string
		
		if text is None:
			for ch in soup.children:
				ret = ret + self._chapter_piece(ch)
		else:
			text = re.sub("\n","",text)
			ret = ret + text
		
		return ret
				
	#gets the entire chapter's text
	#goes through each p element of the desired text & returns total text
	# with each  <p> block separated by a newline
	@property
	def text(self):
		#found here:
		#
		#	<div class="chapter" id="chapter-#">
		#		<div class="userstuff module" role="artivle">
		#			text (many <p> tags with other nexted tags)
		#		</div>
		#	</div>
	
		ch = ""
		
		soup = self._soup.find("div", {"class","chapter"})
		soup = soup.find("div", {"class":"userstuff module"})
		soup = soup.find_all("p")
		
		for p in soup:
			if not (re.search(r'[^\n]$', ch) is None):
				ch = ch + "\n"
			ch = ch + self._chapter_piece(p)
			
		return ch