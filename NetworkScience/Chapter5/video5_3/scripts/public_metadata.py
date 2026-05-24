VIDEO_ID = "video5_3"
VIDEO_LABEL = "Video 5.3"
CHAPTER_LABEL = "Network Science Chapter 5"

COVER_TITLE = "BA模型遗漏了什么？"
COVER_SUBTITLE = "从 hub 到聚类系数、适应度、老化与非线性连接"
COVER_LEFT_LABEL = "BA: hubs, low C"
COVER_RIGHT_LABEL = "Across domains: high C"
COVER_FOOTER = f"{CHAPTER_LABEL} · {VIDEO_LABEL}"

SUGGESTED_TITLE = "BA 模型遗漏了什么？从 hub 到真实网络结构 | Network Science Chapter 5"

SHORT_DESCRIPTION = (
    "这一讲把标准 BA 模型和不同领域中的真实网络放在一起比较。BA 模型能解释 "
    "hub 和重尾度分布的出现，但真实网络往往还有更强的聚类系数和局部社群结构。"
    "我们会用聚类系数作对比，并介绍几类常见扩展：局部聚类机制、fitness、aging "
    "和非线性优先连接，看看它们分别能改变什么，又不能改变什么。"
)

REFERENCES = [
    ("Network Science book", "https://www.networksciencebook.com/"),
    ("Holme and Kim triad formation model", "https://doi.org/10.1103/PhysRevE.65.026107"),
    ("Course code and teaching materials", "https://github.com/haotianh9/graph_teaching"),
]

COVER_OUTPUTS = [
    {
        "label": "16:9 cover",
        "width": 1280,
        "height": 720,
        "filename": "video5_3_cover_16x9.png",
    },
    {
        "label": "4:3 cover",
        "width": 1200,
        "height": 900,
        "filename": "video5_3_cover_4x3.png",
    },
    {
        "label": "compatibility cover",
        "width": 1280,
        "height": 720,
        "filename": "video5_3_cover.png",
    },
]
