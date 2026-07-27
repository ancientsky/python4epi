"""Ch03-07: Forest Plot — 用圖表比較多組風險比

Manim scene for the tutorial video on building a forest plot to visualise
risk ratios across multiple exposure variables in the Legionella outbreak.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch03ForestPlotScene(EpiBaseScene):
    """Tutorial video scene: building a forest plot for comparing risk ratios."""

    total_steps: int = 18

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Forest Plot 森林圖",
            "title_sub": "一張圖比較所有風險比",
            "anatomy_heading": "Forest Plot 的三大元素",
            "anatomy_p1": "• 點估計（point estimate）= RR 的位置",
            "anatomy_p2": "• 信賴區間（CI）= 水平誤差線的長度",
            "anatomy_p3": "• 虛線 RR=1（null line）= 無效果基準",
            "interpret_heading": "如何判讀森林圖",
            "interpret_p1": "• CI 完全在 1 右邊 → 暴露增加風險",
            "interpret_p2": "• CI 跨過 1 → 統計上不顯著",
            "interpret_p3": "• 點離 1 越遠 → 效果越強",
            "interpret_p4": "• CI 越窄 → 估計越精確",
            "summary_heading": "重點整理",
            "summary_p1": "1. 迴圈計算多組 RR + 95% CI",
            "summary_p2": "2. 結果存成 DataFrame 方便繪圖",
            "summary_p3": "3. plt.errorbar() 畫點估計 + 誤差線",
            "summary_p4": "4. axvline(x=1) 畫 null line",
            "summary_p5": "5. CI 不跨 1 才算有統計顯著意義",
            "extra_banner_title": "額外範例：COVID-19 疫苗保護力比較",
            "extra_heading": "情境：比較不同疫苗的 RR",
            "extra_p1": "• 三種疫苗 vs 未接種，結局 = 重症住院",
            "extra_p2": "• 同一張森林圖一次比較三組 RR",
            "extra_p3": "• CI 全在 1 左邊 → 疫苗有保護力",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：分層分析與干擾因子",
            "outro_sub": "Crude RR 不夠用？我們來校正干擾！",
        },
        "en": {
            "title_main": "Forest Plot",
            "title_sub": "One chart to compare every risk ratio",
            "anatomy_heading": "The Three Parts of a Forest Plot",
            "anatomy_p1": "• Point estimate = where the RR sits",
            "anatomy_p2": "• Confidence interval (CI) = length of the horizontal error bar",
            "anatomy_p3": "• Dashed RR=1 (null line) = the no-effect baseline",
            "interpret_heading": "How to Read a Forest Plot",
            "interpret_p1": "• CI entirely right of 1 → exposure raises risk",
            "interpret_p2": "• CI crosses 1 → not statistically significant",
            "interpret_p3": "• The farther the dot from 1 → the stronger the effect",
            "interpret_p4": "• Narrower CI → more precise estimate",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Loop to compute multiple RRs + 95% CIs",
            "summary_p2": "2. Store results in a DataFrame for easy plotting",
            "summary_p3": "3. plt.errorbar() draws point estimates + error bars",
            "summary_p4": "4. axvline(x=1) draws the null line",
            "summary_p5": "5. Only a CI that doesn't cross 1 is statistically significant",
            "extra_banner_title": "Extra example: comparing COVID-19 vaccine efficacy",
            "extra_heading": "Scenario: comparing the RR of different vaccines",
            "extra_p1": "• Three vaccines vs unvaccinated, outcome = severe hospitalization",
            "extra_p2": "• One forest plot compares all three RRs at once",
            "extra_p3": "• All CIs left of 1 → the vaccines are protective",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: Stratified Analysis and Confounders",
            "outro_sub": "Crude RR not enough? Let's adjust for confounding!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the forest plot lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_anatomy(self, duration: float = 6.0, **kwargs) -> None:
        """Explain the anatomy of a forest plot."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            self.t("anatomy_heading"),
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("anatomy_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("anatomy_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("anatomy_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_loop_setup(self, duration: float = 6.0, **kwargs) -> None:
        """Show the setup code: imports and exposure list."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import pandas as pd\n"
                "from epi_learning import risk_ratio\n"
                "\n"
                "df = pd.read_csv('legionella_outbreak.csv')\n"
                "exposures = ['shower_use', 'hydrotherapy_use',\n"
                "             'smoking_history', 'immunosuppressed']"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_loop_body(self, duration: float = 7.0, **kwargs) -> None:
        """Show the for-loop that computes RR + CI for each exposure."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "results = []\n"
                "for exp in exposures:\n"
                "    rr, ci_lo, ci_hi = risk_ratio(\n"
                "        df, exposure=exp, outcome='case_classification'\n"
                "    )\n"
                "    results.append({\n"
                "        'exposure': exp,\n"
                "        'RR': rr, 'CI_lo': ci_lo, 'CI_hi': ci_hi\n"
                "    })"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_to_dataframe(self, duration: float = 6.0, **kwargs) -> None:
        """Convert results list to a DataFrame."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "res = pd.DataFrame(results)\n"
                "print(res)"
            ),
        )

        output_text = kwargs.get(
            "output",
            (
                "           exposure    RR  CI_lo  CI_hi\n"
                "0        shower_use  2.31   1.72   3.10\n"
                "1  hydrotherapy_use  1.85   1.38   2.48\n"
                "2   smoking_history  1.42   1.05   1.92\n"
                "3  immunosuppressed  1.67   1.22   2.29"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_errorbar(self, duration: float = 6.0, **kwargs) -> None:
        """Show plt.errorbar() to draw the forest plot."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import matplotlib.pyplot as plt\n"
                "\n"
                "fig, ax = plt.subplots(figsize=(6, 4))\n"
                "ax.errorbar(\n"
                "    x=res['RR'], y=res['exposure'],\n"
                "    xerr=[res['RR']-res['CI_lo'],\n"
                "          res['CI_hi']-res['RR']],\n"
                "    fmt='o', color='#D97757', capsize=4\n"
                ")"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_null_line(self, duration: float = 5.0, **kwargs) -> None:
        """Add the null line at RR=1."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "ax.axvline(x=1, color='gray',\n"
                "           linestyle='--', label='RR=1')\n"
                "ax.set_xlabel('Risk Ratio (RR)')\n"
                "ax.set_title('Forest Plot: Legionella Exposures')"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_polish(self, duration: float = 5.0, **kwargs) -> None:
        """Final polish: legend, tight_layout, savefig."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "ax.legend()\n"
                "fig.tight_layout()\n"
                "fig.savefig('forest_plot.png', dpi=150)\n"
                "plt.show()"
            ),
        )

        self.show_code(code_lines, title="forest_plot.py")
        self.wait(duration - 0.5)
        self.clear_screen()

    def show_interpret(self, duration: float = 6.0, **kwargs) -> None:
        """How to interpret the forest plot."""
        self.show_step_indicator(8, self.total_steps)

        heading = Text(
            self.t("interpret_heading"),
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("interpret_p1"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interpret_p2"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interpret_p3"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text(self.t("interpret_p4"), font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about building a forest plot."""
        self.show_step_indicator(9, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_context(self, duration: float = 6.0, **kwargs) -> None:
        """Set up the COVID-19 vaccine forest plot context."""
        self.show_step_indicator(10, self.total_steps)

        heading = Text(
            self.t("extra_heading"),
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("extra_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("extra_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("extra_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.3), run_time=1.0)
        self.wait(duration - 1.5)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_extra_result(self, duration: float = 6.0, **kwargs) -> None:
        """Show the COVID vaccine forest plot code."""
        self.show_step_indicator(11, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "vaccines = ['AZ', 'Moderna', 'BNT']\n"
                "rr_vals = [0.35, 0.22, 0.18]\n"
                "ci_lo   = [0.28, 0.16, 0.13]\n"
                "ci_hi   = [0.44, 0.30, 0.25]\n"
                "\n"
                "ax.errorbar(x=rr_vals, y=vaccines,\n"
                "    xerr=[...], fmt='o', capsize=4)\n"
                "ax.axvline(x=1, ls='--', color='gray')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "All CIs below 1 -> all three vaccines reduce risk",
        )

        self.show_code(code_lines, title="vaccine_forest.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_sort(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: sorting exposures by RR for readability."""
        error_code = kwargs.get("error_code", "ax.errorbar(...)  # random order")
        correct_code = kwargs.get("correct_code", "res.sort_values('RR')  # sort by RR first")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_crude_rr(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: plotting crude RR without noting confounders."""
        error_code = kwargs.get("error_code", "# plot crude RR and call it causal")
        correct_code = kwargs.get("correct_code", "# label as crude RR, note confounders")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_multiple(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: ignoring multiple comparisons."""
        error_code = kwargs.get("error_code", "# 10 exposures, p<0.05 = significant")
        correct_code = kwargs.get("correct_code", "# 10 tests -> consider Bonferroni / FDR")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
