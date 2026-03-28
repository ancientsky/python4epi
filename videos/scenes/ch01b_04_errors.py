"""Ch01b-04: 讀懂錯誤訊息——traceback 不是天書

Manim scene for the tutorial video on reading Python error messages,
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
)


class Ch01bErrorsScene(EpiBaseScene):
    """Tutorial video scene: reading Python error messages."""

    total_steps: int = 15

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card("讀懂錯誤訊息", "traceback 不是天書", duration=duration)

    def show_traceback_anatomy(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Traceback 怎麼看？從最後一行開始！",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        lines = VGroup(
            Text('Traceback (most recent call last):', font=FONT_MONO, font_size=18, color=TEXT_SECONDARY),
            Text('  File "analyze.py", line 3, in <module>', font=FONT_MONO, font_size=18, color=TEXT_SECONDARY),
            Text('    print(infceted)', font=FONT_MONO, font_size=18, color=TEXT_SECONDARY),
            Text("NameError: name 'infceted' is not defined", font=FONT_MONO, font_size=18, color="#D94452"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(heading, DOWN, buff=0.6)

        arrow = Text("^ 從這裡開始看！", font=FONT_CJK, font_size=20, color=ACCENT_ORANGE).next_to(lines[-1], DOWN, buff=0.3)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(lines, lag_ratio=0.2), run_time=1.2)
        self.play(FadeIn(arrow), run_time=0.5)
        self.wait(duration - 2.1)
        self.play(FadeOut(VGroup(heading, lines, arrow)), run_time=0.5)

    def show_name_error(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code_text = kwargs.get("code", "infected = 121\nprint(infceted)")
        output_text = kwargs.get("output", "NameError: name 'infceted' is not defined")
        code_panel = self.show_code(code_text, title="name_error.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_type_error(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code_text = kwargs.get("code", 'cases = "121"\nrate = cases / 280')
        output_text = kwargs.get("output", "TypeError: unsupported operand type(s)")
        code_panel = self.show_code(code_text, title="type_error.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_key_error(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code_text = kwargs.get("code", 'data = {"deaths": 19, "cases": 121}\nprint(data["death"])')
        output_text = kwargs.get("output", "KeyError: 'death'")
        code_panel = self.show_code(code_text, title="key_error.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_index_error(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code_text = kwargs.get("code", 'wings = ["1A","1B","2A","2B","3A","3B"]\nprint(wings[6])')
        output_text = kwargs.get("output", "IndexError: list index out of range")
        code_panel = self.show_code(code_text, title="index_error.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_file_error(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code_text = kwargs.get("code", "open('data/outbreak.csv')")
        output_text = kwargs.get("output", "FileNotFoundError: [Errno 2]")
        code_panel = self.show_code(code_text, title="file_error.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        heading = Text("五大常見錯誤", font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text("1. NameError — 打錯變數名稱", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("2. TypeError — 型別不對", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("3. KeyError — 字典找不到 key", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("4. IndexError — 列表超出範圍", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text("5. FileNotFoundError — 檔案路徑錯誤", font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner("額外範例：批次讀取通報檔案")
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        code_text = kwargs.get("code", 'files = ["taipei.csv", "tainan.csv"]\nfor f in files:\n    print(f"reading {f}")')
        code_panel = self.show_code(code_text, title="batch_read.py")
        self.wait(duration)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_read_wrong(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# only reads first line")
        correct_code = kwargs.get("correct_code", "# read LAST line first!")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_copy_paste(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# copy 50 lines to ChatGPT")
        correct_code = kwargs.get("correct_code", "# search: NameError + message")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_warning_vs_error(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "# Warning: panic!")
        correct_code = kwargs.get("correct_code", "# Warning: just a heads-up")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            "下一集：try/except 優雅處理意外",
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text("讓程式碰到壞資料也不會崩潰！", font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
