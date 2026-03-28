"""Ch01b-03: 型別與轉換——數字、文字、布林值

Manim scene for the tutorial video on Python types and type conversion,
using the Legionella outbreak investigation as the teaching narrative.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
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
    CodePanel,
    ExtraExampleBanner,
    OutputPanel,
    StepIndicator,
    VariableBox,
)


class Ch01bTypesScene(EpiBaseScene):
    """Tutorial video scene: Python types and type conversion."""

    total_steps: int = 14

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("型別與轉換", "數字、文字、布林值", duration=duration)

    def show_type_function(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        code_text = kwargs.get("code",
            'print(type(121))\nprint(type(43.2))\nprint(type("Legionella"))\nprint(type(True))')
        output_text = kwargs.get("output",
            "<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>")
        code_panel = self.show_code(code_text, title="type_check.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_conversion(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)

        heading = Text(
            "型別轉換：幫資料換身分證",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        code_text = kwargs.get("code", 'raw = "121"\ncases = int(raw)\nprint(cases + 1)')
        code_panel = CodePanel(code_text, title="convert.py", width=7.0, height=2.4).next_to(heading, DOWN, buff=0.5)

        box_str = VariableBox(label="raw", value='"121"', width=2.5, height=1.2).shift(LEFT * 3 + DOWN * 1.8)
        box_int = VariableBox(label="cases", value="121", width=2.5, height=1.2).shift(RIGHT * 3 + DOWN * 1.8)
        arrow_label = Text("int()", font=FONT_MONO, font_size=22, color=ACCENT_ORANGE).move_to(DOWN * 1.8)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(Create(code_panel), run_time=0.6)
        self.play(FadeIn(box_str), run_time=0.4)
        self.play(FadeIn(arrow_label), run_time=0.3)
        self.play(FadeIn(box_int), run_time=0.4)
        self.wait(duration - 2.1)
        self.play(FadeOut(VGroup(heading, code_panel, box_str, box_int, arrow_label)), run_time=0.5)

    def show_boolean(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code_text = kwargs.get("code", "infected = 121\nprint(infected > 100)\nprint(infected == 0)")
        output_text = kwargs.get("output", "True\nFalse")
        code_panel = self.show_code(code_text, title="boolean.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_logical_ops(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code_text = kwargs.get("code",
            "age = 85\nhas_copd = True\nhigh_risk = age > 80 and has_copd\n"
            'print(f"high risk: {high_risk}")')
        output_text = kwargs.get("output", "high risk: True")
        code_panel = self.show_code(code_text, title="logical.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        heading = Text("重點整理", font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text("1. type() 查型別身分證", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("2. int, float, str, bool 四大型別", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("3. int(), float(), str() 做轉換", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
            Text("4. and, or, not 組合布林條件", font=FONT_CJK, font_size=24, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner("額外範例：清理腸病毒通報年齡欄位")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code_text = kwargs.get("code",
            'raw_ages = ["3", "5", "2", "4", "6"]\nages = []\n'
            "for a in raw_ages:\n    ages.append(int(a))\n"
            'avg = sum(ages) / len(ages)\nprint(f"mean age: {avg}")')
        output_text = kwargs.get("output", "mean age: 4.0")
        code_panel = self.show_code(code_text, title="enterovirus_ages.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_str_add(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", 'print("121" + "19")  # "12119"')
        correct_code = kwargs.get("correct_code", "print(int('121') + int('19'))  # 140")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_bool_str(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", 'flag = "False"\nif flag: print("oops")')
        correct_code = kwargs.get("correct_code", "flag = False\nif flag: print('yes')")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_invalid_int(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", 'int("N/A")  # ValueError!')
        correct_code = kwargs.get("correct_code", 'val = "N/A"\nif val.isdigit(): int(val)')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            "下一集：讀懂錯誤訊息",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text("再也不怕紅色大字了！", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
