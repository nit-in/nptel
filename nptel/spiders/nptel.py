import scrapy
import json
import subprocess
from pathlib import Path


cwd = Path.cwd()
dwnfl = "dwn"
txtext = ".txt"


class NPTELSpider(scrapy.Spider):
    name = 'nptel'

    def start_requests(self):
        url = 'https://tools.nptel.ac.in/npteldata/downloads.php?id='
        nid = getattr(self, 'nid', None)
        if nid is not None:
            url = url + nid
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        mplinks = []
        nptel_dir = Path("~/nptel_videos").expanduser()
        self.chkdir(nptel_dir)

        ts = response.json()["data"]
        jts = json.dumps(ts)
        xjs = json.loads(jts)

        course_folder = str(xjs["title"]).replace(" ", "_") + "_" + str(xjs["course_id"])
        course_folder_p = Path(nptel_dir, course_folder)
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

            if not fpath.exists():
                mplinks.append(str(urlp))
                print(f"Adding {str(urlp)} to list")
            else:
                print(f"File {str(fpath)} is already downloaded")

        dtfname = str(dwnfl) + str(txtext)
        dtfile = Path(cwd, dtfname)

        with open(str(dtfile), "w", encoding="utf-8") as lfile:
            for pl in mplinks:
                lfile.write(f"{str(pl)}\n")
        self.download_vid(str(lfile.name), fpath)

    def download_vid(self, link, vid_path):
        program = "aria2c"
        arg1 = "-x16"
        arg2 = "-s16"
        arg3 = "-j16"
        arg4 = "-d"
        arg5 = "-i"
        
        print(f"Downloading: {vid_path}\n")
        print(f"vid_pth {vid_path}\n")
        print(f"file {str(link)}")
        subprocess.call([program, arg1, arg2, arg3, arg4, str(vid_path), arg5, str(link)], stderr=subprocess.STDOUT)

    def chkdir(self, dir_path):
        dir_path_p = Path(dir_path)
        if not dir_path_p.exists():
            dir_path_p.mkdir(parents=True)
