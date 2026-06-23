VIDEO_ID = "video6_1"
VIDEO_LABEL = "Chapter 6 Fitness Inference"
CHAPTER_LABEL = "Network Science Chapter 6"

SCENES = [
    {"name": "FitnessOpening", "duration": 24.6},
    {"name": "FitnessRule", "duration": 31.7},
    {"name": "FitnessGrowthDerivation", "duration": 108.9},
    {"name": "FitnessInferenceOpening", "duration": 43.3},
    {"name": "LogLogSlope", "duration": 27.8},
    {"name": "GrowthHistoryComparison", "duration": 19.1},
    {"name": "CitationImpact", "duration": 20.6},
    {"name": "RealDataFitnessFit", "duration": 68.2},
    {"name": "PredictionWorkflow", "duration": 23.1},
    {"name": "FitnessTakeaway", "duration": 41.36},
]

RENDER_QUALITY = "-qm"
RENDER_SUBDIR = "720p30"
TTS_AUDIO_DIR = "assets/audio/zh"
TTS_FINAL_OUT = "media/videos/video6_1_zh_tts_review_720p30.mp4"
HUMAN_AUDIO_PATH = "media/audio/audio1596409650.m4a"
HUMAN_FINAL_OUT = "media/videos/video6_1_human_audio_final_720p30.mp4"
HUMAN_AUDIO_FILTER = (
    "highpass=f=90,"
    "lowpass=f=7800,"
    "afftdn=nr=24:nf=-42:tn=1,"
    "anlmdn=s=0.0004:p=0.004:r=0.006,"
    "agate=threshold=0.018:ratio=18:attack=12:release=180:range=0.02,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)

COVER_TITLE = "如何推断 Fitness?"
COVER_SUBTITLE = "from fitness model to growth data"
COVER_LEFT_LABEL = "η changes growth"
COVER_RIGHT_LABEL = "slope estimates fitness"
COVER_FOOTER = "Network Science Chapter 6 · graph_teaching"
COVER_SEED = 61
COVER_OUTPUTS = [
    {"width": 1280, "height": 720, "filename": "video6_1_cover_16x9.jpg"},
    {"width": 1200, "height": 900, "filename": "video6_1_cover_4x3.jpg"},
]

SUGGESTED_TITLE = "如何推断 Fitness? | 从 Bianconi-Barabasi 模型到增长数据"
SHORT_DESCRIPTION = (
    "这一节先用很短时间回顾 Bianconi-Barabasi fitness model："
    "attachment 不只由 degree 决定，也由 fitness η 决定。重点放在数据问题："
    "先推导 β(η)=η/C 和 log-log growth equation，再问如果真实网络里存在 fitness，"
    "我们怎样从节点的增长轨迹、log-log slope、"
    "引用历史和观测窗口中推断它? 视频最后用 SNAP HEP-TH citation data 做一个"
    "真实数据的 effective fitness fitting demo。"
)
REFERENCES = [
    ("Network Science book, Chapter 6", "https://networksciencebook.com/chapter/6#measuring-fitness"),
    ("Bianconi and Barabasi fitness model", "https://doi.org/10.1209/epl/i2001-00260-6"),
    ("SNAP HEP-TH citation network", "https://snap.stanford.edu/data/cit-HepTh.html"),
    ("Course code and teaching materials", "https://github.com/haotianh9/graph_teaching"),
]

FORMULA_SPEECH = {
    r"\(\Pi_i=\eta_i k_i/\sum_j \eta_j k_j\)": "节点 i 被连接的概率，等于艾塔 i 乘以 k i，再除以所有节点艾塔 j 乘以 k j 的总和",
    r"\(\Pi_i=k_i/\sum_j k_j\)": "节点 i 被连接的概率，等于 k i 除以所有节点 degree 的总和",
    r"\(\frac{d\bar{k}_i}{dt}=m\Pi_i(t)\)": "k i 期望值对 t 的导数，等于 m 乘以节点 i 被选中的概率",
    r"\(\sum_j \eta_j k_j(t)\approx Cmt\)": "所有节点艾塔 j 乘以 k j 的总和，近似等于 C 乘以 m 乘以 t",
    r"\(\bar{k}_i(t)=m(t/t_i)^{\eta_i/C}\)": "k i 的期望值等于 m 乘以 t 除以 t i 的艾塔 i 除以 C 次方",
    r"\(\ln \bar{k}_i(t)=\beta(\eta_i)\ln t+B_i\)": "log k i 期望值，等于贝塔艾塔 i 乘以 log t 加 B i",
    r"\(\beta(\eta_i)=\eta_i/C\)": "贝塔艾塔 i 等于艾塔 i 除以 C",
    r"\(B_i=\ln m-\beta(\eta_i)\ln t_i\)": "B i 等于 log m 减去贝塔艾塔 i 乘以 log t i",
    r"\(\widehat{\beta}_i\)": "贝塔 i 的估计值",
    r"\(\widehat{\eta}_i\)": "艾塔 i 的估计值",
    r"\(\beta(\eta_i)\)": "贝塔艾塔 i",
    r"\(\eta_i\)": "艾塔 i",
    r"\(\eta\)": "艾塔",
    r"\(k_i\)": "k i",
    r"\(k\)": "k",
}
