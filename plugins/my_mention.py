from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from slacker import Slacker

import requests as web
import bs4

import numpy as np
import matplotlib
matplotlib.use('Agg') # -----(1)
import matplotlib.pyplot as plt

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
def isHiragana(char):
    if("ぁ" <= char <= "み" or "む" <= char <= "ん"):
        return True
    return False

def isKatakana(char):
    if("ァ" <= char <= "タ" or "ダ" <= char <= "ヶ"):
        return True
    return False

def isAlphabet(char):
    if("A" <= char <= "Z" or "a" <= char <= "z"):
        return True
    return False

def isKanji(char):
    if("一" <= char <= "龻"):
        return True
    return False 

@respond_to('メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ') # メンション

@respond_to('http')
def default_func(message):
    test = message.body['text']     # メッセージを取り出す
    # 送信メッセージを作る。改行やトリプルバッククォートで囲む表現も可能
    test = test[1:]
    test = test[:-1]
    resp = web.get(test)
    # if(resp.status_code == 200):
    #     message.reply("該当しないURLです")
    if(resp.status_code == 200):
        content_type_encoding = resp.encoding if resp.encoding != 'ISO-8859-1' else None
        soup = bs4.BeautifulSoup(resp.content, 'html.parser', from_encoding=content_type_encoding)
        # resp.raise_for_status()

        # 取得したHTMLをパースする
        # soup = bs4.BeautifulSoup(resp.text, "html.parser")
        # 検索結果のタイトルとリンクを取得
        # コメントの削除
        for comment in soup(text=lambda x: isinstance(x, bs4.Comment)):
            comment.extract()

        # scriptタグの除去
        for script in soup.find_all('script', src=False):
            script.decompose()
        # styleタグの除去 
        for style in soup.find_all('style', src=False):
            style.decompose()
        # footerタグの除去
        for foot in soup.find_all('footer', src=False):
            foot.decompose()
        for head in soup.find_all('header', src=False):
            head.decompose()
        # テキストだけの抽出
        data = ''
        for text in soup.find_all(text=True):
            if text.strip():
                tmp = data
                tmp = data + ' ' + text
                data = tmp

        c_hiragana = 0 # ひらがなカウント
        c_katakana = 0 # カタカナカウント
        c_kanji = 0 # 漢字カウント

        for word in range(0,len(data)):
            if isHiragana(data[word]) == True:
                c_hiragana += 1
            if isKatakana(data[word]) == True:
                c_katakana += 1
            if isKanji(data[word]) == True:
                c_kanji += 1

        total = c_hiragana + c_kanji + c_katakana
        # print()

        x = np.arange(-3, 3, 0.1)
        plt.rcParams["font.size"] = 20
        plt.figure(figsize=(10,10),dpi=100)
        x = np.array([c_hiragana, c_katakana, c_kanji])
        label = ["hiragana","katakana","kanji"]
        plt.pie(x, labels=label,counterclock=True, autopct="%1.1f%%")
        plt.axis('equal')
        plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=-3, fontsize=18)
        plt.text(-1.3,1,"Total: "+str(total)+"\nhiragana: "+str(c_hiragana)+"\nkatakana: "+str(c_katakana)+"\nkanji: "+str(c_kanji))

        # save as png
        plt.savefig('figure.png') # -----(2)
        message.reply("\nひらがな："+str(c_hiragana)+'\nカタカナ：'+ str(c_katakana)+'\n漢字：'+str(c_kanji))
        post_file()
    else:
        message.reply("URLを間違っていはいないですか？")
def post_file():
    token="xoxb-20057120048-426982310453-8qlAoTMfeam5vMBx5JcGtNp7"
    c_name = 'se-データ分析'
    files = './figure.png'

    # 投稿
    slacker = Slacker(token)
    slacker.files.upload(files, channels=[c_name], title='文字比率')