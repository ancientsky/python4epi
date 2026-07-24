"""Ch13-04: Read data, produce the single canonical summary (one right answer).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    UP,
    FadeIn,
    FadeOut,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch13DataSummaryScene(EpiBaseScene):
    """Tutorial video scene: the single canonical, deterministic summary."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "讀資料、產出摘要",
            "title_sub": "唯一的標準答案",
            "idea_heading": "這一步的產出：一個 summary",
            "idea_lines": [
                "summary 字典裝著這次分析所有關鍵數字",
                "感染數、死亡數、侵襲率、致死率全收進來",
                "當作這次分析「唯一的標準答案」",
                "→ 有把握，因為全是確定性運算，沒有隨機",
            ],
            "summary_code_heading": "讀資料 → 固定規則 → 摘要",
            "summary_code_title": "make_summary.py",
            "summary_output_heading": "跑出來的標準答案",
            "summary_output_text": (
                "n_infected: 121\n"
                "n_deaths: 19\n"
                "attack_rate: 43.2%   cfr: 15.7%\n"
                "-> the one canonical answer"
            ),
            "why_heading": "為什麼強調確定性",
            "why_lines": [
                "groupby、sum、mean 都是純數學運算",
                "跟亂數、多執行緒排序、時區完全無關",
                "同輸入永遠同輸出（決定論）",
                "→ 拿掉所有讓兩次跑不一樣的因素",
            ],
            "summary_heading": "標準答案三重點",
            "summary_lines": [
                "① summary 字典 = 唯一的標準答案",
                "② 衍生欄位用固定規則，不靠手動標記",
                "③ 全是確定性運算，跑幾次都一樣",
                "→ 存成檔案，下次重跑就能 diff 比對",
            ],
            "extra_banner_title": "額外範例：一份標準的病例計數表",
            "extra_case_heading": "各區病例數：唯一標準表",
            "extra_case_title": "case_counts.py",
            "blindspot_banner_title": "標準答案三個新手地雷",
            "outro_heading": "下一集：seed 決定論",
            "outro_sub": "隨機也要「隨機地一致」",
        },
        "en": {
            "title_main": "Read Data, Produce the Summary",
            "title_sub": "The one canonical answer",
            "idea_heading": "The output: a single summary",
            "idea_lines": [
                "The summary dict holds every key number",
                "infected, deaths, attack rate, CFR - all in it",
                "treated as this analysis's one right answer",
                "-> confident because it's all deterministic",
            ],
            "summary_code_heading": "read data -> fixed rule -> summary",
            "summary_code_title": "make_summary.py",
            "summary_output_heading": "The canonical answer",
            "summary_output_text": (
                "n_infected: 121\n"
                "n_deaths: 19\n"
                "attack_rate: 43.2%   cfr: 15.7%\n"
                "-> the one canonical answer"
            ),
            "why_heading": "Why insist on determinism",
            "why_lines": [
                "groupby, sum, mean are pure math ops",
                "unrelated to RNG, thread order, or timezone",
                "same input, always same output (determinism)",
                "-> remove all sources of run-to-run difference",
            ],
            "summary_heading": "Three Takeaways",
            "summary_lines": [
                "1. The summary dict = the one right answer",
                "2. Derived columns use a fixed rule, not by hand",
                "3. All deterministic - same result every run",
                "-> save to a file so you can diff next time",
            ],
            "extra_banner_title": "Extra example: a canonical case-count table",
            "extra_case_heading": "Cases per zone: the one canonical table",
            "extra_case_title": "case_counts.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: seed determinism",
            "outro_sub": 'random, but "consistently random"',
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=30, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.8)
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=22, color=ManimColor(TEXT_PRIMARY))
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
        h = Text(
            self.t(heading_key), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title=self.t(title_key), position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_the_idea(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("idea_heading", "idea_lines", duration)

    def show_summary_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'df = pd.read_csv(path)\n'
                'sev = df["clinical_severity"]\n'
                'df["infected"] = (sev != "not_ill").astype(int)\n'
                "\n"
                "summary = {\n"
                '    "n_infected": int(df["infected"].sum()),\n'
                '    "n_deaths": int((df["outcome"] == "dead").sum()),\n'
                "}"
            ),
        )
        self._code_block("summary_code_heading", "summary_code_title", code, duration)

    def show_summary_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(
            self.t("summary_output_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(kwargs.get("output", self.t("summary_output_text")), position=ORIGIN)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_why_deterministic(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_case_count(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "counts = (\n"
                '    df.groupby(["floor", "wing"])["infected"]\n'
                "      .sum()\n"
                '      .rename("cases")\n'
                ")\n"
                'counts.to_csv("case_counts.csv")  # one table'
            ),
        )
        self._code_block("extra_case_heading", "extra_case_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_not_saved(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "print(summary)  # only on screen"),
            kwargs.get("correct_code", 'json.dump(summary, open("s.json","w"))'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_manual_label(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'df["inf"] = manual_labels'),
            kwargs.get("correct_code", 'df["inf"] = df.sev != "not_ill"'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_nondeterministic(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "n = df.sample(100).shape[0]"),
            kwargs.get("correct_code", "n = len(df)  # deterministic count"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(
            self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ManimColor(ACCENT_ORANGE)
        ).move_to(ORIGIN + UP * 0.5)
        s = Text(
            self.t("outro_sub"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)
        ).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
