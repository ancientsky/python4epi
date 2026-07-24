"""Ch09-04: Kaplan-Meier stratified by clinical severity - comparing group curves.

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
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch09KMByGroupScene(EpiBaseScene):
    """Tutorial video scene: KM curves stratified by clinical severity."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "分組 KM 曲線",
            "title_sub": "同一張圖疊好幾條線，看誰預後差",
            "why_heading": "為什麼一條線不夠？",
            "why_lines": [
                "全體那條把三種嚴重度混在一起平均",
                "輕症往上拉、重症往下拖",
                "混在一起 → 什麼差異都看不出來",
                "→ 拆開各畫一條，差異才現形",
            ],
            "code_heading": "for 迴圈：每組各 fit、各 plot",
            "code_title": "km_by_group.py",
            "curves_heading": "畫出來大概長這樣",
            "curves_mild": "mild：又高又平（撐得住）",
            "curves_severe": "severe：又早又陡（掉很快）",
            "curves_gap": "兩線之間的距離 = 嚴重度的效應",
            "curves_x": "發病後天數 →",
            "curves_y": "存活比例 ↑",
            "views_heading": "看分組曲線抓三個視角",
            "views_lines": [
                "① 分離時點：越早分開，效應越立竿見影",
                "② 垂直間距：間距越大，效應越強",
                "③ 有沒有交叉：交叉 → PH 假設可能被違反",
                "→ 交叉時 Cox 的 HR 要小心解讀",
            ],
            "summary_heading": "分組 KM 三重點",
            "summary_lines": [
                "① 分組才看得出「誰預後差」",
                "② plt.show() 放迴圈外，三線疊同一張",
                "③ 看分離時點、間距、有沒有交叉",
                "→ 交叉就是 PH 假設的警報",
            ],
            "extra_banner_title": "額外範例：新冠 ICU 按年齡分組",
            "extra_covid_heading": "嚴重度 → 年齡分組",
            "extra_covid_lines": [
                "新冠重症進 ICU，照年齡分三組",
                "年輕 / 中年 / 高齡，各畫一條線",
                "高齡通常掉得又早又快、年輕又高又平",
                "→ 同一套 for 迴圈，換分組變數就好",
            ],
            "blindspot_banner_title": "分組 KM 曲線三個新手地雷",
            "outro_heading": "下一集：對數秩檢定 log-rank",
            "outro_sub": "眼睛看到的差距，是真的還是運氣？",
        },
        "en": {
            "title_main": "KM Curves by Group",
            "title_sub": "Stack several lines on one plot to spot the worst",
            "why_heading": "Why isn't one line enough?",
            "why_lines": [
                "The overall line averages all three severities",
                "Mild pulls it up, severe drags it down",
                "Mixed together -> no difference is visible",
                "-> split into one line each, then it shows",
            ],
            "code_heading": "A for Loop: fit and plot each group",
            "code_title": "km_by_group.py",
            "curves_heading": "Roughly What It Looks Like",
            "curves_mild": "mild: high and flat (holds up)",
            "curves_severe": "severe: early and steep (drops fast)",
            "curves_gap": "the gap between lines = the severity effect",
            "curves_x": "days after onset ->",
            "curves_y": "survival fraction up",
            "views_heading": "Three Angles on Grouped Curves",
            "views_lines": [
                "1. When they split: earlier = a faster effect",
                "2. Vertical gap: wider = a stronger effect",
                "3. Do they cross: crossing -> PH may be violated",
                "-> if they cross, read the Cox HR with care",
            ],
            "summary_heading": "Three Takeaways on Grouped KM",
            "summary_lines": [
                '1. Only grouping shows "who does worse"',
                "2. plt.show() after the loop, so lines share one plot",
                "3. Watch the split point, the gap, and crossing",
                "-> crossing is the PH-assumption alarm",
            ],
            "extra_banner_title": "Extra example: COVID ICU by age group",
            "extra_covid_heading": "Severity -> age group",
            "extra_covid_lines": [
                "Severe COVID in the ICU, split into 3 age groups",
                "young / middle-aged / elderly, one line each",
                "elderly usually drops early and fast, young stays flat",
                "-> same for loop, just swap the grouping variable",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the log-rank test",
            "outro_sub": "is the gap you see real, or just luck?",
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

    def show_why_group(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_group_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'for sev in ["mild", "moderate", "severe"]:\n'
                '    g = cases[cases["clinical_severity"] == sev]\n'
                '    kmf.fit(g["time"], event_observed=g["event"], label=sev)\n'
                "    kmf.plot_survival_function()\n"
                "plt.show()   # after the loop: all lines on one figure"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_two_curves(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("curves_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        x_axis = Line([-3.2, -1.6, 0], [3.2, -1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        y_axis = Line([-3.2, -1.6, 0], [-3.2, 1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)

        # mild: shallow, late drops (stays high); severe: early, steep drops.
        mild = self._staircase([0.55, 0.8], ACCENT_GREEN)
        severe = self._staircase([0.08, 0.18, 0.3, 0.44, 0.6], ERROR_RED)

        mild_label = Text(
            self.t("curves_mild"), font=FONT_CJK, font_size=16, color=ACCENT_GREEN
        ).to_edge(DOWN, buff=1.0).shift(LEFT * 2.4)
        severe_label = Text(
            self.t("curves_severe"), font=FONT_CJK, font_size=16, color=ERROR_RED
        ).to_edge(DOWN, buff=0.6).shift(LEFT * 2.4)
        gap_label = Text(
            self.t("curves_gap"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6).shift(RIGHT * 2.6)

        y_label = Text(
            self.t("curves_y"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(y_axis, UP, buff=0.15)
        x_label = Text(
            self.t("curves_x"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(x_axis, RIGHT, buff=0.1)

        axes = VGroup(x_axis, y_axis, y_label, x_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(axes), run_time=0.5)
        self.play(FadeIn(mild), FadeIn(severe), run_time=1.0)
        self.play(FadeIn(mild_label), FadeIn(severe_label), FadeIn(gap_label), run_time=0.5)
        self.wait(max(0.1, duration - 2.9))
        self.play(
            FadeOut(
                VGroup(heading, axes, mild, severe, mild_label, severe_label, gap_label)
            ),
            run_time=0.5,
        )

    def show_three_views(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("views_heading", "views_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_covid_age(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_covid_heading", "extra_covid_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_show_in_loop(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "for g in grps: kmf.fit(g); plt.show()"),
            kwargs.get("correct_code", "for g in grps: kmf.fit(g)  # show after"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_eyeball_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "severe_worse = curve_below  # by eye"),
            kwargs.get("correct_code", "logrank_test(a.t, b.t, a.e, b.e)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_tiny_group(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "kmf.fit(tiny_group.t, tiny_group.e)"),
            kwargs.get("correct_code", "# need n>=10 per group first"),
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
