# Video 5.1 Posting Draft

## Suggested Title

枢纽节点如何出现？Barabasi-Albert 模型的直觉 | Network Science Chapter 5

## Thumbnail

```text
assets/thumbnails/video5_1_thumbnail.png
assets/thumbnails/video5_1_thumbnail.jpg
```

## Short Description

为什么真实网络中会自然出现少数连接数特别高的枢纽节点？这一节从随机网络的局限出发，介绍 Barabasi-Albert 模型的两个核心机制：网络增长和优先连接。我们会看到，一个简单的局部规则如何通过“富者愈富”的反馈，产生复杂的全局网络结构。

## Full Description

在随机网络中，节点的度会有波动，但通常不会自然产生特别强的枢纽节点。可是网页、论文引用、社交网络、交通网络和生物网络中，经常存在少数连接数远高于其他节点的 hubs。

这段视频解释 Chapter 5 的第一条主线：Barabasi-Albert model 如何用两个简单机制解释 hub emergence：

1. Growth: 网络不是一次性生成的，而是不断加入新节点。
2. Preferential attachment: 新节点更倾向于连接已经有很多连接的节点。

核心公式：

```text
Pi_i = k_i / sum_j k_j
```

也就是说，已有节点的度越高，被新节点连接的概率越大。经过不断重复，这个局部概率规则会放大早期差异，让枢纽节点自然出现。

## Chapters

```text
00:00 Random networks vs hubs
00:52 Growth
02:12 Preferential attachment
04:00 Building the BA model
04:56 BA network vs random network
05:41 Takeaway and next video
```

## References

Network Science book:
https://www.networksciencebook.com/

Original BA paper:
Barabasi, A.-L. and Albert, R. (1999). Emergence of scaling in random networks. Science, 286, 509-512.

Course code and teaching materials:
https://github.com/haotianh9/graph_teaching

## Tags

```text
network science, graph theory, Barabasi-Albert model, preferential attachment,
scale-free network, hubs, complex networks, 网络科学, 图论, 优先连接, 标度无关网络
```
