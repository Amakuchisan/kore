from bs4 import BeautifulSoup
import MeCab
import neologdn
import regex
import requests

from time import sleep

# 名詞を取得


def get_noun(text: str) -> list[str]:
    stop_words = ['もの', 'こと', 'とき', 'そう', 'たち', 'これ', 'よう', 'これら', 'それ', 'すべて', '一つ', '二つ', '三つ',
                  'Qiita', 'note', 'Speaker Deck', 'まとめ', 'コリス', 'blog']
    # 形態素解析
    tagger = MeCab.Tagger(
        '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd'
    )
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_list = []
    while node:
        word_type = node.feature.split(',')[0]
        word_surf = node.surface.split(',')[0]
        if word_type == '名詞' and word_surf not in stop_words:
            if len(set(["副詞可能", "数", "非自立", "代名詞", "接尾"]) & set(node.feature.split(",")[1:4])) == 0:
                word_list.append(node.surface)
        node = node.next
    return list(map(lambda s: s.lower(), word_list))


def strip_tags(html: str) -> str:
    html = html.replace("&lt;", '<').replace("&gt;", '>')
    p = r"(?<rec><(?:[^<>]+|(?&rec))*>)"
    return regex.sub(p, '', html)


def strip_url(html: str) -> str:
    p = r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)"
    return regex.sub(p, '', html)


def strip_symbol(html: str) -> str:
    p = r"[!-/:-@[-`{-~ʹ·]"
    return regex.sub(p, ' ', html)


def get_body_from_URL(url: str) -> str:
    err_code=[500, 502, 503]
    try:
        res = get_retry(url, 3, err_code)
        if res.status_code in err_code:
            return ''
    except Exception as e:
        print(url, e)
        return ''
    soup = BeautifulSoup(res.content, 'html.parser')
    if soup.find('article') is None:
        html = soup.get_text()
    else:
        html = '\n'.join([c.get_text() for c in soup.find_all('article')])
    return strip_symbol(strip_tags(strip_url(neologdn.normalize(html))))


def get_retry(url, retry_times, errs):
    for t in range(retry_times + 1):
        r = requests.get(url, verify=False)
        if t < retry_times:
            if r.status_code in errs:
                sleep(2)
                continue
        return r


def create_dict_from_list(word_list: list[str]) -> dict[str, int]:
    dict = {}
    for word in word_list:
        if word not in dict:
            dict.setdefault(word, 1)
        else:
            dict[word] += 1
    return dict


def get_n_dict(dic: dict[str, int], n: int) -> list[tuple[str, int]]:
    n_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return n_dic[:n]
