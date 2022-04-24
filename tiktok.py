import threading
import requests
import string
import random
import re


class Tiktok:
    def __init__(self, url, threads):
        self.video_id = self.get_video_id(url)
        self.threads = threads
        self.shares = 0

    def share(self):
        session = requests.Session()
        payload = f"item_id={self.video_id}&share_delta=1"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "com.zhiliaoapp.musically/2022309050 (Linux; U; Android 7.1.2; en; G011A; Build/N2G48H;tt-ok/3.10.0.2)"
        }
        device_id = "".join(random.choices(string.digits, k=19))
        url = f"https://api31-core-useast1a.tiktokv.com/aweme/v1/aweme/stats/?channel=googleplay&device_type=G011A&device_id={device_id}&os_version=7.1.2&version_code=220400&app_name=musically_go&device_platform=android&aid=1988"

        r = session.post(url, headers=headers, data=payload)

        if r.status_code == 200:
            self.shares += 1
            print(f"[+]Shares count: {self.shares}", end="\r")

    @staticmethod
    def get_video_id(url):
        if "vm.tiktok.com" in url:
            r = requests.get(url, allow_redirects=False)
            url = r.headers["Location"]
        return re.search(r"/video/(.*)\?", url).group(1)

    def start(self):
        print("[*]Sending shares...\n")
        while True:
            if threading.active_count() <= self.threads:
                threading.Thread(target=self.share).start()


if __name__ == "__main__":
    url = input("[*]Tiktok url: ")
    threads = int(input("[*]Threads count: "))
    Tiktok(url, threads).start()
