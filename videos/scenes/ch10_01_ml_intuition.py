"""Ch10-01: Machine-learning intuition - the model as a training intern doctor.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. The running metaphor: train = classes, validation = mock exam,
test = the one-shot licensing exam, and AUC = the report card.
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
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10MLIntuitionScene(EpiBaseScene):
    """Tutorial video scene: ML intuition via the training-intern-doctor metaphor."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "機器學習超白話",
            "title_sub": "把模型當成一位受訓中的實習醫師",
            "intern_heading": "模型不是天才，是實習醫師",
            "intern_lines": [
                "模型不是天才，是實習醫師",
                "他知道的每件事，都是你餵的線索",
                "線索給錯 → 他會作弊",
                "線索太雜 → 他學不動",
            ],
            "task_heading": "要這位實習醫師做什麼？",
            "task_lines": [
                "迴歸：解釋「為什麼」會感染",
                "機器學習：預測「會不會」會感染",
                "只能用入住當下就有的線索",
                "→ 解釋回頭看、預測往前猜",
            ],
            "exams_heading": "三種考試，三個角色",
            "exam_train_title": "訓練集 train",
            "exam_train_body": "上課學公式\n可翻書慢慢學",
            "exam_val_title": "驗證集 validation",
            "exam_val_body": "模擬考\n可看答案改進",
            "exam_test_title": "測試集 test",
            "exam_test_body": "執照考\n只考一次作廢",
            "cv_heading": "資料太小，怎麼考才公平？",
            "cv_lines": [
                "資料只有 280 筆，超小",
                "只考一次 → 成績全看運氣",
                "交叉驗證：切 5 份、輪流當考題",
                "→ 取平均看實力、看標準差看穩不穩",
            ],
            "auc_heading": "AUC：實習醫師的成績單",
            "auc_05": "0.5\n閉眼猜",
            "auc_07": "0.7\n及格",
            "auc_08": "0.8\n不錯",
            "auc_10": "1.0\n太完美要查",
            "auc_caption": "AUC = 隨機抓一病一健康，把病人排前面的機率",
            "summary_heading": "五句話看懂機器學習",
            "summary_lines": [
                "① 模型是實習醫師，吃你給的線索",
                "② train 上課 / val 模擬考 / test 只考一次",
                "③ 資料小 → 交叉驗證取平均",
                "④ AUC = 排序病人的眼力",
                "⑤ 換聰明腦袋 ≠ 一定考更高",
            ],
            "extra_banner_title": "額外範例：敗血症早期預警分數",
            "extra_sepsis_heading": "換個疾病，養成邏輯不變",
            "extra_sepsis_lines": [
                "場景：加護病房敗血症早期預警",
                "線索：心跳、呼吸、血壓、體溫",
                "一樣切 train / test、看 AUC",
                "→ 換疾病，養成邏輯原封不動",
            ],
            "blindspot_banner_title": "機器學習三個新手地雷",
            "outro_heading": "下一集：資料三切分",
            "outro_sub": "先把考卷分好，執照考絕不偷看",
        },
        "en": {
            "title_main": "Machine Learning, Plain and Simple",
            "title_sub": "Think of the model as an intern doctor in training",
            "intern_heading": "Not a Genius - an Intern Doctor",
            "intern_lines": [
                "The model is no genius - it's an intern doctor",
                "Everything it knows is a clue you fed it",
                "Bad clues -> it cheats",
                "Messy clues -> it can't learn",
            ],
            "task_heading": "What is the intern here to do?",
            "task_lines": [
                'Regression: explains "why" infection happens',
                'ML: predicts "whether" infection will happen',
                "Only uses clues known at admission time",
                "-> explain looks back, predict looks forward",
            ],
            "exams_heading": "Three Exams, Three Roles",
            "exam_train_title": "train set",
            "exam_train_body": "attend class\nbooks allowed",
            "exam_val_title": "validation set",
            "exam_val_body": "mock exam\ncheck & improve",
            "exam_test_title": "test set",
            "exam_test_body": "licensing exam\none shot only",
            "cv_heading": "Data is tiny - how to grade fairly?",
            "cv_lines": [
                "Only 280 rows - very small",
                "One exam only -> the score is pure luck",
                "Cross-validation: 5 folds, each takes a turn as the exam",
                "-> mean = skill, std = how stable",
            ],
            "auc_heading": "AUC: the Intern's Report Card",
            "auc_05": "0.5\ncoin flip",
            "auc_07": "0.7\npass",
            "auc_08": "0.8\ngood",
            "auc_10": "1.0\ntoo perfect - check",
            "auc_caption": "AUC = odds of ranking a case above a healthy person",
            "summary_heading": "ML in Five Sentences",
            "summary_lines": [
                "1. The model is an intern - it eats the clues you give",
                "2. train = class / val = mock / test = one shot",
                "3. Small data -> cross-validate and average",
                "4. AUC = the eye for ranking patients",
                "5. A smarter brain != a higher score",
            ],
            "extra_banner_title": "Extra example: sepsis early-warning score",
            "extra_sepsis_heading": "Swap the disease, keep the training logic",
            "extra_sepsis_lines": [
                "Scenario: ICU sepsis early warning",
                "Clues: heart rate, breathing, BP, temperature",
                "Same train / test split, same AUC",
                "-> swap the disease, the logic is unchanged",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the train / validation / test split",
            "outro_sub": "Split the exams first - never peek at the licensing exam",
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
            .arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            .next_to(h, DOWN, buff=0.55)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _cards_row(
        self,
        heading_key: str,
        cards: list[tuple[str, str, str]],
        duration: float,
        *,
        card_w: float = 3.6,
        card_h: float = 2.6,
    ) -> None:
        """Render a heading over a row of accent-bordered cards.

        ``cards`` is a list of ``(accent_hex, title_key, body_key)`` tuples;
        title/body prose is resolved bilingually via :meth:`t`.
        """
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

    def show_intern_metaphor(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("intern_heading", "intern_lines", duration)

    def show_ml_task(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("task_heading", "task_lines", duration)

    def show_three_exams(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._cards_row(
            "exams_heading",
            [
                (ACCENT_BLUE, "exam_train_title", "exam_train_body"),
                (ACCENT_ORANGE, "exam_val_title", "exam_val_body"),
                (ACCENT_GREEN, "exam_test_title", "exam_test_body"),
            ],
            duration,
        )

    def show_cross_validation(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("cv_heading", "cv_lines", duration)

    def show_auc_scorecard(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("auc_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        axis = Line(LEFT * 4.2, RIGHT * 4.2, color=ManimColor(BORDER_LIGHT), stroke_width=3)

        specs = [
            (LEFT * 4.2, TEXT_SECONDARY, "auc_05"),
            (LEFT * 1.4, ACCENT_ORANGE, "auc_07"),
            (RIGHT * 1.4, ACCENT_GREEN, "auc_08"),
            (RIGHT * 4.2, ERROR_RED, "auc_10"),
        ]
        marks = VGroup(axis)
        for point, color, key in specs:
            dot = Dot(point=point, radius=0.13, color=ManimColor(color))
            label = Text(self.t(key), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY).next_to(
                dot, DOWN, buff=0.3
            )
            marks.add(dot, label)
        marks.move_to(UP * 0.3)

        caption = Text(
            self.t("auc_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(marks), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, marks, caption)), run_time=0.5)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_sepsis(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_sepsis_heading", "extra_sepsis_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_peek_test(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.fit(X_test, y_test)  # tune on test"),
            kwargs.get("correct_code", "model.fit(X_train, y_train)  # keep test"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_train_score(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "score = model.score(X_train, y_train)"),
            kwargs.get("correct_code", "score = cross_val_score(model, X, y).mean()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_complex_model(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model = DeepNet(layers=50)  # data has 280"),
            kwargs.get("correct_code", "model = LogisticRegression()  # small data"),
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
