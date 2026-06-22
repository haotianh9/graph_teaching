# Chapter 6 Transcript Draft

Title: 从凝聚到相变：演化网络的拓扑如何被动力学改变？

## FitnessDistributionOpening

前面我们已经把 fitness model 写成一个增长规则：
\(\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}\)。
这个公式里的 \(\eta_i\) 会改变单个节点的增长速度。
现在问题向上走一层：如果整个网络里的 fitness 分布 \(\rho(\eta)\) 改变，网络拓扑会不会进入不同的相？

左边是许多节点 fitness 接近的情况。竞争会分散，多个节点都可能成为 hub。
右边是出现极端高 fitness 节点的情况。它不只是增长更快，还可能改变整个网络的形状。

## TwoOutcomesOrderParameter

同一个 fitness 规则可以产生两种宏观结果。

第一种是 fit-get-rich 或 scale-free phase。高 fitness 节点有优势，hub 会出现，但多个 hub 仍然共存。随着网络变大，最大 hub 占全部链接的比例会趋向零。

第二种是 condensed phase。一个极端高 fitness 节点长期拿走有限比例的链接。此时网络不只是“hub 更大”，而是拓扑结构变成了 winner-takes-all。

为了区分这两种情况，可以看一个 order parameter：
\(s_{\max}(t)=\frac{k_{\max}(t)}{\sum_j k_j(t)}\)。
如果 \(s_{\max}\) 趋向零，最大 hub 只是层级结构中的一个大节点。
如果 \(s_{\max}\) 保持有限，说明一个节点占据了宏观比例的连接。

## CondensationAsPhaseTransition

这就是网络里的 condensation。
在普通的 hub hierarchy 中，hub 很大，但没有一个节点拥有有限比例的所有链接。
在 condensation 中，一个 super-hub 捕获了有限的 link share。

这时可以再引入 Bose gas 的类比。fitness 可以写成
\(\eta_i=e^{-\beta_T\epsilon_i}\)。
fitness 越高，对应的能量越低。链接像粒子，super-hub 像最低能级。

这个类比的重点不是热力学细节，而是 phase transition：微观竞争规则的改变，导致网络拓扑发生定性变化。

## RuleToTopology

condensation 给出一个更一般的思想。
改变演化规则，不只是改变一条 degree distribution 曲线；它可以改变网络最终允许的拓扑。

有些改变是平滑的参数调节，例如指数变大或变小。
有些改变会带来 cutoff 或 saturation，让尾部不再延伸。
还有一些改变是真正的 phase transition，会把 scale-free 结构变成另一种宏观形态。

所以从这里开始，我们不再只问“是不是幂律”，而是问：哪一个动力学规则留下了这个拓扑痕迹？

## InitialAttractiveness

第一个例子是 initial attractiveness。
把纯 preferential attachment 改成
\(\Pi_k\sim A+k\)。
这表示即使一个节点当前 degree 很小，甚至是零，也有一个基础吸引力。

它的典型效果可以写成
\(\gamma=3+\frac{A}{m}\)。
当 \(A=0\) 时，回到标准 BA 的强 preferential attachment。
当 \(A>0\) 时，小 degree 节点获得额外机会，hub 的优势变弱，\(\gamma\) 变大，网络更均匀。

这不是 winner-takes-all 的相变，而是对 scale-free phase 的平滑变形。

## InternalLinksAcceleratedGrowth

真实网络也不一定每条新边都来自一个新节点。
旧节点之间也会形成 internal links。

如果这些旧节点之间的连接也是 preferential 的，hub-to-hub reinforcement 会增强 heterogeneity。
如果 internal links 更接近随机选择，网络会更接近 random mixing。

还有一种情况是 accelerated growth：
\(m(t)=m_0t^\theta\)。
这表示越晚进入网络的节点，可能带来越多初始链接。于是平均度数随时间增加，系统会偏离干净的 BA scaling。

## NodeDeletionPhaseMap

到目前为止，网络主要是在增长。但真实网络也会删除节点和链接。

如果删除率 \(r<1\)，增长仍然占优势，scale-free phase 可能保留。
如果 \(r=1\)，新增和删除大致平衡，网络大小接近稳定。
如果 \(r>1\)，网络整体在衰减。

更重要的是，当 deletion 和 initial attractiveness 一起出现时，系统可以跨过临界边界。
一侧是 scale-free，另一侧可能是 stretched exponential，甚至 exponential。
这就是演化网络中的 phase diagram 思想：参数不是只调曲线，而是在决定网络处在哪一种相。

## AgingRegimes

aging 是另一个控制参数。
定义节点年龄
\(\tau_i=t-t_i\)，并把连接概率写成
\(\Pi(k_i,\tau_i)\sim k_i\tau_i^{-\nu}\)。

当 \(\nu<0\) 时，老节点被强化，最老的节点可能越来越占优势。
当 \(\nu=0\) 时，没有 aging，接近 BA 的 hierarchy。
当 \(0<\nu<1\) 时，老节点慢慢失去可见度，但 scale-free 行为仍可能保留。
当 \(\nu>1\) 时，aging 压过 preferential attachment，新节点主要连向最近的节点，scale-free 结构会被破坏。

所以 aging 不是一句“节点会变老”，而是一个可以改变拓扑相的动力学参数。

## DynamicsTakeaway

这一节的主线是：拓扑跟随动力学。

fitness distribution 可以让系统停留在 fit-get-rich，也可以进入 condensation。
initial attractiveness 可以调节 \(\gamma\)，让 hub 变弱。
internal links 和 accelerated growth 会改变密度与 heterogeneity。
deletion 可以带来 cutoff，甚至把 scale-free 推向 exponential。
aging 可以让老 hub 失去可见度，也可能破坏 scale-free 结构。

所以第六章真正的结论不是“真实网络就是某一种幂律”。
更准确地说，网络拓扑是演化过程留下的宏观痕迹。
如果想解释结构，必须先理解网络是如何演化的。
