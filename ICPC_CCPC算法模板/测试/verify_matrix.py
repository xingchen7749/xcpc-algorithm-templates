"""Compare generated matrix templates with direct rectangle operations."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEST = r'''
int main() {
    mt19937 rng(20261020);
    long long checks = 0;
    for (int n = 1; n <= 8; ++n) {
        for (int m = 1; m <= 8; ++m) {
            vector<vector<i64>> a(n + 1, vector<i64>(m + 1, 777));
            for (int i = 1; i <= n; ++i) {
                for (int j = 1; j <= m; ++j) {
                    a[i][j] = ((int)(rng() % 201) - 100) * 1000000000LL;
                }
            }
            auto original = a;
            auto diff = difference(a);
            assert(a == original);
            for (int j = 0; j <= m; ++j) a[0][j] = 0;
            for (int i = 0; i <= n; ++i) a[i][0] = 0;
            for (int step = 0; step < 30; ++step) {
                auto saved = diff;
                assert(restore(diff) == a);
                assert(restore(diff) == a && diff == saved);
                auto pre = prefix_sum(step == 0 ? original : a);
                assert(original[0][0] == 777);
                for (int x1 = 1; x1 <= n; ++x1) {
                    for (int x2 = x1; x2 <= n; ++x2) {
                        for (int y1 = 1; y1 <= m; ++y1) {
                            for (int y2 = y1; y2 <= m; ++y2) {
                                i64 sum = 0;
                                for (int i = x1; i <= x2; ++i) {
                                    for (int j = y1; j <= y2; ++j) sum += a[i][j];
                                }
                                assert(query(pre, x1, y1, x2, y2) == sum);
                                ++checks;
                            }
                        }
                    }
                }
                int x1 = 1 + rng() % n, x2 = 1 + rng() % n;
                int y1 = 1 + rng() % m, y2 = 1 + rng() % m;
                if (x1 > x2) swap(x1, x2);
                if (y1 > y2) swap(y1, y2);
                if (step % 5 == 0) {
                    x1 = y1 = 1;
                    x2 = n;
                    y2 = m;
                }
                i64 v = ((int)(rng() % 201) - 100) * 1000000000LL;
                if (step % 7 == 0) v = 0;
                range_add(diff, x1, y1, x2, y2, v);
                for (int i = x1; i <= x2; ++i) {
                    for (int j = y1; j <= y2; ++j) a[i][j] += v;
                }
            }
            assert(restore(diff) == a);
            vector<vector<i64>> zero(n + 2, vector<i64>(m + 2));
            range_add(zero, n, m, n, m, -123);
            auto restored = restore(zero);
            for (int i = 1; i <= n; ++i) {
                for (int j = 1; j <= m; ++j) {
                    assert(restored[i][j] == (i == n && j == m ? -123 : 0));
                }
            }
        }
    }
    cout << checks << " rectangle queries and matrix updates passed\n";
}
'''

with tempfile.TemporaryDirectory(prefix='matrix_check_') as directory:
    tmp = Path(directory)
    bodies = []
    for index, name in enumerate(('1.5.2 二维前缀和.cpp', '1.6.2 二维差分.cpp')):
        source = ROOT / '代码/01_基础与技巧' / name
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                        str(source), '-o', str(tmp / f'standalone{index}.exe')], check=True)
        bodies.append(source.read_text(encoding='utf-8').split('void solve()')[0])
    source = tmp / 'matrix.cpp'
    source.write_text('\n'.join(bodies) + TEST, encoding='utf-8')
    exe = tmp / 'matrix.exe'
    subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                    '-D_GLIBCXX_DEBUG', str(source), '-o', str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
