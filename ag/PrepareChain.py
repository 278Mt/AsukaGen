import unittest
import re
import janome
from collections import defaultdict
from janome.tokenizer import Tokenizer

class PrepareChain(object):

    BEGIN = "__BEGIN_SENTENCE__"
    END = "__END_SENTENCE__"

    def __init__(self, name):
        # 名前をプッシュ
        self.name = name

        fname = "resources/"+name+".txt"
        with open(fname, mode="r") as file:
            text = file.read()

        self.text = text

        # 形態素解析用タガー
        self.tagger = Tokenizer()

    def make_triplet_freqs(self):
        messages = self._divide_text(self.text)

        # 3つ組の出現回数
        triplet_freqs = defaultdict(int)

        # センテンス毎に3つ組にする
        for message in messages:
            # 形態素解析
            morphemes = self._morphological_analysis(message)
            # 3つ組をつくる
            triplets = self._make_triplet(morphemes)
            # 出現回数を加算
            for (triplet, n) in triplets.items():
                triplet_freqs[triplet] += n

        return triplet_freqs

    def _divide_text(self, text):
        messages = text.split("\n")

        return messages

    def _morphological_analysis(self, message):
        # 一文を形態素解析する
        sentence = message.encode("utf-8")
        morphemes = self.tagger.tokenize(message, wakati=True)

        return morphemes

    def _make_triplet(self, morphemes):
        # 形態素解析で分割された配列を、形態素毎に3つ組にしてその出現回数を数える

        # 3つ組をつくれない場合は終える
        if len(morphemes) < 3:
            return {}

        # 出現回数の辞書
        triplet_freqs = defaultdict(int)

        # 繰り返し
        for i in range(len(morphemes)-2):
            triplet = tuple(morphemes[i:i+3])
            triplet_freqs[triplet] += 1

        # beginを追加
        triplet = (PrepareChain.BEGIN, morphemes[0], morphemes[1])
        triplet_freqs[triplet] = 1

        # endを追加
        triplet = (morphemes[-2], morphemes[-1], PrepareChain.END)
        triplet_freqs[triplet] = 1

        return triplet_freqs

    def save(self, triplet_freqs, init=False):
        name = self.name
        # 3つ組毎に出現回数をcsvに保存
        fname = "corpus/"+name+"_corpus.csv"
        datas = [(triplet[0], triplet[1], triplet[2], freq) for (triplet, freq) in triplet_freqs.items()]

        # 初期化から始める場合
        if init:
            # データ整形
            with open(fname, mode="w") as file:
                file.write("prefix1,prefix2,suffix,freq\n")

        # 保存して終了
        with open(fname, mode="a") as file:
            for triplet, freq in triplet_freqs.items():
                file.write(triplet[0]+","+triplet[1]+","+triplet[2]+","+str(freq)+"\n")

if __name__ == '__main__':
    # unittest.main()

    name = "アスカ"
    PC = PrepareChain(name)
    triplet_freqs = PC.make_triplet_freqs()
    PC.save(triplet_freqs, True)
