"""Ch05-07: Effect Modification vs Confounding

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


class Ch05EffectModificationScene(EpiBaseScene):
    """Tutorial video scene: effect modification vs confounding."""

    total_steps: int = 12

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "交互作用 vs 干擾作用",
            "title_sub": "暴露的影響因人而異",
            "hotpot_heading": "麻辣鍋 × 拉肚子的故事",
            "hotpot_bullets": [
                "胃好的人：RR = 1.2",
                "胃不好的人：RR = 4.5",
                "差這麼多 → 不是干擾，是交互作用",
                "→ 必須分層報告：對誰影響多大",
                "合併成一個 RR 會誤導！",
            ],
            "comparison_heading": "干擾 vs 交互作用",
            "comparison_bullets": [
                "干擾：各層 RR 相近，粗≠調整 → 報調整後",
                "交互：各層 RR 差很大 → 分層報告",
                "干擾是假象，交互是真實",
                "兩者可以同時存在",
                "診斷對，才能報告對。",
            ],
            "homogeneity_heading": "同質性檢定：RR 範圍判斷",
            "report_heading": "有交互作用時的報告格式",
            "report_bullets": [
                "句首總結：「影響因 X 而異」",
                "分層列出每組的 RR + CI",
                "不寫合併 MH RR",
                "誠實 > 簡潔",
            ],
            "summary_heading": "重點整理",
            "summary_bullets": [
                "干擾合併報（MH），交互分層報",
                "用 RR 範圍或同質性檢定判斷",
                "CI 重疊 ≠ 沒差異（小樣本陷阱）",
                "一句話：干擾合併、交互分層。",
            ],
            "extra_banner_title": "額外範例：COVID 疫苗 × 免疫狀況",
            "vaccine_heading": "疫苗效力的效果修飾",
            "vaccine_bullets": [
                "免疫正常者：VE = 90%",
                "免疫低下者：VE = 50%",
                "合併 85% 會誤導免疫低下族群",
                "→ 分層報告，讓高風險群自保",
            ],
            "blindspot_banner_title": "常見地雷 3 選",
            "outro_heading": "下一集：病例對照版 MH",
            "outro_sub": "OR 版本，邏輯一樣，公式換一下。",
        },
        "en": {
            "title_main": "Effect Modification vs Confounding",
            "title_sub": "The exposure's effect varies from person to person",
            "hotpot_heading": "The spicy-hotpot × diarrhea story",
            "hotpot_bullets": [
                "Strong stomach: RR = 1.2",
                "Weak stomach: RR = 4.5",
                "So different → not confounding, it's interaction",
                "→ Must report by stratum: who is hit how hard",
                "Pooling into one RR would mislead!",
            ],
            "comparison_heading": "Confounding vs interaction",
            "comparison_bullets": [
                "Confounding: strata RR similar, crude≠adjusted → report adjusted",
                "Interaction: strata RR very different → report by stratum",
                "Confounding is an illusion, interaction is real",
                "Both can occur at once",
                "Diagnose right to report right.",
            ],
            "homogeneity_heading": "Homogeneity test: judging by the RR range",
            "report_heading": "How to report when interaction is present",
            "report_bullets": [
                "Lead line: 'the effect varies by X'",
                "List each group's RR + CI by stratum",
                "Do NOT write a pooled MH RR",
                "Honesty > brevity",
            ],
            "summary_heading": "Recap",
            "summary_bullets": [
                "Confounding → pool (MH); interaction → report by stratum",
                "Decide with the RR range or a homogeneity test",
                "Overlapping CIs ≠ no difference (small-sample trap)",
                "In a phrase: pool confounding, stratify interaction.",
            ],
            "extra_banner_title": "Extra example: COVID vaccine × immune status",
            "vaccine_heading": "Effect modification in vaccine effectiveness",
            "vaccine_bullets": [
                "Immunocompetent: VE = 90%",
                "Immunocompromised: VE = 50%",
                "A pooled 85% misleads the immunocompromised",
                "→ Report by stratum so high-risk groups can protect themselves",
            ],
            "blindspot_banner_title": "3 Common Traps",
            "outro_heading": "Next up: the case-control MH",
            "outro_sub": "The OR version — same logic, just swap the formula.",
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

    def _code_block(self, heading: str, code: str, duration: float) -> None:
        h = Text(heading, font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title="homogeneity.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_hotpot_metaphor(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets(
            self.t("hotpot_heading"),
            self.t("hotpot_bullets"),
            duration,
        )

    def show_comparison_table(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets(
            self.t("comparison_heading"),
            self.t("comparison_bullets"),
            duration,
        )

    def show_homogeneity_test(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._code_block(self.t("homogeneity_heading"), kwargs.get("code", ""), duration)

    def show_report_format(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets(
            self.t("report_heading"),
            self.t("report_bullets"),
            duration,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets(
            self.t("summary_heading"),
            self.t("summary_bullets"),
            duration,
        )

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_vaccine(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets(
            self.t("vaccine_heading"),
            self.t("vaccine_bullets"),
            duration,
        )

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_confuse(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.adjust_for(['age', 'sex', 'more_vars'])"),
            kwargs.get("correct_code", "report_stratified_results(by='effect_modifier')"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_ci_overlap(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if ci_overlap: no_interaction = True"),
            kwargs.get("correct_code", "run_interaction_test_in_regression_model()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_strat(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df.groupby('exposure')['outcome'].mean()"),
            kwargs.get("correct_code", "df.groupby(['exposure','modifier'])['outcome'].mean()"),
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
