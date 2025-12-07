
def kannkaku(point_sets, a):
    p1 = point_sets[0]
    p2 = point_sets[1]

    d = (p2[0]-p1[0]) ** 2 + (p2[1]-p1[1]) ** 2 + (p2[2]-p1[2]) ** 2

    d = np.sqrt(d)

    return p1[0] + a * (p2[0]-p1[0]) / d , p1[1] + a * (p2[1]-p1[1]) / d, p1[2] + a * (p2[2]-p1[2]) / d

def koten():


def main():
    # 1辺の長さ1の正四面体を作る。4点の特徴点を定義
    # 点A
    shimentai[0, 0] = 1/2
    shimentai[0, 1] = 0
    shimentai[0, 2] = 0

    # 点B
    shimentai[1, 0] = -shimentai[0, 0]
    shimentai[1, 1] = shimentai[0, 1]
    shimentai[1, 2] = shimentai[0, 2]

    # 点C
    shimentai[2, 0] = 0
    shimentai[2, 1] = (1 / 2) * np.sqrt(3)
    shimentai[2, 2] = 0

    # 点D
    shimentai[3, 0] = (shimentai[0,0] + shimentai[1, 0] + shimentai[2, 0]) / 3.0
    shimentai[3, 1] = (shimentai[0,1] + shimentai[1, 1] + shimentai[2, 1]) / 3.0
    shimentai[3, 2] = np.sqrt(6) / 3.0
    
    # 正四面体の1辺をどの程度細かくするのかの定数　両側の2点も含む
    grid = 1001 #　基本固定

    # 1辺の細かくした場合の1辺上にある点と点の距離
    n = 1 / (grid - 1) # 割り切れる方がいい
    
    # 配列　(どの面か0〜3, 点の番号、点の番号、xyz座標)
    # 面A 0
    men[0, grid-1, 0, 0] = shimentai[2, 0]
    men[0, grid-1, 0, 1] = shimentai[2, 1]
    men[0, grid-1, 0, 2] = shimentai[2, 2]

    men[0, grid-1, grid-1, 0] = shimentai[0, 0]
    men[0, grid-1, grid-1, 1] = shimentai[0, 1]
    men[0, grid-1, grid-1, 2] = shimentai[0, 2]

    men[0, 0, 0, 0] = shimentai[1, 0]
    men[0, 0, 0, 1] = shimentai[1, 1]
    men[0, 0, 0, 2] = shimentai[1, 2]

    for i in range(1, grid-1):

        ptr1 = men[0, grid-1, 0, :]
        pty1 = men[0, grid-1, grid-1, :]

        point_sets1 = [ptr1, pty1]

        x1, y1, z1 =  kannkaku(point_sets1, n * i)

        men[0, grid-1, i, 0] = x1
        men[0, grid-1, i, 1] = y1
        men[0, grid-1, i, 2] = z1

        hyw1 = men[0, grid-1, 0, :]
        ghj1 = men[0, grid-1, grid-1, :]

        point_sets2 = [hyw1, ghj1]

        x2, y2, z2 = kannkaku(point_set2, n * i)

        men[0, grid-1-i, 0, 0] = x2
        men[0, grid-1-i, 0, 1] = y2
        men[0, grid-1-i, 0, 2] = z2

        nhy1 = [0, 0, 0, :]
        ghj1 = [0, grid-1, grid-1, :]

        point_sets3 = [nhy1, ghj1]

        x3, y3 , z3 = kannkaku(point_sets3, n * i)

        men[0, i, i, 0] = x3
        men[0, i, i, 1] = y3
        men[0, i, i, 2] = z3
    
    for i in range(1, grid-1):
        for j in range(grid-2, 1, -1):










    



    



    # 面B 1

    # 面C 2

    # 面D 3
