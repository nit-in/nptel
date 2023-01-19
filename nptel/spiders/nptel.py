import scrapy
import json
import subprocess
from pathlib import Path

class NPTELSpider(scrapy.Spider):
	name = 'nptel'
	allowed_domains = ['https://archive.nptel.ac.in']

	def start_requests(self):
		url = 'https://tools.nptel.ac.in/npteldata/downloads.php?id='
		nid = getattr(self, 'nid', None)
		if nid is not None:
			url = url + nid
		yield scrapy.Request(url, self.parse)
	
	def parse(self, response):
		nptel_dir = Path("~/nptel").expanduser()
		self.chkdir(nptel_dir)
		ts = response.json()["data"]
		jts = json.dumps(ts)
		xjs = json.loads(jts)
		course_folder = str(xjs["title"]).replace(" ", "_") + "_" + str(xjs["course_id"])
		course_folder_p = Path(nptel_dir,course_folder)
		self.chkdir(course_folder_p)
		js = response.json()["data"]["course_downloads"]
		y = json.dumps(js)
		x = json.loads(y)
		list_vid = len(x)
		for i in range(0, list_vid):
			print(x[i]["title"])
			print(x[i]["url"])
			print(x[i]["lesson_id"])
			tit = str(x[i]["title"])
			urlp = str(x[i]["url"])
			lesid = str(x[i]["lesson_id"])
			tt = "L" + lesid + "_" + tit.replace(" ", "_") + ".mp4"
			fpath = Path(course_folder_p, tt)
			self.download_vid(urlp, fpath)

	def download_vid(self,link,vid_path):
		program = "wget"
		arg1 = "--show-progress"
		arg2 = "--server-response"
		arg3 = "--continue"
		arg4 = "-O"
		print(f"Downloading: {vid_path}\n")
		print(f"vid_pth {vid_path}\n")
		print(f"link {link}\n")
		subprocess.call([program,arg1,arg2,arg3,str(link),arg4,str(vid_path)])

	def chkdir(self,dir_path):
		dir_path_p = Path(dir_path)
		if not dir_path_p.exists():
			dir_path_p.mkdir(parents=True)