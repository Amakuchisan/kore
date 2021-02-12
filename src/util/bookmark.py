import feedparser
import math
import os
import re
import sys

from db import word, article, user_article, article_word
from util import word as wd


class Bookmark:
    # 公開しているブックマークの数を求める
    def __init__(self):
        self.allnoun = []
        self.dic = {}
        self.bodies = []
        self.bodynoun = []
        self.bodydic = {}
        self.osusumedic = {}
        self.entries = {}

    def init(self, hatena_id: str):
        self.calc_feature(hatena_id)

    def count_bookmark_page(self, hatena_id: str) -> int:
        d = feedparser.parse('https://b.hatena.ne.jp/{}/rss'.format(hatena_id))
        content = d['feed']['subtitle']  # 'Userのはてなブックマーク (num)'
        match = re.search(r"(はてなブックマーク \()(.*?)\)", content)
        num = match.group(2).replace(',', '')  # 公開しているブックマーク数
        if not num.isdecimal():
            print('Error: num is string', file=sys.stderr)
            return 0
        return math.ceil(int(num)/20)

    def calc_feature(self, hatena_id: str):
        return
        url_list = self.get_url(hatena_id)

        for url in url_list:
            html = word.get_body_from_URL(url)
            noun = word.get_noun(' '.join(html))
            dic_list = get_n_dict(noun, 3)

            for dic in dic_list:
                article = session.query



            d = feedparser.parse('https://b.hatena.ne.jp/{}/rss?page={}'.format(hatena_id, i+1))
            entries = d['entries']
            for entry in entries:
                titles.append(entry['title'])
        return titles

    def get_title(self, hatena_id: str) -> list[str]:
        # 1ページに20件のデータがある。ページ数を求める
        if hatena_id == "":
            return []
        bookmark_num = self.count_bookmark(hatena_id)
        max_page = (bookmark_num//20) + int((bookmark_num%20) > 0)

        titles = []

        for i in range(max_page):
            d = feedparser.parse('https://b.hatena.ne.jp/{}/rss?page={}'.format(hatena_id, i+1))
            entries = d['entries']
            for entry in entries:
                titles.append(entry['title'])
        return titles

    def get_url(self, hatena_id: str) -> list[str]:
        # 1ページに20件のデータがある。ページ数を求める
        if hatena_id == "":
            return []
        bookmark_num = self.count_bookmark(hatena_id)
        max_page = (bookmark_num//20) + int((bookmark_num%20) > 0)

        links = []

        for i in range(max_page):
            d = feedparser.parse('https://b.hatena.ne.jp/{}/rss?page={}'.format(hatena_id, i+1))
            entries = d['entries']
            for entry in entries:
                links.append(entry['link'])
        return links

    def get_osusume(self, hatena_id: str):
        d = self.dic
        for entry in self.entries:
            if hatena_id == "":
                return ""
            noun = word.get_noun(entry['title'])
            for n in noun:
                if n in d:
                    if n not in self.osusumedic:
                        self.osusumedic.setdefault(entry['link'].replace('/', '').replace(':', '').replace('.', ''), d[n])
                    else:
                        self.osusumedic[entry['link'].replace(':', '').replace('/', '').replace('.', '')] += d[n]

    def update_hotentry(self, category: str):
        d = feedparser.parse('https://b.hatena.ne.jp/hotentry/{}.rss'.format(category))
        self.entries = d['entries']

    def get_hotentry(self, hatena_id, category: str) -> list[dict[str, str]]:
        entries = []
        osusume = "未計算"
        self.update_hotentry(category)
        for entry in self.entries:
            if entry['link'].replace('/', '').replace(':', '').replace('.', '') in self.osusumedic:
                osusume = self.osusumedic[entry['link'].replace(':', '').replace('/', '').replace('.', '')]
            # osusume = self.get_osusume(hatena_id, self.dic, entry['title'])
            entries.append(dict(link=entry['link'], title=entry['title'], recommendation_score=osusume))
        return entries
