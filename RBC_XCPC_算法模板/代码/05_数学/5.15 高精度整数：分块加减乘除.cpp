#include <bits/stdc++.h>
using namespace std;
using i64 = long long;
using i128 = __int128_t;
using u64 = unsigned long long;
#define endl '\n'
// #define int long long

// 返回 10^k，用于编译期计算分块基数；要求 0<=k<=9。
constexpr int power10(int k)
{
    int result = 1;
    while (k--) result *= 10;
    return result;
}

// 有符号高精度整数：arr 存绝对值，低位在前，从 0 下标开始。
// 零统一表示为 sign=1、arr={0}。
struct big_int
{
    static constexpr int width = 3;  // 只修改这里，每块 1～9 位
    static_assert(1 <= width && width <= 9, "width must be between 1 and 9");
    static constexpr int base = power10(width);
    vector<int> arr;  // 绝对值分块，每块位于 [0,base-1]
    int sign = 1;  // 1 表示非负，-1 表示负数

    // 将 i64 转为高精度整数，支持最小值，默认构造为 0。
    big_int(i64 x = 0)
    {
        sign = x < 0 ? -1 : 1;
        // 避免对 i64 最小值直接取负。
        u64 val = x < 0 ? (u64)(-(x + 1)) + 1 : (u64)x;
        do
        {
            arr.push_back((int)(val % base));
            val /= base;
        }
        while (val);
    }

    // 从十进制字符串构造，允许开头带正负号及前导零。
    big_int(const string& s)
    {
        assert(!s.empty());
        int start = 0;  // 数字部分起点
        if (s[0] == '+' || s[0] == '-')
        {
            sign = s[0] == '-' ? -1 : 1;
            start = 1;
        }
        assert(start < (int)s.size());
        for (int r = (int)s.size(); r > start; r -= width)
        {
            int x = 0;
            for (int l = max(start, r - width); l < r; ++l)
            {
                assert(s[l] >= '0' && s[l] <= '9');
                x = x * 10 + s[l] - '0';
            }
            arr.push_back(x);
        }
        trim();
    }

    // 返回有效块数。
    int size() const
    {
        return (int)arr.size();
    }

    // 删除最高端多余的零块，至少保留一块表示 0。
    void trim()
    {
        while (arr.size() > 1 && arr.back() == 0) arr.pop_back();
        if (is_zero()) sign = 1;
    }

    // 判断当前整数是否为 0。
    bool is_zero() const
    {
        return arr.size() == 1 && arr[0] == 0;
    }

    // 返回相反数，不修改当前对象；零仍保持正号。
    big_int operator-() const
    {
        big_int ans = *this;
        if (!ans.is_zero()) ans.sign = -ans.sign;
        return ans;
    }
};

// 输出 a，最高块正常输出，其余块补足 width 位；不自动换行。
void print(const big_int& a)
{
    if (a.sign < 0) cout << '-';
    cout << a.arr.back();
    for (int i = a.size() - 2; i >= 0; --i)
    {
        string s = to_string(a.arr[i]);
        cout << string(big_int::width - (int)s.size(), '0') << s;
    }
}

// 比较绝对值：小于返回 -1，相等返回 0，大于返回 1。
int compare_abs(const big_int& a, const big_int& b)
{
    if (a.size() != b.size()) return a.size() < b.size() ? -1 : 1;
    for (int i = a.size() - 1; i >= 0; --i)
    {
        if (a.arr[i] != b.arr[i]) return a.arr[i] < b.arr[i] ? -1 : 1;
    }
    return 0;
}

// 返回 |a|+|b|，结果非负，从低位向高位处理进位。
big_int add_abs(const big_int& a, const big_int& b)
{
    big_int result;
    int n = max(a.size(), b.size());
    result.arr.assign(n + 1, 0);
    int carry = 0;
    for (int i = 0; i < n; ++i)
    {
        int x = i < a.size() ? a.arr[i] : 0;
        int y = i < b.size() ? b.arr[i] : 0;
        int cur = x + y + carry;
        result.arr[i] = cur % big_int::base;
        carry = cur / big_int::base;
    }
    result.arr[n] = carry;
    result.trim();
    return result;
}

// 返回 |a|-|b|，要求 |a|>=|b|，结果非负。
big_int sub_abs(const big_int& a, const big_int& b)
{
    assert(compare_abs(a, b) >= 0);
    big_int result;
    result.arr.assign(a.size(), 0);
    int borrow = 0;
    for (int i = 0; i < a.size(); ++i)
    {
        int y = i < b.size() ? b.arr[i] : 0;
        int cur = a.arr[i] - y - borrow;
        borrow = cur < 0;
        if (borrow) cur += big_int::base;
        result.arr[i] = cur;
    }
    result.trim();
    return result;
}

// 返回 |a| 与单块 b 的乘积，要求 0<=b<base，供除法试商使用。
big_int mul_abs_digit(const big_int& a, int b)
{
    assert(0 <= b && b < big_int::base);
    if (b == 0 || a.is_zero()) return big_int(0);
    big_int result;
    result.arr.assign(a.size(), 0);
    i64 carry = 0;
    for (int i = 0; i < a.size(); ++i)
    {
        i64 cur = (i64)a.arr[i] * b + carry;
        result.arr[i] = (int)(cur % big_int::base);
        carry = cur / big_int::base;
    }
    while (carry)
    {
        result.arr.push_back((int)(carry % big_int::base));
        carry /= big_int::base;
    }
    result.trim();
    return result;
}

// 返回两个高精度整数的乘积，采用逐块竖式乘法。
big_int operator*(const big_int& a, const big_int& b)
{
    if (a.is_zero() || b.is_zero()) return big_int(0);
    big_int result;
    result.sign = a.sign * b.sign;
    result.arr.assign(a.size() + b.size(), 0);
    for (int i = 0; i < a.size(); ++i)
    {
        i64 carry = 0;
        for (int j = 0; j < b.size(); ++j)
        {
            i64 cur = result.arr[i + j] + (i64)a.arr[i] * b.arr[j] + carry;
            result.arr[i + j] = (int)(cur % big_int::base);
            carry = cur / big_int::base;
        }
        // 此位置尚未被之前的外层循环写入。
        result.arr[i + b.size()] = (int)carry;
    }
    result.trim();
    return result;
}

// 计算 |a| 除以正单块 b，返回非负 {商, 余数}。
pair<big_int, int> divmod_abs_digit(const big_int& a, int b)
{
    assert(b > 0);
    big_int quotient;
    quotient.arr.assign(a.size(), 0);
    i64 remainder = 0;
    for (int i = a.size() - 1; i >= 0; --i)
    {
        i64 cur = remainder * big_int::base + a.arr[i];
        quotient.arr[i] = (int)(cur / b);
        remainder = cur % b;
    }
    quotient.trim();
    return {quotient, (int)remainder};
}

// 计算 |a| 除以非零 |b|，返回非负 {商, 余数}。
// 采用竖式除法，每块商在 [0,base-1] 内二分。
pair<big_int, big_int> divmod_abs(const big_int& a, const big_int& b)
{
    assert(!b.is_zero());
    if (compare_abs(a, b) < 0)
    {
        big_int rem = a;
        rem.sign = 1;
        return {big_int(0), rem};
    }
    if (b.size() == 1)
    {
        auto [q, r] = divmod_abs_digit(a, b.arr[0]);
        return {q, big_int(r)};
    }
    big_int quotient, remainder;
    quotient.arr.assign(a.size(), 0);
    for (int i = a.size() - 1; i >= 0; --i)
    {
        // remainder = remainder*base + a.arr[i]。
        if (remainder.is_zero())
        {
            remainder.arr[0] = a.arr[i];
        }
        else
        {
            remainder.arr.insert(remainder.arr.begin(), a.arr[i]);
        }
        int l = 0, r = big_int::base;
        while (l + 1 < r)
        {
            int m = (l + r) / 2;
            big_int product = mul_abs_digit(b, m);
            if (compare_abs(product, remainder) <= 0)
            {
                l = m;
            }
            else
            {
                r = m;
            }
        }
        quotient.arr[i] = l;
        if (l != 0)
        {
            remainder = sub_abs(remainder, mul_abs_digit(b, l));
        }
    }
    quotient.trim();
    return {quotient, remainder};
}

// 比较有符号整数：小于返回 -1，相等返回 0，大于返回 1。
int compare(const big_int& a, const big_int& b)
{
    if (a.sign != b.sign) return a.sign < b.sign ? -1 : 1;
    return a.sign * compare_abs(a, b);
}

// 判断 a 是否小于 b。
bool operator<(const big_int& a, const big_int& b)
{
    return compare(a, b) < 0;
}

// 判断 a 是否大于 b。
bool operator>(const big_int& a, const big_int& b)
{
    return compare(a, b) > 0;
}

// 判断 a 是否小于等于 b。
bool operator<=(const big_int& a, const big_int& b)
{
    return compare(a, b) <= 0;
}

// 判断 a 是否大于等于 b。
bool operator>=(const big_int& a, const big_int& b)
{
    return compare(a, b) >= 0;
}

// 判断 a 是否等于 b。
bool operator==(const big_int& a, const big_int& b)
{
    return compare(a, b) == 0;
}

// 判断 a 是否不等于 b。
bool operator!=(const big_int& a, const big_int& b)
{
    return compare(a, b) != 0;
}

// 返回 a+b，同号相加，异号按绝对值大小相减。
big_int operator+(const big_int& a, const big_int& b)
{
    big_int ans;
    if (a.sign == b.sign)
    {
        ans = add_abs(a, b);
        ans.sign = a.sign;
    }
    else if (compare_abs(a, b) >= 0)
    {
        ans = sub_abs(a, b);
        ans.sign = a.sign;
    }
    else
    {
        ans = sub_abs(b, a);
        ans.sign = b.sign;
    }
    ans.trim();
    return ans;
}

// 返回 a-b，允许结果为负。
big_int operator-(const big_int& a, const big_int& b)
{
    return a + (-b);
}

// 返回有符号 {商, 余数}，要求 b 非零。
// 商向零取整，非零余数与 a 同号，满足 a=b*q+rem。
pair<big_int, big_int> divmod(const big_int& a, const big_int& b)
{
    auto [q, rem] = divmod_abs(a, b);
    q.sign = a.sign * b.sign;
    rem.sign = a.sign;
    q.trim();
    rem.trim();
    return {q, rem};
}

// 返回 a 除以非零 b 的整数商。
big_int operator/(const big_int& a, const big_int& b)
{
    return divmod(a, b).first;
}

// 返回 a 除以非零 b 的余数，返回类型统一为 big_int。
big_int operator%(const big_int& a, const big_int& b)
{
    return divmod(a, b).second;
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
