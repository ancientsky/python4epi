"""Ch12-04: The collider trap and Berkson's paradox.

Conditioning on a collider (A->K<-Y) manufactures a spurious association between
two variables that are unrelated in the full sample - the formal name is
Berkson's paradox. Includes a sketch DAG for a Sanxia dengue cluster. Extra
example: hospital-based selection bias.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
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
    BORDER_LIGHT,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12ColliderScene(EpiBaseScene):
    """Tutorial video scene: collider bias and Berkson's paradox."""

    total_steps: int = 11

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "對撞因子的陷阱",
            "title_sub": "Berkson 悖論：只看住院者，就冒出假關聯",
            "recap_heading": "先複習：什麼是對撞因子",
            "recap_A": "暴露",
            "recap_Y": "嚴重度",
            "recap_K": "住院",
            "recap_caption": "暴露和嚴重度本來互不相關，卻都會讓人住院 → 住院＝對撞因子",
            "cost_heading": "條件化的代價：Berkson 悖論",
            "cost_lines": [
                "條件化 = 只挑「對撞因子＝某個值」的子集分析",
                "例如：只分析「有住院」的病人",
                "會在兩個本來無關的變項間，生出假關聯",
                "→ 這個現象的正式名字：Berkson 悖論",
            ],
            "intuition_heading": "直覺版：假的負相關怎麼冒出來",
            "intuition_full_title": "全體樣本",
            "intuition_full_caption": "暴露 vs 嚴重度：無相關",
            "intuition_sub_title": "只看住院者",
            "intuition_sub_caption": "冒出假的負相關",
            "intuition_note": "暴露低的因嚴重度高才住院、嚴重度低的因暴露多才住院 → 被硬綁在一起",
            "sanxia_heading": "真實案例草稿：三峽登革熱群聚",
            "sx_water": "積水",
            "sx_vector": "病媒蚊",
            "sx_local": "本土",
            "sx_audit": "稽查",
            "sx_report": "通報",
            "tag_mediator": "中介",
            "tag_collider": "對撞",
            "sanxia_caption": "積水→病媒蚊(中介)→本土 ｜ 本土→通報←稽查(對撞)：只看通報者會出事",
            "traps_heading": "這些「合理篩選」都是條件化對撞",
            "traps_lines": [
                "只分析「有通報／確診」的病例",
                "只分析「有住院」的病人",
                "只分析「有回診」的個案",
                "→ 看似合理，其實都在對某個對撞因子條件化",
            ],
            "summary_heading": "對撞因子三重點",
            "summary_lines": [
                "① 對撞因子：被暴露和結果同時指向的變項",
                "② 對它條件化 → 生出不存在的假關聯（Berkson 悖論）",
                "③ 常見兇手：只看住院／只看通報／只看回診",
                "→ 分析前先畫 DAG，認出對撞因子再決定要不要篩",
            ],
            "extra_banner_title": "額外範例：醫院選樣偏差",
            "extra_hospital_heading": "醫院裡的病例對照，小心 Berkson",
            "extra_hospital_lines": [
                "只從住院病人裡挑病例和對照來比暴露",
                "住院與否，被好幾個疾病共同推高（對撞）",
                "兩個本來無關的病，在住院者裡看起來相關",
                "→ Berkson 當年就是在醫院資料裡發現這件事",
            ],
            "blindspot_banner_title": "對撞因子三個新手地雷",
            "outro_heading": "第十二章因果推論，起手式收工！",
            "outro_sub": "接著翻課本：AR／PAR 歸因風險、DiD 政策評估",
        },
        "en": {
            "title_main": "The Collider Trap",
            "title_sub": "Berkson's paradox: subset the admitted, and a fake link appears",
            "recap_heading": "Recap: what is a collider",
            "recap_A": "exposure",
            "recap_Y": "severity",
            "recap_K": "admitted",
            "recap_caption": "exposure & severity are unrelated, yet both cause admission -> collider",
            "cost_heading": "The cost of conditioning: Berkson's paradox",
            "cost_lines": [
                "Conditioning = analyzing only the subset where collider = a value",
                'For example: analyzing only "admitted" patients',
                "It manufactures a link between two unrelated variables",
                "-> the formal name for this: Berkson's paradox",
            ],
            "intuition_heading": "Intuition: where the fake negative link comes from",
            "intuition_full_title": "Full sample",
            "intuition_full_caption": "exposure vs severity: no correlation",
            "intuition_sub_title": "Admitted only",
            "intuition_sub_caption": "a fake negative link appears",
            "intuition_note": "low-exposure got admitted for high severity, and vice versa -> tied together",
            "sanxia_heading": "Sketch DAG: a Sanxia dengue cluster",
            "sx_water": "water",
            "sx_vector": "vectors",
            "sx_local": "local",
            "sx_audit": "audit",
            "sx_report": "report",
            "tag_mediator": "mediator",
            "tag_collider": "collider",
            "sanxia_caption": "water->vectors(mediator)->local | local->report<-audit(collider): subsetting report bites",
            "traps_heading": 'These "reasonable filters" all condition a collider',
            "traps_lines": [
                'Analyzing only "notified / confirmed" cases',
                'Analyzing only "admitted" patients',
                'Analyzing only "returned for follow-up" cases',
                "-> all look sensible, all condition on some collider",
            ],
            "summary_heading": "Three Takeaways on Colliders",
            "summary_lines": [
                "1. Collider: a variable pointed to by both exposure and outcome",
                "2. Condition on it -> a link that doesn't exist (Berkson's paradox)",
                "3. Usual suspects: admitted-only / notified-only / follow-up-only",
                "-> draw the DAG first, spot the collider, then decide about filtering",
            ],
            "extra_banner_title": "Extra example: hospital selection bias",
            "extra_hospital_heading": "Hospital case-control: mind Berkson",
            "extra_hospital_lines": [
                "Picking cases AND controls only from admitted patients",
                "Admission is pushed up by several diseases at once (collider)",
                "Two unrelated diseases look correlated among the admitted",
                "-> this is exactly where Berkson first spotted it, in hospital data",
            ],
            "blindspot_banner_title": "Three Collider Blind Spots",
            "outro_heading": "Chapter 12's causal opening moves: done!",
            "outro_sub": "Next in the book: AR/PAR attributable risk, DiD policy evaluation",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=29, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.8
        )
        bl = (
            VGroup(
                *[
                    Text(x, font=FONT_CJK, font_size=21, color=TEXT_PRIMARY)
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

    def _dag_node(self, label: str, color: str, pos, *, radius: float = 0.68, font_size: int = 16):
        circ = Circle(
            radius=radius,
            color=ManimColor(color),
            stroke_width=3,
            fill_color=ManimColor(color),
            fill_opacity=0.12,
        )
        txt = Text(label, font=FONT_CJK, font_size=font_size, color=ManimColor(color), weight="BOLD")
        txt.move_to(circ.get_center())
        return VGroup(circ, txt).move_to(pos)

    def _arrow(self, a: VGroup, b: VGroup, color: str, *, buff: float = 0.74):
        return Arrow(
            a.get_center(),
            b.get_center(),
            buff=buff,
            color=ManimColor(color),
            stroke_width=4,
            max_tip_length_to_length_ratio=0.16,
        )

    def _scatter_panel(self, title_key: str, caption_key: str, points, color: str, *, trend: bool):
        card = RoundedRectangle(
            corner_radius=0.15,
            width=4.6,
            height=3.2,
            fill_color=ManimColor(BG_CARD),
            fill_opacity=1,
            stroke_color=ManimColor(BORDER_LIGHT),
            stroke_width=2,
        )
        title = Text(
            self.t(title_key), font=FONT_CJK, font_size=20, color=ManimColor(color), weight="BOLD"
        ).move_to(card.get_top() + DOWN * 0.35)
        dots = VGroup(
            *[
                Dot(point=card.get_center() + RIGHT * x + UP * y, radius=0.08, color=ManimColor(color))
                for x, y in points
            ]
        )
        extras = VGroup()
        if trend:
            extras.add(
                DashedLine(
                    card.get_center() + LEFT * 1.5 + UP * 0.9,
                    card.get_center() + RIGHT * 1.5 + DOWN * 0.9,
                    color=ManimColor(ERROR_RED),
                    stroke_width=3,
                )
            )
        caption = Text(
            self.t(caption_key), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).move_to(card.get_bottom() + UP * 0.32)
        return VGroup(card, title, dots, extras, caption)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_collider_recap(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        heading = Text(
            self.t("recap_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        a = self._dag_node(self.t("recap_A"), ACCENT_BLUE, LEFT * 2.0 + UP * 0.8)
        y = self._dag_node(self.t("recap_Y"), ACCENT_ORANGE, RIGHT * 2.0 + UP * 0.8)
        k = self._dag_node(self.t("recap_K"), ERROR_RED, DOWN * 1.1)
        arr_ak = self._arrow(a, k, ACCENT_BLUE)
        arr_yk = self._arrow(y, k, ACCENT_ORANGE)
        diagram = VGroup(a, y, k, arr_ak, arr_yk).move_to(UP * 0.3)

        caption = Text(
            self.t("recap_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(VGroup(a, y, k), lag_ratio=0.2), run_time=0.9)
        self.play(Create(VGroup(arr_ak, arr_yk)), run_time=0.8)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.9))
        self.play(FadeOut(VGroup(heading, diagram, caption)), run_time=0.5)

    def show_conditioning_cost(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("cost_heading", "cost_lines", duration)

    def show_berkson_intuition(self, duration: float = 10.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        heading = Text(
            self.t("intuition_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        full = self._scatter_panel(
            "intuition_full_title",
            "intuition_full_caption",
            [(-1.4, 0.3), (-0.7, -0.4), (0.1, 0.5), (0.3, -0.3), (1.0, 0.2), (1.4, -0.5)],
            ACCENT_BLUE,
            trend=False,
        )
        sub = self._scatter_panel(
            "intuition_sub_title",
            "intuition_sub_caption",
            [(-1.4, 0.8), (-0.7, 0.4), (0.0, 0.0), (0.7, -0.4), (1.4, -0.8)],
            ERROR_RED,
            trend=True,
        )
        panels = VGroup(full, sub).arrange(RIGHT, buff=0.6).move_to(UP * 0.15)

        note = Text(
            self.t("intuition_note"), font=FONT_CJK, font_size=16, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(full), run_time=0.7)
        self.play(FadeIn(sub), run_time=0.7)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, panels, note)), run_time=0.5)

    def show_sanxia_dag(self, duration: float = 11.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        heading = Text(
            self.t("sanxia_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.6)

        water = self._dag_node(self.t("sx_water"), ACCENT_BLUE, LEFT * 4.0 + UP * 0.7)
        vector = self._dag_node(self.t("sx_vector"), ACCENT_GREEN, LEFT * 1.4 + UP * 0.7)
        local = self._dag_node(self.t("sx_local"), ACCENT_ORANGE, RIGHT * 1.2 + UP * 0.7)
        audit = self._dag_node(self.t("sx_audit"), ACCENT_BLUE, RIGHT * 3.8 + UP * 0.7)
        report = self._dag_node(self.t("sx_report"), ERROR_RED, RIGHT * 2.5 + DOWN * 1.5)

        arr_wv = self._arrow(water, vector, ACCENT_BLUE)
        arr_vl = self._arrow(vector, local, ACCENT_GREEN)
        arr_lr = self._arrow(local, report, ACCENT_ORANGE)
        arr_ar = self._arrow(audit, report, ACCENT_BLUE)

        tag_med = Text(
            self.t("tag_mediator"), font=FONT_CJK, font_size=15, color=ManimColor(ACCENT_GREEN)
        ).next_to(vector, DOWN, buff=0.12)
        tag_col = Text(
            self.t("tag_collider"), font=FONT_CJK, font_size=15, color=ManimColor(ERROR_RED)
        ).next_to(report, DOWN, buff=0.12)

        diagram = VGroup(
            water, vector, local, audit, report, arr_wv, arr_vl, arr_lr, arr_ar, tag_med, tag_col
        )
        caption = Text(
            self.t("sanxia_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(VGroup(water, vector, local, audit, report), lag_ratio=0.15), run_time=1.1)
        self.play(Create(VGroup(arr_wv, arr_vl, arr_lr, arr_ar)), run_time=1.0)
        self.play(FadeIn(VGroup(tag_med, tag_col)), run_time=0.4)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 3.8))
        self.play(FadeOut(VGroup(heading, diagram, caption)), run_time=0.5)

    def show_common_traps(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("traps_heading", "traps_lines", duration)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_hospital(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_hospital_heading", "extra_hospital_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_only_hospitalized(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "df = df[df['hospitalized'] == 1]"),
            kwargs.get("correct_code", "df = full_cohort  # no collider filter"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_only_notified(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "cases = df[df['notified'] == 1]"),
            kwargs.get("correct_code", "cases = df  # include unreported too"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_adjust_collider(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.ols('sev ~ exp + hospitalized')"),
            kwargs.get("correct_code", "smf.ols('sev ~ exp')  # drop collider"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
