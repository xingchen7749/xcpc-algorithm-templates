#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;
#define endl '\n'
// #define int long long

// 由矩形数组 a[1..n][1..m] 构造二维前缀和，要求 n,m>=1。
// 忽略第 0 行和第 0 列，不修改 a；返回 pre，时间和空间均为 O(nm)。
vector<vector<i64>> prefix_sum(const vector<vector<i64>>& a)
{
    assert(a.size() >= 2 && a[0].size() >= 2);
    int n = (int)a.size() - 1;
    int m = (int)a[0].size() - 1;
    // pre[i][j]：矩形 [1,i] × [1,j] 的元素和，第 0 行和第 0 列为 0。
    vector<vector<i64>> pre(n + 1, vector<i64>(m + 1));
    for (int i = 1; i <= n; ++i)
    {
        assert((int)a[i].size() == m + 1);
        for (int j = 1; j <= m; ++j)
        {
            pre[i][j] = pre[i - 1][j] + pre[i][j - 1]
                - pre[i - 1][j - 1] + a[i][j];
        }
    }
    return pre;
}

// 返回闭矩形 [x1,x2] × [y1,y2] 的元素和，x 为行，y 为列。
// pre 由 prefix_sum 构造；要求矩形非空且下标有效，时间 O(1)。
i64 query(const vector<vector<i64>>& pre,
    int x1, int y1, int x2, int y2)
{
    assert(1 <= x1 && x1 <= x2 && x2 < (int)pre.size());
    assert(1 <= y1 && y1 <= y2 && y2 < (int)pre[0].size());
    return pre[x2][y2] - pre[x1 - 1][y2]
        - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1];
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
