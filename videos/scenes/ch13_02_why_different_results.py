"""Ch13-02: Why do I get different results on re-run? Three landmines vs pillars.

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
    ManimColor,
    RoundedRectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch13WhyDifferentScene(EpiBaseScene):
    """Tutorial video scene: three landmines vs three pillars of reproducibility."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "為什麼我重跑結果不一樣？",
            "title_sub": "三顆地雷 vs 三根支柱",
            "complaint_heading": "重跑就飄的痛點",
            "complaint_lines": [
                "上次 121 人感染、19 人死亡",
                "什麼都沒動，重跑數字卻飄了",
                "先別懷疑人生：九成九不是邏輯錯",
                "→ 是「隱形變因」偷偷改了結果",
            ],
            "landmines_heading": "三顆常見地雷",
            "landmines_lines": [
                "① 未鎖套件版本：pandas 2.0 → 2.2 預設悄悄變",
                "② 沒固定亂數種子：每次執行都重洗一次牌",
                "③ notebook 手動改資料：那雙手忘了動過什麼",
                "→ 數字飄，多半就中這三顆之一",
            ],
            "pillars_heading": "地雷 → 支柱，一顆對一根",
            "landmine_items": [
                "未鎖套件版本",
                "沒固定亂數種子",
                "手動改資料沒紀錄",
            ],
            "pillar_items": [
                "uv.lock 鎖死版本，uv sync 一致",
                "每步指定 seed，隨機地一致",
                "所有轉換寫成程式碼一行",
            ],
            "drift_heading": "漂移 vs 收斂",
            "drift_lines": [
                "地雷：每次重跑結果慢慢「漂移」，越跑越散",
                "支柱：像校正線，把每次重跑拉回同一答案",
                "可重現 = 把會漂移的因素逐一拿掉",
                "→ 決定論：同輸入永遠同輸出",
            ],
            "summary_heading": "重跑不一致三重點",
            "summary_lines": [
                "① 數字飄，先想三雷：環境、隨機、資料漂移",
                "② 三雷各配一柱：uv.lock、固定 seed、寫進程式",
                "③ 可重現不是玄學，是把隱形變因鎖死",
                "→ 下一集：三行指令產出最小可重跑報告",
            ],
            "extra_banner_title": "額外範例：同事重現不出你的登革熱病例數",
            "extra_dengue_heading": "登革熱本週 340 vs 337？",
            "extra_dengue_lines": [
                "你算 340 例，同事重跑卻是 337 例",
                "① 確認兩人 uv.lock 一致（環境）",
                "② 確認抽樣／切分有鎖種子（隨機）",
                "③ 確認清理規則全寫進程式（資料）",
            ],
            "blindspot_banner_title": "重現不一致三個新手地雷",
            "outro_heading": "下一集：三行指令，從乾淨環境到報告",
            "outro_sub": "single-command workflow，複製貼上就重現",
        },
        "en": {
            "title_main": "Why Do I Get Different Results on Re-run?",
            "title_sub": "Three landmines vs three pillars",
            "complaint_heading": "The Re-run Drift Pain",
            "complaint_lines": [
                "Last time: 121 infected, 19 deaths",
                "You changed nothing, yet the numbers drifted",
                "Don't panic: almost never a logic bug",
                '-> a "hidden variable" quietly changed the result',
            ],
            "landmines_heading": "Three Common Landmines",
            "landmines_lines": [
                "1. Unpinned versions: pandas 2.0 -> 2.2 defaults shift",
                "2. No fixed seed: every run reshuffles the deck",
                "3. Hand-edited notebook data: hands forget what they did",
                "-> drift usually means one of these three",
            ],
            "pillars_heading": "Landmine -> Pillar, one for one",
            "landmine_items": [
                "Unpinned package versions",
                "No fixed random seed",
                "Hand-edited data, no record",
            ],
            "pillar_items": [
                "uv.lock pins versions, uv sync matches",
                "Seed every step, consistently random",
                "Every transform as one line of code",
            ],
            "drift_heading": "Drift vs Convergence",
            "drift_lines": [
                'Landmines: results slowly "drift" wider each run',
                "Pillars: like guide-lines pulling back to one answer",
                "Reproducible = remove drift factors one by one",
                "-> determinism: same input, always same output",
            ],
            "summary_heading": "Three Takeaways",
            "summary_lines": [
                "1. Drift? Think three landmines: env, random, data",
                "2. Each pairs a pillar: uv.lock, fixed seed, in code",
                "3. Reproducibility isn't magic, it's pinning variables",
                "-> Next: three commands to a minimal report",
            ],
            "extra_banner_title": "Extra example: a colleague can't reproduce your dengue counts",
            "extra_dengue_heading": "Dengue this week: 340 vs 337?",
            "extra_dengue_lines": [
                "You get 340 cases, your colleague re-runs to 337",
                "1. Check both uv.lock match (environment)",
                "2. Check sampling / split is seeded (random)",
                "3. Check all cleaning rules are in code (data)",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: three commands, clean env to report",
            "outro_sub": "single-command workflow, copy-paste to reproduce",
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_the_complaint(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("complaint_heading", "complaint_lines", duration)

    def show_three_landmines(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("landmines_heading", "landmines_lines", duration)

    def show_landmine_pillars(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        heading = Text(
            self.t("pillars_heading"), font=FONT_CJK, font_size=28, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.6)

        landmines = self.t("landmine_items")
        pillars = self.t("pillar_items")
        rows = VGroup()
        for lm, pl in zip(landmines, pillars):
            lcard = RoundedRectangle(
                corner_radius=0.12,
                width=4.7,
                height=1.05,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(ERROR_RED),
                stroke_width=2,
            )
            ltxt = Text(
                lm, font=FONT_CJK, font_size=17, color=ManimColor(TEXT_PRIMARY)
            ).move_to(lcard.get_center())
            arrow = Text("→", font=FONT_CJK, font_size=30, color=ManimColor(TEXT_SECONDARY))
            rcard = RoundedRectangle(
                corner_radius=0.12,
                width=6.0,
                height=1.05,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(ACCENT_GREEN),
                stroke_width=2,
            )
            rtxt = Text(
                pl, font=FONT_CJK, font_size=17, color=ManimColor(TEXT_PRIMARY)
            ).move_to(rcard.get_center())
            row = VGroup(
                VGroup(lcard, ltxt), arrow, VGroup(rcard, rtxt)
            ).arrange(RIGHT, buff=0.3)
            rows.add(row)
        rows.arrange(DOWN, buff=0.35).next_to(heading, DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(rows, lag_ratio=0.25), run_time=1.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(heading, rows)), run_time=0.5)

    def show_drift_note(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("drift_heading", "drift_lines", duration)

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

    def show_extra_dengue(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("extra_dengue_heading", "extra_dengue_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_env(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "pip install -U pandas"),
            kwargs.get("correct_code", "uv sync  # respect uv.lock"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_seed(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "train_test_split(X, y)"),
            kwargs.get("correct_code", "train_test_split(X, y, random_state=42)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_data_drift(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df = df.drop(bad_rows)  # by hand"),
            kwargs.get("correct_code", 'df = df.query("age >= 0")  # in code'),
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
