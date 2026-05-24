# Video 5.2 Transcript Draft

Title: 从连接规则到幂律：BA 模型为什么给出 \(\gamma=3\)？

English working title: From Attachment Rules to Power Laws: Why the BA Model
Gives \(\gamma=3\)

Purpose: This merged video replaces the former separate algorithm and
continuum-theory videos. It keeps only the algorithm details needed for the
derivation, then derives the BA degree distribution.

Human audio recording:

```text
media/audio/audio1593684705.m4a
```

Human-audio final:

```text
media/videos/video5_2_human_audio_final_720p30.mp4
```

## Human Audio Alignment

| Scene | Time | Notes |
|---|---:|---|
| `BAAlgorithmDefinition` | 0:00-1:19 | Intro, algorithm inputs, algorithm loop. |
| `BARoleOfM` | 1:19-2:12 | \(m\) fixes birth degree and affects density/average degree. |
| `BAContinuumSetup` | 2:12-3:27 | \(N(t)\), \(E(t)\), total degree, large-\(t\) approximation. |
| `BADegreeGrowthEquation` | 3:27-5:03 | Expected degree, stochastic jumps, differential equation solution. |
| `BABirthTimeDistribution` | 5:03-5:29 | Earlier birth time gives higher expected degree. |
| `BAPowerLawExponent` | 5:29-6:11 | CDF, PDF, and \(p(k)\sim k^{-3}\). |
| `BAExponentRegimeMap` | 6:11-7:30 | \(\gamma=3\) as the boundary between regimes. |
| `BASimulationSanityCheck` | 7:30-8:07 | Finite simulation and noisy tail. |
| `BATheoryTakeaway` | 8:07-8:29 | Next video transition. |

Raw Whisper transcription is saved under:

```text
media/audio/transcription/audio1593684705.*
```

## BAAlgorithmDefinition

### 中文

上一段视频里，我们看到 hub 可以从“增长”和“偏好连接”中自然出现。现在
的问题是：这个直观机制，能不能变成一个可以计算的模型？这节视频我们做
两件事。第一，把 BA 模型写成一个精确算法。先给定最终节点数 \(N\)，连接
数 \(m\)，以及一个小的连通种子图 \(G_0\)。每一步加入一个新节点，所以
\(N(t)=N_0+t\)。如果新节点带来 \(m\) 条边，那么 \(E(t)=E_0+mt\)。接着看
所有已有节点的度 \(k_i\)，并用
\(\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}\) 把度转成概率。最后，从这个概率
分布中抽取 \(m\) 个已有节点，连上新的边。第二，我们会从这个算法出发，
解释为什么它在连续近似下给出 \(p(k)\sim k^{-3}\)。

## BARoleOfM

### 中文

这里的 \(m\) 只做一件核心事情：它规定每个新节点出生时带来多少条边。
因此新节点刚加入后的度不是另一个随机变量，也不是由 \(\Pi_i\) 算出来的；
它就是 \(k_{\mathrm{new}}(t^+)=m\)。改变 \(m\) 会改变出生度、边密度和
平均度。因为无向网络中每条边贡献两个度端，所以
\(\langle k\rangle\approx 2m\)。但是 \(m\) 不能指定哪一个旧节点会被抽中，
也不能指定最后谁成为最大 hub；这些仍然由偏好连接的随机抽样决定。

## BAContinuumSetup

### 中文

接下来我们从算法进入连续近似。目标不是跟踪每一次随机跳动，而是跟踪
某一个节点 \(i\) 的期望增长。先看总度数。每一步加入一个节点，也加入
\(m\) 条边，所以 \(N(t)=N_0+t\)，\(E(t)=E_0+mt\)。无向网络中每条边贡献
两个度端，因此所有节点度数的和先写成
\(\sum_j k_j(t)=2E(t)=2(E_0+mt)\)。当时间足够大时，初始边数可以忽略，
所以偏好连接概率里的分母近似为 \(2mt\)。在这个总度数的基础上，平均度再写成
\(\langle k\rangle(t)=\frac{1}{N(t)}\sum_j k_j(t)=\frac{2E(t)}{N(t)}\)，并且
在大 \(t\) 下趋近于 \(2m\)。有了这个分母，再代入偏好连接概率
\(\Pi_i(t)=\frac{k_i(t)}{\sum_j k_j(t)}\)，单个节点的期望增长就是
\(\frac{d\bar{k}_i}{dt}=m\Pi_i(t)\)。

## BADegreeGrowthEquation

### 中文

把这些量放在一起时，要特别注意：这里不是在说单次运行中的精确度数，
而是在说期望度，或者连续近似下的平均轨迹。我们记
\(\bar{k}_i(t)=\mathbb{E}[k_i(t)]\)。于是有
\(\frac{d\bar{k}_i}{dt}=m\frac{\bar{k}_i}{2mt}\)。这里的 \(m\) 会约掉，
剩下 \(\frac{d\bar{k}_i}{dt}=\frac{\bar{k}_i}{2t}\)。节点 \(i\) 在出生时间
\(t_i\) 的初始条件是 \(\bar{k}_i(t_i)=m\)。解这个微分方程得到
\(\bar{k}_i(t)=m(t/t_i)^{1/2}\)。真实的一次模拟会一跳一跳地增加，
而这条光滑曲线描述的是平均趋势。

## BABirthTimeDistribution

### 中文

现在把“出生时间”转换成“度”。从
\(k_i(t)=m(t/t_i)^{1/2}\) 出发，可以反解出
\(t_i=\frac{m^2t}{k_i^2}\)。在 BA 过程中，节点大致均匀地在时间轴上进入
网络。因此，一个节点今天能达到很大的度，通常意味着它的出生时间足够早。
所以度分布的问题，可以转化为：有多少节点出生得足够早。

## BAPowerLawExponent

### 中文

这个转换给出累积分布的形状：
\(P(k_i(t)<k)=1-\frac{m^2}{k^2}\)。再对 \(k\) 求导，就得到概率密度。
忽略常数因子后，结果是 \(p(k)\sim k^{-3}\)。这就是 BA 模型中幂律指数
等于三的来源。注意这里依赖连续近似、大网络近似，以及对高阶项的忽略；
它说明的是机制的主导趋势，而不是每一个有限网络都会完美落在一条直线上。

## BAExponentRegimeMap

### 中文

为什么 \(\gamma=3\) 这个数值得单独停一下？参考 Network Science 第四章
关于度指数的相图，\(\gamma=3\) 正好是一个边界。对于
\(2<\gamma<3\) 的尺度无关区间，平均度可以是有限的，但
\(\langle k^2\rangle\) 会发散；这意味着 hub 对网络结构的影响非常强，
典型距离可以像 \(\langle d\rangle\sim\ln\ln N\) 这样增长，甚至比普通随机
网络的对数距离还慢。到了 \(\gamma>3\)，二阶矩变成有限，网络更接近普通
small-world 情形，距离通常按 \(\langle d\rangle\sim\ln N\) 的尺度增长。
所以 BA 的 \(\gamma=3\) 不只是一个拟合斜率，它是在 ultra-small world 和
small-world 行为之间的临界边界。

## BASimulationSanityCheck

### 中文

最后用模拟做一个 sanity check。有限网络的尾部一定会有噪声，因为高度节点
本来就很少。单次模拟不应该被当成完美分布。但是图中仍然能看到一个清楚的
模式：大多数节点度很小，少数节点进入高连接尾部。这个尾部正是增长和偏好
连接共同作用的结果。

## BATheoryTakeaway

### 中文

总结一下。算法层面，BA 模型规定新节点带来 \(m\) 条边，并用
\(\Pi_i=\frac{k_i}{\sum_j k_j}\) 选择已有目标。连续近似层面，这个随机过程
变成单个节点的期望增长方程。解方程得到
\(k_i(t)=m(t/t_i)^{1/2}\)，再把出生时间转换成度，就得到
\(p(k)\sim k^{-3}\)。下一段视频，我们不再推导公式，而是问：BA 模型解释了
什么，又遗漏了真实网络中的哪些结构。
