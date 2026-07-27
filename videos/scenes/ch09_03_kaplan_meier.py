"""Ch09-03: The Kaplan-Meier overall survival curve - a descending staircase.

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
    DashedLine,
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch09KaplanMeierScene(EpiBaseScene):
    """Tutorial video scene: the overall Kaplan-Meier survival curve."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Kaplan-Meier 曲線",
            "title_sub": "一條會「下樓梯」的存活線",
            "idea_heading": "KM 曲線是怎麼長出來的",
            "idea_lines": [
                "一開始大家都活著 → 存活比例 100%",
                "每死一個人，線就往下踏一階",
                "沒人死的日子，線就平平地走",
                "→ 整條線 = 還活著的比例往下走",
            ],
            "staircase_heading": "來仔細看這座樓梯",
            "staircase_y": "還活著的比例 ↑",
            "staircase_x": "發病後天數 →",
            "staircase_tick": "＋ = 設限，這裡不下降",
            "staircase_median": "穿過 50% = 中位存活時間",
            "read_heading": "讀 KM 曲線記四件事",
            "read_lines": [
                "階梯下降 = 那天有人死亡",
                "小加號 tick = 設限，不影響高度",
                "穿過 50% = 中位存活時間",
                "尾端陰影變寬 = 人變少、CI 越不確定",
            ],
            "code_heading": "程式超短：兩欄 + 一行畫圖",
            "code_title": "km_overall.py",
            "summary_heading": "全體 KM 曲線三重點",
            "summary_lines": [
                "① 還活著的比例往下樓梯，越陡越糟",
                "② 小加號是設限，不會讓線往下踏",
                "③ 中位 = 穿過 50% 那天",
                "→ 印出 inf 是好消息：過半沒死",
            ],
            "extra_banner_title": "額外範例：術後傷口感染追蹤",
            "extra_postop_heading": "死亡 → 術後傷口感染",
            "extra_postop_lines": [
                "開完刀，想知道「幾天內會感染」",
                "事件 = 感染，時間 = 術後天數",
                "平安出院、還沒感染 = 設限",
                "→ 曲線越平，感染管制做得越好",
            ],
            "blindspot_banner_title": "Kaplan-Meier 三個新手地雷",
            "outro_heading": "下一集：按嚴重度分組比一比",
            "outro_sub": "同一張圖疊好幾條線，看誰預後差",
        },
        "en": {
            "title_main": "The Kaplan-Meier Curve",
            "title_sub": "A survival line that walks down a staircase",
            "idea_heading": "How the KM Curve Grows",
            "idea_lines": [
                "Everyone starts alive -> survival = 100%",
                "Each death drops the line one step down",
                "On days with no deaths, the line runs flat",
                "-> the whole line = fraction still alive",
            ],
            "staircase_heading": "A Closer Look at the Staircase",
            "staircase_y": "fraction still alive up",
            "staircase_x": "days after onset ->",
            "staircase_tick": "+ = censored, no drop here",
            "staircase_median": "crossing 50% = median survival",
            "read_heading": "Four Things to Read on a KM Curve",
            "read_lines": [
                "a step down = a death on that day",
                "a small + tick = censored, height unchanged",
                "crossing 50% = median survival time",
                "widening tail band = fewer at risk, wider CI",
            ],
            "code_heading": "Tiny Code: two columns + one plot line",
            "code_title": "km_overall.py",
            "summary_heading": "Three Takeaways on the Overall KM Curve",
            "summary_lines": [
                "1. Fraction alive walks down; steeper is worse",
                "2. A + is censored, it doesn't step the line down",
                "3. Median = the day the line crosses 50%",
                "-> printing inf is good news: over half survived",
            ],
            "extra_banner_title": "Extra example: post-op wound infection",
            "extra_postop_heading": "Death -> post-op wound infection",
            "extra_postop_lines": [
                'After surgery, ask "how many days until infection"',
                "event = infection, time = days after surgery",
                "discharged with no infection = censored",
                "-> a flatter curve = better infection control",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: compare curves by severity group",
            "outro_sub": "stack several lines on one plot to spot the worst",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.8
        )
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY)
                    for x in self.t(lines_key)
                ]
            )
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

    def _staircase(self, drops: list[float], color: str) -> VGroup:
        """Descending step function drawn with Line segments.

        ``drops`` are fractional x positions (0..1) where the curve steps down.
        """
        x0, x1, y_top, y_bot = -3.0, 3.0, 1.4, -1.4
        n = len(drops)
        step = (y_top - y_bot) / n
        segs = VGroup()
        x, y = x0, y_top
        for f in drops:
            px = x0 + f * (x1 - x0)
            segs.add(Line([x, y, 0], [px, y, 0], color=ManimColor(color), stroke_width=5))
            segs.add(Line([px, y, 0], [px, y - step, 0], color=ManimColor(color), stroke_width=5))
            x, y = px, y - step
        segs.add(Line([x, y, 0], [x1, y, 0], color=ManimColor(color), stroke_width=5))
        return segs

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_km_idea(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("idea_heading", "idea_lines", duration)

    def show_staircase(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("staircase_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        x_axis = Line([-3.2, -1.6, 0], [3.2, -1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        y_axis = Line([-3.2, -1.6, 0], [-3.2, 1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        stairs = self._staircase([0.16, 0.3, 0.46, 0.64, 0.82], ACCENT_ORANGE)

        # A censoring tick: a small + sitting on the flat run after the 4th
        # drop (fractional x=0.72 -> y = 1.4 - 4 * 0.56), where the line does
        # NOT step down.
        tick = Text(
            "+", font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_GREEN)
        ).move_to([1.32, -0.84 + 0.22, 0])
        tick_label = Text(
            self.t("staircase_tick"), font=FONT_CJK, font_size=15, color=ACCENT_GREEN
        ).to_edge(DOWN, buff=0.7).shift(RIGHT * 2.4)

        median_line = DashedLine([-3.2, 0, 0], [3.2, 0, 0], color=ManimColor(TEXT_SECONDARY))
        median_label = (
            Text(self.t("staircase_median"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY)
            .next_to(median_line, RIGHT, buff=0.1)
            .shift(UP * 0.25 + LEFT * 2.2)
        )

        y_label = Text(
            self.t("staircase_y"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(y_axis, UP, buff=0.15)
        x_label = Text(
            self.t("staircase_x"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(x_axis, RIGHT, buff=0.1)

        axes = VGroup(x_axis, y_axis, y_label, x_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(axes), run_time=0.5)
        self.play(FadeIn(stairs), run_time=1.0)
        self.play(FadeIn(median_line), FadeIn(median_label), run_time=0.4)
        self.play(FadeIn(tick), FadeIn(tick_label), run_time=0.4)
        self.wait(max(0.1, duration - 3.2))
        self.play(
            FadeOut(
                VGroup(
                    heading, axes, stairs, median_line, median_label, tick, tick_label
                )
            ),
            run_time=0.5,
        )

    def show_read_curve(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("read_heading", "read_lines", duration)

    def show_km_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from lifelines import KaplanMeierFitter\n"
                "\n"
                "kmf = KaplanMeierFitter()\n"
                'kmf.fit(cases["time_to_event"], event_observed=cases["event"])\n'
                "kmf.plot_survival_function()\n"
                "print(kmf.median_survival_time_)"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_postop(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_postop_heading", "extra_postop_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_no_event(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'kmf.fit(cases["time"])'),
            kwargs.get("correct_code", "kmf.fit(t, event_observed=cases.event)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_date_not_duration(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'kmf.fit(cases["death_date"], e)'),
            kwargs.get("correct_code", 'kmf.fit(cases["time_days"], e)'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_inf_median(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "bad = kmf.median_survival_time_ == inf"),
            kwargs.get("correct_code", "# inf median = over half never died"),
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
