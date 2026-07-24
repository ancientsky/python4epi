"""Ch09-07: HR forest plot - reading adjusted hazard ratios at a glance.

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


class Ch09HRForestScene(EpiBaseScene):
    """Tutorial video scene: HR forest plot and how to read adjusted HRs."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "HR 森林圖",
            "title_sub": "一眼看出誰危險、誰保護、誰不顯著",
            "why_heading": "表格看到眼花？畫成森林圖",
            "why_lines": [
                "print_summary() 一堆數字，容易看花",
                "森林圖 = 同一組數字的圖形版",
                "每個變項一個「點 + 橫線」",
                "→ 誰危險、誰保護、誰不顯著，一眼分辨",
            ],
            "forest_heading": "森林圖的結構",
            "forest_ref_label": "HR=1 參考線",
            "forest_labels": ["severe", "age", "immuno", "female"],
            "forest_verdicts": ["危險", "不顯著", "危險", "保護"],
            "forest_caption": "紅=危險且顯著、灰=跨線不顯著、綠=保護且顯著",
            "code_heading": "一行畫出森林圖",
            "code_title": "hr_forest.py",
            "read_heading": "讀森林圖的三步驟",
            "read_lines": [
                "① 點在參考線哪一邊 → 方向（危險/保護）",
                "② 橫線有沒有跨過參考線 → 顯不顯著",
                "③ 橫線多長 → 確定性（越長越不確定）",
                "⚠ lifelines 畫 log(HR)，參考線在 x=0",
            ],
            "adjusted_heading": "每個 HR 都是「校正後」的",
            "adjusted_lines": [
                "Cox 同時放多因子，互相校正",
                "所以每個 HR 都是 adjusted HR",
                "不是單看一個因子的粗略關聯",
                "→ 這正是多變項模型的價值",
            ],
            "summary_heading": "HR 森林圖三重點",
            "summary_lines": [
                "① 點的位置看方向、橫線看顯著",
                "② CI 跨過 1（log 圖跨 0）＝ 不顯著",
                "③ 每個都是校正後的 adjusted HR",
                "→ 但這一切都建立在 PH 假設上",
            ],
            "extra_banner_title": "額外範例：癌症篩檢世代的校正 HR",
            "extra_screening_heading": "篩檢有沒有降低死亡風險？",
            "extra_screening_title": "hr_screening.py",
            "blindspot_banner_title": "HR 森林圖三個新手地雷",
            "outro_heading": "下一集：比例風險假設驗證",
            "outro_sub": "這些漂亮的 HR，得先通過 PH 假設才算數",
        },
        "en": {
            "title_main": "The HR Forest Plot",
            "title_sub": "See at a glance who's harmful, protective, or not significant",
            "why_heading": "Table too busy? Draw a forest plot",
            "why_lines": [
                "print_summary() is a wall of numbers - easy to blur",
                "the forest plot = the same numbers, drawn",
                'each variable is one "dot + horizontal line"',
                "-> harmful, protective, or not significant at a glance",
            ],
            "forest_heading": "Anatomy of a Forest Plot",
            "forest_ref_label": "HR=1 reference",
            "forest_labels": ["severe", "age", "immuno", "female"],
            "forest_verdicts": ["harmful", "n.s.", "harmful", "protective"],
            "forest_caption": "red=harmful & sig, grey=crosses line (n.s.), green=protective & sig",
            "code_heading": "One line draws the forest plot",
            "code_title": "hr_forest.py",
            "read_heading": "Three steps to read a forest plot",
            "read_lines": [
                "1. which side of the reference -> direction",
                "2. does the bar cross the reference -> significance",
                "3. how long the bar is -> certainty (longer = less)",
                "! lifelines plots log(HR), so the line is at x=0",
            ],
            "adjusted_heading": 'Every HR here is "adjusted"',
            "adjusted_lines": [
                "Cox holds all factors at once, mutually adjusted",
                "so each HR is an adjusted HR",
                "not the crude association of one factor alone",
                "-> this is the value of a multivariable model",
            ],
            "summary_heading": "Three Takeaways on the HR Forest Plot",
            "summary_lines": [
                "1. dot position = direction, bar = significance",
                "2. CI crossing 1 (0 on the log plot) = not significant",
                "3. every HR shown is an adjusted HR",
                "-> but all of it rests on the PH assumption",
            ],
            "extra_banner_title": "Extra example: adjusted HRs in a cancer-screening cohort",
            "extra_screening_heading": "Did screening lower the risk of death?",
            "extra_screening_title": "hr_screening.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: checking the proportional-hazards assumption",
            "outro_sub": "these pretty HRs only count once they pass the PH assumption",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)
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

    def _forest_row(
        self,
        y: float,
        label: str,
        ci_lo: float,
        ci_hi: float,
        dot_x: float,
        color: str,
        verdict: str,
    ) -> VGroup:
        """One forest-plot row: label, CI bar with caps, point estimate, verdict."""
        label_x, verdict_x = -5.4, 4.4
        lab = Text(label, font=FONT_MONO, font_size=18, color=ManimColor(TEXT_PRIMARY))
        lab.move_to([label_x + lab.width / 2, y, 0])
        ci = Line([ci_lo, y, 0], [ci_hi, y, 0], color=ManimColor(color), stroke_width=4)
        lo_cap = Line([ci_lo, y - 0.12, 0], [ci_lo, y + 0.12, 0], color=ManimColor(color), stroke_width=4)
        hi_cap = Line([ci_hi, y - 0.12, 0], [ci_hi, y + 0.12, 0], color=ManimColor(color), stroke_width=4)
        dot = Dot([dot_x, y, 0], radius=0.11, color=ManimColor(color))
        verd = Text(verdict, font=FONT_CJK, font_size=17, color=ManimColor(color)).move_to(
            [verdict_x, y, 0]
        )
        return VGroup(lab, ci, lo_cap, hi_cap, dot, verd)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_forest(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_forest_anatomy(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("forest_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        ref_x = 0.5
        ref = DashedLine(
            [ref_x, 1.75, 0], [ref_x, -1.7, 0], color=ManimColor(TEXT_SECONDARY), stroke_width=2
        )
        ref_label = Text(
            self.t("forest_ref_label"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).move_to([ref_x + 0.9, -2.05, 0])

        labels = self.t("forest_labels")
        verdicts = self.t("forest_verdicts")
        # (y, ci_lo, ci_hi, dot_x, color)
        rows_spec = [
            (1.25, 1.3, 2.9, 2.1, ERROR_RED),
            (0.45, -0.4, 1.8, 0.7, TEXT_SECONDARY),
            (-0.35, 1.6, 3.3, 2.4, ERROR_RED),
            (-1.15, -1.7, 0.1, -0.8, ACCENT_GREEN),
        ]
        rows = VGroup(
            *[
                self._forest_row(y, labels[i], lo, hi, dx, color, verdicts[i])
                for i, (y, lo, hi, dx, color) in enumerate(rows_spec)
            ]
        )

        caption = Text(
            self.t("forest_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(ref), FadeIn(ref_label), run_time=0.5)
        self.play(FadeIn(rows, lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.9))
        self.play(FadeOut(VGroup(heading, ref, ref_label, rows, caption)), run_time=0.5)

    def show_forest_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "cph.plot()   # forest plot of every HR + 95% CI\n"
                'plt.axvline(0, color="grey", ls="--")  # log(HR)=0 -> HR=1\n'
                'plt.title("Cox Regression - Hazard Ratio")\n'
                "plt.show()"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_read_forest(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("read_heading", "read_lines", duration)

    def show_adjusted_meaning(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("adjusted_heading", "adjusted_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_screening(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# cancer-screening cohort, adjust age + sex\n"
                'cox.fit(screen, "years", "cancer_death")\n'
                "cox.plot()   # forest of adjusted HRs\n"
                "# screened arm: HR < 1 and CI below 1 -> protective"
            ),
        )
        self._code_block("extra_screening_heading", "extra_screening_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_refline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "plt.axvline(1)  # x is log(HR)"),
            kwargs.get("correct_code", "plt.axvline(0)  # log(HR)=0 is HR=1"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ci_crosses_one(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "significant = hr > 1  # ignores CI"),
            kwargs.get("correct_code", "significant = ci_low > 1 or ci_hi < 1"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ci_width(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "effect = ci_width  # wider=stronger"),
            kwargs.get("correct_code", "effect = hr  # width is uncertainty"),
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
