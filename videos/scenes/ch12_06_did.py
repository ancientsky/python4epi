"""Ch12-06: Difference-in-Differences (DiD) for policy evaluation.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. Teaches why a plain
before-vs-after comparison is dangerous and how DiD subtracts the control
group's change to isolate the true intervention effect (the ``treated:post``
interaction term). All on-screen prose is read from ``TEXT`` via
``self.t(key)``; code strings stay identical across languages.
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
    RoundedRectangle,
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


class Ch12DiDScene(EpiBaseScene):
    """Tutorial video scene: Difference-in-Differences for policy evaluation."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "差異中之差異 DiD",
            "title_sub": "介入之後數字降了，真的是你的功勞嗎？",
            "why_heading": "為什麼不能只比介入前後？",
            "why_lines": [
                "只比前後，會被其他同時發生的變化混淆",
                "疫情本來就要退燒？季節在變？通報作業調整？",
                "分不清是介入的功勞，還是時間自己走的",
                "→ DiD 用「對照組」把時間趨勢扣掉",
            ],
            "did_diagram_heading": "DiD 的核心邏輯",
            "did_treated_label": "介入組\ntreated",
            "did_control_label": "對照組\ncontrol",
            "did_cf_label": "反事實\n延伸線",
            "did_effect_label": "DiD\n效果",
            "did_iv_label": "介入日",
            "did_diagram_caption": "實際線與反事實延伸線之間的落差 = 介入效果",
            "nursing_heading": "護理之家的介入情境",
            "nursing_lines": [
                "1/25 對 2-3 樓 B 翼（高侵襲率、近汙染源）緊急消毒",
                "其餘樓層／翼別 → 對照組",
                "病例整理成「組別 × 每日」的面板資料",
                "→ 就能跑下面這條 DiD 迴歸",
            ],
            "did_code_heading": "一行迴歸，眼睛盯緊 treated:post",
            "did_code_title": "did_regression.py",
            "did_table_heading": "「差異中的差異」怎麼算",
            "did_col_before": "介入前 before",
            "did_col_after": "介入後 after",
            "did_row_treated": "介入組 treated",
            "did_row_control": "對照組 control",
            "did_table_formula": "DiD = (3.0 − 8.0) − (4.0 − 5.0) = −4.0",
            "summary_heading": "DiD 三重點",
            "summary_lines": [
                "① 別只比前後，一定要有對照組",
                "② 答案在 treated:post，不是 treated、不是 post",
                "③ 記得 cov_type='HC3' 穩健標準誤",
                "→ 本書資料觀察窗太短，DiD≈0、不顯著（誠實面對）",
            ],
            "extra_banner_title": "額外範例：口罩令 + 對照區",
            "extra_mask_heading": "口罩令加上對照區的 DiD",
            "extra_mask_lines": [
                "A 縣實施室內口罩令，B 縣沒有 → 對照組",
                "treated = 是否 A 縣、post = 是否政策上路後",
                "treated:post = 扣掉時間趨勢後的淨效果",
                "→ 才是口罩令真正壓下的病例",
            ],
            "blindspot_banner_title": "DiD 三個新手地雷",
            "outro_heading": "下一集：平行趨勢假設",
            "outro_sub": "DiD 的命脈，一垮全崩",
        },
        "en": {
            "title_main": "Difference-in-Differences (DiD)",
            "title_sub": "Cases dropped after the intervention - was it really you?",
            "why_heading": "Why not just compare before vs after?",
            "why_lines": [
                "Before-after alone is confounded by other simultaneous changes",
                "Was the outbreak fading anyway? Seasonality? Reporting shifts?",
                "You can't tell the intervention apart from the passage of time",
                "-> DiD uses a control group to subtract the time trend",
            ],
            "did_diagram_heading": "The core logic of DiD",
            "did_treated_label": "treated\ngroup",
            "did_control_label": "control\ngroup",
            "did_cf_label": "counter-\nfactual",
            "did_effect_label": "DiD\neffect",
            "did_iv_label": "intervention",
            "did_diagram_caption": "Gap between the actual line and the counterfactual = the effect",
            "nursing_heading": "The nursing-home intervention",
            "nursing_lines": [
                "1/25: emergency disinfection of 2-3F wing B (high rate, near source)",
                "Other floors / wings -> control group",
                'Cases reshaped into a "group x day" panel',
                "-> now we can run the DiD regression below",
            ],
            "did_code_heading": "One regression - keep your eyes on treated:post",
            "did_code_title": "did_regression.py",
            "did_table_heading": 'How the "difference of differences" works',
            "did_col_before": "before",
            "did_col_after": "after",
            "did_row_treated": "treated",
            "did_row_control": "control",
            "did_table_formula": "DiD = (3.0 - 8.0) - (4.0 - 5.0) = -4.0",
            "summary_heading": "Three Takeaways on DiD",
            "summary_lines": [
                "1. Never just before-after - you must have a control group",
                "2. The answer is treated:post, not treated, not post",
                "3. Remember cov_type='HC3' robust standard errors",
                "-> Our window is too short: DiD~0, not significant (be honest)",
            ],
            "extra_banner_title": "Extra example: mask mandate + a control region",
            "extra_mask_heading": "DiD for a mask mandate with a control region",
            "extra_mask_lines": [
                "County A imposes an indoor mask mandate, county B doesn't -> control",
                "treated = is it county A, post = is it after the policy",
                "treated:post = net effect after subtracting the time trend",
                "-> the cases the mask mandate truly pushed down",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Coming next: the parallel-trends assumption",
            "outro_sub": "DiD's lifeblood - if it breaks, everything collapses",
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

    def _did_cell(self, value: str, tint: str, pos) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.12,
            width=2.3,
            height=1.3,
            fill_color=ManimColor(tint),
            fill_opacity=0.14,
            stroke_color=ManimColor(tint),
            stroke_width=3,
        )
        val = Text(value, font=FONT_MONO, font_size=32, color=ManimColor(tint), weight="BOLD")
        val.move_to(card.get_center())
        return VGroup(card, val).move_to(pos)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_why_not_before_after(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_did_diagram(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("did_diagram_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        control = Line(
            LEFT * 3.6 + UP * 0.5,
            RIGHT * 3.6 + DOWN * 0.4,
            color=ManimColor(ACCENT_BLUE),
            stroke_width=4,
        )
        treated_pre = Line(
            LEFT * 3.6 + UP * 1.8,
            UP * 1.35,
            color=ManimColor(ACCENT_ORANGE),
            stroke_width=4,
        )
        treated_post = Line(
            UP * 1.35,
            RIGHT * 3.6 + UP * 0.1,
            color=ManimColor(ACCENT_ORANGE),
            stroke_width=4,
        )
        counterfactual = DashedLine(
            UP * 1.35,
            RIGHT * 3.6 + UP * 0.9,
            color=ManimColor(TEXT_SECONDARY),
            stroke_width=3,
        )
        iv_line = DashedLine(
            DOWN * 1.2,
            UP * 2.2,
            color=ManimColor(ERROR_RED),
            stroke_width=2,
        )
        did_gap = Line(
            RIGHT * 3.9 + UP * 0.1,
            RIGHT * 3.9 + UP * 0.9,
            color=ManimColor(ACCENT_GREEN),
            stroke_width=5,
        )
        dots = VGroup(
            Dot(UP * 1.35, radius=0.08, color=ManimColor(ACCENT_ORANGE)),
            Dot(RIGHT * 3.6 + UP * 0.1, radius=0.08, color=ManimColor(ACCENT_ORANGE)),
            Dot(RIGHT * 3.6 + UP * 0.9, radius=0.08, color=ManimColor(TEXT_SECONDARY)),
        )

        treated_label = Text(
            self.t("did_treated_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_ORANGE)
        ).move_to(LEFT * 5.1 + UP * 1.8)
        control_label = Text(
            self.t("did_control_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_BLUE)
        ).move_to(LEFT * 5.1 + UP * 0.5)
        cf_label = Text(
            self.t("did_cf_label"), font=FONT_CJK, font_size=15, color=ManimColor(TEXT_SECONDARY)
        ).move_to(RIGHT * 5.2 + UP * 1.1)
        effect_label = Text(
            self.t("did_effect_label"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_GREEN)
        ).move_to(RIGHT * 5.2 + DOWN * 0.2)
        iv_label = Text(
            self.t("did_iv_label"), font=FONT_CJK, font_size=15, color=ManimColor(ERROR_RED)
        ).next_to(iv_line, UP, buff=0.1)

        caption = Text(
            self.t("did_diagram_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        lines = VGroup(control, treated_pre, treated_post, counterfactual, iv_line, did_gap, dots)
        labels = VGroup(
            treated_label, control_label, cf_label, effect_label, iv_label
        )

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(lines), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, lines, labels, caption)), run_time=0.5)

    def show_nursing_scenario(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("nursing_heading", "nursing_lines", duration)

    def show_did_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import statsmodels.formula.api as smf\n"
                "\n"
                "model = smf.ols(\n"
                '    "daily_cases ~ treated + post + treated:post",\n'
                "    data=panel,\n"
                ').fit(cov_type="HC3")\n'
                'did = model.params["treated:post"]   # DiD 估計值'
            ),
        )
        self._code_block("did_code_heading", "did_code_title", code, duration)

    def show_did_table(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)

        heading = Text(
            self.t("did_table_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        tb = self._did_cell("8.0", ACCENT_ORANGE, LEFT * 1.3 + UP * 0.7)
        ta = self._did_cell("3.0", ACCENT_ORANGE, RIGHT * 1.3 + UP * 0.7)
        cb = self._did_cell("5.0", ACCENT_BLUE, LEFT * 1.3 + DOWN * 0.8)
        ca = self._did_cell("4.0", ACCENT_BLUE, RIGHT * 1.3 + DOWN * 0.8)
        grid = VGroup(tb, ta, cb, ca)

        col_before = Text(
            self.t("did_col_before"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).next_to(tb, UP, buff=0.22)
        col_after = Text(
            self.t("did_col_after"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).next_to(ta, UP, buff=0.22)
        row_treated = Text(
            self.t("did_row_treated"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_ORANGE)
        ).next_to(tb, LEFT, buff=0.3)
        row_control = Text(
            self.t("did_row_control"), font=FONT_CJK, font_size=16, color=ManimColor(ACCENT_BLUE)
        ).next_to(cb, LEFT, buff=0.3)

        formula = Text(
            self.t("did_table_formula"), font=FONT_MONO, font_size=24, color=ManimColor(ACCENT_GREEN)
        ).to_edge(DOWN, buff=0.7)

        labels = VGroup(col_before, col_after, row_treated, row_control)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.15), run_time=1.1)
        self.play(FadeIn(labels), run_time=0.5)
        self.play(FadeIn(formula), run_time=0.5)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, grid, labels, formula)), run_time=0.5)

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

    def show_extra_mask(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_mask_heading", "extra_mask_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_control(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "effect = after.mean() - before.mean()"),
            kwargs.get("correct_code", "effect = did_treated - did_control"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_coef(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "effect = model.params['post']"),
            kwargs.get("correct_code", "effect = model.params['treated:post']"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_robust(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.ols(f, data=panel).fit()"),
            kwargs.get("correct_code", "smf.ols(f, data=panel).fit(cov_type='HC3')"),
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
