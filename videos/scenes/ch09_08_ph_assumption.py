"""Ch09-08: The proportional-hazards (PH) assumption - checking and fixing it.

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


class Ch09PHAssumptionScene(EpiBaseScene):
    """Tutorial video scene: the PH assumption, check_assumptions, and remedies."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "比例風險假設",
            "title_sub": "那些漂亮的 HR，先過這一關才算數",
            "what_heading": "Cox 的關鍵前提：PH 假設",
            "what_lines": [
                "假設：兩組 hazard 比值整段追蹤保持常數",
                "白話：HR 從頭到尾「不隨時間變」",
                "成立：暴露組一直比對照快 1.5 倍",
                "違反：前期快很多、後期反而變慢",
            ],
            "curves_heading": "log(-log S) 圖：平行 vs 交叉",
            "curves_hold_title": "PH 成立",
            "curves_hold_sub": "兩線平行",
            "curves_violate_title": "PH 違反",
            "curves_violate_sub": "兩線交叉",
            "curves_caption": "兩條 log-log 曲線平行＝假設成立；交叉＝違反",
            "code_heading": "check_assumptions() 一行驗證",
            "code_title": "ph_check.py",
            "read_heading": "怎麼讀檢定結果",
            "read_lines": [
                "No violation detected → 全部通過，HR 可信",
                "某變項 p < 0.05 → 它違反，HR 隨時間變",
                "Schoenfeld 殘差有趨勢 → 違反的訊號",
                "⚠ 事件少檢定力低，記得搭配 KM 目視",
            ],
            "remedy_heading": "違反了怎麼辦？四帖藥",
            "remedy_lines": [
                "① 分層 strata：讓它的 baseline 自由變",
                "② 時變係數：讓效應隨時間改變",
                "③ 加「與時間的交互作用」項",
                "④ 拆時間段，或改用 AFT 模型",
            ],
            "summary_heading": "PH 假設三重點",
            "summary_lines": [
                "① Cox 的 HR 假設「比值不隨時間變」",
                "② check_assumptions() + 分組 KM 交叉一起看",
                "③ 違反就分層 / 時變 / 加時間交互作用",
                "→ 存活分析完整武器包，到手！",
            ],
            "extra_banner_title": "額外範例：結核病長期追蹤，風險會變",
            "extra_tb_heading": "TB 追蹤數年，早晚風險不同",
            "extra_tb_title": "ph_tb.py",
            "blindspot_banner_title": "PH 假設三個新手地雷",
            "outro_heading": "存活分析第四幕，完結！",
            "outro_sub": "描述 → 推論 → 迴歸 → 診斷，你全走過一遍了",
        },
        "en": {
            "title_main": "The Proportional-Hazards Assumption",
            "title_sub": "Those pretty HRs only count once they pass this gate",
            "what_heading": "Cox's key premise: the PH assumption",
            "what_lines": [
                "Assumes: the two groups' hazard ratio stays constant",
                'Plainly: the HR "does not change over time"',
                "Holds: the exposed stay 1.5x faster throughout",
                "Violated: much faster early, then slower late",
            ],
            "curves_heading": "log(-log S) plot: parallel vs crossing",
            "curves_hold_title": "PH holds",
            "curves_hold_sub": "curves parallel",
            "curves_violate_title": "PH violated",
            "curves_violate_sub": "curves cross",
            "curves_caption": "two log-log curves parallel = holds; crossing = violated",
            "code_heading": "check_assumptions(): one-line verification",
            "code_title": "ph_check.py",
            "read_heading": "How to read the check output",
            "read_lines": [
                "No violation detected -> all pass, HRs trustworthy",
                "a variable with p < 0.05 -> it violates, HR varies",
                "Schoenfeld residuals with a trend -> a warning sign",
                "! few events = low power, pair it with a KM eyeball",
            ],
            "remedy_heading": "Violated? Four remedies",
            "remedy_lines": [
                "1. strata: let its baseline hazard vary freely",
                "2. time-varying coefficient: let the effect change",
                '3. add an "interaction with time" term',
                "4. split time periods, or switch to an AFT model",
            ],
            "summary_heading": "Three Takeaways on the PH Assumption",
            "summary_lines": [
                '1. Cox HRs assume "the ratio never changes with time"',
                "2. check_assumptions() + KM crossing, read together",
                "3. if violated: stratify / time-vary / time interaction",
                "-> the full survival-analysis toolkit is yours!",
            ],
            "extra_banner_title": "Extra example: long-term TB follow-up, risk shifts",
            "extra_tb_heading": "TB followed for years: early vs late differ",
            "extra_tb_title": "ph_tb.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Act Four, survival analysis: complete!",
            "outro_sub": "describe -> infer -> regress -> diagnose, you've walked it all",
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

    def _panel(
        self,
        x_lo: float,
        x_hi: float,
        curve_a: tuple[float, float],
        curve_b: tuple[float, float],
        title: str,
        subtitle: str,
        title_color: str,
    ) -> VGroup:
        """One mini log-log plot: L-shaped axes + two group curves + labels."""
        y_bot, y_top = -1.15, 1.25
        x_axis = Line([x_lo, y_bot, 0], [x_hi, y_bot, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        y_axis = Line([x_lo, y_bot, 0], [x_lo, y_top, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        cx_lo, cx_hi = x_lo + 0.2, x_hi - 0.2
        line_a = Line(
            [cx_lo, curve_a[0], 0], [cx_hi, curve_a[1], 0], color=ManimColor(ACCENT_BLUE), stroke_width=4
        )
        line_b = Line(
            [cx_lo, curve_b[0], 0], [cx_hi, curve_b[1], 0], color=ManimColor(ACCENT_ORANGE), stroke_width=4
        )
        mid_x = (x_lo + x_hi) / 2
        title_mob = Text(title, font=FONT_CJK, font_size=22, color=ManimColor(title_color)).move_to(
            [mid_x, 1.75, 0]
        )
        sub_mob = Text(subtitle, font=FONT_CJK, font_size=17, color=TEXT_SECONDARY).move_to(
            [mid_x, -1.55, 0]
        )
        return VGroup(x_axis, y_axis, line_a, line_b, title_mob, sub_mob)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_what_is_ph(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("what_heading", "what_lines", duration)

    def show_ph_curves(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            self.t("curves_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        # Left panel: PH holds -> two parallel descending curves (same slope).
        hold = self._panel(
            -5.2, -1.6, (1.05, -0.35), (0.45, -0.95),
            self.t("curves_hold_title"), self.t("curves_hold_sub"), ACCENT_GREEN,
        )
        # Right panel: PH violated -> two curves that cross.
        violate = self._panel(
            1.6, 5.2, (1.05, -0.6), (-0.5, 0.85),
            self.t("curves_violate_title"), self.t("curves_violate_sub"), ERROR_RED,
        )

        caption = Text(
            self.t("curves_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(hold), run_time=0.9)
        self.play(FadeIn(violate), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.9))
        self.play(FadeOut(VGroup(heading, hold, violate, caption)), run_time=0.5)

    def show_check_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# same cox_df used to fit the model\n"
                "cph.check_assumptions(cox_df, show_plots=False)\n"
                "# prints a Schoenfeld test p-value per variable\n"
                "# lists any variable that violates PH + advice"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_read_check(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("read_heading", "read_lines", duration)

    def show_remedies(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("remedy_heading", "remedy_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_tb(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# TB followed for years: risk changes over time\n"
                'cph.fit(tb, "years", "death")\n'
                'cph.check_assumptions(tb, show_plots=False)  # PH violated\n'
                'cph.fit(tb, "years", "death", strata=["hiv_status"])'
            ),
        )
        self._code_block("extra_tb_heading", "extra_tb_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_never_check(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'cph.fit(df, "t", "e")  # HR trusted'),
            kwargs.get("correct_code", "cph.check_assumptions(df)  # check!"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_df(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cph.check_assumptions(new_df)"),
            kwargs.get("correct_code", "cph.check_assumptions(train_df)  # same"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_report_constant_hr(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'hr = cph.summary["exp(coef)"]  # violated'),
            kwargs.get("correct_code", 'cph.fit(df, "t", "e", strata=["sev"])'),
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
