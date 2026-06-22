# Chapter 6 Fitness Inference Transcript Draft

Title: 如何推断 Fitness?

## FitnessOpening

在第五章结尾，我们已经引入了 Bianconi-Barabasi fitness model。这里先快速回顾一下：BA 模型用 degree 决定 attachment，而 fitness model 在 degree 之外加入节点自己的吸引力。

第六章第一段重点不再是重新推导模型，而是问一个数据问题：如果真实网络里确实存在 fitness，我们怎么从增长历史里推断它？

## FitnessRule

fitness 记作 \(\eta_i\)。加入 fitness 以后，连接概率变成 \(\Pi_i=\eta_i k_i/\sum_j \eta_j k_j\)。

这里的逻辑非常清楚：degree \(k_i\) 仍然表示可见度，fitness \(\eta_i\) 表示在同样可见度下，节点把注意力转化成新连接的能力。分母把所有节点的 \(\eta_j k_j\) 加起来，保证概率总和等于一。

所以 fitness 不是替代 degree，而是改变 degree 带来的增长速度。

## FitnessGrowthDerivation

现在把这个“改变增长速度”写成方程。这里用的是 continuum approximation，所以我们追踪的不是某一次随机模拟里的精确 degree，而是节点 \(i\) 的期望 degree，记作 \(\bar{k}_i(t)\)。

第一步，节点 \(i\) 的期望增长率等于每一步新边数乘以它被选中的概率：
\[
\frac{d\bar{k}_i}{dt}=m\Pi_i(t).
\]
把 fitness attachment rule 代进去，得到
\[
\frac{d\bar{k}_i}{dt}
=m\frac{\eta_i \bar{k}_i(t)}{\sum_j \eta_j k_j(t)}.
\]

关键近似在分母。随着网络增长，\(\sum_j \eta_j k_j(t)\) 也大致线性增长，所以写成
\[
\sum_j \eta_j k_j(t)\approx Cmt.
\]
这里的 \(C\) 不是某个节点自己的参数，而是由整个网络的 fitness distribution \(\rho(\eta)\) 决定的常数。

于是微分方程变成
\[
\frac{d\bar{k}_i}{dt}=\frac{\eta_i}{C}\frac{\bar{k}_i}{t}.
\]
两边积分，从节点出生时间 \(t_i\) 开始，并使用出生时的条件 \(\bar{k}_i(t_i)=m\)，得到
\[
\bar{k}_i(t)=m\left(\frac{t}{t_i}\right)^{\eta_i/C}.
\]

所以在这个模型里，
\[
\beta(\eta_i)=\frac{\eta_i}{C}.
\]
也就是说，\(\beta\) 是 fitness 到增长指数的函数。fitness 越高，\(\beta\) 越大，期望 degree 增长越快。如果所有节点 fitness 相同，就回到 BA 模型的 \(\beta=1/2\)。

## FitnessInferenceOpening

如果 fitness 只是我们在模型里指定的参数，它的解释力仍然有限。Chapter 6 更重要的一步，是把 fitness 和真实增长历史联系起来。

把刚才的解取 logarithm，就得到
\[
\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i.
\]
这里 \(B_i=\ln m-\beta(\eta_i)\ln t_i\)，它把出生时间 \(t_i\) 和出生 degree \(m\) 收进截距里。真正控制斜率的是 \(\beta(\eta_i)=\eta_i/C\)。

所以 \(\beta(\eta_i)\) 不是给每个节点额外手动设置的新参数。它表达的是：fitness 越高，期望增长指数越大，长期增长越快。

## LogLogSlope

在 log-log 图上，如果两个节点的增长曲线斜率不同，它们的长期增长速度就不同。这个斜率就是 effective \(\beta(\eta_i)\)。斜率越大，说明这个节点在同样时间尺度下更容易积累新连接。

所以 fitness 的估计不是看某个时刻的 degree，而是看 degree 随时间增长的形状。这里估计出来的是 effective fitness，因为真实网络里还会有噪声、外部事件和观测窗口。

## GrowthHistoryComparison

早期流行可能会误导我们。一个节点可能一开始因为曝光很强，短时间得到很多链接，但后来增长变慢。另一个节点可能早期不突出，但是长期增长曲线更陡。

如果只看第一个快照，我们会把 early popularity 误认为高 fitness。更好的做法是看完整的增长历史，比较长期斜率。

## CitationImpact

在 citation network 里，fitness 可以理解为论文本身的吸引力或者重要性。但引用还有 aging effect：论文越老，越可能从读者视野里淡出。

所以论文影响力不是只由 fitness 决定，也受时间衰减和研究领域变化影响。推断 fitness 时，需要把增长能力和可见时间窗口区分开。

## RealDataFitnessFit

现在看一个真实数据的例子。这里使用 SNAP HEP-TH citation network：如果论文 \(i\) 引用论文 \(j\)，数据里就有一条从 \(i\) 指向 \(j\) 的有向边，同时数据还给出了论文提交到 arXiv 的时间。

我们把每篇论文的引用事件按论文年龄 \(\tau\) 对齐，然后拟合 \(\log(c_i(\tau)+1)\) 对 \(\log(\tau+1)\) 的斜率。这个斜率记作 \(\widehat{\beta}_i\)，再除以平均斜率得到 \(\widehat{\eta}_i\)。

在这个 dated subset 里，有 1271 篇论文有足够的时间戳引用可以做这个简单拟合。三条高亮曲线展示了不同类型：early burst 的引用很早集中到来，但长期斜率较低；steady growth 接近平均；late bloomer 早期引用很少，但后来的增长斜率更高。

这里的 \(\widehat{\eta}_i\) 不是论文的最终真理，也不是完整的 citation impact model。它只是一个 effective growth fitness：从真实增长轨迹里估计出的增长倾向。

## PredictionWorkflow

实际工作流可以这样理解：先收集带时间戳的链接或者引用；然后对齐每个节点的 birth time；再拟合 log-log growth curve 的 slope；最后用这个 slope 去比较未来影响力的概率趋势。

这不是保证排名的水晶球。它给的是 probabilistic prediction：哪些节点更可能继续增长，而不是哪些节点一定赢。

## FitnessTakeaway

这节课的结论是：fitness model 用 \(\eta_i\) 乘以 \(k_i\) 驱动 attachment。理论上，fitness 通过 \(\beta(\eta_i)=\eta_i/C\) 变成期望增长指数；真实数据中，我们再用 growth trajectory 的 log-log slope 去估计这个指数。

所以 log-log slope 给出 effective \(\beta(\eta_i)\)：它是 fitness 映射出来的增长指数。早期流行不等于长期影响。

下一节我们讨论 Chapter 6.4 和 6.5：fitness model 什么时候会进入 condensation，网络演化为什么会出现相变。
