"""Ch10-05: Pipeline & data leakage - bind preprocessing + model into one, fit the
scaler on the training fold only.

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
    FadeIn,
    FadeOut,
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    BG_CARD,
    BG_CARD_ALT,
    BORDER_LIGHT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10PipelineLeakageScene(EpiBaseScene):
    """Tutorial video scene: sklearn Pipeline as a leakage guard."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Pipeline 與資料洩漏",
            "title_sub": "把前處理和模型綁成一條，順便防作弊",
            "leakage_problem_heading": "資料洩漏：ML 的頭號殺手",
            "leakage_problem_lines": [
                "測試集資訊偷偷混進訓練 → 考很高、上線慘敗",
                "禁忌一：先標準化 / SMOTE 再切分",
                "禁忌二：把結果的一部分當特徵（如症狀）",
                "禁忌三：用到未來資訊（時序要 TimeSeriesSplit）",
            ],
            "pipeline_idea_heading": "一個 Pipeline 綁住兩件事",
            "pi_prep_num": "數值 age → StandardScaler 縮放",
            "pi_prep_cat": "類別 sex/wing → OneHotEncoder",
            "pi_prep_bin": "二元 shower_use → passthrough",
            "pi_model": "Logistic\nRegression 模型",
            "pi_wrap_label": "Pipeline（fit / predict 一起走）",
            "pipeline_idea_caption": "整條在交叉驗證每一折內重跑 → 縮放只學訓練折",
            "pipeline_code_heading": "把前處理 + 模型串成一個物件",
            "pipeline_code_title": "pipeline.py",
            "fold_safety_heading": "為什麼交叉驗證裡不會洩漏？",
            "fold_safety_lines": [
                "每一折：scaler 只用訓練折算平均、標準差",
                "測試折完全不參與縮放的計算",
                "等於改考卷前，答案卷絕不偷看",
                "→ Pipeline 幫你自動守住這條線",
            ],
            "summary_heading": "Pipeline + 防洩漏 三重點",
            "summary_lines": [
                "① 前處理 + 模型綁成一條，fit / predict 一起走",
                "② 縮放的平均只從訓練折學，測試折不參與",
                "③ 換模型只換 model 那一格（下一集見）",
                "→ 規規矩矩，才不會考高上線崩",
            ],
            "extra_banner_title": "額外範例：COVID 檢驗值模型的縮放洩漏",
            "extra_covid_heading": "換 COVID 檢驗值，同一招防洩漏",
            "extra_covid_title": "covid_pipeline.py",
            "blindspot_banner_title": "Pipeline 與資料洩漏 三個新手地雷",
            "outro_heading": "下一集：交叉驗證 + AUC，成績單在比什麼",
            "outro_sub": "k-fold 讓每一筆都當一次考題",
        },
        "en": {
            "title_main": "Pipeline & Data Leakage",
            "title_sub": "Bind preprocessing to the model, and stop cheating",
            "leakage_problem_heading": "Data leakage: ML's number-one killer",
            "leakage_problem_lines": [
                "Test info sneaks into training -> high score, real-world flop",
                "Sin 1: scale / SMOTE before splitting",
                "Sin 2: use part of the outcome as a feature (e.g. symptoms)",
                "Sin 3: use future info (time series needs TimeSeriesSplit)",
            ],
            "pipeline_idea_heading": "One Pipeline binds two things",
            "pi_prep_num": "numeric age -> StandardScaler",
            "pi_prep_cat": "categorical sex/wing -> OneHotEncoder",
            "pi_prep_bin": "binary shower_use -> passthrough",
            "pi_model": "Logistic\nRegression model",
            "pi_wrap_label": "Pipeline (fit / predict together)",
            "pipeline_idea_caption": "Reruns inside every CV fold -> scaler learns from train fold only",
            "pipeline_code_heading": "Chain preprocessing + model into one object",
            "pipeline_code_title": "pipeline.py",
            "fold_safety_heading": "Why no leakage inside cross-validation?",
            "fold_safety_lines": [
                "Each fold: scaler learns mean/std from the train fold only",
                "The test fold never joins the scaling computation",
                "Like never peeking at the answer sheet before grading",
                "-> Pipeline holds this line for you automatically",
            ],
            "summary_heading": "Pipeline + Anti-leakage: 3 Takeaways",
            "summary_lines": [
                "1. Preprocess + model in one chain, fit / predict together",
                "2. Scaling mean learned from the train fold only",
                "3. Swap models by changing one cell (see next episode)",
                "-> Do it by the book, no high-score-then-crash",
            ],
            "extra_banner_title": "Extra: scaling leakage in a COVID lab-value model",
            "extra_covid_heading": "Swap to COVID labs, same anti-leakage trick",
            "extra_covid_title": "covid_pipeline.py",
            "blindspot_banner_title": "Pipeline & Leakage: 3 Beginner Blind Spots",
            "outro_heading": "Next: cross-validation + AUC, what the score compares",
            "outro_sub": "k-fold lets every row take the exam once",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _mini_card(
        self,
        text: str,
        *,
        width: float = 4.0,
        height: float = 0.8,
        fill: str = BG_CARD_ALT,
        accent: str = BORDER_LIGHT,
    ) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            fill_color=ManimColor(fill),
            fill_opacity=1,
            stroke_color=ManimColor(accent),
            stroke_width=2,
        )
        label = Text(text, font=FONT_CJK, font_size=18, color=ManimColor(TEXT_PRIMARY))
        if label.width > width - 0.4:
            label.scale_to_fit_width(width - 0.4)
        if label.height > height - 0.2:
            label.scale_to_fit_height(height - 0.2)
        label.move_to(card.get_center())
        return VGroup(card, label)

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
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_leakage_problem(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("leakage_problem_heading", "leakage_problem_lines", duration)

    def show_pipeline_idea(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        heading = Text(
            self.t("pipeline_idea_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        prep_cards = VGroup(
            *[
                self._mini_card(self.t(k), width=4.7, height=0.85)
                for k in ("pi_prep_num", "pi_prep_cat", "pi_prep_bin")
            ]
        ).arrange(DOWN, buff=0.25)
        arrow = Text("→", font=FONT_CJK, font_size=44, color=ManimColor(TEXT_SECONDARY))
        model_card = self._mini_card(
            self.t("pi_model"), width=2.9, height=1.4, fill=BG_CARD, accent=ACCENT_BLUE
        )
        body = VGroup(prep_cards, arrow, model_card).arrange(RIGHT, buff=0.4).move_to(UP * 0.15)

        wrap = RoundedRectangle(
            corner_radius=0.2,
            width=body.width + 0.7,
            height=body.height + 0.7,
            stroke_color=ManimColor(ACCENT_ORANGE),
            stroke_width=2.5,
            fill_opacity=0,
        ).move_to(body.get_center())
        wrap_label = (
            Text(self.t("pi_wrap_label"), font=FONT_CJK, font_size=16, color=ACCENT_ORANGE)
            .next_to(wrap, UP, buff=0.12)
            .align_to(wrap, LEFT)
            .shift(RIGHT * 0.25)
        )
        caption = Text(
            self.t("pipeline_idea_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(wrap), FadeIn(wrap_label), run_time=0.5)
        self.play(FadeIn(body), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, wrap, wrap_label, body, caption)), run_time=0.5)

    def show_pipeline_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.compose import ColumnTransformer\n"
                "\n"
                "preprocess = ColumnTransformer([\n"
                '    ("num", StandardScaler(), num_cols),\n'
                '    ("cat", OneHotEncoder(), cat_cols),\n'
                '    ("bin", "passthrough", bin_cols),\n'
                "])\n"
                'clf = Pipeline([("prep", preprocess), ("model", lr)])'
            ),
        )
        self._code_block("pipeline_code_heading", "pipeline_code_title", code, duration)

    def show_fold_safety(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("fold_safety_heading", "fold_safety_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_covid(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "covid_clf = Pipeline([\n"
                '    ("scale", StandardScaler()),\n'
                '    ("model", LogisticRegression(max_iter=500)),\n'
                "])\n"
                "scores = cross_val_score(covid_clf, X, y, cv=5)"
            ),
        )
        self._code_block("extra_covid_heading", "extra_covid_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_scale_before_split(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "scaler.fit(X); split(X)  # leaked!"),
            kwargs.get("correct_code", "Pipeline([scaler, model])  # safe"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_smote_before_split(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "X, y = SMOTE().fit_resample(X, y)"),
            kwargs.get("correct_code", "Pipeline([SMOTE(), model])  # in fold"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_outcome_feature(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "X = df[['age', 'fever', 'cough']]"),
            kwargs.get("correct_code", "X = df[['age', 'shower_use']]"),
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
