import functools
import math
import operator
import typing

class LevenshteinSimilarity:
    """Levenshtein距離による文字列の類似度を計算する"""

    def __init__(self, param=5):
        """paramは類似度算出のためのパラメータ。値が大きくなるほど変化がゆるやかになる。"""
        self.param = int(abs(param))

    @functools.lru_cache(maxsize=None)
    def levenshtein_distance(self, a: str, b: str) -> int:
        """文字列間のLevenshtein距離を計算する"""
        if not a:
            return len(b)
        if not b:
            return len(a)
        return min(self.levenshtein_distance(a[1:], b[1:]) + (a[0] != b[0]), self.levenshtein_distance(a[1:], b) + 1,
                   self.levenshtein_distance(a, b[1:]) + 1)

    def __call__(self, a: str, b: str) -> float:
        """文字列の類似度を計算する。類似度は0から1の間で1に近いほど類似度が高い。"""
        distance = self.levenshtein_distance(a, b)
        return math.exp(-distance / self.param)

if __name__ == "__main__":

    lev = LevenshteinSimilarity(10)
    hoge = "長谷成人"
    foo = "長谷"
    print("Levenshtein Similarity:", lev(hoge, foo))
    print()