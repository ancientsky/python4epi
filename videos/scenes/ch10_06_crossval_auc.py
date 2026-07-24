"""Ch10-06: k-fold cross-validation + AUC/ROC - what the number actually compares.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is read
from ``TEXT`` via ``self.t(key)``; code strings stay identical across languages.
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
    Square,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_WARM,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10CrossvalAucScene(EpiBaseScene):
    """Tutorial video scene: k-fold cross-validation and the meaning of AUC."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "交叉驗證 + AUC",
            "title_sub": "這張成績單到底在比什麼？",
            "cv_idea_heading": "5-fold 交叉驗證：輪流當考題",
            "cv_legend_test": "綠 = 測試折（當考題）",
            "cv_legend_train": "藍 = 訓練折（拿去學）",
            "cv_result_card": "5 個 AUC → 取平均 ± 標準差",
            "cv_idea_caption": "每一列換一折當測試 → 每筆資料都剛好考一次",
            "cv_code_heading": "cross_val_score 一行跑完 5 折",
            "cv_code_title": "cross_val.py",
            "cv_output_heading": "跑出來的結果",
            "cv_output_text": (
                "AUC = 0.623 +/- 0.048\n→ 平均約 0.62、標準差小 = 穩"
            ),
            "auc_meaning_heading": "AUC 到底是什麼？",
            "auc_scale_05": "0.5\n閉眼猜",
            "auc_scale_07": "0.7\n及格",
            "auc_scale_08": "0.8\n不錯",
            "auc_scale_10": "1.0\n全對（先疑洩漏）",
            "auc_meaning_caption": "隨機抓一個感染、一個健康，模型把感染者排前面的機率",
            "why_not_accuracy_heading": "為什麼不看準確率 accuracy？",
            "why_not_accuracy_lines": [
                "Task B 只有 24% 重症",
                "模型全猜「沒重症」→ 準確率照樣 76%",
                "聽起來高，其實一個病人都沒抓到",
                "→ 不平衡資料看 AUC，不看準確率",
            ],
            "summary_heading": "交叉驗證 + AUC 三重點",
            "summary_lines": [
                "① CV 給同一個模型一個更可信的分數（非比兩模型）",
                "② 看兩個數字：平均 = 多強、標準差 = 穩不穩",
                "③ AUC = 把感染者排在健康人前面的機率",
                "→ 0.5 猜、0.7 及格、0.8 不錯、1.0 先疑洩漏",
            ],
            "extra_banner_title": "額外範例：30 天再住院預測模型",
            "extra_readmit_heading": "換 30 天再住院，同一把尺",
            "extra_readmit_title": "readmission_cv.py",
            "blindspot_banner_title": "交叉驗證與 AUC 三個新手地雷",
            "outro_heading": "下一集：換一顆更聰明的腦袋 Random Forest",
            "outro_sub": "還要看哪條線索最有用（特徵重要性）",
        },
        "en": {
            "title_main": "Cross-Validation + AUC",
            "title_sub": "What does this score actually compare?",
            "cv_idea_heading": "5-fold CV: take turns being the exam",
            "cv_legend_test": "green = test fold (the exam)",
            "cv_legend_train": "blue = train folds (to learn on)",
            "cv_result_card": "5 AUCs -> take mean +/- std",
            "cv_idea_caption": "Each row rotates the test fold -> every row is examined once",
            "cv_code_heading": "cross_val_score runs 5 folds in one line",
            "cv_code_title": "cross_val.py",
            "cv_output_heading": "The result",
            "cv_output_text": (
                "AUC = 0.623 +/- 0.048\n-> mean about 0.62, small std = stable"
            ),
            "auc_meaning_heading": "So what is AUC?",
            "auc_scale_05": "0.5\ncoin flip",
            "auc_scale_07": "0.7\npass",
            "auc_scale_08": "0.8\ngood",
            "auc_scale_10": "1.0\nperfect (suspect leakage)",
            "auc_meaning_caption": "Grab one infected + one healthy: chance the model ranks the infected higher",
            "why_not_accuracy_heading": "Why not just look at accuracy?",
            "why_not_accuracy_lines": [
                "Task B has only 24% severe cases",
                'Always guess "not severe" -> accuracy is still 76%',
                "Sounds high, but it caught zero real patients",
                "-> On imbalanced data read AUC, not accuracy",
            ],
            "summary_heading": "Cross-Validation + AUC: 3 Takeaways",
            "summary_lines": [
                "1. CV gives ONE model a more trustworthy score (not a duel)",
                "2. Read two numbers: mean = how strong, std = how stable",
                "3. AUC = chance the infected is ranked above the healthy",
                "-> 0.5 guess, 0.7 pass, 0.8 good, 1.0 suspect leakage",
            ],
            "extra_banner_title": "Extra: a 30-day hospital readmission model",
            "extra_readmit_heading": "Swap to 30-day readmission, same ruler",
            "extra_readmit_title": "readmission_cv.py",
            "blindspot_banner_title": "Cross-Validation & AUC: 3 Beginner Blind Spots",
            "outro_heading": "Next: a smarter brain, the Random Forest",
            "outro_sub": "And which clue matters most (feature importance)",
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

    def _swatch(self, color: str, label_key: str) -> VGroup:
        sq = Square(
            side_length=0.34,
            fill_color=ManimColor(color),
            fill_opacity=0.9,
            stroke_width=0,
        )
        lab = Text(self.t(label_key), font=FONT_CJK, font_size=17, color=ManimColor(TEXT_PRIMARY))
        return VGroup(sq, lab).arrange(RIGHT, buff=0.2)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_cv_idea(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        heading = Text(
            self.t("cv_idea_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        rows = VGroup()
        for i in range(5):
            row = VGroup()
            for j in range(5):
                color = ACCENT_GREEN if j == i else ACCENT_BLUE
                sq = Square(
                    side_length=0.5,
                    fill_color=ManimColor(color),
                    fill_opacity=0.85,
                    stroke_color=ManimColor(BG_WARM),
                    stroke_width=2,
                )
                row.add(sq)
            row.arrange(RIGHT, buff=0.08)
            rows.add(row)
        grid = rows.arrange(DOWN, buff=0.08).move_to(LEFT * 2.3 + UP * 0.15)

        legend = VGroup(
            self._swatch(ACCENT_GREEN, "cv_legend_test"),
            self._swatch(ACCENT_BLUE, "cv_legend_train"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        result = Text(
            self.t("cv_result_card"), font=FONT_CJK, font_size=18, color=ManimColor(ACCENT_ORANGE)
        )
        right = VGroup(legend, result).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(
            RIGHT * 3.0 + UP * 0.15
        )

        caption = Text(
            self.t("cv_idea_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.05), run_time=1.1)
        self.play(FadeIn(right), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, grid, right, caption)), run_time=0.5)

    def show_cv_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.model_selection import cross_val_score\n"
                "\n"
                "scores = cross_val_score(\n"
                '    clf_lr, X, y, cv=5, scoring="roc_auc")\n'
                'print(f"AUC = {scores.mean():.3f} +/- {scores.std():.3f}")'
            ),
        )
        self._code_block("cv_code_heading", "cv_code_title", code, duration)

    def show_cv_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(
            self.t("cv_output_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(kwargs.get("output", self.t("cv_output_text")), position=ORIGIN)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_auc_meaning(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(
            self.t("auc_meaning_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        axis = Line(LEFT * 3.5, RIGHT * 3.5, color=ManimColor(BORDER_LIGHT), stroke_width=3)
        specs = [
            (-3.5, TEXT_SECONDARY, "auc_scale_05"),
            (-0.7, ACCENT_BLUE, "auc_scale_07"),
            (0.7, ACCENT_GREEN, "auc_scale_08"),
            (3.5, ERROR_RED, "auc_scale_10"),
        ]
        marks = VGroup(axis)
        for x, color, key in specs:
            dot = Dot(point=RIGHT * x, radius=0.13, color=ManimColor(color))
            lab = Text(
                self.t(key), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY
            ).next_to(dot, DOWN, buff=0.3)
            marks.add(dot, lab)
        marks.move_to(UP * 0.3)

        caption = Text(
            self.t("auc_meaning_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(marks), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, marks, caption)), run_time=0.5)

    def show_why_not_accuracy(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("why_not_accuracy_heading", "why_not_accuracy_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_readmit(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'readmit = Pipeline([("prep", prep), ("model", rf)])\n'
                "scores = cross_val_score(\n"
                '    readmit, X, y, cv=5, scoring="roc_auc")\n'
                'print(f"30-day readmit AUC = {scores.mean():.3f}")'
            ),
        )
        self._code_block("extra_readmit_heading", "extra_readmit_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_mean_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(scores.mean())"),
            kwargs.get("correct_code", "print(scores.mean(), scores.std())"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_not_stratified(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cross_val_score(clf, X, y, cv=5)"),
            kwargs.get("correct_code", "cv = StratifiedKFold(5, shuffle=True)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_accuracy_metric(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'scoring="accuracy"  # imbalanced!'),
            kwargs.get("correct_code", 'scoring="roc_auc"  # rank-based'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 4.0, **kwargs) -> None:
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
