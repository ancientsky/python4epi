"""Ch09-01: Survival analysis intuition - the phone-battery race metaphor.

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
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch09SurvivalIntuitionScene(EpiBaseScene):
    """Tutorial video scene: survival-analysis intuition via a phone-battery race."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "存活分析超白話",
            "title_sub": "用「手機電池大賽」看懂 time-to-event",
            "battery_heading": "一場手機電池大賽",
            "battery_lines": [
                "全班每人一支充飽電的手機來比賽",
                "比的是「誰撐最久才關機」",
                "重點不是會不會關機（遲早都會）",
                "→ 而是「撐了多久」才關機",
            ],
            "time_heading": "存活時間 = 撐多久",
            "time_lines": [
                "關機（電量歸零）＝ 我們在等的「事件」",
                "醫院裡：死亡 / 出院 / 復發",
                "從充飽到關機的時數 ＝ 存活時間",
                "→ 每人一個碼表：發病 start、死亡 stop",
            ],
            "censor_heading": "下課了，手機還開著",
            "censor_lines": [
                "寫 0 小時？不對，它撐很久",
                "寫壞掉沒資料？也不對，它好得很",
                "正解：至少撐了 12 小時，結局沒看到",
                "→ 這種一半的故事，叫「設限 censored」",
            ],
            "staircase_heading": "KM 曲線：一條會下樓梯的線",
            "staircase_y": "還開著的比例 ↑",
            "staircase_x": "時間 →",
            "staircase_steep": "陡 = 很快關機（存活差）",
            "staircase_flat": "平 = 很耐用（存活好）",
            "staircase_median": "穿過 50% = 中位存活時間",
            "code_heading": "程式超短：只餵兩欄",
            "code_title": "battery_km.py",
            "summary_heading": "三個核心概念打包",
            "summary_lines": [
                "① 看「多久之後發生」，不只「有沒有」",
                "② 設限 ≠ 關機、≠ 壞掉，是一半的故事",
                "③ KM 曲線 = 下樓梯，越陡越糟",
                "→ 設限也算得進去，一支都不浪費",
            ],
            "extra_banner_title": "額外範例：新冠加護病房病人",
            "extra_covid_heading": "手機 → 加護病房病人",
            "extra_covid_lines": [
                "新冠重症插管，想知道「撐多久」",
                "死亡 ＝ 關機（event=1）",
                "拔管出院 ＝ 設限（event=0）",
                "→ 同一台 KaplanMeierFitter，換病照用",
            ],
            "blindspot_banner_title": "存活分析入門三個新手地雷",
            "outro_heading": "下一集：設限資料的正式版",
            "outro_sub": "event 旗標怎麼填、為什麼不能丟",
        },
        "en": {
            "title_main": "Survival Analysis, Plain and Simple",
            "title_sub": 'Understanding time-to-event via a "phone battery race"',
            "battery_heading": "A Phone Battery Race",
            "battery_lines": [
                "Everyone brings a fully-charged phone to race",
                'The contest: "whose phone lasts longest before dying"',
                "The point isn't whether it dies (all do eventually)",
                "-> it's HOW LONG it lasted before dying",
            ],
            "time_heading": "Survival Time = How Long It Lasted",
            "time_lines": [
                'Powering off (0%) = the "event" we wait for',
                "In hospitals: death / discharge / relapse",
                "Hours from full charge to off = survival time",
                "-> a stopwatch each: onset start, death stop",
            ],
            "censor_heading": "Class Ends, the Phone Is Still On",
            "censor_lines": [
                "Write 0 hours? No, it lasted a long time",
                "Write broken / no data? No, it's perfectly fine",
                "Right: lasted at least 12h, ending unseen",
                '-> this half-a-story is called "censored"',
            ],
            "staircase_heading": "The KM Curve: a Descending Staircase",
            "staircase_y": "fraction still on up",
            "staircase_x": "time ->",
            "staircase_steep": "steep = dies fast (poor survival)",
            "staircase_flat": "flat = long-lasting (good survival)",
            "staircase_median": "crossing 50% = median survival time",
            "code_heading": "The Code Is Tiny: Just Two Columns",
            "code_title": "battery_km.py",
            "summary_heading": "Three Core Ideas",
            "summary_lines": [
                '1. "How long until", not just "whether"',
                "2. Censored is not off, not broken - half a story",
                "3. KM curve = staircase, steeper is worse",
                "-> censored rows still count, none wasted",
            ],
            "extra_banner_title": "Extra example: COVID-19 ICU patients",
            "extra_covid_heading": "Phone -> ICU patient",
            "extra_covid_lines": [
                "Severe COVID on a ventilator: how long?",
                "Death = powering off (event=1)",
                "Extubated & discharged = censored (event=0)",
                "-> same KaplanMeierFitter, new disease",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: censored data, the formal version",
            "outro_sub": "how to code the event flag, why you can't drop it",
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

    def _staircase(self, drops: list[float], color: str) -> VGroup:
        """Descending step function drawn with Line segments.

        ``drops`` are fractional x positions (0..1) where the curve steps down.
        """
        x0, x1, y_top, y_bot = -3.0, 3.0, 1.4, -1.4
        n = len(drops)
        step = (y_top - y_bot) / n
        segs = VGroup()
        x, y = x0, y_top
        for f in drops:
            px = x0 + f * (x1 - x0)
            segs.add(Line([x, y, 0], [px, y, 0], color=ManimColor(color), stroke_width=5))
            segs.add(Line([px, y, 0], [px, y - step, 0], color=ManimColor(color), stroke_width=5))
            x, y = px, y - step
        segs.add(Line([x, y, 0], [x1, y, 0], color=ManimColor(color), stroke_width=5))
        return segs

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_battery_race(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("battery_heading", "battery_lines", duration)

    def show_time_to_event(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("time_heading", "time_lines", duration)

    def show_censoring_intuition(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("censor_heading", "censor_lines", duration)

    def show_km_staircase(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("staircase_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        x_axis = Line([-3.2, -1.6, 0], [3.2, -1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        y_axis = Line([-3.2, -1.6, 0], [-3.2, 1.6, 0], color=ManimColor(BORDER_LIGHT), stroke_width=3)
        stairs = self._staircase([0.15, 0.28, 0.42, 0.6, 0.78], ACCENT_ORANGE)

        median_line = DashedLine([-3.2, 0, 0], [3.2, 0, 0], color=ManimColor(TEXT_SECONDARY))
        median_label = Text(
            self.t("staircase_median"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).next_to(median_line, RIGHT, buff=0.1).shift(UP * 0.25 + LEFT * 2.2)

        y_label = Text(
            self.t("staircase_y"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(y_axis, UP, buff=0.15)
        x_label = Text(
            self.t("staircase_x"), font=FONT_CJK, font_size=15, color=TEXT_SECONDARY
        ).next_to(x_axis, RIGHT, buff=0.1)

        steep = Text(
            self.t("staircase_steep"), font=FONT_CJK, font_size=16, color=ERROR_RED
        ).to_edge(DOWN, buff=0.7).shift(LEFT * 2.6)
        flat = Text(
            self.t("staircase_flat"), font=FONT_CJK, font_size=16, color=ACCENT_GREEN
        ).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.6)

        axes = VGroup(x_axis, y_axis, y_label, x_label)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(axes), run_time=0.5)
        self.play(FadeIn(stairs), run_time=1.0)
        self.play(FadeIn(median_line), FadeIn(median_label), run_time=0.4)
        self.play(FadeIn(steep), FadeIn(flat), run_time=0.5)
        self.wait(max(0.1, duration - 3.3))
        self.play(
            FadeOut(VGroup(heading, axes, stairs, median_line, median_label, steep, flat)),
            run_time=0.5,
        )

    def show_battery_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from lifelines import KaplanMeierFitter\n"
                "\n"
                "kmf = KaplanMeierFitter()\n"
                'kmf.fit(phones["hours"], event_observed=phones["died"], label="battery")\n'
                "kmf.plot_survival_function()\n"
                "print(kmf.median_survival_time_)  # half the phones are off by here"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_covid(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_covid_heading", "extra_covid_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_drop_censored(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "deaths = cases[cases.event == 1]  # dropped survivors"),
            kwargs.get("correct_code", "kmf.fit(cases.time, event_observed=cases.event)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_yaxis(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pct_dead = kmf.survival_function_  # this is survival"),
            kwargs.get("correct_code", "pct_dead = 1 - kmf.survival_function_"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_median(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "everyone_dead_by = kmf.median_survival_time_"),
            kwargs.get("correct_code", "half_still_alive_at = kmf.median_survival_time_"),
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
