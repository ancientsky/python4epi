"""Ch10-03: Problem definition - turn the boss's question into a 0/1 label.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. Covers building the 0/1 target, the label-defines-cheating rule,
and why class imbalance means AUC over accuracy.
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
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10ProblemDefinitionScene(EpiBaseScene):
    """Tutorial video scene: defining a 0/1 label and handling class imbalance."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "問題定義",
            "title_sub": "把長官的模糊問題變成 0/1 標籤",
            "boss_heading": "模型只認得 0 與 1",
            "boss_lines": [
                "「預測誰會生病」→ 模型聽不懂",
                "模型只認得 0 與 1",
                "要一欄乾淨的 0/1 標籤",
                "→ 0＝沒發生、1＝發生",
            ],
            "label_code_heading": "把問題寫成 0/1 標籤",
            "label_code_title": "labels.py",
            "two_tasks_heading": "兩個預測任務，各一欄 0/1",
            "task_a_title": "Task A infected",
            "task_a_body": "是否感染\n121/280 = 43%",
            "task_b_title": "Task B severe",
            "task_b_body": "住院或死亡\n68/280 = 24%",
            "cheating_heading": "標籤定了，作弊欄位也定了",
            "cheating_lines": [
                "標籤定了 → 作弊欄位也定了",
                "infected 來自 clinical_severity",
                "症狀 / 住院 / 死亡＝結果端，不能當特徵",
                "→ 拿答案預測答案，AUC 假高",
            ],
            "imbalance_heading": "類別不平衡：別被準確率騙",
            "imbalance_lines": [
                "Task B 只有 24% 是重症",
                "全猜「沒重症」→ 準確率 76%",
                "但一個都沒抓到，完全沒用",
                "→ 少數事件看 AUC，別看準確率",
            ],
            "summary_heading": "問題定義三重點",
            "summary_lines": [
                "① 模糊問題 → 一欄 0/1 標籤（astype int）",
                "② 結果端欄位＝作弊，踢出特徵",
                "③ 不平衡 → 看 AUC 不看準確率",
                "→ 標籤定義是整條工作流的地基",
            ],
            "extra_banner_title": "額外範例：登革熱重症的 0/1 標籤",
            "extra_dengue_heading": "換個疾病，一樣定 0/1",
            "extra_dengue_title": "dengue_label.py",
            "blindspot_banner_title": "問題定義三個新手地雷",
            "outro_heading": "下一集：特徵工程",
            "outro_sub": "把雜亂病歷翻譯成模型看得懂的數字",
        },
        "en": {
            "title_main": "Defining the Problem",
            "title_sub": "Turn the boss's vague question into a 0/1 label",
            "boss_heading": "The Model Only Knows 0 and 1",
            "boss_lines": [
                '"Predict who gets sick" -> the model can\'t parse it',
                "The model only knows 0 and 1",
                "It needs one clean 0/1 label column",
                "-> 0 = did not happen, 1 = happened",
            ],
            "label_code_heading": "Write the problem as a 0/1 label",
            "label_code_title": "labels.py",
            "two_tasks_heading": "Two prediction tasks, one 0/1 column each",
            "task_a_title": "Task A infected",
            "task_a_body": "was infected?\n121/280 = 43%",
            "task_b_title": "Task B severe",
            "task_b_body": "admitted or died\n68/280 = 24%",
            "cheating_heading": "Fix the label, you fix the cheat list",
            "cheating_lines": [
                "Label fixed -> the cheat columns are fixed too",
                "infected comes from clinical_severity",
                "symptoms / admission / death are outcomes, not features",
                "-> answer-predicts-answer inflates AUC",
            ],
            "imbalance_heading": "Class Imbalance: don't trust accuracy",
            "imbalance_lines": [
                "Task B is only 24% severe",
                'Always guess "not severe" -> 76% accuracy',
                "but it catches zero real cases - useless",
                "-> rare events: read AUC, not accuracy",
            ],
            "summary_heading": "Three Takeaways on Problem Definition",
            "summary_lines": [
                "1. Vague question -> one 0/1 label (astype int)",
                "2. Outcome columns = cheating, drop from features",
                "3. Imbalanced -> read AUC, not accuracy",
                "-> the label is the foundation of the workflow",
            ],
            "extra_banner_title": "Extra example: a 0/1 label for severe dengue",
            "extra_dengue_heading": "Swap the disease, still a 0/1 label",
            "extra_dengue_title": "dengue_label.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: feature engineering",
            "outro_sub": "Translate the messy chart into numbers the model can eat",
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
        card_w: float = 4.4,
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
            tt = Text(self.t(title_key), font=FONT_CJK, font_size=22, color=accent, weight="BOLD")
            bb = Text(self.t(body_key), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY)
            inner = VGroup(tt, bb).arrange(DOWN, buff=0.35).move_to(card.get_center())
            group.add(VGroup(card, inner))
        group.arrange(RIGHT, buff=0.6).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(group, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(h, group)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_boss_question(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("boss_heading", "boss_lines", duration)

    def show_label_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "\n"
                'df = pd.read_csv("data/synthetic/legionella_outbreak.csv")\n'
                'sev = df["clinical_severity"]\n'
                'df["infected"] = (sev != "not_ill").astype(int)\n'
                'df["severe"] = (\n'
                '    (df["hospitalized"] == 1) | (df["outcome"] == "dead")\n'
                ").astype(int)"
            ),
        )
        self._code_block("label_code_heading", "label_code_title", code, duration)

    def show_two_tasks(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._cards_row(
            "two_tasks_heading",
            [
                (ACCENT_BLUE, "task_a_title", "task_a_body"),
                (ACCENT_ORANGE, "task_b_title", "task_b_body"),
            ],
            duration,
        )

    def show_label_defines_cheating(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("cheating_heading", "cheating_lines", duration)

    def show_class_imbalance(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("imbalance_heading", "imbalance_lines", duration)

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

    def show_extra_dengue(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# 登革熱重症標籤：警示徵象或需要加護\n"
                'df["dengue_severe"] = (\n'
                '    (df["warning_signs"] == 1) | (df["icu"] == 1)\n'
                ").astype(int)"
            ),
        )
        self._code_block("extra_dengue_heading", "extra_dengue_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_leak_feature(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'X = df[["clinical_severity"]]  # answer'),
            kwargs.get("correct_code", 'X = df[["age", "shower_use"]]  # ok'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_raw_label(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'y = df["outcome"]  # strings dead/alive'),
            kwargs.get("correct_code", 'y = (df["outcome"] == "dead").astype(int)'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_accuracy(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "score = accuracy_score(y_test, pred)"),
            kwargs.get("correct_code", "score = roc_auc_score(y_test, proba)"),
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
