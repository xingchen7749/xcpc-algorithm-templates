#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;
#define endl '\n'
// #define int long long

// Trie（名称源自 retrieval）：字典树。
class Trie {
private:
    struct Node {
        int ch[26] = {};  // 各字符对应的子节点，0 表示不存在
        int cnt = 0;     // 以当前路径为前缀的字符串数量，包含重复串
        int end = 0;     // 在当前节点结束的字符串数量
    };

    vector<Node> tr;  // tr[0] 占位，tr[1] 为根节点

    // 查找字符串 s 对应的节点；路径不存在时返回 0。
    int find(const string &s) const {
        int u = 1;
        for (char c : s) {
            assert('a' <= c && c <= 'z');
            int v = c - 'a';
            if (tr[u].ch[v] == 0) return 0;
            u = tr[u].ch[v];
        }
        return u;
    }

public:
    // 建立空字典树。
    Trie() : tr(2) {}

    // 清空所有字符串，恢复根节点。
    void clear() {
        tr.assign(2, Node{});
    }

    // 插入字符串 s，允许重复插入，时间复杂度 O(|s|)。
    void insert(const string &s) {
        int u = 1;
        tr[u].cnt++;
        for (char c : s) {
            assert('a' <= c && c <= 'z');
            int v = c - 'a';
            if (tr[u].ch[v] == 0) {
                int id = (int)tr.size();
                tr.emplace_back();
                tr[u].ch[v] = id;
            }
            u = tr[u].ch[v];
            tr[u].cnt++;
        }
        tr[u].end++;
    }

    // 返回完整字符串 s 的出现次数，不存在时返回 0。
    // 时间复杂度 O(|s|)。
    int count(const string &s) const {
        int u = find(s);
        return u == 0 ? 0 : tr[u].end;
    }

    // 返回以 s 为前缀的字符串数量，包含重复串。
    // 时间复杂度 O(|s|)；空前缀返回所有字符串的数量。
    int prefix_count(const string &s) const {
        int u = find(s);
        return u == 0 ? 0 : tr[u].cnt;
    }
};

void solve() {
    // Read one test case. Arrays and vertices use 1..n.
}
signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    cin >> T; // Remove for a single test case.
    while (T--) solve();
}
