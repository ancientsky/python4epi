"""Ch11-05: When to use deep learning - a decision framework (don't crack a nut with a sledgehammer).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch11WhenToUseDLScene(EpiBaseScene):
    """Tutorial video scene: the decision framework for reaching for deep learning."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "該不該用深度學習？",
            "title_sub": "決策框架：別殺雞用牛刀",
            "temptation_heading": "同事的提議：要不要上深度學習？",
            "temptation_lines": [
                "「聽說 DL 很強，說不定能抓到複雜交互」",
                "好問題——但答案不是「上就對了」",
                "先問四個問題，再決定磨不磨這把牛刀",
                "→ 深度學習是牛刀，不是萬靈丹",
            ],
            "decision_heading": "決策框架：四個問題依序問",
            "decision_lines": [
                "① 資料 < 1000 筆？→ 傳統統計 / 簡單 ML",
                "② 只問「會不會」還是要「為什麼」？→ 機制模型",
                "③ 高維、長序列、資料量夠大？→ 才輪到 DL",
                "④ 新病原、初期沒資料？→ 借 TSFM 零樣本",
            ],
            "spectrum_heading": "280 筆落在光譜的哪一端？",
            "spectrum_left": "小資料\n用簡單模型",
            "spectrum_mid": "數千筆\n中間地帶",
            "spectrum_right": "數萬筆+\n才輪到 DL",
            "spectrum_dot_label": "280 筆",
            "spectrum_caption": "280 筆遠低於 DL 通常需要的數千筆 → 停在第一格",
            "fit_heading": "適合用 DL vs 殺雞用牛刀",
            "fit_lines": [
                "✅ 資料量大、高維、非線性、影像 / 長序列",
                "✅ 已跑過 baseline 還是不夠好",
                "❌ 小樣本、低維表格、橫斷面互相獨立",
                "❌ 還沒跑 baseline 就想上 DL",
            ],
            "iron_heading": "鐵律：先 baseline，再考慮 DL",
            "iron_lines": [
                "280 筆、約 15 維 → 邏輯斯迴歸已足夠",
                "DL 參數 ≫ 樣本 → 過擬合風險極高",
                "值得學 PyTorch，但正式分析用 sklearn",
                "→ 牛刀留給大樣本、影像、長序列",
            ],
            "extra_banner_title": "額外範例：邏輯斯迴歸打敗神經網路",
            "extra_output_heading": "400 筆、8 特徵的再入院預測",
            "extra_output_text": (
                "Logistic Regression   AUC = 0.72\n"
                "3-layer MLP           AUC = 0.68\n"
                "→ 小樣本、低維表格：簡單模型反而贏\n"
                "→ 而且係數能直接跟醫師解釋"
            ),
            "blindspot_banner_title": "該用 DL 嗎？三個新手地雷",
            "outro_heading": "下一集：親手跑一次 PyTorch MLP",
            "outro_sub": "在 280 筆資料上驗證「牛刀殺雞」",
        },
        "en": {
            "title_main": "Should You Use Deep Learning?",
            "title_sub": "A decision framework: don't crack a nut with a sledgehammer",
            "temptation_heading": "A colleague's pitch: shall we try deep learning?",
            "temptation_lines": [
                '"DL is powerful - maybe it catches hidden interactions"',
                'Good question - but the answer is not "just use it"',
                "Ask four questions before sharpening this blade",
                "-> DL is a cleaver, not a cure-all",
            ],
            "decision_heading": "The framework: four questions, in order",
            "decision_lines": [
                "1. data < 1000 rows? -> stats / simple ML",
                '2. just "will it" or "why"? -> mechanistic model',
                "3. high-dim, long sequences, big data? -> now DL",
                "4. new pathogen, no early data? -> TSFM zero-shot",
            ],
            "spectrum_heading": "Where do 280 rows sit on the spectrum?",
            "spectrum_left": "small data\nsimple models",
            "spectrum_mid": "a few thousand\ngray zone",
            "spectrum_right": "tens of thousands+\nnow DL",
            "spectrum_dot_label": "280 rows",
            "spectrum_caption": "280 rows is far below the thousands DL needs -> stop at box 1",
            "fit_heading": "Good fit for DL vs overkill",
            "fit_lines": [
                "OK: big data, high-dim, nonlinear, images / long sequences",
                "OK: ran a baseline and it's still not enough",
                "NG: small n, low-dim tables, independent rows",
                "NG: reaching for DL before any baseline",
            ],
            "iron_heading": "Iron rule: baseline first, DL second",
            "iron_lines": [
                "280 rows, ~15 features -> logistic is enough",
                "DL params >> samples -> huge overfitting risk",
                "worth learning PyTorch, but ship with sklearn",
                "-> save the cleaver for big / image / sequence data",
            ],
            "extra_banner_title": "Extra example: logistic regression beats a neural net",
            "extra_output_heading": "Readmission prediction: 400 rows, 8 features",
            "extra_output_text": (
                "Logistic Regression   AUC = 0.72\n"
                "3-layer MLP           AUC = 0.68\n"
                "-> small n, low-dim table: the simple model wins\n"
                "-> and its coefficients explain to clinicians"
            ),
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: run a PyTorch MLP by hand",
            "outro_sub": 'Test "cracking a nut with a sledgehammer" on 280 rows',
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_temptation(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("temptation_heading", "temptation_lines", duration)

    def show_decision_tree(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("decision_heading", "decision_lines", duration)

    def show_data_spectrum(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("spectrum_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        axis = Line(LEFT * 4.5, RIGHT * 4.5, color=ManimColor(BORDER_LIGHT), stroke_width=3)
        left_tick = Dot(point=LEFT * 4.5, radius=0.09, color=ManimColor(TEXT_SECONDARY))
        mid_tick = Dot(point=ORIGIN, radius=0.09, color=ManimColor(TEXT_SECONDARY))
        right_tick = Dot(point=RIGHT * 4.5, radius=0.09, color=ManimColor(ACCENT_BLUE))

        left_label = Text(
            self.t("spectrum_left"), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY
        ).next_to(left_tick, DOWN, buff=0.3)
        mid_label = Text(
            self.t("spectrum_mid"), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY
        ).next_to(mid_tick, DOWN, buff=0.3)
        right_label = Text(
            self.t("spectrum_right"), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY
        ).next_to(right_tick, DOWN, buff=0.3)

        scale = VGroup(
            axis, left_tick, mid_tick, right_tick, left_label, mid_label, right_label
        ).move_to(UP * 0.2)

        data_dot = Dot(point=axis.get_start() + RIGHT * 0.9, radius=0.16, color=ManimColor(ACCENT_ORANGE))
        data_label = Text(
            self.t("spectrum_dot_label"), font=FONT_CJK, font_size=20, color=ACCENT_ORANGE
        ).next_to(data_dot, UP, buff=0.25)

        caption = Text(
            self.t("spectrum_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(scale), run_time=0.9)
        self.play(FadeIn(data_dot), FadeIn(data_label), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(
            FadeOut(VGroup(heading, scale, data_dot, data_label, caption)), run_time=0.5
        )

    def show_fit_vs_overkill(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("fit_heading", "fit_lines", duration)

    def show_iron_rule(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("iron_heading", "iron_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_logreg_wins(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        h = Text(
            self.t("extra_output_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(
            kwargs.get("output", self.t("extra_output_text")),
            position=ORIGIN,
        )
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_baseline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "dl = MLP().fit(X, y)  # no baseline"),
            kwargs.get("correct_code", "lr = LogisticRegression().fit(X, y)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_giant_model(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "net = MLP(hidden=[256, 128])  # n=280"),
            kwargs.get("correct_code", "net = MLP(hidden=[16])  # or skip DL"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_train_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "acc = score(model, X_train, y_train)"),
            kwargs.get("correct_code", "auc = score(model, X_test, y_test)"),
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
