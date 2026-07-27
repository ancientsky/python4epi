"""Manim scene for Ch01-04: 列表 (Lists)."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
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
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch01ListsScene(EpiBaseScene):
    """Tutorial video scene: Python lists for epi data."""

    total_steps: int = 3

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "列表",
            "title_sub": "存放一組同類資料的好幫手",
            "summary_p1": "列表用方括號 [] 建立",
            "summary_p2": "索引從 0 開始，不是 1",
            "summary_p3": "max() / min() / .index() 快速分析",
            "summary_p4": "平行列表：相同索引代表同一個對象",
            "outro_title": "小結",
            "outro_sub": "列表讓你一次管理多筆資料，記住索引從 0 開始！",
        },
        "en": {
            "title_main": "Lists",
            "title_sub": "Your go-to for a group of similar data",
            "summary_p1": "Build a list with square brackets []",
            "summary_p2": "Indexing starts at 0, not 1",
            "summary_p3": "max() / min() / .index() for quick analysis",
            "summary_p4": "Parallel lists: the same index means the same subject",
            "outro_title": "Recap",
            "outro_sub": "Lists let you manage many records at once — remember, indexing starts at 0!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Part 1 – Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(
            self.t("title_main"),
            self.t("title_sub"),
            duration=duration,
        )

    def show_create_lists(self, duration: float = 5.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# 松柏護理之家各翼住房的病例數\n"
                "floor_wing_cases = [15, 10, 24, 25, 20, 27]\n"
                "floor_wing_names = [\"1A\", \"1B\", \"2A\", \"2B\", \"3A\", \"3B\"]\n"
                "\n"
                "# 取得第一個元素（索引從 0 開始）\n"
                "print(floor_wing_names[0])  # → '1A'\n"
                "print(floor_wing_cases[0])  # → 15"
            ),
        )
        step = self.show_step_indicator(1)
        panel = self.show_code(code, duration=duration * 0.55)
        output = self.show_output("'1A'\n15", duration=duration * 0.3)
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), FadeOut(step), run_time=0.5)

    def show_find_max(self, duration: float = 5.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# 找出病例數最多的翼別\n"
                "max_cases = max(floor_wing_cases)          # → 27\n"
                "max_idx   = floor_wing_cases.index(max_cases)  # → 5\n"
                "worst_wing = floor_wing_names[max_idx]     # → '3B'\n"
                "\n"
                "print(f\"感染最嚴重的翼: {worst_wing}，病例數: {max_cases}\")"
            ),
        )
        step = self.show_step_indicator(2)
        panel = self.show_code(code, duration=duration * 0.55)
        output = self.show_output("感染最嚴重的翼: 3B，病例數: 27", duration=duration * 0.3)
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), FadeOut(step), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        step = self.show_step_indicator(3)
        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE),
            Text(self.t("summary_p3"), font=FONT_MONO, font_size=26, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        points.move_to([0, 0, 0])
        self.play(FadeIn(points), run_time=0.6)
        self.wait(max(0.5, duration - 0.6))
        self.play(FadeOut(points), FadeOut(step), run_time=0.5)

    # ------------------------------------------------------------------
    # Part 2 – Extra epi example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner())
        self.wait(max(0.1, duration - 0.5))

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# COVID-19 各週新增病例（某縣市）\n"
                "weeks      = [1,  2,  3,  4,  5,  6,  7]\n"
                "new_cases  = [12, 34, 89, 210, 178, 95, 41]\n"
                "\n"
                "peak_week_idx = new_cases.index(max(new_cases))  # → 3\n"
                "peak_week     = weeks[peak_week_idx]             # → 4\n"
                "\n"
                "print(f\"疫情高峰在第 {peak_week} 週，病例數 {max(new_cases)} 例\")"
            ),
        )
        panel = self.show_code(code, duration=duration * 0.6)
        output = self.show_output("疫情高峰在第 4 週，病例數 210 例", duration=duration * 0.25)
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), run_time=0.5)

    # ------------------------------------------------------------------
    # Part 3 – Beginner blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner())
        self.wait(max(0.1, duration - 0.5))

    def show_blindspot_zero_index(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "names = [\"1A\", \"1B\", \"2A\"]\nfirst = names[1]  # ❌ 以為 1 是第一個",
        )
        correct_code = kwargs.get(
            "correct_code",
            "names = [\"1A\", \"1B\", \"2A\"]\nfirst = names[0]  # ✅ 索引從 0 開始",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_index_error(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "cases = [15, 10, 24]\ncases[3]  # ❌ IndexError: list index out of range",
        )
        correct_code = kwargs.get(
            "correct_code",
            "cases = [15, 10, 24]\nprint(len(cases))  # → 3\ncases[2]  # ✅ 最後一個索引是 len-1",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_misaligned(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "names = [\"1A\", \"1B\", \"2A\", \"2B\"]  # 4 個\n"
            "cases = [15, 10, 24]              # 3 個 ❌\n"
            "# names[3] 對應的 cases[3] 根本不存在！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "names = [\"1A\", \"1B\", \"2A\", \"2B\"]  # 4 個\n"
            "cases = [15, 10, 24, 25]          # 4 個 ✅\n"
            "# 長度一致，平行關係才正確",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(
            self.t("outro_title"),
            self.t("outro_sub"),
            duration=duration,
        )
