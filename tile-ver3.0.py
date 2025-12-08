import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 一部環境では不要だけど一応
import trimesh
import random
import numpy as np

# ある点とある点の直線上に、ある点からその直線上で距離t離れたときの点を求める関数
def kannkaku(point_sets, a):
    p1 = point_sets[0]
    p2 = point_sets[1]

    d = (p2[0]-p1[0]) ** 2 + (p2[1]-p1[1]) ** 2 + (p2[2]-p1[2]) ** 2

    d = np.sqrt(d)

    return p1[0] + a * (p2[0]-p1[0]) / d , p1[1] + a * (p2[1]-p1[1]) / d, p1[2] + a * (p2[2]-p1[2]) / d

# xyz空間における二つの線の交点を求める。理論的には二つの交点は必ず存在するが、数値的に交点を計算しているので、誤差が発生しているので普通に計算
# しても交点が求められるか、わからないため、二つの直線の距離が最も短いときの２点を平均を求める手法を取る。
def koten(k):
    A = k[0]
    B = k[1]

    C = k[2]
    D = k[3]

    ux = B[0] - A[0]
    uy = B[1] - A[1]
    uz = B[2] - A[2]

    vx = D[0] - C[0]
    vy = D[1] - C[1]
    vz = D[2] - C[2]

    wx = A[0] - C[0]
    wy = A[1] - C[1]
    wz = A[2] - C[2]

    a = ux ** 2 + uy ** 2 + uz ** 2
    b = ux * vx + uy * vy + uz * vz
    c = vx ** 2 + vy ** 2 + vz ** 2
    d = ux * wx + uy * wy + uz * wz
    e = vx * wx + vy * wy + vz * wz

    s = (b*e-c*d) / (a*c-b**2)
    t = (a*e-b*d) / (a*c-b**2)

    px = A[0] + s * ux
    py = A[1] + s * uy
    pz = A[2] + s * uz

    qx = C[0] + t * vx
    qy = C[1] + t * vy
    qz = C[2] + t * vz

    return (px + qx) / 2.0, (py + qy) / 2.0, (pz + qz) / 2.0

# ある点とある点を通る線分を回転軸として、ある点をθ度回転させる関数である。回転される方向に注意。
def xyz_θ(h, a):
    A = h[0]
    B = h[1]
    C = h[2]

    px = C[0] - A[0]
    py = C[1] - A[1]
    pz = C[2] - A[2]

    l = (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 + (A[2] - B[2]) ** 2
    n = np.sqrt(l)

    ux = (B[0] - A[0]) / n
    uy = (B[1] - A[1]) / n
    uz = (B[2] - A[2]) / n

    s1x = px * np.cos(np.radians(a))
    s1y = py * np.cos(np.radians(a))
    s1z = pz * np.cos(np.radians(a))

    s2x = (uy * pz - uz * py) * np.sin(np.radians(a))
    s2y = (px * uz - ux * pz) * np.sin(np.radians(a))
    s2z = (ux * py - px * uy) * np.sin(np.radians(a))

    s3x = ux * (ux * px + uy * py + uz * pz) * (1 - np.cos(np.radians(a)))
    s3y = uy * (ux * px + uy * py + uz * pz) * (1 - np.cos(np.radians(a)))
    s3z = uz * (ux * px + uy * py + uz * pz) * (1 - np.cos(np.radians(a)))

    return A[0] + s1x + s2x + s3x, A[1] + s1y + s2y + s3y, A[2] + s1z + s2z + s3z

def main():
    # 1辺の長さ1の正四面体を作る。4点の特徴点を定義
    # 1辺の長さを1としても、一般性を失われない。
    shimentai = np.zeros((4, 3), dtype=float)

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

    # 面Aと面Bのなす角
    ma = np.degrees(np.arccos(1/3)）
    
    # 配列　(どの面か0〜3, 点の番号、点の番号、xyz座標)
    men = np.zeros((4, grid, grid, 3), dtype=float)

    # 面A 0　底の面
    # 点C
    men[0, grid-1, 0, 0] = shimentai[2, 0]
    men[0, grid-1, 0, 1] = shimentai[2, 1]
    men[0, grid-1, 0, 2] = shimentai[2, 2]

    # 点A
    men[0, grid-1, grid-1, 0] = shimentai[0, 0]
    men[0, grid-1, grid-1, 1] = shimentai[0, 1]
    men[0, grid-1, grid-1, 2] = shimentai[0, 2]

    # 点B
    men[0, 0, 0, 0] = shimentai[1, 0]
    men[0, 0, 0, 1] = shimentai[1, 1]
    men[0, 0, 0, 2] = shimentai[1, 2]

    # 点Cと点Aの両端の点を除く、線分のグリッド点
    # 点Cと点Bの両端の点を除く、線分のグリッド点
    # 点Bと点Aの両端の点を除く、線分のグリッド点
    for i in range(1, grid-1):
        
        # 点Cと点A
        ptr1 = men[0, grid-1, 0, :]
        pty1 = men[0, grid-1, grid-1, :]

        point_sets1 = [ptr1, pty1]

        x1, y1, z1 =  kannkaku(point_sets1, n * i)

        men[0, grid-1, i, 0] = x1
        men[0, grid-1, i, 1] = y1
        men[0, grid-1, i, 2] = z1
        
        # 点Cと点B
        hyw1 = men[0, grid-1, 0, :]
        ghj1 = men[0, 0, 0, :]

        point_sets2 = [hyw1, ghj1]

        x2, y2, z2 = kannkaku(point_sets2, n * i)

        men[0, grid-1-i, 0, 0] = x2
        men[0, grid-1-i, 0, 1] = y2
        men[0, grid-1-i, 0, 2] = z2

        # 点Bと点A
        nhy1 = men[0, 0, 0, :]
        ghj1 = men[0, grid-1, grid-1, :]

        point_sets3 = [nhy1, ghj1]

        x3, y3 , z3 = kannkaku(point_sets3, n * i)

        men[0, i, i, 0] = x3
        men[0, i, i, 1] = y3
        men[0, i, i, 2] = z3
    
    # 正4面体の底の三角形ABCの内部のグリッドの点群の座標値を求める。
    for i in range(1, grid-1):
        m = 0

        for j in range(grid-2, 0, -1):

            ptw1 = men[0, grid-1, i, :]
            ptw2 = men[0, i, i, :]

            tyq1 = men[0, j, 0, :]
            tyq2 = men[0, j, j, :]

            point_sets4 = [ptw1, ptw2, tyq1, tyq2]

            x4, y4, z4 = koten(point_sets4)

            men[0, j, i, 0] = x4
            men[0, j, i, 1] = y4
            men[0, j, i, 2] = z4

            m = m + 1 # 新しい点を作られるたびにカウント

            if (grid-1-i) == m: # 必要な点を作られたらこのfor文を終了して、一番最初のfor文に戻る。
                break

    # 面B 1 面Aの点群を面Bに写す
    for i in range(0, grid):
        m = 0

        for j in range(grid-1, -1, -1):

            # 点Cと点Aを通る線
            ynu1 = men[0, grid-1, 0, :]
            ynu2 = men[0, grid-1, grid-1, :]

            # 回転させる点
            tby1 = men[0, j, i, :]

            point_sets5 = [ynu1, ynu2, tby1]

            x5, y5, z5 = xyz_θ(point_sets5, ma)

            # 3次元で任意の軸で回転する。
            men[1, j, i, 0]= x5
            men[1, j, i, 1]= y5 
            men[1, j, i, 2]= z5

            m = m + 1

            if m == (grid - i):
                break

    # 面C 2 面Aの点群を面Cに写す
    for i in range(grid-1, -1, -1):
        m = 0

        for j in range(0, grid):

            # 点Cと点Bを通る線
            akb1 = men[0, grid-1, 0, :]
            akb2 = men[0, 0, 0, :]

            # 回転させる点
            ghc1 = men[0, i, j, :]

            point_sets6 = [akb1, akb2, ghc1]

            x6, y6, z6 = xyz_θ(point_sets6, -ma)

            # 3次元で任意の軸で回転する。
            men[2, i, j, 0] = x6
            men[2, i, j, 1] = y6
            men[2, i, j, 2] = z6

            m = m + 1

            if m == i + 1:
                break

    # 面D 3　面Aの点群を面Dに写す
    for i in range(0, grid):
        m = 0

        for j in range(0, grid):

            # 点Bと点Aを通る線
            wet1 = men[0, 0, 0, :]
            wet2 = men[0, grid-1, grid-1, :]

            # 回転さえる点
            bbt1 = men[0, j, i, :]

            point_sets7 = [wet1, wet2, bbt1]

            x7, y7, z7 = xyz_θ(point_sets7, -ma)

            # 3次元で任意の軸で回転する。
            men[3, j, i, 0] = x7
            men[3, j, i, 1] = y7
            men[3, j, i, 2] = z7

            m = m + 1

            if m == grid - i:
                break

    # ====== 四面体の全ての面でのグリッドの定義完了 =====

    # 次は、配列自動探索コードの作成
    # 秋山仁の4面体タイル定理は、正四面体の適当な所に切り込みを入れて、4頂点をすべて通るように切り進んで一つの平面に展開します。
    # これと全く同じものを数個作成します。
    # これらを適当に組み合わせると、ジグソーパズルのように隙間なく敷き詰めることだできます。

    # まず、簡易的な自動探索
    i = random.randint(0, 3)




if __name__ == "__main__":
    main()
