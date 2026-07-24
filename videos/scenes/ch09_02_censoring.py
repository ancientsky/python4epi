"""Ch09-02: Survival time and censored data - the event flag and why you can't drop censored rows.

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
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch09CensoringScene(EpiBaseScene):
    """Tutorial video scene: survival time, the event flag, and censoring."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "設限資料",
            "title_sub": "碼表還在跑，觀察就結束了",
            "stopwatch_heading": "存活時間 = 碼表 start → stop",
            "stopwatch_lines": [
                "在每個病人身邊放一個碼表",
                "發病那天按 start（起點）",
                "死亡那天按 stop（結局）",
                "→ 中間的天數 = 存活時間",
            ],
            "eventflag_heading": "event 旗標：記錄結局是 1 還是 0",
            "eventflag_lines": [
                "死亡 → event = 1（事件真的發生）",
                "還活著 → event = 0（只看到一半）",
                "event=1 永遠是「我們在等的事件」",
                "→ 這個 1/0 是存活分析的命根子",
            ],
            "timeline_heading": "三個病人、三種結局",
            "timeline_death": "死亡（event=1）",
            "timeline_censored": "撐到觀察結束（event=0，設限）",
            "timeline_lost": "中途失聯（event=0，設限）",
            "timeline_obs_end": "觀察結束",
            "timeline_caption": "設限不是遺漏值：每個人都帶著「至少撐了這麼久」的資訊",
            "build_heading": "程式三行：時間、事件、餵進去",
            "build_title": "build_survival.py",
            "why_heading": "為什麼設限不能丟？",
            "why_lines": [
                "丟掉設限 = 刪光「撐最久」的好體質",
                "→ 存活時間被嚴重低估",
                "還會生出選擇偏差（selection bias）",
                "→ 設限資料是資產，不是垃圾",
            ],
            "summary_heading": "設限三重點打包",
            "summary_lines": [
                "① 存活資料要三樣：時間、事件、誰設限",
                "② event 死亡填 1、存活填 0，別填反",
                "③ 設限一定要留、一定要餵進去",
                "→ 一個病人都不能丟",
            ],
            "extra_banner_title": "額外範例：結核病治療世代",
            "extra_tb_heading": "結核病：失聯 = 設限",
            "extra_tb_lines": [
                "TB 要吃半年以上的藥，追蹤期很長",
                "搬家、換醫院、失聯是家常便飯",
                "失聯不是治療失敗，是沒看到結局",
                "→ event 填 0、時間照算，不浪費",
            ],
            "blindspot_banner_title": "設限資料三個新手地雷",
            "outro_heading": "下一集：畫出 Kaplan-Meier 曲線",
            "outro_sub": "那條會下樓梯的線，到底怎麼讀",
        },
        "en": {
            "title_main": "Censored Data",
            "title_sub": "The stopwatch is still running when observation ends",
            "stopwatch_heading": "Survival Time = stopwatch start -> stop",
            "stopwatch_lines": [
                "Put a stopwatch next to each patient",
                "Press start on the day of onset",
                "Press stop on the day of death (the outcome)",
                "-> the days in between = survival time",
            ],
            "eventflag_heading": "The event Flag: record the outcome as 1 or 0",
            "eventflag_lines": [
                "Death -> event = 1 (the event really happened)",
                "Still alive -> event = 0 (only half the story)",
                'event=1 is always "the event we wait for"',
                "-> this 1/0 is the heart of survival analysis",
            ],
            "timeline_heading": "Three Patients, Three Endings",
            "timeline_death": "death (event=1)",
            "timeline_censored": "lasted to study end (event=0, censored)",
            "timeline_lost": "lost to follow-up (event=0, censored)",
            "timeline_obs_end": "observation ends",
            "timeline_caption": 'Censored is not missing: each carries "observed at least this long"',
            "build_heading": "Three Lines: time, event, feed it in",
            "build_title": "build_survival.py",
            "why_heading": "Why can't we drop censored rows?",
            "why_lines": [
                'Dropping censored = deleting the "longest lasting"',
                "-> survival time is badly underestimated",
                "-> it also creates selection bias",
                "-> censored data is an asset, not trash",
            ],
            "summary_heading": "Three Takeaways on Censoring",
            "summary_lines": [
                "1. Survival data needs three things: time, event, censored",
                "2. event = 1 for death, 0 for alive - don't flip it",
                "3. Always keep and feed in censored rows",
                "-> not a single patient wasted",
            ],
            "extra_banner_title": "Extra example: a TB treatment cohort",
            "extra_tb_heading": "TB: lost to follow-up = censored",
            "extra_tb_lines": [
                "TB needs 6+ months of drugs, long follow-up",
                "Moving, switching clinics, losing contact is common",
                "Lost != treatment failure, just an unseen ending",
                "-> event = 0, keep the time, waste nothing",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: drawing the Kaplan-Meier curve",
            "outro_sub": "how to actually read that descending staircase",
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_stopwatch(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("stopwatch_heading", "stopwatch_lines", duration)

    def show_event_flag(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("eventflag_heading", "eventflag_lines", duration)

    def show_censor_timeline(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("timeline_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        x0, xend = -4.2, 2.4
        ys = [1.1, 0.1, -0.9]

        obs = DashedLine([xend, 1.55, 0], [xend, -1.35, 0], color=ManimColor(TEXT_SECONDARY))
        obs_label = Text(
            self.t("timeline_obs_end"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(obs, UP, buff=0.1)

        # Patient A: dies at x = 0.0 (event = 1)
        line_a = Line([x0, ys[0], 0], [0.0, ys[0], 0], color=ManimColor(ACCENT_BLUE), stroke_width=5)
        death_dot = Dot([0.0, ys[0], 0], radius=0.14, color=ManimColor(ERROR_RED))
        lab_a = Text(
            self.t("timeline_death"), font=FONT_CJK, font_size=15, color=TEXT_PRIMARY
        ).next_to(death_dot, RIGHT, buff=0.25)

        # Patient B: censored, lasts to observation end (event = 0)
        line_b = Line([x0, ys[1], 0], [xend, ys[1], 0], color=ManimColor(ACCENT_BLUE), stroke_width=5)
        tick_b = Line(
            [xend, ys[1] - 0.18, 0], [xend, ys[1] + 0.18, 0], color=ManimColor(ACCENT_GREEN),
            stroke_width=5,
        )
        lab_b = Text(
            self.t("timeline_censored"), font=FONT_CJK, font_size=15, color=TEXT_PRIMARY
        ).next_to(tick_b, RIGHT, buff=0.25)

        # Patient C: lost to follow-up at x = -1.4 (event = 0)
        line_c = Line([x0, ys[2], 0], [-1.4, ys[2], 0], color=ManimColor(ACCENT_BLUE), stroke_width=5)
        tick_c = Line(
            [-1.4, ys[2] - 0.18, 0], [-1.4, ys[2] + 0.18, 0], color=ManimColor(ACCENT_GREEN),
            stroke_width=5,
        )
        lab_c = Text(
            self.t("timeline_lost"), font=FONT_CJK, font_size=15, color=TEXT_PRIMARY
        ).next_to(tick_c, RIGHT, buff=0.25)

        caption = Text(
            self.t("timeline_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        diagram = VGroup(
            obs, obs_label, line_a, death_dot, lab_a, line_b, tick_b, lab_b, line_c, tick_c, lab_c
        )

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(diagram), run_time=1.1)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(heading, diagram, caption)), run_time=0.5)

    def show_build_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'cases["event"] = (cases["outcome"] == "dead").astype(int)\n'
                'cases["time"] = (end_date - onset_date).dt.days\n'
                'kmf.fit(cases["time"], event_observed=cases["event"])'
            ),
        )
        self._code_block("build_heading", "build_title", code, duration)

    def show_why_not_drop(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_tb(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_tb_heading", "extra_tb_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_zero_time(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'cases.loc[alive, "time"] = 0'),
            kwargs.get("correct_code", 'cases.loc[alive, "time"] = obs_days'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_flag_reversed(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'event = (outcome != "dead").astype(int)'),
            kwargs.get("correct_code", 'event = (outcome == "dead").astype(int)'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_drop_censored(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cases = cases[cases.event == 1]"),
            kwargs.get("correct_code", "kmf.fit(cases.time, cases.event)"),
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
