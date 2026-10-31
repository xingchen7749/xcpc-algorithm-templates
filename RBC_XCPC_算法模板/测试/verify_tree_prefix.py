"""Compile both standalone templates and compare path sums with direct traversal."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEST = r'''
int main()
{
    mt19937 rng(20261018);
    long long checks = 0;
    for (int mode = 0; mode < 3; ++mode)
    {
        for (int n = 1; n <= 40; ++n)
        {
            vector<vector<int>> g(n + 1);
            vector<vector<pair<int, i64>>> edges(n + 1);
            vector<i64> point(n + 1);
            for (int u = 1; u <= n; ++u) point[u] = (int)(rng() % 201) - 100;
            for (int u = 2; u <= n; ++u)
            {
                int p = mode == 0 ? u - 1 : mode == 1 ? 1
                                                      : 1 + rng() % (u - 1);
                i64 w = (int)(rng() % 201) - 100;
                g[u].push_back(p);
                g[p].push_back(u);
                edges[u].push_back({p, w});
                edges[p].push_back({u, w});
            }
            for (int root : {1, n, 1 + (int)(rng() % n)})
            {
                vector<int> father(n + 1, -1), order{root};
                vector<i64> a(n + 1, 777);
                father[root] = root;
                for (int i = 0; i < n; ++i)
                {
                    int u = order[i];
                    for (auto [v, w] : edges[u])
                    {
                        if (father[v] != -1) continue;
                        father[v] = u;
                        a[v] = w;
                        order.push_back(v);
                    }
                }
                TreePointPrefix points(g, point, root);
                TreeEdgePrefix weights(g, a, root);
                for (int s = 1; s <= n; ++s)
                {
                    vector<int> seen(n + 1);
                    vector<i64> ps(n + 1), es(n + 1);
                    vector<int> q{s};
                    seen[s] = 1;
                    ps[s] = point[s];
                    for (int i = 0; i < n; ++i)
                    {
                        int u = q[i];
                        assert(points.query(s, u) == ps[u]);
                        assert(weights.query(s, u) == es[u]);
                        checks += 2;
                        for (auto [v, w] : edges[u])
                        {
                            if (seen[v]) continue;
                            seen[v] = 1;
                            ps[v] = ps[u] + point[v];
                            es[v] = es[u] + w;
                            q.push_back(v);
                        }
                    }
                }
            }
        }
    }
    int n = 200000;
    vector<vector<int>> g(n + 1);
    vector<i64> a(n + 1, 1000000000LL);
    for (int u = 2; u <= n; ++u)
    {
        g[u].push_back(u - 1);
        g[u - 1].push_back(u);
    }
    TreePointPrefix points(g, a, n);
    TreeEdgePrefix weights(g, a, n);
    assert(points.query(1, n) == 1LL * n * a[1]);
    assert(weights.query(1, n) == 1LL * (n - 1) * a[1]);
    cout << checks + 2 << " path-sum checks passed\n";
}
'''

with tempfile.TemporaryDirectory(prefix='tree_prefix_') as tmp:
    tmp = Path(tmp)
    bodies = []
    for index, name in enumerate(('3.8.1 点权前缀和（TreePointPrefix）.cpp',
                                  '3.8.2 边权前缀和（TreeEdgePrefix）.cpp')):
        source = ROOT / '代码/03_图论与树' / name
        subprocess.run(['g++', '-std=c++17', '-O2', str(source), '-o', str(tmp / f'standalone{index}.exe')], check=True)
        body = source.read_text(encoding='utf-8').split('void solve()')[0]
        if index:
            body = body[body.index('class TreeEdgePrefix'):]
        bodies.append(body)
    test = tmp / 'verify.cpp'
    test.write_text('\n'.join(bodies) + TEST, encoding='utf-8')
    exe = tmp / 'verify.exe'
    subprocess.run(['g++', '-std=c++17', '-O2', str(test), '-o', str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
