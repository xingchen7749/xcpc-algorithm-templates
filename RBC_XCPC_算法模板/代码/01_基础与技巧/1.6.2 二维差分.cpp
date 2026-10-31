#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;
#define endl '\n'
// #define int long long

// 由矩形数组 a[1..n][1..m] 构造二维差分，要求 n,m>=1。
// 忽略第 0 行和第 0 列，不修改 a；返回 diff，时间和空间均为 O(nm)。
vector<vector<i64>> difference(const vector<vector<i64>>& a)
{
    assert(a.size() >= 2 && a[0].size() >= 2);
    int n = (int)a.size() - 1;
    int m = (int)a[0].size() - 1;
    // diff：二维差分数组；第 n+1 行、第 m+1 列用于更新边界标记。
    vector<vector<i64>> diff(n + 2, vector<i64>(m + 2));
    for (int i = 1; i <= n; ++i)
    {
        assert((int)a[i].size() == m + 1);
        for (int j = 1; j <= m; ++j)
        {
            diff[i][j] = a[i][j];
            if (i > 1) diff[i][j] -= a[i - 1][j];
            if (j > 1) diff[i][j] -= a[i][j - 1];
            if (i > 1 && j > 1)
            {
                diff[i][j] += a[i - 1][j - 1];
            }
        }
    }
    return diff;
}

// 在 diff 上记录闭矩形 [x1,x2] × [y1,y2] 的元素加 v，无返回值。
// diff 由 difference 构造；要求矩形非空且下标有效，时间 O(1)。
void range_add(vector<vector<i64>>& diff,
    int x1, int y1, int x2, int y2, i64 v)
{
    assert(1 <= x1 && x1 <= x2 && x2 < (int)diff.size() - 1);
    assert(1 <= y1 && y1 <= y2 && y2 < (int)diff[0].size() - 1);
    diff[x1][y1] += v;
    diff[x2 + 1][y1] -= v;
    diff[x1][y2 + 1] -= v;
    diff[x2 + 1][y2 + 1] += v;
}

// 将 difference 构造的 diff 还原为 a[1..n][1..m]，第 0 行、第 0 列为 0。
// 不修改 diff，允许继续更新后再次还原；返回 a，时间和空间均为 O(nm)。
vector<vector<i64>> restore(const vector<vector<i64>>& diff)
{
    assert(diff.size() >= 3 && diff[0].size() >= 3);
    int n = (int)diff.size() - 2;
    int m = (int)diff[0].size() - 2;
    vector<vector<i64>> a(n + 1, vector<i64>(m + 1));
    for (int i = 1; i <= n; ++i)
    {
        for (int j = 1; j <= m; ++j)
        {
            a[i][j] = a[i - 1][j] + a[i][j - 1]
                - a[i - 1][j - 1] + diff[i][j];
        }
    }
    return a;
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
