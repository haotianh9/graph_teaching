# Video 5.3 Human-Audio Transcript

Title: BA 模型遗漏了什么？从 hub 到真实网络结构

Final human-audio output:

```text
media/videos/video5_3_human_audio_final_720p30.mp4
```

Human audio:

```text
media/audio/audio1641536479.m4a
```

This transcript is a cleaned alignment draft based on the recorded Chinese
audio. It follows the spoken order rather than the older TTS review order.

## Scene Alignment

| Scene | Audio interval | Visual purpose |
|---|---:|---|
| `BAWhatItExplains` | 0:00-0:22 | Introduce BA vs networks across domains. |
| `BAVisualDifference` | 0:22-0:54 | Compare BA with a Facebook local sample. |
| `BAClusteringComparison` | 0:54-1:43 | Show real networks across domains have much larger clustering \(C\). |
| `BATriadicClosure` | 1:43-2:19 | Introduce Holme-Kim style triad formation. |
| `BAExponentQuestion` | 2:19-2:46 | Move from clustering to the exponent \(\gamma\). |
| `BAFitness` | 2:46-3:24 | Fitness changes node attractiveness and degree tails. |
| `BAAging` | 3:24-4:09 | Aging changes visibility over time. |
| `BANonlinearAttachment` | 4:09-4:53 | Nonlinear attachment changes the \(\gamma=3\) result. |
| `BAExtensionsTakeaway` | 4:53-5:26 | Summarize extensions and transition to Chapter 6. |

## BAWhatItExplains

大家好。上一节课中我们一起讨论了 BA 模型是怎么具体产生一个网络，以及这样的网络有什么样的统计学特征。那么这一节课我们就将一起探讨 BA 模型和真实网络的对比：哪些真实网络中的特征，是 BA 模型已经可以描述的；哪些我们仍然需要对 BA 模型做一些修正。

## BAVisualDifference

这里首先我们来看 BA 模型和一个真实的 Facebook 社交网络。我们会发现，在社交网络中有一个很经典的特征：一个节点的两个邻居之间也经常彼此相连。而这样一种特征，就是邻居之间的 clustering。这个特征在 BA 模型中几乎并不存在。

## BAClusteringComparison

这个特征也并不仅仅是 Facebook 这个社交网络单独存在的。这里我们看了三个来自不同领域的真实网络：第一个是 C. elegans 这种蠕虫的神经元连接；第二个是刚刚看过的 Facebook 网络；最后一个是 collaboration，也就是科学家之间合作的网络。

如果我们来看它们的 clustering coefficient，会发现这三个真实网络都很高。而和它们有同样大小，并且平均度尽量接近的 BA 网络，聚类系数比它们低非常多。这也说明，BA 模型相比真实网络，一个很重要的缺失是：它不能很好地表征邻居之间的连接。

## BATriadicClosure

为了解决这个问题，2002 年的一篇文章基于 BA 模型提出了一个扩展：每次连接选择一个 target 之后，接下来会更倾向于连接到这个 target 自身的邻居。这会让邻居之间的连接变得更多。这样的方式就能很好地提升模型中的 clustering coefficient，让模型和真实网络更接近。

## BAExponentQuestion

上节课中，我们还探讨了 BA 模型中另外一个特性，就是它的 exponent。节点度的分布中，度为 \(k\) 的概率正比于 \(k^{-3}\)。这里的 3 是 critical exponent。接下来的问题是：我们能不能用一些扩展来改变这个 exponent \(\gamma\)？

## BAFitness

事实证明，我们有很多种方式可以改变。第一种方式是 fitness。在基础的 BA 模型中，我们假设每个节点本身没有特性；它被优先连接或者不被优先连接，完全是由它当前的度产生的。

而在 fitness 模型中，我们假设每个节点自身也有一个偏好。它本身可能就有更容易被连接的特性。比如在论文引用网络中，有些论文本身质量更高，它自然就更容易被引用。

## BAAging

第二种改变方式是 aging。也就是说，每个节点被连接的概率不仅正比于它当前的度，也和它目前已经来到网络上的时间有关系。因为我们之前看到，度本身在统计意义上也和节点进入网络的时间正相关。

如果这里我们再显式加入一项关于时间的因素，比如让连接更接近最近被加入的节点，因为它们平均下来度会比较低，如果用 aging 的方式提升它们的权重，也可以改变网络的特性，改变 exponent \(\gamma\)。

## BANonlinearAttachment

另一种更直接改变 exponent 的方式，是让连接概率不再正比于 \(k_i\) 本身，而是正比于 \(k_i^\alpha\)。这会引入一个非线性项。当 \(\alpha=1\) 的时候，它就是标准 BA 网络。当 \(\alpha<1\) 的时候，它更不倾向于连接度比较大的节点。走到一个极端，\(\alpha=0\) 时，连接到每一个节点的概率都是均等的。当 \(\alpha>1\) 时，它会更容易出现一个非常强的 hub，出现 winner-takes-all 的情况。

## BAExtensionsTakeaway

我们讲了这么多 BA 模型的 extension。它们会引入更多和真实网络类似的特性。以后如果我们处理一个真实网络，也可以用这种方式来拟合它更像哪一种 BA 模型的变种。下一节课，我们将进入第六章，更详细地探讨一个网络是怎么增长的。谢谢大家。
