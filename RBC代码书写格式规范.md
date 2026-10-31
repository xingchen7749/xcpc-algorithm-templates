# RBC代码书写格式规范

## 1. 缩进与大括号

每层缩进使用 **4 个空格**，不混用 Tab。

左大括号放在当前行末尾，右大括号单独一行，与所属语句对齐。

```cpp
void solve() {
    for (int i = 1; i <= n; i++) {
        if (a[i] > 0) {
            ans += a[i];
        }
    }
}
```

`else`、`else if` 另起一行，与对应的 `if` 对齐。

```cpp
if (x < 0) {
    ans = -1;
}
else if (x == 0) {
    ans = 0;
}
else {
    ans = 1;
}
```

类和结构体的访问标记与大括号对齐，成员缩进一层。

```cpp
class ST {
private:
    int n;
    vector<vector<int>> st;

public:
    // 返回原数组的元素数量。
    int size() const {
        return n;
    }
};
```

## 2. 空格

二元运算符、赋值运算符两侧加空格；逗号后加空格，前面不加。

```cpp
int mid = l + (r - l) / 2;
ans += a[i];
add(u, v, w);
vector<vector<int>> st;
```

`if`、`for`、`while`、`switch` 与左括号之间加空格；函数名与左括号之间不加。

```cpp
if (x > 0) {
    update(x);
}

for (int i = 1; i <= n; i++) {
    cin >> a[i];
}
```

括号内部不额外加空格，成员访问和单目运算符保持紧凑。

```cpp
a[i]
q.front()
node.sum
ptr->next
i++
!found
```

引用和指针符号跟随类型书写：

```cpp
const vector<int>& a
Node* root
```

## 3. 哪些地方换行

一行通常写一条语句。多次赋值、修改和函数调用分别换行。

```cpp
dist[v] = dist[u] + w;
father[v] = u;
q.push({dist[v], v});
```

不要把多个操作挤在一行：

```cpp
// 避免这样的写法。
dist[v] = dist[u] + w; father[v] = u; q.push({dist[v], v});
```

核心算法步骤、多步操作和嵌套流程使用大括号展开。

```cpp
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        dp[i][j] = dp[i - 1][j];
        if (j >= w[i]) {
            dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i]] + v[i]);
        }
    }
}
```

简单的提前返回、跳过、直接操作，以及输入输出循环可以单行。

```cpp
if (l > r) return;
if (vis[u]) continue;
if (a > b) swap(a, b);
for (int i = 1; i <= n; i++) cin >> a[i];
```

`if ... else ...` 中只要一侧需要展开，两侧都使用大括号。

## 4. 长语句与续行

正常长度的表达式不必拆开。过长时，在参数之间或逻辑运算符处换行，续行增加一层缩进。

长条件换行时，将逻辑运算符放在续行开头：

```cpp
if (1 <= nx && nx <= n
    && 1 <= ny && ny <= m
    && !vis[nx][ny]) {
    vis[nx][ny] = true;
    q.push({nx, ny});
}
```

函数调用参数过长时，可以每个参数单独一行，右括号与调用语句起点对齐：

```cpp
update(
    root,
    1,
    n,
    query_l,
    query_r,
    delta
);
```

不为了让续行对齐某个括号而添加大量空格，统一按缩进层级排版。

## 5. 空行

函数之间留一个空行。函数内部不同逻辑阶段之间按需留一个空行。

```cpp
void solve() {
    int n;
    cin >> n;

    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    sort(a.begin() + 1, a.end());

    for (int i = 1; i <= n; i++) cout << a[i] << " ";
    cout << endl;
}
```

紧密相关的语句保持连续，不必每行之间都加空行；通常不连续留多个空行。

## 6. 对齐

依靠缩进表示代码层级，不强制纵向对齐变量名、等号或行尾注释。

```cpp
int n = 0;
int edge_count = 0;
i64 ans = 0;
```

无需写成：

```cpp
int n          = 0;
int edge_count = 0;
i64 ans        = 0;
```

同一层级的语句使用相同缩进。右大括号与对应的函数、循环或分支起点对齐。

## 7. 变量命名

采用竞赛常用短名；复杂含义使用小写下划线命名。

```cpp
int n, m;
int l, r, mid;
i64 ans;
i64 path_sum;
int edge_count;
```

常见名称约定：

| 含义 | 名称 |
| --- | --- |
| 规模 | `n、m` |
| 循环下标 | `i、j、k` |
| 普通数组、字符串 | `a、b、s、t` |
| 区间端点、中点 | `l、r、mid` |
| 图的端点、边权 | `u、v、w` |
| 答案、计数、总和 | `ans、cnt、sum` |
| 最大值、最小值 | `mx、mn` |
| 距离、深度、访问标记 | `dist、dep、vis` |
| 父节点、大小、秩 | `father、sz、rk` |
| 模数、余数 | `mod、rem` |
| 前缀、后缀、前驱 | `pre、suf、prev` |

布尔变量应表达判断含义：

```cpp
bool found;
bool is_prime;
bool has_cycle;
```

复杂含义不要随意缩写。例如路径和使用 `path_sum`，不写成难以理解的 `ps` 或 `sum2`。

同一含义尽量保持同名，例如深度统一使用 `dep`。算法已有惯用名称或专门约定时保留，例如 `pi`、`sa`。

前缀、后缀默认用 `pre`、`suf`，通过注释说明保存的内容。只有同时维护多种信息时，再使用 `pre_sum`、`pre_mx` 等名称区分。

## 8. 变量声明

同类型、含义紧密相关的简单变量可以放在同一行：

```cpp
int n, m;
int l = 1, r = n;
```

含义不同、初始化较复杂，或者需要分别注释的变量分行声明：

```cpp
vector<int> dep;     // 节点深度。
vector<int> father;  // 父节点编号。
vector<i64> dist;    // 从起点到各节点的距离。
```

指针和普通变量不要混在同一条声明中：

```cpp
Node* root;
Node* current;
int cnt;
```

## 9. 注释排版

函数说明放在函数上方，与函数声明对齐。

```cpp
// 返回 x 的最低有效二进制位所代表的值。
int lowbit(int x) {
    return x & -x;
}
```

短变量说明放在行尾，代码与 `//` 之间留两个空格，`//` 后留一个空格。

```cpp
vector<int> sz;  // 子树大小。
```

注释较长时移到代码上方，避免把整行拉得过长。

```cpp
// 保存分区基准的值，避免后续交换数组元素时改变比较基准。
int pivot = a[l + (r - l) / 2];
```

注释与它解释的代码保持相同缩进。说明关键含义和原因，不逐行翻译代码。
