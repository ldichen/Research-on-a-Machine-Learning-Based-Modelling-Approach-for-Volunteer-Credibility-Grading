import time

import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Cookie': 'Ffvy8doNUuzTO=60NCJGCeT_h.PrARTTDo2..cwfQ7wHwS6T.wIHEAoRas7fniCX1dWBk4xHDD8VGCz8VLKszp.qbffW5g4iAqaJeq; JSESSIONID=E6FD28F74DC4EE968280AA6B2AAF7750; Ffvy8doNUuzTP=0Lkkhhs_XXTkQKi_ljkD12iq4hlmBfa9Cs3vVcMKgeYASwTEm6gtEXbhmWtP6KMSlOgxbhqIATHT0yhU_paIqpKO0UoWiL208fbHHqH8bxMWVZUToXRuX8ERErLHjiMi5D3jCpC1z3pH6F6IRgXbn7EpMS_myFY2cAf0N05GnzNaoLfT6s2uqMhI6gWZBEgKMTk7CcS0TbrM7_FfrW1ySMv2yIxK.Roxwj9p28e48X3ortYpYiILEPAPoe0cJOlcbqwD_wKI4F93koIJu7PALFtCRimZqK2XGCRG36JPZkxbwA4UCqM1ZoLdP3hPEoUK9flbzz4UwAIpXvOUa94QSKT0ii9JS7EegiVTUys8IUwYennroD5jbNKeS8wGd8kelRNTuyqdSN0Ke3FocAS2oY_..22mTbWSGR0dlQGC7aiW'
}

res = requests.get('https://geomodeling.njnu.edu.cn/dataTransferServer/data/bdd1bb11-2b4f-4d15-a87e-c14998645689',
                   headers=header)
# res = requests.get('https://geomodeling.njnu.edu.cn/dataTransferServer/data/bdd1bb11-2b4f-4d15-a87e-c14998645689')
print(res.status_code)
