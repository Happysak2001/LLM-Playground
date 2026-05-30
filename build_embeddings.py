"""
Run this once locally to generate data/embeddings.npz
Uses the already-downloaded GloVe model via gensim.
Output file is committed to git — Streamlit Cloud never needs gensim.
"""
import numpy as np
import json
import os

import gensim.downloader
wv = gensim.downloader.load("glove-wiki-gigaword-50")

# ── Vocabulary to save ────────────────────────────────────────────
# word map + arithmetic + search sentences + common words for user input
CORE = [
    # word map
    "cat","dog","fish","bird","horse",
    "king","queen","prince","princess","crown",
    "computer","software","algorithm","database","code",
    "pizza","bread","coffee","soup","rice",
    "happy","sad","angry","calm","fear",
    "football","basketball","tennis","swimming","running",
    # arithmetic
    "man","woman","boy","girl","father","mother",
    "son","daughter","uncle","aunt","brother","sister","husband","wife",
    # search sentences words
    "stock","market","fell","sharply","today","scientists","discovered",
    "species","deep","sea","team","won","championship","final","minute",
    "programming","language","released","google","patient","recovered",
    "surgery","heavy","rainfall","caused","flooding","region","latest",
    "smartphone","features","foldable","screen","astronomers","detected",
    "signal","distant","galaxy","chef","opened","restaurant","downtown",
    "electric","vehicles","outsell","petrol","cars","norway",
    # common words for user sentence similarity
    "the","a","an","is","are","was","were","be","been","being",
    "have","has","had","do","does","did","will","would","could","should",
    "may","might","shall","can","need","dare","ought","used",
    "i","you","he","she","it","we","they","me","him","her","us","them",
    "my","your","his","its","our","their","mine","yours","hers","ours",
    "this","that","these","those","which","who","whom","whose","what","where",
    "when","why","how","all","both","each","few","more","most","other",
    "some","such","no","not","only","same","so","than","too","very",
    "just","but","and","or","if","in","on","at","to","of","for","with",
    "about","as","into","through","during","before","after","above","below",
    "from","up","down","out","off","over","under","between","among","then",
    "once","here","there","again","further","also","new","old","good","great",
    "big","small","long","little","own","right","large","next","early","young",
    "important","public","private","real","best","free","sure","every","near",
    "run","go","come","see","know","get","give","take","make","think","look",
    "want","use","find","tell","ask","work","seem","feel","try","leave","call",
    "keep","let","begin","show","hear","play","move","live","believe","hold",
    "bring","happen","write","provide","sit","stand","lose","pay","meet","include",
    "continue","set","learn","change","lead","understand","watch","follow","stop",
    "create","speak","read","spend","grow","open","walk","win","offer","remember",
    "love","consider","appear","buy","wait","serve","die","send","expect","build",
    "stay","fall","cut","reach","kill","remain","suggest","raise","pass","sell",
    "require","report","decide","pull","time","year","people","way","day","man",
    "world","life","hand","part","place","case","week","company","system","program",
    "question","government","number","night","point","home","water","room","mother",
    "area","money","story","fact","month","lot","right","study","book","eye","job",
    "word","business","issue","side","kind","head","house","service","friend","father",
    "power","hour","game","line","end","among","turn","city","community","name",
    "president","team","minute","body","back","social","state","family","student",
    "group","country","problem","hand","history","war","result","change","reason",
    "research","girl","guy","moment","air","teacher","force","education","never",
    "medical","law","news","health","food","child","black","white","red","green",
    "blue","high","low","deep","far","hard","hot","cold","dark","light","fast","slow",
    "bad","better","different","early","easy","free","full","high","large","late",
    "local","long","main","major","military","national","new","next","old","open",
    "other","own","political","possible","public","real","recent","second","small",
    "social","special","strong","true","white","whole","young",
]

vocab = sorted(set(w.lower() for w in CORE if w.lower() in wv))
vectors = np.array([wv[w] for w in vocab], dtype=np.float32)

os.makedirs("data", exist_ok=True)
np.savez_compressed("data/embeddings.npz", vectors=vectors)
with open("data/vocab.json", "w") as f:
    json.dump(vocab, f)

print(f"Saved {len(vocab)} words × {vectors.shape[1]} dims")
print(f"File size: {os.path.getsize('data/embeddings.npz') / 1024:.1f} KB")
