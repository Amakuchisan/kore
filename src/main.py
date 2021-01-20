from bookmark import Bookmark
import os
import wc
import word

def main():
    # hatena_id = os.environ['HATENAID']
    bookmark = Bookmark()
    # titles = bookmark.get_title(hatena_id)

    # wc.create_wordcloud(word.get_noun(' '.join(titles)))

if __name__ == "__main__":
    main()
