from icrawler.builtin import GoogleImageCrawler
import Project_Translate as trans
class CRAWL:
	def set_info(self, plist, num):
		self.plist = plist
		self.plist_e = [trans.hanrom(p) for p in plist]
		self.num = num
		self.myd = dict(zip(self.plist, self.plist_e))
	def crawl(self) :
		for han,eng in self.myd.items():
			google_crawler = GoogleImageCrawler(
				feeder_threads=1,
				parser_threads=2,
				downloader_threads=4,
				storage={'root_dir': eng})
			filters = dict(
				#size='large',
				#color='orange',
				#license='commercial,modify',
				date=((2010, 1, 1), (2018, 5, 31)))
			google_crawler.crawl(keyword=han, filters=filters, max_num=self.num, file_idx_offset=0)
		

