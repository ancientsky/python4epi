"""Ch03-07: Forest Plot — 用圖表比較多組風險比

Manim scene for the tutorial video on building a forest plot to visualise
risk ratios across multiple exposure variables in the Legionella outbreak.
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
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    StepIndicator,
)


class Ch03ForestPlotScene(EpiBaseScene):
    """Tutorial video scene: building a forest plot for comparing risk ratios."""

    total_steps: int = 18

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the forest plot lesson."""
        self.show_title_card("Forest Plot 森林圖", "一張圖比較所有風險比", duration=duration)

    def show_anatomy(self, duration: float = 6.0, **kwargs) -> None:
        """Explain the anatomy of a forest plot."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Forest Plot 的三大元素",
            font=FONT_MONO,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 點估計（point estimate）= RR 的位置", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 信賴區間（CI）= 水平誤差線的長度", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 虛線 RR=1（null line）= 無效果基準", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
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
            "如何判讀森林圖",
            font=FONT_CJK,
            font_size=32,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• CI 完全在 1 右邊 → 暴露增加風險", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• CI 跨過 1 → 統計上不顯著", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• 點離 1 越遠 → 效果越強", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("• CI 越窄 → 估計越精確", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    def show_main_summary(self, duration: float = 5.0, **kwargs) -> None:
        """Summarise key points about building a forest plot."""
        self.show_step_indicator(9, self.total_steps)

        heading = Text(
            "重點整理",
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("1. 迴圈計算多組 RR + 95% CI", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("2. 結果存成 DataFrame 方便繪圖", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("3. plt.errorbar() 畫點估計 + 誤差線", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("4. axvline(x=1) 畫 null line", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("5. CI 不跨 1 才算有統計顯著意義", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = ExtraExampleBanner("額外範例：COVID-19 疫苗保護力比較")
        self.show_section_banner(banner, duration=duration)

    def show_extra_context(self, duration: float = 6.0, **kwargs) -> None:
        """Set up the COVID-19 vaccine forest plot context."""
        self.show_step_indicator(10, self.total_steps)

        heading = Text(
            "情境：比較不同疫苗的 RR",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text("• 三種疫苗 vs 未接種，結局 = 重症住院", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• 同一張森林圖一次比較三組 RR", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text("• CI 全在 1 左邊 → 疫苗有保護力", font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
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
        banner = BlindSpotBanner("初學者常見地雷 3 選")
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
            "下一集：分層分析與干擾因子",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "Crude RR 不夠用？我們來校正干擾！",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
