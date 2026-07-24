"""Ch13-05: Seed determinism - random, but consistently random.

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
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)

# Illustrative integer sequences: the same seed reproduces the same five numbers,
# no seed gives a different set each run.
_SEQ_SEED = ["8", "77", "65", "43", "9"]
_SEQ_NOSEED = ["51", "2", "88", "14", "70"]


class Ch13SeedScene(EpiBaseScene):
    """Tutorial video scene: fixing a seed makes randomness reproducible."""

    total_steps: int = 9

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "seed 決定論",
            "title_sub": "隨機也要「隨機地一致」",
            "problem_heading": "隨機沒鎖種子的痛",
            "problem_lines": [
                "train_test_split、np.random、torch 都會隨機",
                "沒設種子 = 每次執行都重洗一次牌",
                "同程式兩次跑出不同準確率",
                "→ 你以為程式壞了，其實只是忘了固定亂數",
            ],
            "seed_code_heading": "十行最小範例：同種子 → 同亂數",
            "seed_code_title": "seed_demo.py",
            "seed_output_heading": "跑出來見真章",
            "seed_output_text": (
                "seed=42 #1: [ 8 77 65 43  9]\n"
                "seed=42 #2: [ 8 77 65 43  9]\n"
                "no seed   : [51  2 88 14 70]\n"
                "-> same seed, same numbers"
            ),
            "strips_heading": "把輸出畫成圖",
            "strip_seed1": "seed=42 第一次",
            "strip_seed2": "seed=42 第二次",
            "strip_noseed": "沒設種子",
            "strips_caption": "綠燈：可重現　紅燈：每次都不同",
            "summary_heading": "seed 決定論三重點",
            "summary_lines": [
                "① 任何隨機步驟，沒鎖種子就每次是不同實驗",
                "② 固定 seed → 隨機地一致，同種子同結果",
                "③ 各套件一起鎖：default_rng / random_state / torch",
                "→ 隨機不可怕，忘了鎖種子才可怕",
            ],
            "extra_banner_title": "額外範例：可重現的自助法信賴區間",
            "extra_boot_heading": "bootstrap 致死率 95% CI",
            "extra_boot_title": "bootstrap_ci.py",
            "blindspot_banner_title": "隨機種子三個新手地雷",
            "outro_heading": "下一集：schema 契約",
            "outro_sub": "搶在資料改動之前把錯誤攔下來",
        },
        "en": {
            "title_main": "Seed Determinism",
            "title_sub": 'Random, but "consistently random"',
            "problem_heading": "The pain of unseeded randomness",
            "problem_lines": [
                "train_test_split, np.random, torch all randomize",
                "no seed = reshuffle the deck every run",
                "same code, two runs, two accuracies",
                "-> looks like a bug, but you just forgot the seed",
            ],
            "seed_code_heading": "Ten-line demo: same seed -> same numbers",
            "seed_code_title": "seed_demo.py",
            "seed_output_heading": "The moment of truth",
            "seed_output_text": (
                "seed=42 #1: [ 8 77 65 43  9]\n"
                "seed=42 #2: [ 8 77 65 43  9]\n"
                "no seed   : [51  2 88 14 70]\n"
                "-> same seed, same numbers"
            ),
            "strips_heading": "Draw the output",
            "strip_seed1": "seed=42 run #1",
            "strip_seed2": "seed=42 run #2",
            "strip_noseed": "no seed",
            "strips_caption": "green: reproducible   red: different each run",
            "summary_heading": "Three Takeaways",
            "summary_lines": [
                "1. Any random step, unseeded, is a new experiment",
                "2. Fix the seed -> consistently random, same result",
                "3. Seed all libs: default_rng / random_state / torch",
                "-> randomness is fine, forgetting the seed isn't",
            ],
            "extra_banner_title": "Extra example: a reproducible bootstrap CI",
            "extra_boot_heading": "Bootstrap 95% CI for the CFR",
            "extra_boot_title": "bootstrap_ci.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the schema contract",
            "outro_sub": "catch data changes before they corrupt results",
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

    def _number_strip(self, nums: list[str], accent: str) -> VGroup:
        boxes = VGroup()
        for n in nums:
            box = RoundedRectangle(
                corner_radius=0.08,
                width=0.9,
                height=0.7,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(accent),
                stroke_width=2,
            )
            t = Text(n, font=FONT_MONO, font_size=20, color=ManimColor(TEXT_PRIMARY)).move_to(
                box.get_center()
            )
            boxes.add(VGroup(box, t))
        return boxes.arrange(RIGHT, buff=0.15)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_the_problem(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("problem_heading", "problem_lines", duration)

    def show_seed_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import numpy as np\n"
                "\n"
                "def sample(seed=None):\n"
                "    rng = np.random.default_rng(seed)\n"
                "    return rng.integers(0, 100, 5)\n"
                "\n"
                'print("seed=42:", sample(42), sample(42))\n'
                'print("no seed:", sample())'
            ),
        )
        self._code_block("seed_code_heading", "seed_code_title", code, duration)

    def show_seed_output(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(
            self.t("seed_output_heading"),
            font=FONT_CJK,
            font_size=28,
            color=ManimColor(ACCENT_ORANGE),
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(kwargs.get("output", self.t("seed_output_text")), position=ORIGIN)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_determinism_strips(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(
            self.t("strips_heading"), font=FONT_CJK, font_size=28, color=ManimColor(ACCENT_ORANGE)
        ).to_edge(UP, buff=0.7)

        s1 = self._number_strip(_SEQ_SEED, ACCENT_GREEN)
        s2 = self._number_strip(_SEQ_SEED, ACCENT_GREEN)
        s3 = self._number_strip(_SEQ_NOSEED, ERROR_RED)
        strips = (
            VGroup(s1, s2, s3)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            .move_to(RIGHT * 1.1 + DOWN * 0.1)
        )

        lab1 = Text(
            self.t("strip_seed1"), font=FONT_CJK, font_size=18, color=ManimColor(ACCENT_GREEN)
        ).next_to(s1, LEFT, buff=0.4)
        lab2 = Text(
            self.t("strip_seed2"), font=FONT_CJK, font_size=18, color=ManimColor(ACCENT_GREEN)
        ).next_to(s2, LEFT, buff=0.4)
        lab3 = Text(
            self.t("strip_noseed"), font=FONT_CJK, font_size=18, color=ManimColor(ERROR_RED)
        ).next_to(s3, LEFT, buff=0.4)

        caption = Text(
            self.t("strips_caption"), font=FONT_CJK, font_size=18, color=ManimColor(TEXT_SECONDARY)
        ).to_edge(DOWN, buff=0.6)

        group = VGroup(strips, lab1, lab2, lab3).move_to(ORIGIN + DOWN * 0.1)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(group, lag_ratio=0.15), run_time=1.3)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(heading, group, caption)), run_time=0.5)

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

    def show_extra_bootstrap(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "rng = np.random.default_rng(42)  # lock seed\n"
                "boot = [rng.choice(cfr, len(cfr)).mean()\n"
                "        for _ in range(2000)]\n"
                "lo, hi = np.percentile(boot, [2.5, 97.5])\n"
                'print(f"95% CI = ({lo:.1%}, {hi:.1%})")'
            ),
        )
        self._code_block("extra_boot_heading", "extra_boot_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_bs_split(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "train_test_split(X, y)"),
            kwargs.get("correct_code", "train_test_split(X, y, random_state=42)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_global_seed(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "np.random.seed(42)  # global, fragile"),
            kwargs.get("correct_code", "rng = np.random.default_rng(42)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_bs_torch(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model = train(data)  # torch unseeded"),
            kwargs.get("correct_code", "torch.manual_seed(42); model = train(data)"),
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
