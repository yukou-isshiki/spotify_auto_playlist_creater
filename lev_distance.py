def calc_distance(a, b):
    """
    レーベンシュタイン距離の比較
    :param a: 探したい対象物の表記
    :param b: Spotifyから返ってきた対象物の表記
    :return: 2つのレーベンシュタイン距離
    """
    if a == b: return  0
    a_len = len(a)
    b_len = len(b)
    if a == "":
        return b_len
    if b == "":
        return a_len
    matrix = [[] for i in range(a_len + 1)]
    for i in range(a_len + 1):
        matrix[i] = [0 for j in  range(b_len+1)]
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j
    for i in range(1, a_len + 1):
        ac = a[i-1]
        for j in range(1, b_len + 1):
            bc = b[j-1]
            cost = 0 if (ac == bc) else 1
            matrix[i][j] = min([matrix[i-1][j]+1, matrix[i][j-1]+1,matrix[i-1][j-1] + cost])
    return matrix[a_len][b_len]

