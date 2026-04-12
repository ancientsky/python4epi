"""Ch04-08: PII Protection — 拿到 Line List 的第一件事

Manim scene for the tutorial video on Personally Identifiable Information (PII)
de-identification techniques (Suppression, Pseudonymization, Hashing,
Generalization, Masking) plus k-anonymity — covering Chapter 04 Step 1.5.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ORIGIN,
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
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch04PiiProtectionScene(EpiBaseScene):
    """Tutorial video scene: PII protection and de-identification."""

    total_steps: int = 15

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _bullet_list(
        self,
        heading_text: str,
        lines: list[str],
        duration: float,
        *,
        heading_font_size: int = 32,
        bullet_font_size: int = 23,
        heading_color: str = ACCENT_ORANGE,
    ) -> None:
        """Standard heading + bullet list layout used across segments."""
        heading = Text(
            heading_text,
            font=FONT_CJK,
            font_size=heading_font_size,
            color=heading_color,
        ).to_edge(UP, buff=0.8)

        bullets = VGroup(
            *[
                Text(line, font=FONT_CJK, font_size=bullet_font_size, color=TEXT_PRIMARY)
                for line in lines
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40).next_to(heading, DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.5)
        self.play(FadeIn(bullets, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(heading, bullets)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        """Title card for the PII protection lesson."""
        self.show_title_card(
            "個資保護",
            "拿到 Line List 的第一件事",
            duration=duration,
        )

    def show_sweeney(self, duration: float = 6.0, **kwargs) -> None:
        """Sweeney 2002 — 87% re-identification warning."""
        self.show_step_indicator(1, self.total_steps)

        heading = Text(
            "Sweeney 2002 的經典警告",
            font=FONT_CJK,
            font_size=30,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.8)

        big_stat = Text(
            "87%",
            font=FONT_CJK,
            font_size=120,
            color=ACCENT_ORANGE,
        ).next_to(heading, DOWN, buff=0.6)

        sub = Text(
            "僅憑 郵遞區號 + 生日 + 性別",
            font=FONT_CJK,
            font_size=26,
            color=TEXT_PRIMARY,
        ).next_to(big_stat, DOWN, buff=0.4)

        caption = Text(
            "就能重新識別全美 87% 的人",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(sub, DOWN, buff=0.3)

        group = VGroup(heading, big_stat, sub, caption)
        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(big_stat), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(group), run_time=0.5)

    def show_three_categories(self, duration: float = 7.0, **kwargs) -> None:
        """Three categories of PII."""
        self.show_step_indicator(2, self.total_steps)
        self._bullet_list(
            "PII 三大類",
            [
                "1. 直接識別：姓名、身分證、電話、地址",
                "2. 準識別：年齡、性別、生日、郵遞區號",
                "3. 敏感屬性：HIV、精神科、基因、收入",
                "三種都要保護，但方法不同。",
            ],
            duration,
        )

    def show_suppression(self, duration: float = 7.0, **kwargs) -> None:
        """Technique 1: Suppression — drop PII columns."""
        self.show_step_indicator(3, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "pii_columns = [\n"
                "    'name', 'national_id',\n"
                "    'phone', 'address',\n"
                "]\n"
                "df_safe = df.drop(\n"
                "    columns=pii_columns,\n"
                "    errors='ignore',\n"
                ")"
            ),
        )

        heading = Text(
            "① Suppression — 直接刪除",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="suppression.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    def show_pseudonymization(self, duration: float = 7.0, **kwargs) -> None:
        """Technique 2: Pseudonymization — assign fake IDs."""
        self.show_step_indicator(4, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "df_safe['case_id'] = [\n"
                "    'CASE_' + str(i).zfill(3)\n"
                "    for i in range(1, len(df_safe)+1)\n"
                "]"
            ),
        )

        heading = Text(
            "② Pseudonymization — 假名化",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="pseudonymize.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    def show_hashing(self, duration: float = 8.0, **kwargs) -> None:
        """Technique 3: Hashing with salt (SHA-256)."""
        self.show_step_indicator(5, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "import hashlib, os\n"
                "SALT = os.environ['PII_SALT']\n"
                "def hash_id(raw_id):\n"
                "    combined = (SALT + str(raw_id)).encode()\n"
                "    h = hashlib.sha256(combined).hexdigest()\n"
                "    return 'H_' + h[:12]"
            ),
        )

        heading = Text(
            "③ Hashing — 加鹽雜湊",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="hash_id.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    def show_generalization(self, duration: float = 8.0, **kwargs) -> None:
        """Technique 4: Generalization — bin ages, use epi weeks."""
        self.show_step_indicator(6, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "df_safe['age_group'] = pd.cut(\n"
                "    df['age'],\n"
                "    bins=[59, 69, 79, 89, 120],\n"
                "    labels=['60-69','70-79','80-89','90+'],\n"
                ")\n"
                "df_safe['epi_week'] = (\n"
                "    df['symptom_onset_date'].dt.isocalendar().week\n"
                ")"
            ),
        )

        heading = Text(
            "④ Generalization — 泛化組距",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="generalize.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    def show_masking(self, duration: float = 7.0, **kwargs) -> None:
        """Technique 5: Masking — keep format, hide content."""
        self.show_step_indicator(7, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "def mask_phone(phone):\n"
                "    parts = str(phone).split('-')\n"
                "    if len(parts) == 3:\n"
                "        return f'{parts[0]}-***-***'\n"
                "    return '***'"
            ),
        )

        heading = Text(
            "⑤ Masking — 遮罩",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="mask.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    def show_k_anonymity(self, duration: float = 8.0, **kwargs) -> None:
        """k-anonymity self-check."""
        self.show_step_indicator(8, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "quasi_ids = ['age_group', 'sex', 'wing']\n"
                "sizes = (\n"
                "    df_safe.groupby(quasi_ids, observed=True)\n"
                "           .size()\n"
                ")\n"
                "risky = sizes[sizes < 5]\n"
                "print(f'Risky groups: {len(risky)}')"
            ),
        )

        output_text = kwargs.get("output", "Risky groups: 2")

        heading = Text(
            "自我檢查：k-anonymity (k ≥ 5)",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="k_anonymity.py", position=LEFT * 3 + UP * 0.3)
        self.wait(0.8)
        out = self.show_output(output_text, position=DOWN * 2.8)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, panel, out)), run_time=0.5)

    def show_workflow(self, duration: float = 7.0, **kwargs) -> None:
        """Three-tier folder workflow."""
        self.show_step_indicator(9, self.total_steps)
        self._bullet_list(
            "三層資料夾工作流",
            [
                "raw_restricted/       ← 原始資料，加密 + .gitignore",
                "scripts/deidentify.py ← 去識別化腳本",
                "deidentified/         ← 乾淨資料，可進 notebook",
                "規則：notebook 只能讀最底層 deidentified/",
            ],
            duration,
            heading_font_size=30,
            bullet_font_size=22,
        )

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        """Summarise key points about PII protection."""
        self.show_step_indicator(10, self.total_steps)
        self._bullet_list(
            "重點整理：五招去識別化",
            [
                "① Suppression：能刪就刪",
                "② Pseudonymization：換成 CASE_001",
                "③ Hashing：SHA-256 + salt",
                "④ Generalization：年齡組、流行週",
                "⑤ Masking：留形式、藏內容",
                "最後用 k-anonymity 自我檢查",
            ],
            duration,
            heading_font_size=32,
            bullet_font_size=22,
        )

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the ExtraExampleBanner section divider."""
        banner = ExtraExampleBanner("額外範例：台灣 COVID-19 實聯制")
        self.show_section_banner(banner, duration=duration)

    def show_extra_covid(self, duration: float = 7.0, **kwargs) -> None:
        """COVID-19 Taiwan 1922 SMS contact tracing example."""
        self.show_step_indicator(11, self.total_steps)

        code_lines = kwargs.get(
            "code",
            (
                "# Taiwan 1922 SMS contact tracing\n"
                "# Phone -> SHA256(phone + salt)\n"
                "# Auto-purge after 28 days\n"
                "# Access: outbreak investigation only"
            ),
        )

        heading = Text(
            "實聯制的四道防線",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        panel = self.show_code(code_lines, title="sms_tracing.py", position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(heading, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        """Show the BlindSpotBanner section divider."""
        banner = BlindSpotBanner("初學者常見地雷 3 選")
        self.show_section_banner(banner, duration=duration)

    def show_blindspot_quasi_id(self, duration: float = 6.0, **kwargs) -> None:
        """Blindspot 1: only dropping name, leaving quasi-identifiers."""
        self.show_step_indicator(12, self.total_steps)
        error_code = kwargs.get("error_code", "df.drop(columns=['name'])")
        correct_code = kwargs.get(
            "correct_code", "df.drop(columns=['name','dob','zip'])"
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_salt(self, duration: float = 6.0, **kwargs) -> None:
        """Blindspot 2: hashing without salt (rainbow-table attack)."""
        self.show_step_indicator(13, self.total_steps)
        error_code = kwargs.get(
            "error_code", "hashlib.sha256(id.encode()).hexdigest()"
        )
        correct_code = kwargs.get(
            "correct_code", "hashlib.sha256((SALT+id).encode()).hexdigest()"
        )
        panel = self.show_error_vs_correct(error_code, correct_code, duration=duration)
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_git(self, duration: float = 6.0, **kwargs) -> None:
        """Blindspot 3: committing raw CSV to git."""
        self.show_step_indicator(14, self.total_steps)
        error_code = kwargs.get("error_code", "git add data/line_list_raw.csv")
        correct_code = kwargs.get(
            "correct_code", "echo 'data/raw_restricted/' >> .gitignore"
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
            "下一集：SitRep 摘要指標",
            font=FONT_CJK,
            font_size=28,
            color=ACCENT_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub = Text(
            "資料不是你的，是住民託付給你的。",
            font=FONT_CJK,
            font_size=22,
            color=TEXT_SECONDARY,
        ).next_to(heading, DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(heading, sub)), run_time=0.5)
