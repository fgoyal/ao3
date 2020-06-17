from . import works
from .searchValues import Sort_By

"""
	allows iterating through a collection of works (usually obtained from a search)
	
	for bugs please mention: lambricm
"""

class WorkIterator(object):

	def __init__(self, searchRes):
		#print("created")
	
		#get search result
		self.search = searchRes.search
		self.search.set_sort_by(Sort_By.DATE_POSTED)
		self.search = self.search.get_result()
		self.search.last_page() #start on last page
		
		self.total_works = set()
		self.curr_works = []
		self.work_iter = iter(self.curr_works)
		self.page_hash = None
		
	def next_work(self):
	
		#can't do anything without a search
		if not (self.search is None):
			#print("search initialized")
		
			#try getting the next work
			try:
				#print("trying to get work")
				#works if there are ids in the set and they are new ids
				id = next(self.work_iter)
				#print("loop next")
				
				while id in self.total_works:
					id = next(self.work_iter)
					#print("next work")
					
				self.total_works.add(id)
				work = works.Work(id)
				#print("get work: " + str(id))
				return work
			except Exception as e:
				#print("EXCEPTION: " + str(e))
				#print("no more works on page")
				
				#no more ids in the set that we want
				
				if self.page_hash is None:
					#print("no hash, getting page")
					#we don't have a hash to compare to
					
					self.curr_works = self.search.get_page_works()
					#print("WORKS")
					#print(self.curr_works)
					#print("WORKS")
					self.work_iter = iter(self.curr_works)
					self.page_hash = hash(tuple(self.curr_works))
					return self.next_work()
				else:
					#print("hash!")
					#we need to check the hash is the same before moving on
					self.search.refresh()
					check_works = self.search.get_page_works()
					check_hash = hash(tuple(check_works))
					
					if not (check_hash == self.page_hash):
						#print("not the same! refresh page")
						#need to get the page again
						self.curr_works = self.check_works
						self.work_iter = iter(self.curr_works)
						self.page_hash = check_hash
						return self.next_work()
						
					else:
						#print("hash is the same")
						if not self.search.is_first_page:
							#print("not first page, get prev page")
							self.search.prev_page()
							self.page_hash = None
							return self.next_work()
						else:
							#print("done :)")
							return None
		return None
			

#deprecated because server keeps cutting me off - possibly noticing the extensive load coming from 1 IP address
#also this way is soooo slow
class WorkList(object):

	def __init__(self, works=set()):
		self.works = set()
		
		self.add_works(works)
		self.work_iter = iter(self.works)
		
	def add_works(self, works):
		if (type(works) == type([])):
			for work in works:
				self.works.add(work)
		elif (type(works) == type(set())):
			self.works = self.works.union(works)

		self.work_iter = iter(self.works)
		
	def __add__(self, other_worklist):
		if other_worklist == None:
			return self
		else:
			return WorkList(self.works.union(other_worklist.works))
			
	def __repr__(self):
		return str(self.works)
		
	@property
	def next_work(self):
		try:
			id = next(self.work_iter)
			work = works.Work(id)
			return work
		except:
			return None
			
	@property
	def num_works(self):
		return len(self.works)