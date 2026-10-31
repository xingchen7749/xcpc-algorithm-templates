"""Compile the generated bigint template and compare all widths with Python integers."""
from pathlib import Path
import random
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from build_handbook import CODE_PATHS

SOURCE = ROOT / 'RBC_XCPC_算法模板/代码' / CODE_PATHS['bigint']
HARNESS = r"""
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string sa, sb;
    i64 k;
    while (cin >> sa >> sb >> k)
    {
        big_int a(sa), b(sb);
        auto output = [](const big_int& x)
        {
            assert(x.size() > 0);
            assert(x.size() == 1 || x.arr.back() != 0);
            assert(x.sign == 1 || x.sign == -1);
            assert(!x.is_zero() || x.sign == 1);
            for (int v : x.arr) assert(0 <= v && v < big_int::base);
            print(x);
            cout << '\n';
        };
        output(a);
        output(b);
        output(big_int(k));
        output(big_int());
        cout << compare(a, b) << '\n';
        output(a + b);
        output(a - b);
        output(a * b);
        output(a * k);
        output(-a);
        output(k * a);
        output(k + a);
        output(k - a);
        cout << (a < b) << '\n' << (a > b) << '\n'
             << (a <= b) << '\n' << (a >= b) << '\n'
             << (a == b) << '\n' << (a != b) << '\n';
        if (!b.is_zero())
        {
            auto [q, r] = divmod(a, b);
            output(q);
            output(r);
            output(a / b);
            output(a % b);
            assert(b * q + r == a);
            assert(compare_abs(r, b) < 0);
        }
        if (k != 0)
        {
            auto [q, r] = divmod(a, k);
            output(q);
            output(r);
            output(a / k);
            output(a % k);
        }
    }
}
"""

def trunc_divmod(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q, a - b * q


def main():
    rng=random.Random(20261010)
    values=[0,1,9,10,999,1000,1001,10**9-1,10**9,2**31-1,10**100-1,10**100,10**100+1]
    cases=[(str(a),str(b),rng.choice([0,1,999,1000,2**31-1])) for a in values for b in values]
    for _ in range(180):
        a=rng.randrange(10**rng.randrange(1,301))
        b=rng.randrange(10**rng.randrange(1,201))
        cases.append(('000'+str(a),'000'+str(b),rng.randrange(2**31)))
    cases.extend([('9'*1000,'1',2**31-1),('1'+'0'*1000,'9'*500,0),('0000','0000',0)])
    # Exercise every sign combination, signed zero, and the full i64 boundary.
    original = cases[:]
    cases.extend(('-'+a,b,-k) for a,b,k in original)
    cases.extend((a,'-'+b,-k) for a,b,k in original)
    cases.extend(('-'+a,'-'+b,k) for a,b,k in original)
    cases.extend([('+0000','-0000',-(2**63)),
                  ('-17','+5',2**63-1), ('+17','-5',-(2**63)),
                  (str(-(2**63)), '-1', -(2**63)),
                  ('-1', str(-(2**63)), 2**63-1)])
    expected=[]
    for sa,sb,k in cases:
        a,b=int(sa),int(sb)
        expected.extend(map(str,[a,b,k,0,(a>b)-(a<b),a+b,a-b,a*b,a*k,
                                 -a,k*a,k+a,k-a]))
        expected.extend(str(int(v)) for v in [a<b,a>b,a<=b,a>=b,a==b,a!=b])
        if b: expected.extend(map(str,trunc_divmod(a,b)*2))
        if k: expected.extend(map(str,trunc_divmod(a,k)*2))
    data=''.join(f'{a} {b} {k}\n' for a,b,k in cases)
    source=SOURCE.read_text(encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='verify_bigint_') as directory:
        temp=Path(directory)
        # Verify the real standalone file outside the project.
        standalone=temp/'standalone.cpp'
        standalone.write_text(source,encoding='utf-8')
        exe=temp/'standalone.exe'
        subprocess.run(['g++','-std=c++17','-O2',str(standalone),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],input='0\n',text=True,check=True)
        for width in range(1,10):
            body=source.split('void solve()',1)[0].replace('static constexpr int width = 3;',f'static constexpr int width = {width};')
            test=temp/'test.cpp'; exe=temp/'test.exe'
            test.write_text(body+HARNESS,encoding='utf-8')
            subprocess.run(['g++','-std=c++17','-O2','-D_GLIBCXX_ASSERTIONS',str(test),'-o',str(exe)],check=True)
            run=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=60)
            actual=run.stdout.splitlines()
            assert actual==expected, f'width={width}: mismatch'
            print(f'width={width}: {len(cases)} cases / {len(expected)} outputs passed',flush=True)
    print('Standalone compilation and all bigint checks passed.')

if __name__=='__main__':
    main()
