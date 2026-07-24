"""Ch11-08: The modern deep-learning landscape - a concept tour (Part B).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. These are concept cards; the only ``code`` block is a short,
illustrative TSFM zero-shot snippet (not runnable in the book).
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch11LandscapeScene(EpiBaseScene):
    """Tutorial video scene: a concept tour of the modern deep-learning model zoo."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "現代深度學習全景",
            "title_sub": "看題目長什麼樣，就知道找誰幫忙",
            "zoo_heading": "模型動物園：看題目找專長",
            "zoo_lines": [
                "MLP：什麼表格都能接的通才",
                "LSTM：記性好、讀懂整段脈絡的老偵探",
                "CNN：專找局部指紋的鑑識官",
                "→ 不同任務，找不同專長的模型",
            ],
            "gnn_heading": "GNN：社群網絡分析師",
            "gnn_lines": [
                "節點 = 住民，邊 = 有接觸史",
                "不只看個人特質，還看誰跟誰相連",
                "用途：接觸者追蹤、轉診網絡、空間傳播",
                "工具：torch-geometric (PyG)、DGL",
            ],
            "transformer_heading": "時空 Transformer / TFT：懂得分配注意力",
            "transformer_lines": [
                "在一長串資料裡自動找「這次該多看哪天」",
                "同時吃病例、氣溫、人流、疫苗覆蓋率",
                "用途：多變量、長序列、要預測很多天後",
                "工具：pytorch-forecasting (TFT)",
            ],
            "deepsurv_heading": "DeepSurv：神經網路版 Cox 迴歸",
            "deepsurv_lines": [
                "Ch09 的 Cox 假設 log(HR) 線性相加",
                "DeepSurv 把它換成神經網路，抓非線性",
                "用途：存活分析但懷疑有交互、高維資料",
                "工具：pycox (DeepSurv、DeepHit)",
            ],
            "tsfm_heading": "TSFM：讀遍全球案件的老手",
            "tsfm_title": "tsfm_zero_shot.py",
            "hybrid_heading": "混合 / 知識注入：綁著物理定律的模型",
            "hybrid_lines": [
                "PINN：loss = L_data + L_physics",
                "同時要求「貼近資料」且「遵守 SEIR 方程式」",
                "用途：資料少但機制明確的新興傳染病",
                "→ 最推薦給流行病學家的務實路線",
            ],
            "extra_banner_title": "額外範例：把模型配給對的題目",
            "extra_matching_heading": "看題目，找專長：一張配對表",
            "extra_matching_lines": [
                "接觸網絡、node + edge → GNN",
                "多變量長序列、要 attention → Transformer / TFT",
                "存活資料 + 非線性交互 → DeepSurv",
                "新病原初期、外面有大量資料 → TSFM",
                "資料少但機制明確 → PINN / 混合模型",
            ],
            "blindspot_banner_title": "選模型三個新手地雷",
            "outro_heading": "下一章 Ch12：因果推論",
            "outro_sub": "淋浴暴露真的「導致」感染嗎？",
        },
        "en": {
            "title_main": "The Modern Deep-Learning Landscape",
            "title_sub": "See what the problem looks like, then pick the specialist",
            "zoo_heading": "The model zoo: match the task to a specialist",
            "zoo_lines": [
                "MLP: the generalist for any table",
                "LSTM: the veteran who remembers the whole story",
                "CNN: the forensics expert for local fingerprints",
                "-> different tasks, different specialists",
            ],
            "gnn_heading": "GNN: the social-network analyst",
            "gnn_lines": [
                "nodes = residents, edges = contact history",
                "reads who connects to whom, not just each person",
                "use: contact tracing, referral nets, spatial spread",
                "tools: torch-geometric (PyG), DGL",
            ],
            "transformer_heading": "Spatio-temporal Transformer / TFT: it allocates attention",
            "transformer_lines": [
                'auto-finds "which day matters most" in a long series',
                "ingests cases, temp, mobility, vaccine coverage at once",
                "use: multivariate, long-horizon forecasting",
                "tools: pytorch-forecasting (TFT)",
            ],
            "deepsurv_heading": "DeepSurv: a neural version of Cox regression",
            "deepsurv_lines": [
                "Ch09's Cox assumes log(HR) adds up linearly",
                "DeepSurv swaps that for a net to catch nonlinearity",
                "use: survival with interactions or high-dim data",
                "tools: pycox (DeepSurv, DeepHit)",
            ],
            "tsfm_heading": "TSFM: the veteran who has read every global case",
            "tsfm_title": "tsfm_zero_shot.py",
            "hybrid_heading": "Hybrid / knowledge injection: models bound by physics",
            "hybrid_lines": [
                "PINN: loss = L_data + L_physics",
                '"fit the data" AND "obey the SEIR equations"',
                "use: emerging disease, scarce data, known mechanism",
                "-> the most practical route for epidemiologists",
            ],
            "extra_banner_title": "Extra example: matching models to epi tasks",
            "extra_matching_heading": "Match the task to a specialist: a cheat sheet",
            "extra_matching_lines": [
                "contact network, node + edge -> GNN",
                "multivariate long series, need attention -> Transformer / TFT",
                "survival data + nonlinear interactions -> DeepSurv",
                "new pathogen, external data abundant -> TSFM",
                "scarce data, clear mechanism -> PINN / hybrid",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next chapter (Ch12): causal inference",
            "outro_sub": 'Does shower exposure really "cause" infection?',
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading_key: str, title_key: str, code: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title=self.t(title_key), position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson (concept tour)
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_model_zoo(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("zoo_heading", "zoo_lines", duration)

    def show_gnn(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("gnn_heading", "gnn_lines", duration)

    def show_transformer(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("transformer_heading", "transformer_lines", duration)

    def show_deepsurv(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("deepsurv_heading", "deepsurv_lines", duration)

    def show_tsfm(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import timesfm\n"
                "\n"
                "tfm = timesfm.TimesFm(context_len=512, horizon_len=14)\n"
                'tfm.load_from_checkpoint("google/timesfm-1.0-200m")\n'
                "# 直接預測，沒有 fit() 這一步（零樣本）\n"
                "forecast, _ = tfm.forecast([cases_history], freq=[0])"
            ),
        )
        self._code_block("tsfm_heading", "tsfm_title", code, duration)

    def show_hybrid(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("hybrid_heading", "hybrid_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_matching(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_matching_heading", "extra_matching_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_overkill_graph(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "GNN(x, random_edges)  # edges = noise"),
            kwargs.get("correct_code", "LogisticRegression().fit(X, y)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_shap_causal(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cause = top_shap_feature(model)"),
            kwargs.get("correct_code", "effect = adjusted_or(fit_adj)  # Ch06"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_uncertainty(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "yhat = model.predict(x)  # point only"),
            kwargs.get("correct_code", "lo, hi = model.predict_interval(x)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
