from datasketch import MinHash, MinHashLSH
from rapidfuzz import distance


class NodeLSHRetriever:
    def __init__(self, nodes, threshold=0.5, num_perm=128):
        self.nodes = nodes
        self.threshold = threshold
        self.num_perm = num_perm

        # LSH index
        self.lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

        # store
        self.value_store = {}
        self.minhash_store = {}

        # build index
        self._build_index()

    def build_minhash(self, text):
        m = MinHash(num_perm=self.num_perm)
        t = text.lower()

        # char-level
        for ch in t:
            m.update(ch.encode("utf8"))

        # word-level
        tokens = t.split()
        for tok in tokens:
            m.update(tok.encode("utf8"))

        return m

    def _build_index(self):
        for idx, val in enumerate(self.nodes):
            mh = self.build_minhash(val)
            vid = f"v{idx}"

            self.lsh.insert(vid, mh)
            self.value_store[vid] = val
            self.minhash_store[vid] = mh

        print("LSH indexing completed.")

    def search(self, keyword, top_k=1):
        mk = self.build_minhash(keyword)

        # LSH candidates
        candidates = self.lsh.query(mk)
        if not candidates:
            return []

        scored = []
        for cid in candidates:
            v = self.value_store[cid]
            mv = self.minhash_store[cid]

            # Jaccard similarity
            jacc = mk.jaccard(mv)

            # edit-distance similarity
            edit_sim = 1 - distance.Levenshtein.normalized_distance(
                keyword.lower(), v.lower()
            )

            # Combined score
            score = 0.6 * jacc + 0.4 * edit_sim

            scored.append((v, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [node for node, score in scored[:top_k]]
