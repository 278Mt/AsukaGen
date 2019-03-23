import os.path
import re
import random
import pandas as pd
from PrepareChain import PrepareChain
from glob import glob

class GenerateText(object):

    def __init__(self, name, n=5):
        self.name = name
        self.n = n

    def generate(self):
        name = self.name
        # 文章を生成する
        # csv 書籍が存在しないときは例外をあげる
        fname = "corpus/"+name+"_corpus.csv"
        if not os.path.exists(fname):
            raise IOError("コーパスが保存されているcsvファイルが存在しません")

        # read csv
        df = pd.read_csv(fname)

        # 指定の数だけ作成する
        # if initialization is false
        try:
            pattern = "output/"+name+"*?.txt"
            fnames = sorted(glob(pattern))
            fname = [fname for fname in fnames if name == re.search("/.*?_", fname).group(0)[1:-1]][-1]
            i = int(re.search("_.*\.", fname).group(0)[1:-1]) + 1
        except:
            i = 0

        fname = "output/"+name+"_{:03}.txt".format(i)
        glob(fname)
        with open(fname, mode="w") as file:
            file.write("")

        with open(fname, mode="a") as file:
            for i in range(self.n):
                text = self._generate_sentence(df)
                file.write(text+"\n")

    def _generate_sentence(self, df):
        # ランダムに一文を生成する

        # 生成文章のリスト
        morphemes = []

        # はじまりを取得
        first_triplet = self._get_first_triplet(df)
        morphemes.append(first_triplet[1])
        morphemes.append(first_triplet[2])

        # 文章を紡いでいく
        while morphemes[-1] != PrepareChain.END:
            prefix1 = morphemes[-2]
            prefix2 = morphemes[-1]
            triplet = self._get_triplet(df, prefix1, prefix2)
            morphemes.append(triplet[2])

        # 連結
        result = "".join(morphemes[:-1])

        return result

    def _get_chain_from_df(self, df, prefixes):
        # dfから取得
        # prefixが2つなら条件に加える
        if len(prefixes) == 2:
            return df.loc[df["prefix1"]==prefixes[0]].loc[df["prefix2"]==prefixes[1]]
        else:
            return df.loc[df["prefix1"]==prefixes[0]]

    def _get_first_triplet(self, df):
        # 文章のはじまりの3つ組をランダムに取得する

        # BEGINをprefix1としてチェーンを取得
        prefixes = (PrepareChain.BEGIN,)

        # チェーン情報を取得
        chains = self._get_chain_from_df(df, prefixes)

        # 取得したチェーンから、確率的に1つ選ぶ
        triplet = self._get_probable_triplet(chains)

        return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_triplet(self, df, prefix1, prefix2):
        # prefix1とprefix2からsuffixをランダムに取得する

        # BEGINをprefix1としてチェーンを取得
        prefixes = (prefix1, prefix2)

        # チェーン情報を取得
        chains = self._get_chain_from_df(df, prefixes)

        # 取得したチェーンから、確率的に1つ選ぶ
        triplet = self._get_probable_triplet(chains)

        return (triplet["prefix1"], triplet["prefix2"], triplet["suffix"])

    def _get_probable_triplet(self, chains):
        # チェーンの配列の中から確率的に1つを返す

        # 確率配列
        probability = []

        # 確率に合うように、インデックスを入れる
        for i in chains.index:
            for j in range(chains.loc[i,"freq"]):
                probability.append(i)

        # ランダムに1つを選ぶ
        chain_index = random.choice(probability)

        return chains.loc[chain_index]

if __name__ == '__main__':

    name = "アスカ"
    GT = GenerateText(name, n=20)

    GT.generate()

