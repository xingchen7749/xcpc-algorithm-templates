"""Compile the standalone Trie and compare queries with a string list."""
from pathlib import Path
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / '代码/04_字符串/4.5 普通字典树.cpp'
TEST = r'''
int main()
{
    Trie trie;
    assert(trie.count("") == 0 && trie.prefix_count("") == 0);
    trie.insert("apple");
    trie.insert("apple");
    trie.insert("app");
    trie.insert("");
    assert(trie.count("apple") == 2 && trie.count("ap") == 0);
    assert(trie.prefix_count("app") == 3 && trie.prefix_count("") == 4);
    assert(trie.count("") == 1 && trie.prefix_count("z") == 0);
    trie.clear();
    assert(trie.count("apple") == 0 && trie.prefix_count("") == 0);
    string long_word(100000, 'z');
    trie.insert(long_word);
    assert(trie.count(long_word) == 1);
    assert(trie.prefix_count(long_word.substr(0, 99999)) == 1);
    trie.clear();

    mt19937 rng(20261023);
    vector<string> a;
    for (int step = 0; step < 20000; step++)
    {
        string s;
        int len = rng() % 15;
        for (int i = 0; i < len; i++) s += char('a' + rng() % 26);
        if (!a.empty() && rng() % 2 == 0)
        {
            s = a[rng() % a.size()];
            if (rng() % 2 == 0) s.resize(rng() % (s.size() + 1));
        }
        if (step % 997 == 0)
        {
            trie.clear();
            a.clear();
        }
        else if (rng() % 3 == 0)
        {
            trie.insert(s);
            a.push_back(s);
        }
        int exact = 0, prefix = 0;
        for (const string& t : a)
        {
            exact += t == s;
            prefix += t.compare(0, s.size(), s) == 0;
        }
        assert(trie.count(s) == exact);
        assert(trie.prefix_count(s) == prefix);
        assert(trie.prefix_count("") == (int)a.size());
    }
    cout << "Trie: boundaries and 20000 randomized operations passed.\n";
}
'''

with tempfile.TemporaryDirectory(prefix='trie_') as directory:
    folder = Path(directory)
    original = SOURCE.read_text(encoding='utf-8')
    (folder / 'standalone.cpp').write_text(original, encoding='utf-8')
    (folder / 'test.cpp').write_text(
        original.replace('signed main()', 'void template_main()') + TEST,
        encoding='utf-8',
    )
    for name in ('standalone', 'test'):
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                        str(folder / (name + '.cpp')), '-o', str(folder / (name + '.exe'))], check=True)
    subprocess.run([str(folder / 'test.exe')], check=True)
