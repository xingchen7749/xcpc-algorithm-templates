#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;
#define endl '\n'
// #define int long long

// 二维整数点，也用于表示二维向量。
struct Point
{
    i64 x, y;
    // 按 (x,y) 字典序比较当前点和 b，供严格排序使用；不使用浮点容差，O(1)。
    bool operator<(Point b) const
    {
        return tie(x, y) < tie(b.x, b.y);
    }
    // 判断当前点与 b 的两个整数坐标是否完全相等，供点集去重使用，O(1)。
    bool operator==(Point b) const
    {
        return x == b.x && y == b.y;
    }
};
// 返回二维向量 a 与 b 的叉积，绝对值为平行四边形面积。
// 正值表示逆时针，负值表示顺时针，0 表示共线或存在零向量。
// 坐标绝对值不超过 10^18；先转为 i128 再乘法，时间 O(1)。
i128 cross(Point a, Point b)
{
    return i128(a.x) * b.y - i128(a.y) * b.x;
}

// 返回向量 AB 与 AC 的叉积，即三角形 ABC 的两倍有向面积。
// a != b 时，正值表示 c 在 a→b 左侧，负值表示右侧；0 表示三点共线。
// 坐标绝对值不超过 10^18；先转为 i128 再减法，时间 O(1)。
i128 cross(Point a, Point b, Point c)
{
    i128 x1 = i128(b.x) - a.x;
    i128 y1 = i128(b.y) - a.y;
    i128 x2 = i128(c.x) - a.x;
    i128 y2 = i128(c.y) - a.y;
    return x1 * y2 - y1 * x2;
}

void solve()
{
    // Read one test case. Arrays and vertices use 1..n.
}
signed main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    cin >> T;  // Remove for a single test case.
    while (T--) solve();
}
