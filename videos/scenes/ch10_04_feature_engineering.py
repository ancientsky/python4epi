"""Ch10-04: Feature engineering - encode a messy chart into numbers.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings and code-style cell labels
stay identical across languages. Covers the three column types (numeric ->
scale, categorical -> one-hot, binary -> passthrough), missing values, and the
``ColumnTransformer`` that wires them together.
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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BG_CARD_ALT,
    BORDER_LIGHT,
    CODE_TEXT,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    VariableBox,
)


class Ch10FeatureEngineeringScene(EpiBaseScene):
    """Tutorial video scene: encoding a messy chart into model-ready numbers."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "特徵工程",
            "title_sub": "把雜亂病歷翻譯成模型看得懂的數字",
            "why_heading": "模型只會算數學，看不懂文字",
            "why_lines": [
                "模型只會算數學，看不懂文字",
                "「男/女」「A 棟」它讀不懂",
                "「年齡 85」和「floor 3」尺度不同",
                "→ 特徵工程＝整理成一致的數字表",
            ],
            "three_types_heading": "三種欄位，三種處理法",
            "num_title": "數值 numeric",
            "num_body": "例：age\n→ 標準化 scaler",
            "cat_title": "類別 categorical",
            "cat_body": "例：sex、wing\n→ one-hot 編碼",
            "bin_title": "二元 binary",
            "bin_body": "例：shower_use\n→ 直接放行",
            "onehot_heading": "類別為什麼要 one-hot？",
            "onehot_caption": "拆成平等的 0/1 開關，不是 A=1、B=2 的大小順序",
            "scaling_heading": "數值要縮放、缺值要補",
            "scaling_lines": [
                "age 20–100，其他欄位是 0/1",
                "不縮放 → age 被誤當「重要」",
                "StandardScaler：減平均、除標準差",
                "→ 有缺值用 SimpleImputer 補，別直接丟",
            ],
            "ct_code_heading": "ColumnTransformer：三條路一次搞定",
            "ct_code_title": "preprocess.py",
            "summary_heading": "特徵工程三重點",
            "summary_lines": [
                "① 數值標準化、類別 one-hot、二元放行",
                "② 類別別用 1/2/3，要 one-hot",
                "③ 缺值要補、尺度要縮",
                "→ 全部包進 Pipeline 才不洩漏",
            ],
            "extra_banner_title": "額外範例：結核病登記檔的風險特徵",
            "extra_tb_heading": "結核病登記檔：一樣三條路",
            "extra_tb_lines": [
                "場景：結核病防治登記檔",
                "數值：年齡 → 標準化",
                "類別：居住地、職業 → one-hot",
                "→ 二元：HIV、糖尿病、接觸史 → 直接用",
            ],
            "blindspot_banner_title": "特徵工程三個新手地雷",
            "outro_heading": "前三站完成：切分、定義、特徵工程",
            "outro_sub": "接著用 Pipeline 串起來，交叉驗證看 AUC",
        },
        "en": {
            "title_main": "Feature Engineering",
            "title_sub": "Encode the messy chart into numbers the model can read",
            "why_heading": "The Model Only Does Math",
            "why_lines": [
                "The model only does math - it can't read text",
                '"male/female", "wing A" mean nothing to it',
                '"age 85" and "floor 3" are different scales',
                "-> feature engineering = one consistent number table",
            ],
            "three_types_heading": "Three Column Types, Three Recipes",
            "num_title": "numeric",
            "num_body": "e.g. age\n-> StandardScaler",
            "cat_title": "categorical",
            "cat_body": "e.g. sex, wing\n-> one-hot encode",
            "bin_title": "binary",
            "bin_body": "e.g. shower_use\n-> passthrough",
            "onehot_heading": "Why one-hot the categories?",
            "onehot_caption": "Split into equal 0/1 switches, not an A=1, B=2 order",
            "scaling_heading": "Scale the numbers, fill the gaps",
            "scaling_lines": [
                "age is 20-100, other columns are 0/1",
                'no scaling -> age looks "important" by size',
                "StandardScaler: subtract mean, divide by SD",
                "-> missing? SimpleImputer, never feed raw NaN",
            ],
            "ct_code_heading": "ColumnTransformer: all three paths at once",
            "ct_code_title": "preprocess.py",
            "summary_heading": "Three Takeaways on Feature Engineering",
            "summary_lines": [
                "1. numeric scale / categorical one-hot / binary pass",
                "2. Never label categories 1/2/3 - use one-hot",
                "3. Fill missing values, match the scales",
                "-> wrap it all in a Pipeline to avoid leakage",
            ],
            "extra_banner_title": "Extra example: TB registry risk features",
            "extra_tb_heading": "TB registry: the same three paths",
            "extra_tb_lines": [
                "Scenario: a TB control registry",
                "numeric: age -> standardize",
                "categorical: residence, occupation -> one-hot",
                "-> binary: HIV, diabetes, contact -> passthrough",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "First three stops done: split, define, features",
            "outro_sub": "Next: wire it in a Pipeline, cross-validate for AUC",
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
            VGroup(*[Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            .next_to(h, DOWN, buff=0.55)
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

    def _cards_row(
        self,
        heading_key: str,
        cards: list[tuple[str, str, str]],
        duration: float,
        *,
        card_w: float = 3.6,
        card_h: float = 2.6,
    ) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )
        group = VGroup()
        for accent, title_key, body_key in cards:
            card = RoundedRectangle(
                corner_radius=0.15,
                width=card_w,
                height=card_h,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(accent),
                stroke_width=2.5,
            )
            tt = Text(self.t(title_key), font=FONT_CJK, font_size=21, color=accent, weight="BOLD")
            bb = Text(self.t(body_key), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY)
            inner = VGroup(tt, bb).arrange(DOWN, buff=0.3).move_to(card.get_center())
            group.add(VGroup(card, inner))
        group.arrange(RIGHT, buff=0.45).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(group, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(h, group)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_features(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_three_types(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._cards_row(
            "three_types_heading",
            [
                (ACCENT_BLUE, "num_title", "num_body"),
                (ACCENT_ORANGE, "cat_title", "cat_body"),
                (ACCENT_GREEN, "bin_title", "bin_body"),
            ],
            duration,
        )

    def show_onehot(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("onehot_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        src = VariableBox("wing", "'B'").scale(0.9).move_to(LEFT * 3.8 + UP * 0.2)

        cells = VGroup()
        for name, val, hot in [("wing_A", "0", False), ("wing_B", "1", True), ("wing_C", "0", False)]:
            cell = RoundedRectangle(
                corner_radius=0.1,
                width=2.3,
                height=0.8,
                fill_color=ManimColor(ACCENT_GREEN if hot else BG_CARD_ALT),
                fill_opacity=1,
                stroke_color=ManimColor(BORDER_LIGHT),
                stroke_width=1.5,
            )
            lbl = Text(
                f"{name} = {val}",
                font=FONT_MONO,
                font_size=18,
                color=(CODE_TEXT if hot else TEXT_PRIMARY),
            ).move_to(cell.get_center())
            cells.add(VGroup(cell, lbl))
        cells.arrange(DOWN, buff=0.25).move_to(RIGHT * 3 + UP * 0.2)

        arrow = Text("→", font=FONT_CJK, font_size=44, color=TEXT_SECONDARY).move_to(
            LEFT * 0.6 + UP * 0.2
        )

        caption = Text(
            self.t("onehot_caption"), font=FONT_CJK, font_size=19, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(src), run_time=0.5)
        self.play(FadeIn(arrow), FadeIn(cells, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, src, arrow, cells, caption)), run_time=0.5)

    def show_scaling_missing(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("scaling_heading", "scaling_lines", duration)

    def show_columntransformer_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.compose import ColumnTransformer\n"
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                "\n"
                "preprocess = ColumnTransformer([\n"
                '    ("num", StandardScaler(), num_cols),\n'
                '    ("cat", OneHotEncoder(drop="first"), cat_cols),\n'
                '    ("bin", "passthrough", bin_cols),\n'
                "])"
            ),
        )
        self._code_block("ct_code_heading", "ct_code_title", code, duration)

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

    def show_extra_tb(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_tb_heading", "extra_tb_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_label_encode(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'X["wing"] = LabelEncoder().fit_transform(w)'),
            kwargs.get("correct_code", 'OneHotEncoder().fit_transform(X[["wing"]])'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_forgot_scale(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'X = df[["age"] + bin_cols]  # no scaling'),
            kwargs.get("correct_code", 'StandardScaler().fit_transform(X[["age"]])'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_missing(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.fit(X, y)  # X still has NaN"),
            kwargs.get("correct_code", 'SimpleImputer(strategy="median")  # in pipe'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=25, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
