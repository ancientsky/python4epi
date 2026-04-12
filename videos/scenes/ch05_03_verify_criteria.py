"""Ch05-03: Verify Confounder Criteria with pd.crosstab"""

from __future__ import annotations

from manim import DOWN, LEFT, UP, ORIGIN, FadeIn, FadeOut, Text, VGroup

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch05VerifyCriteriaScene(EpiBaseScene):
    """Tutorial video scene: verify confounder criteria with pd.crosstab."""

    total_steps: int = 13

    def construct(self) -> None:
        self.construct_from_segments()

    def _bullets(self, heading: str, lines: list[str], duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = VGroup(
            *[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(h, DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_with_heading(self, heading: str, code: str, duration: float, output: str | None = None) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title="stratified.py", position=LEFT * 3 + UP * 0.2 if output else ORIGIN + DOWN * 0.3)
        if output:
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("驗證三要件", "pd.crosstab 實戰", duration=duration)

    def show_data_prep(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._code_with_heading(
            "Step 1：資料準備",
            kwargs.get("code", "import pandas as pd\ndf = pd.read_csv('legionella_outbreak.csv')"),
            duration,
        )

    def show_criterion_1(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._code_with_heading(
            "條件 ①：C ↔ E（功能狀態 × 淋浴）",
            kwargs.get("code", "pd.crosstab(df['functional_status'], df['shower_use'], normalize='index')"),
            duration,
            output=kwargs.get("output"),
        )

    def show_criterion_2(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_with_heading(
            "條件 ②：C ↔ D（功能狀態 × 感染）",
            kwargs.get("code", "pd.crosstab(df['functional_status'], df['infected'], normalize='index')"),
            duration,
            output=kwargs.get("output"),
        )

    def show_criterion_3(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            "條件 ③：不是中間變項（邏輯判斷）",
            [
                "問：洗澡 → 改變功能狀態？",
                "答：不會。洗澡不會讓人變能走動。",
                "→ 因果方向不對，不是中間變項",
                "三條都通過，確認是干擾因子。",
            ],
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            "重點整理：驗證流程",
            [
                "① crosstab(C, E, normalize='index')",
                "② crosstab(C, D, normalize='index')",
                "③ 邏輯判斷：C 是不是中間變項？",
                "三條通過 → 進入分層分析",
            ],
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner("額外範例：COVID-19 疫苗 × 年齡"), duration=duration)

    def show_extra_vaccine(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._code_with_heading(
            "疫苗效力的年齡干擾",
            kwargs.get(
                "code",
                "pd.crosstab(df['age_group'], df['vaccinated'], normalize='index')\n"
                "pd.crosstab(df['age_group'], df['severe'], normalize='index')",
            ),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner("驗證時的常見地雷 3 選"), duration=duration)

    def show_blindspot_absolute(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pd.crosstab(df['fs'], df['shower'])"),
            kwargs.get("correct_code", "pd.crosstab(df['fs'], df['shower'], normalize='index')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_test(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if 'looks different': confound = True"),
            kwargs.get("correct_code", "chi2, p, *_ = chi2_contingency(ct); ok = p < 0.05"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_small_cell(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "chi2_contingency(ct)  # cell n=2"),
            kwargs.get("correct_code", "fisher_exact(ct)  # small cell safe"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text("下一集：for loop 分層算 RR", font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text("把干擾因子「鎖」在每一層內部。", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
