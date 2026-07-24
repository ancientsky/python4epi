"""Ch13-06: The schema contract - catch data changes before they corrupt results.

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
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    BG_CARD_ALT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch13SchemaScene(EpiBaseScene):
    """Tutorial video scene: a schema contract as a gate that stops bad data."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "schema 契約",
            "title_sub": "搶在資料改動之前擋下來",
            "risk_heading": "最可怕的是不報錯的錯",
            "risk_lines": [
                "可重現也要保證「以後的資料結構一樣」",
                "欄位被改名、值域跑掉，分析照樣跑完",
                "→ 不報錯，只是每個數字都悄悄錯了",
                "這種錯最難抓，它不會舉手說「我壞了」",
            ],
            "schema_code_heading": "用 assert 寫下三個假設",
            "schema_code_title": "schema_check.py",
            "schema_output_heading": "資料正常 vs 資料變動",
            "schema_output_text": (
                "[OK] schema pass: cols, dtype, range\n"
                "rename a column ->\n"
                "AssertionError: stops the run early"
            ),
            "gate_heading": "把 schema 想成一道閘門",
            "gate_raw": "原始資料\nraw CSV",
            "gate_check": "schema 契約\nassert 檢查",
            "gate_ok": "綠燈通過\n→ 進入 Step 2 摘要",
            "gate_ng": "紅燈攔下\nAssertionError 中斷",
            "summary_heading": "schema 契約三重點",
            "summary_lines": [
                "① 最危險的是不報錯的錯，契約專抓這種",
                "② assert 三假設：欄位、型別、值域",
                "③ 對「原始資料」驗證，趕在轉換之前把關",
                "→ 正式專案可用 pandera 自動化",
            ],
            "extra_banner_title": "額外範例：守住被改名欄位的監測管線",
            "extra_surv_heading": "county 被改名成 city 就報錯",
            "extra_surv_title": "surveillance_guard.py",
            "blindspot_banner_title": "schema 契約三個新手地雷",
            "outro_heading": "四道防線到齊：環境 / 摘要 / 種子 / 契約",
            "outro_sub": "下一章：整合成完整實戰案例 SitRep",
        },
        "en": {
            "title_main": "The Schema Contract",
            "title_sub": "Catch data changes before they corrupt results",
            "risk_heading": "The scariest bug throws no error",
            "risk_lines": [
                'Reproducible also means "same data shape later"',
                "A renamed column or bad range still runs fine",
                "-> no error, but every number is quietly wrong",
                "The hardest bug: it never says \"I'm broken\"",
            ],
            "schema_code_heading": "Write three assumptions as asserts",
            "schema_code_title": "schema_check.py",
            "schema_output_heading": "Data valid vs data changed",
            "schema_output_text": (
                "[OK] schema pass: cols, dtype, range\n"
                "rename a column ->\n"
                "AssertionError: stops the run early"
            ),
            "gate_heading": "Think of the schema as a gate",
            "gate_raw": "raw data\nraw CSV",
            "gate_check": "schema contract\nassert checks",
            "gate_ok": "green: pass\n-> into Step 2 summary",
            "gate_ng": "red: blocked\nAssertionError stops it",
            "summary_heading": "Three Takeaways",
            "summary_lines": [
                "1. Silent bugs are worst; the contract catches them",
                "2. assert three things: columns, dtype, value range",
                "3. Validate the RAW data, before any transform",
                "-> automate it with pandera in real projects",
            ],
            "extra_banner_title": "Extra example: guarding a pipeline against a renamed column",
            "extra_surv_heading": "county renamed to city -> it errors",
            "extra_surv_title": "surveillance_guard.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Four defenses: env / summary / seed / contract",
            "outro_sub": "Next chapter: the full SitRep case study",
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

    def _gate_card(self, text_key: str, accent: str, fill: str, width: float = 3.0):
        card = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=1.3,
            fill_color=ManimColor(fill),
            fill_opacity=1,
            stroke_color=ManimColor(accent),
            stroke_width=2,
        )
        txt = Text(
            self.t(text_key), font=FONT_CJK, font_size=17, color=ManimColor(TEXT_PRIMARY)
        ).move_to(card.get_center())
        return VGroup(card, txt)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_the_risk(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("risk_heading", "risk_lines", duration)

    def show_schema_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'REQUIRED = {"case_id", "age", "clinical_severity"}\n'
                'VALID_SEV = {"not_ill", "mild", "moderate", "severe"}\n'
                "\n"
                "raw = pd.read_csv(path)\n"
                "assert not (REQUIRED - set(raw.columns))\n"
                'assert set(raw["clinical_severity"]) <= VALID_SEV\n'
                'assert raw["age"].between(0, 120).all()'
            ),
        )
        self._code_block("schema_code_heading", "schema_code_title", code, duration)

    def show_schema_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(
            self.t("schema_output_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(kwargs.get("output", self.t("schema_output_text")), position=ORIGIN)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_contract_gate(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(
            self.t("gate_heading"), font=FONT_CJK, font_size=28, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.7)

        raw = self._gate_card("gate_raw", ACCENT_BLUE, BG_CARD, width=2.6).move_to(LEFT * 4.6)
        gate = self._gate_card("gate_check", ACCENT_ORANGE, BG_CARD_ALT, width=2.9).move_to(ORIGIN)
        ok = self._gate_card("gate_ok", ACCENT_GREEN, BG_CARD, width=3.1).move_to(
            RIGHT * 4.4 + UP * 1.05
        )
        ng = self._gate_card("gate_ng", ERROR_RED, BG_CARD, width=3.1).move_to(
            RIGHT * 4.4 + DOWN * 1.05
        )

        l1 = Line(
            raw.get_right(), gate.get_left(), color=ManimColor(TEXT_SECONDARY), stroke_width=3
        )
        l2 = Line(
            gate.get_right(), ok.get_left(), color=ManimColor(ACCENT_GREEN), stroke_width=3
        )
        l3 = Line(
            gate.get_right(), ng.get_left(), color=ManimColor(ERROR_RED), stroke_width=3
        )

        diagram = VGroup(l1, l2, l3, raw, gate, ok, ng).move_to(ORIGIN + DOWN * 0.2)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(raw), FadeIn(l1), FadeIn(gate), run_time=0.9)
        self.play(FadeIn(l2), FadeIn(ok), FadeIn(l3), FadeIn(ng), run_time=0.9)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, diagram)), run_time=0.5)

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

    def show_extra_surveillance(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'EXPECTED = {"county", "week", "cases"}\n'
                "missing = EXPECTED - set(df.columns)\n"
                'assert not missing, f"renamed? missing {missing}"\n'
                '# e.g. "county" renamed to "city" -> caught here'
            ),
        )
        self._code_block("extra_surv_heading", "extra_surv_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_no_check(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df = pd.read_csv(path)  # trust it"),
            kwargs.get("correct_code", "assert set(REQUIRED) <= set(df.columns)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_one_col(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'if "age" in df: pass  # only one col'),
            kwargs.get("correct_code", "assert not (REQUIRED - set(df.columns))"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_after_transform(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "validate(df_after_cleaning)"),
            kwargs.get("correct_code", "validate(raw)  # check before use"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(
            self.t("outro_heading"), font=FONT_CJK, font_size=25, color=ManimColor(ACCENT_ORANGE)
        ).move_to(ORIGIN + UP * 0.5)
        s = Text(
            self.t("outro_sub"), font=FONT_CJK, font_size=20, color=ManimColor(TEXT_SECONDARY)
        ).next_to(h, DOWN, buff=0.4)
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
