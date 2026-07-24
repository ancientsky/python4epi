"""Ch10-02: The train / validation / test split - never peek at the test set.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. Teaches ``train_test_split(..., stratify=y)`` and why scaling
before the split leaks the test set.
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
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10TrainTestSplitScene(EpiBaseScene):
    """Tutorial video scene: the train / validation / test split with stratify."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "資料三切分",
            "title_sub": "先把考卷分好，測試集絕不偷看",
            "why_split_heading": "為什麼一定要先切開？",
            "why_split_lines": [
                "同一份資料又上課又考試 → 背答案就滿分",
                "看不出真本事",
                "呼應第七章：不能偷看未來",
                "→ 解法：切成 train / validation / test",
            ],
            "split_diagram_heading": "三份資料，三種工作",
            "split_train_title": "訓練集 train",
            "split_train_body": "約 60%\n上課學公式、fit",
            "split_val_title": "驗證集 val",
            "split_val_body": "約 20%\n模擬考、調參選模",
            "split_test_title": "測試集 test",
            "split_test_body": "約 20%\n只掀一次作廢",
            "ratios_heading": "60/20/20 還是 80/10/10？",
            "ratios_lines": [
                "資料越多 → val / test 比例可越小",
                "中資料：60/20/20 或 70/15/15",
                "大資料：80/10/10 甚至更極端",
                "→ 本章 280 筆＝小資料，val 交給交叉驗證",
            ],
            "split_code_heading": "一行 train_test_split 切好",
            "split_code_title": "split.py",
            "stratify_heading": "分層切 stratify：不平衡的保命符",
            "stratify_lines": [
                "重症只佔 24%，屬於少數",
                "隨機切 → 某折可能幾乎沒正例",
                "stratify=y：每份都維持原始比例",
                "→ 切分與 CV 都要用分層（StratifiedKFold）",
            ],
            "summary_heading": "資料切分三重點",
            "summary_lines": [
                "① 先切分：train 上課、test 打分數，看過作廢",
                "② 資料越大，test 比例可越小",
                "③ 小資料：validation 交給交叉驗證",
                "④ 不平衡 → 一定分層 stratify=y",
            ],
            "extra_banner_title": "額外範例：流感季住院預測模型",
            "extra_flu_heading": "換個疾病，切分邏輯不變",
            "extra_flu_title": "flu_split.py",
            "blindspot_banner_title": "資料切分三個新手地雷",
            "outro_heading": "下一集：問題定義",
            "outro_sub": "把長官的問題變成 0/1 標籤",
        },
        "en": {
            "title_main": "The Train / Val / Test Split",
            "title_sub": "Split the exams first - never peek at the test set",
            "why_split_heading": "Why split it up first?",
            "why_split_lines": [
                "One dataset for both class and exam -> memorize = 100%",
                "You can't see the real skill",
                "Echoes chapter 7: don't peek at the future",
                "-> fix: split into train / validation / test",
            ],
            "split_diagram_heading": "Three Sets, Three Jobs",
            "split_train_title": "train set",
            "split_train_body": "~60%\nlearn & fit",
            "split_val_title": "val set",
            "split_val_body": "~20%\nmock exam, tuning",
            "split_test_title": "test set",
            "split_test_body": "~20%\nopen once, then void",
            "ratios_heading": "60/20/20 or 80/10/10?",
            "ratios_lines": [
                "More data -> val / test share can shrink",
                "Medium data: 60/20/20 or 70/15/15",
                "Big data: 80/10/10 or even more extreme",
                "-> 280 rows here = small; val goes to cross-validation",
            ],
            "split_code_heading": "One line of train_test_split",
            "split_code_title": "split.py",
            "stratify_heading": "stratify: the lifesaver for imbalance",
            "stratify_lines": [
                "Severe cases are only 24% - a minority",
                "Random split -> a fold may have almost no positives",
                "stratify=y: every set keeps the original ratio",
                "-> use it for both the split and CV (StratifiedKFold)",
            ],
            "summary_heading": "Three Takeaways on Splitting",
            "summary_lines": [
                "1. Split first: train learns, test grades, then void",
                "2. Bigger data -> smaller test share is fine",
                "3. Small data: hand validation to cross-validation",
                "4. Imbalanced -> always stratify=y",
            ],
            "extra_banner_title": "Extra example: flu-season admission model",
            "extra_flu_heading": "Swap the disease, keep the split logic",
            "extra_flu_title": "flu_split.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: defining the problem",
            "outro_sub": "Turn the boss's question into a 0/1 label",
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

    def show_why_split(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_split_heading", "why_split_lines", duration)

    def show_split_diagram(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._cards_row(
            "split_diagram_heading",
            [
                (ACCENT_BLUE, "split_train_title", "split_train_body"),
                (ACCENT_ORANGE, "split_val_title", "split_val_body"),
                (ACCENT_GREEN, "split_test_title", "split_test_body"),
            ],
            duration,
        )

    def show_split_ratios(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("ratios_heading", "ratios_lines", duration)

    def show_split_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.model_selection import train_test_split\n"
                "\n"
                "X_train, X_test, y_train, y_test = train_test_split(\n"
                "    X, y, test_size=0.2, random_state=42, stratify=y,\n"
                ")"
            ),
        )
        self._code_block("split_code_heading", "split_code_title", code, duration)

    def show_stratify_why(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("stratify_heading", "stratify_lines", duration)

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

    def show_extra_flu(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# 流感季住院預測：一樣先切、一樣分層\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(\n"
                "    X, admit, test_size=0.2, stratify=admit,\n"
                ")"
            ),
        )
        self._code_block("extra_flu_heading", "extra_flu_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_scale_before_split(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "X = scaler.fit_transform(X)  # before split"),
            kwargs.get("correct_code", "pipe = make_pipeline(StandardScaler(), lr)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_stratify(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "train_test_split(X, y)  # no stratify"),
            kwargs.get("correct_code", "train_test_split(X, y, stratify=y)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_time_series(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "train_test_split(X, y, shuffle=True)  # ts"),
            kwargs.get("correct_code", "TimeSeriesSplit(n_splits=5)  # ordered"),
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
