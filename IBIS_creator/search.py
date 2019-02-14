# cording: utf-8
# import MeCab

# mecab_dic_path = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'
# refer to
# http://chasen.naist.jp/snapshot/ipadic/ipadic/doc/ipadic-ja.pdf
# https://github.com/taku910/mecab/blob/master/mecab-ipadic/pos-id.def
# tagger = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def search(query):

    query_dic = dict()
    query_dic["query"] = []

    """
    tagger = MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(query)

    # 名詞の抜き出し
    noun_list = [36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 67]


    while node:
        if node.posid in noun_list:
            query_dic["query"].append(node.surface)
        node = node.next

    if len(query_dic) != 0:
        query_dic["query"].append("wiki")
        query_dic["query"].append("現状")
        query_dic["query"].append("対策")
        query_dic["query"] = sorted(set(query_dic["query"]), key=query_dic["query"].index)

    """

    return query_dic
