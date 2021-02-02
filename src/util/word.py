from bs4 import BeautifulSoup
import MeCab
import regex
import requests
import codecs

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
    return word_list

def strip_tags(html: str) -> str:
    html = html.replace("&lt;", '<').replace("&gt;", '>')
    p = r"(?<rec><(?:[^<>]+|(?&rec))*>)"
    return regex.sub(p, "", html)

def strip_url(html: str) -> str:
    p = r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)"
    return regex.sub(p, "" , html)

def w():
    with codecs.open('myfiler4.txt', 'w', 'utf-8') as f:
        url = 'https://cnaan.hatenablog.com/entry/2020/12/04/234523'
        html = get_body_from_URL(url)
        f.write(html)

def get_body_from_URL(url: str) -> str:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    if soup.find('article') is None:
        return soup.get_text()
    return '\n'.join([c.get_text() for c in soup.find_all('article')])

def create_dict_from_list(word_list: list[str]):
    dict = {}
    for word in word_list:
        if word not in dict:
            dict.setdefault(word, 1)
        else:
            dict[word] += 1
    return dict

def get_n_dict(dic: list[dict[str, int]], n: int) -> list[dict[str, int]]:
    n_dic = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    return n_dic[:n]
