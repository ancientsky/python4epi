"""Ch12-07: The parallel-trends assumption - DiD's lifeblood.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. DiD is only credible
when the treated and control groups moved on parallel pre-intervention trends;
this scene contrasts a healthy (parallel) case with a broken (diverging) one,
shows the "plot first, trust the model second" rule, and introduces the
event-study check (pre-period coefficients should sit near zero). All on-screen
prose is read from ``TEXT`` via ``self.t(key)``; code strings stay identical
across languages.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    DashedLine,
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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ERROR_RED,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12ParallelTrendsScene(EpiBaseScene):
    """Tutorial video scene: the parallel-trends assumption behind DiD."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "平行趨勢假設",
            "title_sub": "DiD 的命脈，一垮全崩",
            "why_heading": "為什麼平行趨勢是命脈？",
            "why_lines": [
                "DiD 拿對照組的變化，代表介入組「若沒介入本應如何」",
                "這只有在兩組介入前趨勢平行時才成立",
                "介入前斜率若不同 → 介入後的差可能只是本來就在分岔",
                "→ 跟介入本身一點關係都沒有",
            ],
            "ok_heading": "健康的樣子：介入前平行",
            "ok_treated_label": "介入組\ntreated",
            "ok_control_label": "對照組\ncontrol",
            "ok_check_label": "介入前平行 ✓",
            "ok_caption": "介入前平行，反事實延伸線才可信，落差才算介入效果",
            "broken_heading": "壞掉的樣子：介入前就分岔",
            "broken_treated_label": "介入組\ntreated",
            "broken_control_label": "對照組\ncontrol",
            "broken_x_label": "介入前就分道揚鑣 ✗",
            "broken_caption": "介入組本來就在漲，硬算成介入效果就是自己騙自己",
            "check_heading": "鐵律：先畫圖，再信模型",
            "check_lines": [
                "跑迴歸前，先把兩組每日趨勢畫在同一張圖",
                "只盯著介入日「左側」（介入前）看",
                "兩條線是否大致平行地一起起伏？",
                "→ 一張圖、一雙眼睛，就能救你一命",
            ],
            "event_heading": "更嚴謹：event study 事件研究法",
            "event_pre_label": "介入前係數 ≈ 0",
            "event_post_label": "介入後才偏離",
            "event_zero_label": "0",
            "event_caption": "介入前每期係數都貼著零 → 平行趨勢站得住腳",
            "summary_heading": "平行趨勢三重點",
            "summary_lines": [
                "① DiD 可信的前提：介入前兩組趨勢平行",
                "② 先畫圖只看介入日左側，眼睛勝過公式",
                "③ 想嚴謹就跑 event study，查介入前係數 ≈ 0",
                "→ 守住命脈，DiD 才不是空中樓閣",
            ],
            "extra_banner_title": "額外範例：最低購菸年齡政策",
            "extra_mla_heading": "趨勢在介入前就分岔的反例",
            "extra_mla_lines": [
                "某州把最低購菸年齡從 18 提高到 21",
                "想用 DiD 比自己 vs 鄰州的青少年吸菸率",
                "但政策前該州吸菸率本來就一路下滑",
                "→ 平行趨勢不成立，DiD 會高估政策效果",
            ],
            "blindspot_banner_title": "平行趨勢三個新手地雷",
            "outro_heading": "下一章：可重現研究",
            "outro_sub": "讓每一步分析都禁得起別人重新檢查",
        },
        "en": {
            "title_main": "The Parallel-Trends Assumption",
            "title_sub": "DiD's lifeblood - if it breaks, everything collapses",
            "why_heading": "Why are parallel trends the lifeblood?",
            "why_lines": [
                'DiD uses the control\'s change as the treated\'s "what if not treated"',
                "That only holds if both groups were parallel before the intervention",
                "Different pre-slopes -> the post gap may just be pre-existing divergence",
                "-> nothing to do with the intervention itself",
            ],
            "ok_heading": "Healthy case: parallel before the intervention",
            "ok_treated_label": "treated\ngroup",
            "ok_control_label": "control\ngroup",
            "ok_check_label": "parallel pre-trend OK",
            "ok_caption": "Parallel pre-trends make the counterfactual - and the gap - trustworthy",
            "broken_heading": "Broken case: diverging before the intervention",
            "broken_treated_label": "treated\ngroup",
            "broken_control_label": "control\ngroup",
            "broken_x_label": "already diverging pre-intervention X",
            "broken_caption": "The treated group was already rising - calling it an effect fools you",
            "check_heading": "Rule: plot first, trust the model second",
            "check_lines": [
                "Before the regression, plot both daily trends on one chart",
                'Look only at the "left" of the intervention day (the pre-period)',
                "Do the two lines rise and fall roughly in parallel?",
                "-> one chart and a pair of eyes can save your analysis",
            ],
            "event_heading": "Stricter: the event-study method",
            "event_pre_label": "pre coefs ~ 0",
            "event_post_label": "deviates only after",
            "event_zero_label": "0",
            "event_caption": "Every pre-period coef hugs zero -> parallel trends holds up",
            "summary_heading": "Three Takeaways on Parallel Trends",
            "summary_lines": [
                "1. DiD is only credible if pre-trends were parallel",
                "2. Plot first, look left of the intervention - eyes beat formulas",
                "3. For rigor run an event study, check pre coefs ~ 0",
                "-> Guard the lifeblood and your DiD isn't a castle in the air",
            ],
            "extra_banner_title": "Extra example: a minimum smoking-age policy",
            "extra_mla_heading": "A counter-example where pre-trends diverge",
            "extra_mla_lines": [
                "A state raises the minimum smoking age from 18 to 21",
                "It wants DiD to compare its vs the neighbor's youth smoking rate",
                "But its smoking rate was already sliding before the policy",
                "-> parallel trends fails, DiD overstates the policy effect",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Coming next: reproducible research",
            "outro_sub": "Make every analysis step survive someone else's re-check",
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
            VGroup(*[Text(x, font=FONT_CJK, font_size=21, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _iv_line(self) -> DashedLine:
        return DashedLine(
            DOWN * 1.2,
            UP * 2.1,
            color=ManimColor(ERROR_RED),
            stroke_width=2,
        )

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_matters(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_parallel_ok(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("ok_heading"), font=FONT_CJK, font_size=30, color=ACCENT_GREEN
        ).to_edge(UP, buff=0.6)

        control = Line(
            LEFT * 3.6 + UP * 0.4, RIGHT * 3.6 + DOWN * 0.5,
            color=ManimColor(ACCENT_BLUE), stroke_width=4,
        )
        treated_pre = Line(
            LEFT * 3.6 + UP * 1.7, UP * 1.25,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4,
        )
        treated_post = Line(
            UP * 1.25, RIGHT * 3.6 + UP * 0.2,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4,
        )
        counterfactual = DashedLine(
            UP * 1.25, RIGHT * 3.6 + UP * 0.8,
            color=ManimColor(TEXT_SECONDARY), stroke_width=3,
        )
        iv_line = self._iv_line()
        check = Text("✓", font=FONT_CJK, font_size=46, color=ManimColor(ACCENT_GREEN)).move_to(
            LEFT * 1.9 + UP * 1.95
        )

        treated_label = Text(
            self.t("ok_treated_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_ORANGE)
        ).move_to(LEFT * 5.1 + UP * 1.7)
        control_label = Text(
            self.t("ok_control_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_BLUE)
        ).move_to(LEFT * 5.1 + UP * 0.4)
        check_label = Text(
            self.t("ok_check_label"), font=FONT_CJK, font_size=18, color=ManimColor(ACCENT_GREEN)
        ).move_to(LEFT * 1.9 + UP * 1.05)

        caption = Text(
            self.t("ok_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        lines = VGroup(control, treated_pre, treated_post, counterfactual, iv_line, check)
        labels = VGroup(treated_label, control_label, check_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(lines), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, lines, labels, caption)), run_time=0.5)

    def show_parallel_broken(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("broken_heading"), font=FONT_CJK, font_size=30, color=ERROR_RED
        ).to_edge(UP, buff=0.6)

        control = Line(
            LEFT * 3.6 + DOWN * 0.1, RIGHT * 3.6 + UP * 0.2,
            color=ManimColor(ACCENT_BLUE), stroke_width=4,
        )
        treated_pre = Line(
            LEFT * 3.6 + DOWN * 0.6, UP * 0.9,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4,
        )
        treated_post = Line(
            UP * 0.9, RIGHT * 3.6 + UP * 1.7,
            color=ManimColor(ACCENT_ORANGE), stroke_width=4,
        )
        iv_line = self._iv_line()
        xmark = Text("✗", font=FONT_CJK, font_size=46, color=ManimColor(ERROR_RED)).move_to(
            LEFT * 2.0 + UP * 1.4
        )

        treated_label = Text(
            self.t("broken_treated_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_ORANGE)
        ).move_to(LEFT * 5.1 + DOWN * 0.5)
        control_label = Text(
            self.t("broken_control_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_BLUE)
        ).move_to(LEFT * 5.1 + UP * 0.2)
        x_label = Text(
            self.t("broken_x_label"), font=FONT_CJK, font_size=18, color=ManimColor(ERROR_RED)
        ).move_to(LEFT * 1.9 + UP * 0.6)

        caption = Text(
            self.t("broken_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        lines = VGroup(control, treated_pre, treated_post, iv_line, xmark)
        labels = VGroup(treated_label, control_label, x_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(lines), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, lines, labels, caption)), run_time=0.5)

    def show_how_to_check(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("check_heading", "check_lines", duration)

    def show_event_study(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("event_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        zero_line = DashedLine(
            LEFT * 4.0 + UP * 0.4, RIGHT * 4.0 + UP * 0.4,
            color=ManimColor(TEXT_SECONDARY), stroke_width=2,
        )
        iv_line = DashedLine(
            DOWN * 1.4, UP * 1.5, color=ManimColor(ERROR_RED), stroke_width=2
        )
        zero_label = Text(
            self.t("event_zero_label"), font=FONT_MONO, font_size=18, color=ManimColor(TEXT_SECONDARY)
        ).next_to(zero_line, LEFT, buff=0.15)

        pre_dots = VGroup(
            Dot(LEFT * 3.3 + UP * 0.5, radius=0.1, color=ManimColor(ACCENT_BLUE)),
            Dot(LEFT * 2.2 + UP * 0.35, radius=0.1, color=ManimColor(ACCENT_BLUE)),
            Dot(LEFT * 1.1 + UP * 0.48, radius=0.1, color=ManimColor(ACCENT_BLUE)),
        )
        post_dots = VGroup(
            Dot(RIGHT * 1.1 + DOWN * 0.2, radius=0.1, color=ManimColor(ACCENT_ORANGE)),
            Dot(RIGHT * 2.2 + DOWN * 0.7, radius=0.1, color=ManimColor(ACCENT_ORANGE)),
            Dot(RIGHT * 3.3 + DOWN * 1.05, radius=0.1, color=ManimColor(ACCENT_ORANGE)),
        )

        pre_label = Text(
            self.t("event_pre_label"), font=FONT_CJK, font_size=17, color=ManimColor(ACCENT_GREEN)
        ).move_to(LEFT * 2.3 + UP * 1.25)
        post_label = Text(
            self.t("event_post_label"), font=FONT_CJK, font_size=17, color=ManimColor(ACCENT_ORANGE)
        ).move_to(RIGHT * 2.5 + DOWN * 1.35)

        caption = Text(
            self.t("event_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        diagram = VGroup(zero_line, iv_line, zero_label, pre_dots, post_dots)
        labels = VGroup(pre_label, post_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(diagram), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, diagram, labels, caption)), run_time=0.5)

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

    def show_extra_mla(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_mla_heading", "extra_mla_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_skip_plot(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "did = fit_did(panel)  # no pre-check"),
            kwargs.get("correct_code", "plot_pretrends(panel); did = fit_did(panel)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_two_points(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "times = [pre, post]  # only 2 points"),
            kwargs.get("correct_code", "times = range(-4, 4)  # many periods"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ignore_precoef(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "trust_did = True"),
            kwargs.get("correct_code", "trust_did = (pre_coefs.abs() < eps).all()"),
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
