import MeCab
import os
from wordcloud import WordCloud

#ワードクラウドの作成
def create_wordcloud(text: str):
    fontpath = '/work/.fonts/' + os.environ['FONTFILE']

    word_chain = ' '.join(text)
    wordcloud = WordCloud(background_color=None,
                          mode="RGBA",
                          font_path=fontpath,
                          width=900,
                          height=500,
                          relative_scaling=0.5 # フォントサイズの相対的な単語頻度の重要性
                         ).generate(word_chain)

    #ファイルの作成
    wordcloud.to_file("/work/images/image-" + os.environ['HATENAID'] + ".png")
