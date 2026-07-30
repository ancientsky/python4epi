"""Manim scene for Ch01-06: 函式 (Functions)."""

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


class Ch01FunctionsScene(EpiBaseScene):
    """Tutorial video scene: Python functions for epi calculations."""

    total_steps: int = 3

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "函式",
            "title_sub": "把重複的計算包起來，一行搞定",
            "summary_p1": "def 函式名稱(參數): 定義函式",
            "summary_p2": "docstring 說明用途、參數與回傳值",
            "summary_p3": "return 把結果傳回給呼叫者",
            "summary_p4": "一次定義，多次呼叫，減少重複程式碼",
            "outro_title": "小結",
            "outro_sub": "函式是流病學家的計算公式模板，寫一次到處用！",
        },
        "en": {
            "title_main": "Functions",
            "title_sub": "Wrap repeated calculations, done in one line",
            "summary_p1": "def function_name(params): defines a function",
            "summary_p2": "docstring explains purpose, parameters, and return value",
            "summary_p3": "return hands the result back to the caller",
            "summary_p4": "Define once, call many times, cut duplicate code",
            "outro_title": "Recap",
            "outro_sub": "A function is an epidemiologist's formula template — write once, use everywhere!",
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

    def show_define_function(self, duration: float = 6.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "def attack_rate(cases: int, population: int) -> float:\n"
                "    \"\"\"計算侵襲率（%）。\n"
                "\n"
                "    Parameters\n"
                "    ----------\n"
                "    cases      : 病例數\n"
                "    population : 暴露人口數\n"
                "    \"\"\"\n"
                "    if population <= 0:\n"
                "        raise ValueError(\"人口數必須大於 0\")\n"
                "    return cases / population * 100"
            ),
        )
        step = self.show_step_indicator(1)
        panel = self.show_code(code, duration=duration * 0.7)
        self.wait(max(0.1, duration * 0.2))
        self.play(FadeOut(panel), FadeOut(step), run_time=0.5)

    def show_call_function(self, duration: float = 5.0, **kwargs) -> None:
        code = kwargs.get(
            "code",
            (
                "# 呼叫函式：松柏護理之家\n"
                "ar_nursing = attack_rate(cases=121, population=280)\n"
                "print(f\"護理之家侵襲率: {ar_nursing:.1f}%\")  # → 43.2%\n"
                "\n"
                "# 同一個函式，換個場景照樣用\n"
                "ar_staff = attack_rate(cases=8, population=45)\n"
                "print(f\"員工侵襲率: {ar_staff:.1f}%\")        # → 17.8%"
            ),
        )
        step = self.show_step_indicator(2)
        panel = self.show_code(code, duration=duration * 0.55)
        output = self.show_output(
            kwargs.get("output", "護理之家侵襲率: 43.2%\n員工侵襲率: 17.8%"),
            duration=duration * 0.3,
        )
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), FadeOut(step), run_time=0.5)

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        step = self.show_step_indicator(3)
        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_MONO, font_size=26, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=28, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_MONO, font_size=26, color=ACCENT_ORANGE),
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
                "# 結核病發生率（每 10 萬人）\n"
                "def incidence_rate(\n"
                "    new_cases: int,\n"
                "    population: int,\n"
                "    multiplier: int = 100_000,\n"
                ") -> float:\n"
                "    \"\"\"計算發生率（per multiplier 人）。\"\"\"\n"
                "    if population <= 0:\n"
                "        raise ValueError(\"人口數必須大於 0\")\n"
                "    return new_cases / population * multiplier\n"
                "\n"
                "tb_rate = incidence_rate(new_cases=7_000, population=23_000_000)\n"
                "print(f\"台灣結核病發生率：{tb_rate:.1f} / 10 萬人\")"
            ),
        )
        panel = self.show_code(code, duration=duration * 0.65)
        output = self.show_output(
            kwargs.get("output", "台灣結核病發生率：30.4 / 10 萬人"),
            duration=duration * 0.2,
        )
        self.wait(max(0.1, duration * 0.1))
        self.play(FadeOut(panel), FadeOut(output), run_time=0.5)

    # ------------------------------------------------------------------
    # Part 3 – Beginner blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner())
        self.wait(max(0.1, duration - 0.5))

    def show_blindspot_no_parens(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "result = attack_rate   # ❌ 忘記括號\n"
            "print(result)         # 印出函式物件，不是數值！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "result = attack_rate(121, 280)  # ✅ 加上括號才是呼叫\n"
            "print(result)                   # → 43.214...",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_return(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "def attack_rate(cases, population):\n"
            "    result = cases / population * 100  # ❌ 沒有 return\n"
            "\n"
            "ar = attack_rate(121, 280)\n"
            "print(ar)  # → None  ← 拿到空的！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "def attack_rate(cases, population):\n"
            "    result = cases / population * 100\n"
            "    return result  # ✅ 記得回傳\n"
            "\n"
            "ar = attack_rate(121, 280)\n"
            "print(ar)  # → 43.21...",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_wrong_order(self, duration: float = 4.0, **kwargs) -> None:
        error_code = kwargs.get(
            "error_code",
            "# 函式定義：attack_rate(cases, population)\n"
            "ar = attack_rate(280, 121)  # ❌ 順序搞反了！\n"
            "print(f\"{ar:.1f}%\")        # → 231.4%  ← 荒謬的數字",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# 用關鍵字引數，順序不再是問題\n"
            "ar = attack_rate(cases=121, population=280)  # ✅\n"
            "print(f\"{ar:.1f}%\")  # → 43.2%",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(
            self.t("outro_title"),
            self.t("outro_sub"),
            duration=duration,
        )
