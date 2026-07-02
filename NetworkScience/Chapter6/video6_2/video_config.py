VIDEO_ID = "video6_2"
VIDEO_LABEL = "Chapter 6 Condensation and Phase Transitions"
CHAPTER_LABEL = "Network Science Chapter 6"

SCENES = [
    {"name": "FitnessDistributionOpening", "duration": 46},
    {"name": "TwoOutcomesOrderParameter", "duration": 82},
    {"name": "CondensationAsPhaseTransition", "duration": 66},
    {"name": "RuleToTopology", "duration": 48},
    {"name": "InitialAttractiveness", "duration": 58},
    {"name": "InternalLinksAcceleratedGrowth", "duration": 48},
    {"name": "NodeDeletionPhaseMap", "duration": 70},
    {"name": "AgingRegimes", "duration": 70},
    {"name": "DynamicsTakeaway", "duration": 48},
]

RENDER_QUALITY = "-qm"
RENDER_SUBDIR = "720p30"
TTS_AUDIO_DIR = "assets/audio/zh"
TTS_FINAL_OUT = "media/videos/video6_2_zh_tts_review_720p30.mp4"
HUMAN_AUDIO_PATH = None
HUMAN_FINAL_OUT = "media/videos/video6_2_human_audio_final_720p30.mp4"

COVER_TITLE = "从凝聚到相变"
COVER_SUBTITLE = "topology follows dynamics"
COVER_LEFT_LABEL = "fitness distribution"
COVER_RIGHT_LABEL = "phase transition"
COVER_FOOTER = "Network Science Chapter 6 · graph_teaching"
COVER_SEED = 62
COVER_OUTPUTS = [
    {"width": 1280, "height": 720, "filename": "video6_2_cover_16x9.jpg"},
    {"width": 1200, "height": 900, "filename": "video6_2_cover_4x3.jpg"},
]

SUGGESTED_TITLE = "从凝聚到相变：演化网络的拓扑如何被动力学改变？"
SHORT_DESCRIPTION = (
    "如果少数节点真的更有“吸引力”，网络只是多几个大 hub，还是会进入 winner-takes-all？"
    "这一节先看两个可复现的时间历史 proxy：HEP-TH citation histories 拟合出的 estimated fitness，"
    "以及 Common Crawl Web-domain PageRank snapshots 得到的 Web visibility growth proxy。"
    "然后问一个更大的问题：整个 fitness distribution 的形状会不会改变网络的相？"
    "同一个增长规则既可能产生 fit-get-rich，也可能进入 condensation："
    "一个节点拿走有限比例的链接。后半部分把这个想法推广到 initial attractiveness、"
    "internal links、deletion、aging 和 accelerated growth，强调网络拓扑是演化动力学留下的宏观痕迹。"
)
REFERENCES = [
    ("Network Science book, Chapter 6.4", "https://networksciencebook.com/chapter/6#bose-einstein-condensation"),
    ("Network Science book, measuring fitness", "https://networksciencebook.com/chapter/6#measuring-fitness"),
    ("Experience versus talent shapes the structure of the Web", "https://doi.org/10.1073/pnas.0805921105"),
    ("Common Crawl Web Graphs", "https://commoncrawl.org/web-graphs"),
    ("Common Crawl Web Graph statistics", "https://commoncrawl.github.io/cc-webgraph-statistics/"),
    ("Bianconi and Barabasi, Bose-Einstein condensation in complex networks", "https://doi.org/10.1103/PhysRevLett.86.5632"),
    ("SNAP HEP-TH citation network", "https://snap.stanford.edu/data/cit-HepTh.html"),
    ("Course code and teaching materials", "https://github.com/haotianh9/graph_teaching"),
]

FORMULA_SPEECH = {
    r"\(\widehat{\eta}\)": "艾塔的估计值",
    r"\(\widehat{\eta}_{web}\)": "网页可见度艾塔的估计值",
    r"\(\eta\)": "艾塔",
    r"\(\rho(\eta)\)": "柔艾塔",
    r"\(\Pi_i=\frac{\eta_i k_i}{\sum_j \eta_j k_j}\)": "节点 i 被连接的概率，等于艾塔 i 乘以 k i，再除以所有节点艾塔 j 乘以 k j 的总和",
    r"\(s_{\max}(t)=\frac{k_{\max}(t)}{\sum_j k_j(t)}\)": "s max t 等于最大度数除以所有节点度数之和",
    r"\(\eta_i=e^{-\beta_T\epsilon_i}\)": "艾塔 i 等于 e 的负贝塔 T 乘以 epsilon i 次方",
    r"\(\Pi_k\sim A+k\)": "连接概率正比于 A 加 k",
    r"\(\gamma=3+\frac{A}{m}\)": "伽马等于三加 A 除以 m",
    r"\(m(t)=m_0t^\theta\)": "m t 等于 m 零乘以 t 的 theta 次方",
    r"\(\tau_i=t-t_i\)": "tau i 等于 t 减 t i",
    r"\(\Pi(k_i,\tau_i)\sim k_i\tau_i^{-\nu}\)": "连接概率正比于 k i 乘以 tau i 的负 nu 次方",
}
