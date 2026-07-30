"""Ch01-03: 字典 — 把資料打包成一張資料卡

Manim scene for the tutorial video on Python dictionaries, using the
Legionella outbreak investigation as the teaching narrative.
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
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    CodePanel,
    ExtraExampleBanner,
    VariableBox,
)


class Ch01DictionariesScene(EpiBaseScene):
    """Tutorial video scene: Python dictionaries for epi data cards."""

    total_steps: int = 11

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "字典",
            "title_sub": "把資料打包成一張資料卡",
            "create_dict_explanation": "字典 = 一張有欄位的資料卡，每個欄位有名稱（鍵）和內容（值）",
            "access_dict_formula": "字典名稱['鍵']  →  取出對應的值",
            "summary_heading": "重點整理",
            "summary_p1": "1. 字典用 {} 建立，鍵值對用 : 分隔",
            "summary_p2": "2. 鍵（key）通常是字串，要加引號",
            "summary_p3": "3. 用 dict['key'] 存取，方括號不能換成圓括號",
            "summary_p4": "4. 一個字典 = 一筆資料卡，適合儲存個案資料",
            "extra_banner_title": "額外範例：腸病毒個案資料卡",
            "blindspot_banner_title": "初學者常見地雷 3 選 1",
            "outro_heading": "下一集：用串列儲存多位個案",
            "outro_sub": "把字典放進串列，就是迷你資料庫！",
        },
        "en": {
            "title_main": "Dictionaries",
            "title_sub": "Pack data into a single data card",
            "create_dict_explanation": "A dict = a data card with fields; each field has a name (key) and content (value)",
            "access_dict_formula": "dict_name['key']  →  fetch the matching value",
            "summary_heading": "Key Takeaways",
            "summary_p1": "1. Build a dict with {}, separate key-value pairs with :",
            "summary_p2": "2. Keys are usually strings, so add quotes",
            "summary_p3": "3. Access with dict['key']; square brackets, not parentheses",
            "summary_p4": "4. One dict = one data card, great for storing a case",
            "extra_banner_title": "Extra example: enterovirus case card",
            "blindspot_banner_title": "3 Common Beginner Traps",
            "outro_heading": "Next up: store many cases with lists",
            "outro_sub": "Put dicts in a list and you've got a mini database!",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Main lesson methods
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the dictionaries lesson."""
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_create_dict(self, duration: float = 7.0, **kwargs) -> None:
        """Show dictionary creation with the labeled-box metaphor."""
        self.show_step_indicator(1, self.total_steps)

        explanation = Text(
            self.t("create_dict_explanation"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_PRIMARY,
        ).to_edge(UP, buff=0.8)

        code_lines = (
            "# 把一位個案的資料打包成字典\n"
            "case_001 = {\n"
            "    'case_id':   'C001',\n"
            "    'age':       82,\n"
            "    'floor':     3,\n"
            "    'infected':  True,\n"
            "    'outcome':   'survived',\n"
            "}"
        )

        code_panel = CodePanel(
            code_lines,
            title="create_dict.py",
            width=6.8,
            height=4.0,
        ).shift(LEFT * 1.0 + DOWN * 0.3)

        key_boxes = VGroup(
            VariableBox("case_id", "'C001'", label_color=ACCENT_ORANGE),
            VariableBox("age", "82", label_color=ACCENT_ORANGE),
            VariableBox("floor", "3", label_color=ACCENT_ORANGE),
            VariableBox("outcome", "'survived'", label_color=ACCENT_ORANGE),
        ).arrange(DOWN, buff=0.25).shift(RIGHT * 3.2 + DOWN * 0.3)

        self.play(FadeIn(explanation), run_time=0.5)
        self.play(Create(code_panel), run_time=1.0)
        self.play(FadeIn(key_boxes, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 2.5))
        self.play(FadeOut(VGroup(explanation, code_panel, key_boxes)), run_time=0.5)

    def show_access_dict(self, duration: float = 7.0, **kwargs) -> None:
        """Show bracket access and using dict values in calculations."""
        self.show_step_indicator(2, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "case_001 = {\n"
                "    'case_id':   'C001',\n"
                "    'age':       82,\n"
                "    'infected':  True,\n"
                "}\n"
                "\n"
                "# 用方括號 [] 取出值\n"
                "print(case_001['case_id'])   # 'C001'\n"
                "print(case_001['age'])       # 82\n"
                "\n"
                "# 也可以拿來計算\n"
                "if case_001['infected']:\n"
                "    print('此個案為確診')"
            ),
        )

        output_text = kwargs.get(
            "output",
            "C001\n82\n此個案為確診",
        )

        formula = Text(
            self.t("access_dict_formula"),
            font=FONT_CJK,
            font_size=24,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.7)

        self.play(FadeIn(formula), run_time=0.5)
        self.show_code(code_lines, title="access_dict.py")
        self.wait(1.0)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.5))
        self.clear_screen()

    def show_main_summary(self, duration: float = 4.0, **kwargs) -> None:
        """Summarise key points about dictionaries."""
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("summary_heading"),
            font=FONT_CJK,
            font_size=34,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        points = VGroup(
            Text(self.t("summary_p1"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p2"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p3"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
            Text(self.t("summary_p4"), font=FONT_CJK, font_size=23, color=TEXT_PRIMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(points, lag_ratio=0.25), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, points)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example methods
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner(self.t("extra_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_extra_example(self, duration: float = 7.0, **kwargs) -> None:
        """Enterovirus case card example demonstrating the same dict pattern."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# 腸病毒 71 型個案資料卡\n"
                "ev71_case = {\n"
                "    'case_id':    'EV2026-0042',\n"
                "    'age_months': 18,\n"
                "    'symptom':    'hand_foot_mouth',\n"
                "    'severe':     False,\n"
                "    'county':     '台南市',\n"
                "}\n"
                "\n"
                "print(ev71_case['case_id'])      # EV2026-0042\n"
                "print(ev71_case['county'])       # 台南市\n"
                "print(ev71_case['age_months'])   # 18"
            ),
        )

        output_text = kwargs.get(
            "output",
            "EV2026-0042\n台南市\n18",
        )

        self.show_code(code_lines, title="ev71_case_card.py")
        self.wait(1.2)
        self.show_output(output_text)
        self.wait(max(0.1, duration - 1.2))
        self.clear_screen()

    # ------------------------------------------------------------------
    # Blind-spot methods
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner(self.t("blindspot_banner_title"))
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_key_quotes(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: missing quotes on string keys."""
        error_code = kwargs.get(
            "error_code",
            "case = {case_id: 'C001'}   # NameError：沒有加引號",
        )
        correct_code = kwargs.get(
            "correct_code",
            "case = {'case_id': 'C001'} # 鍵是字串，要加引號",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_bracket_type(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: parentheses () instead of square brackets [] for access."""
        error_code = kwargs.get(
            "error_code",
            "print(case_001('age'))   # TypeError：() 是呼叫函式！",
        )
        correct_code = kwargs.get(
            "correct_code",
            "print(case_001['age'])   # [] 才是取值的語法",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_key_error(self, duration: float = 5.0, **kwargs) -> None:
        """Error vs correct: accessing a non-existent key raises KeyError."""
        error_code = kwargs.get(
            "error_code",
            "# case_001 沒有 'weight' 這個鍵\n"
            "print(case_001['weight'])  # KeyError!",
        )
        correct_code = kwargs.get(
            "correct_code",
            "# 用 .get() 安全取值，找不到回傳 None\n"
            "print(case_001.get('weight'))  # None",
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        """Closing card."""
        self.show_step_indicator(self.total_steps, self.total_steps)

        heading = Text(
            self.t("outro_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            self.t("outro_sub"),
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
