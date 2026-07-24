"""Ch05-06: Mantel-Haenszel Weighted RR

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

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


class Ch05MantelHaenszelScene(EpiBaseScene):
    """Tutorial video scene: Mantel-Haenszel weighted RR."""

    total_steps: int = 13

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "Mantel-Haenszel 加權",
            "title_sub": "公平的學期成績",
            "intuition_heading": "加權的直覺：學期成績",
            "intuition_bullets": [
                "小考 20%、期末 40%、報告 40%",
                "各項乘以權重，再加總除以總權重",
                "MH 一樣：人多的層權重大",
                "不是簡單算術平均。",
            ],
            "formula_heading": "MH 公式（RR 版）",
            "formula_bullets": [
                "分子：Σᵢ  aᵢ × (cᵢ + dᵢ) / Nᵢ",
                "分母：Σᵢ  cᵢ × (aᵢ + bᵢ) / Nᵢ",
                "RR_MH = 分子 / 分母",
                "不用背——for loop 一行一行累加即可。",
            ],
            "code_heading": "Python 實作",
            "ten_percent_heading": "10% 法則判斷干擾",
            "summary_heading": "重點整理：MH 四步驟",
            "summary_bullets": [
                "① for loop 跑每一層",
                "② 累加 a(c+d)/N 當分子",
                "③ 累加 c(a+b)/N 當分母",
                "④ 分子除以分母 = 調整後 RR",
                "→ 再用 10% 法則判斷干擾幅度",
            ],
            "extra_banner_title": "額外範例：Simpson 悖論",
            "simpson_heading": "柏克萊 1973 錄取歧視案",
            "simpson_bullets": [
                "Crude：男 44% vs 女 35%（看似歧視）",
                "按科系分層：各系 女 ≥ 男",
                "原因：女生申請錄取率低的文科",
                "MH 調整後 RR ≈ 1.0，歧視其實沒有",
                "→ 干擾因子：申請科系",
            ],
            "blindspot_banner_title": "MH 常見地雷 3 選",
            "outro_heading": "下一集：交互作用 vs 干擾作用",
            "outro_sub": "別再把兩者搞混了！",
        },
        "en": {
            "title_main": "Mantel-Haenszel Weighting",
            "title_sub": "A fair term grade",
            "intuition_heading": "The intuition behind weighting: your term grade",
            "intuition_bullets": [
                "Quiz 20%, final 40%, report 40%",
                "Multiply each by its weight, sum, divide by total weight",
                "MH is the same: bigger strata get bigger weight",
                "It is NOT a simple arithmetic mean.",
            ],
            "formula_heading": "The MH formula (RR version)",
            "formula_bullets": [
                "Numerator: Σᵢ  aᵢ × (cᵢ + dᵢ) / Nᵢ",
                "Denominator: Σᵢ  cᵢ × (aᵢ + bᵢ) / Nᵢ",
                "RR_MH = numerator / denominator",
                "No memorizing — a for loop just accumulates it.",
            ],
            "code_heading": "Python implementation",
            "ten_percent_heading": "The 10% rule for spotting confounding",
            "summary_heading": "Recap: MH in four steps",
            "summary_bullets": [
                "① for-loop over every stratum",
                "② Accumulate a(c+d)/N as the numerator",
                "③ Accumulate c(a+b)/N as the denominator",
                "④ Numerator / denominator = adjusted RR",
                "→ Then use the 10% rule to gauge confounding",
            ],
            "extra_banner_title": "Extra example: Simpson's paradox",
            "simpson_heading": "The 1973 Berkeley admissions bias case",
            "simpson_bullets": [
                "Crude: men 44% vs women 35% (looks like bias)",
                "Stratified by department: women ≥ men in each",
                "Reason: women applied to low-admit humanities",
                "MH-adjusted RR ≈ 1.0, no bias after all",
                "→ Confounder: the department applied to",
            ],
            "blindspot_banner_title": "3 Common MH Traps",
            "outro_heading": "Next up: effect modification vs confounding",
            "outro_sub": "Stop mixing up the two!",
        },
    }

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

    def _code_block(self, heading: str, code: str, duration: float, output: str | None = None) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        if output:
            panel = self.show_code(code, title="mh.py", position=LEFT * 3 + UP * 0.2)
            self.wait(0.6)
            out = self.show_output(output, position=DOWN * 2.8)
            self.wait(max(0.1, duration - 2.0))
            self.play(FadeOut(VGroup(h, panel, out)), run_time=0.5)
        else:
            panel = self.show_code(code, title="mh.py", position=ORIGIN + DOWN * 0.3)
            self.wait(max(0.1, duration - 1.4))
            self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_mh_intuition(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("intuition_heading"),
            self.t("intuition_bullets"),
            duration,
        )

    def show_mh_formula(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("formula_heading"),
            self.t("formula_bullets"),
            duration,
        )

    def show_mh_code(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("code_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_ten_percent_rule(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._code_block(self.t("ten_percent_heading"), kwargs.get("code", ""), duration, output=kwargs.get("output"))

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_simpson(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("simpson_heading"),
            self.t("simpson_bullets"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_simple_avg(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rr_adj = results_df['RR'].mean()"),
            kwargs.get("correct_code", "rr_mh = mh_numerator / mh_denominator"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_denominator(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "change = abs(crude - adj) / crude * 100"),
            kwargs.get("correct_code", "change = abs(crude - adj) / adj * 100"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_interaction(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(f'Adjusted RR = {rr_mh}')"),
            kwargs.get("correct_code", "if homogeneity_ok: print(rr_mh); else: print(per_stratum)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(ORIGIN + UP * 0.5)
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
