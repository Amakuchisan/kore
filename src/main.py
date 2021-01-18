from bookmark import Bookmark
# import MeCab
import os
# from wordcloud import WordCloud
import wc
import word

def main():
    hatena_id = os.environ['HATENAID']
    bookmark = Bookmark(hatena_id)
    titles = bookmark.get_title()

    # wc.create_wordcloud(word.get_noun(' '.join(titles)))

if __name__ == "__main__":
    main()
