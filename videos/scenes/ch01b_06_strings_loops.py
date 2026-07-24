"""Ch01b-06: 字串與迴圈進階——清理疫調資料的瑞士刀

Manim scene for the tutorial video on string methods and advanced loops,
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


class Ch01bStringsLoopsScene(EpiBaseScene):
    """Tutorial video scene: string methods and advanced loop patterns."""

    total_steps: int = 15

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "字串與迴圈進階",
            "title_sub": "清理疫調資料的瑞士刀",
            "summary_heading": "重點整理",
            "summary_p1": "1. strip() 去空白、split() 切分",
            "summary_p2": "2. replace() 取代字串內容",
            "summary_p3": "3. for + range() 跑固定次數",
            "summary_p4": "4. enumerate() 同時拿索引和值",
            "summary_p5": "5. in 檢查成員是否存在",
            "extra_banner_title": "額外範例：清理 TB 通報檢驗結果",
            "blindspot_banner_title": "初學者常見地雷 3 選",
            "outro_heading": "下一集：uv 進階用法",
            "outro_sub": "管理 Python 版本和套件！",
        },
        "en": {
            "title_main": "Strings and Advanced Loops",
            "title_sub": "The Swiss army knife for cleaning outbreak data",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. strip() trims spaces, split() splits apart",
            "summary_p2": "2. replace() swaps content inside a string",
            "summary_p3": "3. for + range() runs a fixed number of times",
            "summary_p4": "4. enumerate() grabs index and value together",
            "summary_p5": "5. in checks whether a member exists",
            "extra_banner_title": "Extra example: cleaning TB lab-result fields",
            "blindspot_banner_title": "3 Common Beginner Pitfalls",
            "outro_heading": "Next up: advanced uv usage",
            "outro_sub": "Manage Python versions and packages!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_strip(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        code_text = kwargs.get("code", 'raw = "  Legionella  "\nclean = raw.strip()\nprint(f"[{clean}]")')
        output_text = kwargs.get("output", "[Legionella]")
        code_panel = self.show_code(code_text, title="strip.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_split(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code_text = kwargs.get("code", 'symptoms = "fever,cough,dyspnea"\nparts = symptoms.split(",")\nprint(parts)')
        output_text = kwargs.get("output", "['fever', 'cough', 'dyspnea']")
        code_panel = self.show_code(code_text, title="split.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_replace(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code_text = kwargs.get("code", 'status = "confirmed_YES"\nclean = status.replace("YES", "True")\nprint(clean)')
        output_text = kwargs.get("output", "confirmed_True")
        code_panel = self.show_code(code_text, title="replace.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_for_range(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code_text = kwargs.get("code", 'for i in range(5):\n    print(f"processing wing {i}")')
        output_text = kwargs.get("output", "processing wing 0\nprocessing wing 1\n...")
        code_panel = self.show_code(code_text, title="for_range.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_enumerate(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code_text = kwargs.get("code", 'wings = ["1A", "1B", "2A", "2B"]\nfor i, wing in enumerate(wings):\n    print(f"#{i}: {wing}")')
        output_text = kwargs.get("output", "#0: 1A\n#1: 1B\n#2: 2A\n#3: 2B")
        code_panel = self.show_code(code_text, title="enumerate.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_in_operator(self, duration: float = 5.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code_text = kwargs.get("code", 'pathogens = ["Legionella", "TB", "Dengue"]\nprint("Legionella" in pathogens)\nprint("COVID" in pathogens)')
        output_text = kwargs.get("output", "True\nFalse")
        code_panel = self.show_code(code_text, title="in_check.py")
        self.wait(0.8)
        output_panel = self.show_output(output_text)
        self.wait(duration - 0.8)
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        heading = Text(self.t("summary_heading"), font=FONT_CJK, font_size=34, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
            Text(self.t("summary_p5"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(heading, DOWN, buff=0.5)
        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.2), run_time=1.2)
        self.wait(duration - 1.7)
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        code_text = kwargs.get("code",
            'results = [" Positive", "negative ", "POSITIVE"]\nfor r in results:\n'
            '    clean = r.strip().lower()\n    is_pos = clean == "positive"\n'
            '    print(f"{clean}: {is_pos}")')
        output_text = kwargs.get("output", "positive: True\nnegative: False\npositive: True")
        code_panel = self.show_code(code_text, title="tb_clean.py")
        self.wait(1.0)
        output_panel = self.show_output(output_text)
        self.wait(duration - 1.0)
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_strip_inplace(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", 'name = " John "\nname.strip()\nprint(name)  # " John "')
        correct_code = kwargs.get("correct_code", 'name = " John "\nname = name.strip()\nprint(name)')
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_modify_list(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "for x in items:\n    items.remove(x)  # bug!")
        correct_code = kwargs.get("correct_code", "keep = [x for x in items if ok(x)]")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_range_off(self, duration: float = 5.0, **kwargs) -> None:
        error_code = kwargs.get("error_code", "range(5)  # 0,1,2,3,4 not 5!")
        correct_code = kwargs.get("correct_code", "range(1, 6)  # 1,2,3,4,5")
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK, font_size=28, color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)
        sub = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(duration - 1.1)
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
