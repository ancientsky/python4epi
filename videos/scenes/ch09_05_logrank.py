"""Ch09-05: The log-rank test - is the gap between survival curves real or luck?

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


class Ch09LogrankScene(EpiBaseScene):
    """Tutorial video scene: the log-rank test for comparing survival curves."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Log-rank 檢定",
            "title_sub": "那道差距，是真的還是運氣？",
            "question_heading": "眼睛很容易被騙",
            "question_lines": [
                "兩條曲線看起來分很開",
                "但每組只有幾個人時…",
                "那點差距可能只是隨機波動",
                "→ 需要客觀工具：看起來有差 → 真的有差",
            ],
            "idea_heading": "log-rank 在問什麼？",
            "idea_lines": [
                "H₀：兩組存活曲線其實一模一樣",
                "那實際觀察到的死亡，會長成這樣嗎？",
                "它比的是「整條曲線」，不是某一天",
                "→ 中位一樣、形狀不同，也可能顯著",
            ],
            "curves_heading": "這道差距，是真的還是碰巧？",
            "curves_a": "A 組：掉得慢",
            "curves_b": "B 組：掉得快",
            "curves_gap_q": "這道距離真的嗎？→ log-rank",
            "curves_x": "發病後天數 →",
            "curves_y": "存活比例 ↑",
            "code_heading": "餵四樣：兩組時間 + 兩組 event",
            "code_title": "logrank.py",
            "read_heading": "怎麼讀 p 值",
            "read_lines": [
                "p < 0.05 → 拒絕 H₀，有統計顯著差異",
                "p ≥ 0.05 → 證據不足，還不能說有差",
                "log-rank 只說「有沒有差」",
                "→ 想知道「差多少」請用 Cox 迴歸",
            ],
            "summary_heading": "Log-rank 三重點",
            "summary_lines": [
                "① 在問「這道差距是真的還是運氣」",
                "② 一定要餵四樣：兩組時間、兩組 event",
                "③ 只說「有沒有差」，不說「差多少」",
                "→ 量化效應交給 Cox 的風險比 HR",
            ],
            "extra_banner_title": "額外範例：登革熱新藥雙臂試驗",
            "extra_dengue_heading": "兩組比一比：用藥 vs 安慰劑",
            "extra_dengue_title": "logrank_dengue.py",
            "blindspot_banner_title": "Log-rank 三個新手地雷",
            "outro_heading": "下一步：Cox 比例風險迴歸",
            "outro_sub": "從「有沒有差」到「差幾倍風險」",
        },
        "en": {
            "title_main": "The Log-rank Test",
            "title_sub": "That gap - is it real, or just luck?",
            "question_heading": "The Eye Is Easily Fooled",
            "question_lines": [
                "Two curves look far apart",
                "but when each group has only a few people...",
                "that gap may be pure random noise",
                '-> need an objective tool: "looks different" -> "is different"',
            ],
            "idea_heading": "What Does log-rank Ask?",
            "idea_lines": [
                "H0: the two survival curves are truly identical",
                "would the observed deaths look like this then?",
                'it compares the "whole curve", not one day',
                "-> same median, different shape can still be significant",
            ],
            "curves_heading": "That Gap - Real or Coincidence?",
            "curves_a": "group A: drops slowly",
            "curves_b": "group B: drops fast",
            "curves_gap_q": "is this gap real? -> log-rank",
            "curves_x": "days after onset ->",
            "curves_y": "survival fraction up",
            "code_heading": "Feed four: both times + both event flags",
            "code_title": "logrank.py",
            "read_heading": "How to Read the p-value",
            "read_lines": [
                "p < 0.05 -> reject H0, a significant difference",
                "p >= 0.05 -> not enough evidence yet",
                'log-rank only says "different or not"',
                '-> for "how much" use Cox regression',
            ],
            "summary_heading": "Three Takeaways on Log-rank",
            "summary_lines": [
                '1. It asks "is this gap real or luck"',
                "2. Always feed four: both times, both event flags",
                '3. It says "different or not", not "how much"',
                "-> quantify the effect with the Cox hazard ratio",
            ],
            "extra_banner_title": "Extra example: a two-arm dengue drug trial",
            "extra_dengue_heading": "Compare two arms: drug vs placebo",
            "extra_dengue_title": "logrank_dengue.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: Cox proportional hazards regression",
            "outro_sub": 'from "is there a difference" to "how many times the risk"',
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
                    Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY)
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

    def show_question(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("question_heading", "question_lines", duration)

    def show_logrank_idea(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("idea_heading", "idea_lines", duration)

    def show_two_curves(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("curves_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        x_axis = Line([-3.2, -1.6, 0], [3.2, -1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        y_axis = Line([-3.2, -1.6, 0], [-3.2, 1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)

        # A: slow drops (stays high); B: fast, early drops (falls below).
        curve_a = self._staircase([0.5, 0.82], ACCENT_BLUE)
        curve_b = self._staircase([0.12, 0.24, 0.4, 0.58, 0.76], ACCENT_ORANGE)

        a_label = Text(
            self.t("curves_a"), font=FONT_CJK, font_size=16, color=ACCENT_BLUE
        ).to_edge(DOWN, buff=1.0).shift(LEFT * 2.5)
        b_label = Text(
            self.t("curves_b"), font=FONT_CJK, font_size=16, color=ACCENT_ORANGE
        ).to_edge(DOWN, buff=0.6).shift(LEFT * 2.5)
        gap_q = Text(
            self.t("curves_gap_q"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6).shift(RIGHT * 2.4)

        y_label = Text(
            self.t("curves_y"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(y_axis, UP, buff=0.15)
        x_label = Text(
            self.t("curves_x"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(x_axis, RIGHT, buff=0.1)

        axes = VGroup(x_axis, y_axis, y_label, x_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(axes), run_time=0.5)
        self.play(FadeIn(curve_a), FadeIn(curve_b), run_time=1.0)
        self.play(FadeIn(a_label), FadeIn(b_label), FadeIn(gap_q), run_time=0.5)
        self.wait(max(0.1, duration - 2.9))
        self.play(
            FadeOut(VGroup(heading, axes, curve_a, curve_b, a_label, b_label, gap_q)),
            run_time=0.5,
        )

    def show_logrank_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from lifelines.statistics import logrank_test\n"
                "\n"
                "result = logrank_test(\n"
                '    severe["time"], non_severe["time"],\n'
                '    event_observed_A=severe["event"],\n'
                '    event_observed_B=non_severe["event"],\n'
                ")\n"
                'print(f"log-rank p = {result.p_value:.4f}")'
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_pvalue_read(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("read_heading", "read_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_dengue(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'arm_a = trial[trial["arm"] == "drug"]\n'
                'arm_b = trial[trial["arm"] == "placebo"]\n'
                'res = logrank_test(arm_a["days"], arm_b["days"],\n'
                '                   arm_a["fever"], arm_b["fever"])\n'
                "print(res.p_value)"
            ),
        )
        self._code_block("extra_dengue_heading", "extra_dengue_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_missing_events(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "logrank_test(a.time, b.time)"),
            kwargs.get("correct_code", "logrank_test(a.t, b.t, a.e, b.e)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_p_as_effect(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "effect_size = result.p_value"),
            kwargs.get("correct_code", "# p tells if, not how much: use Cox"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_multiple_tests(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "logrank_test(a,b); logrank_test(a,c)"),
            kwargs.get("correct_code", "# adjust alpha for many comparisons"),
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
