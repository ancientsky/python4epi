"""Ch12-03: Drawing causation with a DAG - fork, chain, collider.

Three DAG structures and their two opposite adjustment rules:
* confounder (fork, C->A and C->Y): DO adjust
* mediator (chain, A->M->Y): usually DON'T adjust
* collider (A->K<-Y): NEVER adjust

Extra example: the smoking -> tar -> cancer chain (adjusting the mediator hides
the total effect). Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``.
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
    FadeIn,
    FadeOut,
    ManimColor,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch12DAGScene(EpiBaseScene):
    """Tutorial video scene: DAGs - confounder, mediator, collider."""

    total_steps: int = 11

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "用 DAG 把因果畫出來",
            "title_sub": "有向無環圖：三結構，兩套相反規則",
            "basics_heading": "DAG 是什麼？",
            "basics_lines": [
                "DAG = 有向無環圖 directed acyclic graph",
                "用箭頭表示「誰影響誰」，箭頭方向就是因果方向",
                "無環：不能繞一圈回到自己（因不能是自己的果）",
                "→ 難的不是選軟體，是「畫之前先想清楚」",
            ],
            "fork_heading": "① 干擾因子（fork）：要調整",
            "fork_caption": "C → A、C → Y：C 是共同原因，虛線是假關聯 → 分層或迴歸校正",
            "chain_heading": "② 中介變項（chain）：通常不調整",
            "chain_caption": "A → M → Y：M 在因果路徑上 → 看總效應別調 M，看直接效應才調",
            "collider_heading": "③ 對撞因子（collider）：絕不調整",
            "collider_caption": "A → K ← Y：K 被兩邊指向 → 條件化它會生出假關聯（下集細講）",
            "n_A": "A",
            "n_C": "C",
            "n_Y": "Y",
            "n_M": "M",
            "n_K": "K",
            "map_heading": "對照護理之家的三個角色",
            "map_lines": [
                "干擾：functional_status → shower_use、→ infection（Ch05 校正過）",
                "中介：water_contamination → shower_aerosol → infection",
                "對撞：severity 與其他因素 → hospitalized（別只看住院者）",
                "→ 先分清角色，再決定調整誰、放過誰",
            ],
            "summary_heading": "DAG 三結構，一次記牢",
            "summary_lines": [
                "① 干擾 fork（C→A、C→Y）：要調整",
                "② 中介 chain（A→M→Y）：看總效應不調整",
                "③ 對撞 collider（A→K←Y）：絕不調整",
                "→ 同樣是第三個變項，箭頭方向決定命運",
            ],
            "extra_banner_title": "額外範例：抽菸 → 焦油 → 肺癌",
            "extra_smoking_heading": "中介鏈：別把 tar 調掉",
            "smk_smoke": "吸菸",
            "smk_tar": "焦油",
            "smk_cancer": "肺癌",
            "extra_smoking_caption": "焦油是中介：想看抽菸的總效應，校正 tar 反而把因果路徑關掉",
            "blindspot_banner_title": "DAG 三個新手地雷",
            "outro_heading": "下一集：對撞因子的陷阱",
            "outro_sub": "Berkson 悖論 + 三峽登革熱 DAG 草稿",
        },
        "en": {
            "title_main": "Drawing Causation with a DAG",
            "title_sub": "Directed acyclic graph: 3 shapes, 2 opposite rules",
            "basics_heading": "What is a DAG?",
            "basics_lines": [
                "DAG = directed acyclic graph",
                'Arrows show "who affects whom" - the arrow IS the causal direction',
                "Acyclic: no loop back to yourself (a cause can't be its own effect)",
                '-> the hard part is not the tool, it is "think before you draw"',
            ],
            "fork_heading": "1. Confounder (fork): DO adjust",
            "fork_caption": "C -> A, C -> Y: C is a common cause; the dashed link is spurious -> adjust",
            "chain_heading": "2. Mediator (chain): usually DON'T adjust",
            "chain_caption": "A -> M -> Y: M is on the causal path -> keep M out for the total effect",
            "collider_heading": "3. Collider: NEVER adjust",
            "collider_caption": "A -> K <- Y: K is pointed to by both -> conditioning fakes a link (next up)",
            "n_A": "A",
            "n_C": "C",
            "n_Y": "Y",
            "n_M": "M",
            "n_K": "K",
            "map_heading": "The three roles in the nursing-home case",
            "map_lines": [
                "Confounder: functional_status -> shower_use & -> infection (Ch05)",
                "Mediator: water_contamination -> shower_aerosol -> infection",
                "Collider: severity & other factors -> hospitalized (don't subset it)",
                "-> sort the roles first, then decide what to adjust and what to leave",
            ],
            "summary_heading": "The 3 DAG Shapes, Locked In",
            "summary_lines": [
                "1. Confounder fork (C->A, C->Y): DO adjust",
                "2. Mediator chain (A->M->Y): keep out for total effect",
                "3. Collider (A->K<-Y): NEVER adjust",
                "-> same third variable, the arrow direction decides its fate",
            ],
            "extra_banner_title": "Extra example: smoking -> tar -> cancer",
            "extra_smoking_heading": "A mediator chain: don't adjust away tar",
            "smk_smoke": "smoking",
            "smk_tar": "tar",
            "smk_cancer": "cancer",
            "extra_smoking_caption": "Tar is the mediator: adjusting it shuts down smoking's own causal path",
            "blindspot_banner_title": "Three DAG Blind Spots",
            "outro_heading": "Next: the collider trap",
            "outro_sub": "Berkson's paradox + a Sanxia dengue-cluster DAG sketch",
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

    def _dag_node(self, label: str, color: str, pos, *, radius: float = 0.62, font_size: int = 26):
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

    def _show_dag_structure(
        self,
        step: int,
        heading_key: str,
        node_specs: list,
        edges: list,
        caption_key: str,
        *,
        dashed: list | None = None,
        node_font: int = 26,
        duration: float = 8.0,
    ) -> None:
        self.show_step_indicator(step, self.total_steps)
        heading = Text(
            self.t(heading_key), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        nodes: dict[str, VGroup] = {}
        node_group = VGroup()
        for key, label_key, color, pos in node_specs:
            n = self._dag_node(self.t(label_key), color, pos, font_size=node_font)
            nodes[key] = n
            node_group.add(n)

        edge_group = VGroup()
        for a, b, color in edges:
            arr = Arrow(
                nodes[a].get_center(),
                nodes[b].get_center(),
                buff=0.72,
                color=ManimColor(color),
                stroke_width=4,
                max_tip_length_to_length_ratio=0.16,
            )
            edge_group.add(arr)

        dash_group = VGroup()
        if dashed:
            for a, b in dashed:
                dl = DashedLine(
                    nodes[a].get_center(),
                    nodes[b].get_center(),
                    buff=0.72,
                    color=ManimColor(TEXT_SECONDARY),
                    stroke_width=2,
                )
                dash_group.add(dl)

        diagram = VGroup(node_group, edge_group, dash_group).move_to(UP * 0.3)
        caption = Text(
            self.t(caption_key), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(node_group, lag_ratio=0.2), run_time=0.9)
        self.play(Create(edge_group), run_time=0.8)
        if dashed:
            self.play(Create(dash_group), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 3.3))
        self.play(FadeOut(VGroup(heading, diagram, caption)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_dag_basics(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("basics_heading", "basics_lines", duration)

    def show_fork_confounder(self, duration: float = 9.0, **kwargs) -> None:
        self._show_dag_structure(
            2,
            "fork_heading",
            [
                ("C", "n_C", ERROR_RED, UP * 1.2),
                ("A", "n_A", ACCENT_BLUE, LEFT * 1.9 + DOWN * 0.7),
                ("Y", "n_Y", ACCENT_ORANGE, RIGHT * 1.9 + DOWN * 0.7),
            ],
            [("C", "A", ERROR_RED), ("C", "Y", ERROR_RED)],
            "fork_caption",
            dashed=[("A", "Y")],
            duration=duration,
        )

    def show_chain_mediator(self, duration: float = 9.0, **kwargs) -> None:
        self._show_dag_structure(
            3,
            "chain_heading",
            [
                ("A", "n_A", ACCENT_BLUE, LEFT * 2.4),
                ("M", "n_M", ACCENT_GREEN, ORIGIN),
                ("Y", "n_Y", ACCENT_ORANGE, RIGHT * 2.4),
            ],
            [("A", "M", ACCENT_BLUE), ("M", "Y", ACCENT_BLUE)],
            "chain_caption",
            duration=duration,
        )

    def show_collider(self, duration: float = 9.0, **kwargs) -> None:
        self._show_dag_structure(
            4,
            "collider_heading",
            [
                ("A", "n_A", ACCENT_BLUE, LEFT * 1.9 + UP * 0.8),
                ("Y", "n_Y", ACCENT_ORANGE, RIGHT * 1.9 + UP * 0.8),
                ("K", "n_K", ERROR_RED, DOWN * 1.1),
            ],
            [("A", "K", ACCENT_BLUE), ("Y", "K", ACCENT_ORANGE)],
            "collider_caption",
            duration=duration,
        )

    def show_nursing_home_map(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("map_heading", "map_lines", duration)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(ExtraExampleBanner(self.t("extra_banner_title")), duration=duration)

    def show_extra_smoking(self, duration: float = 9.0, **kwargs) -> None:
        self._show_dag_structure(
            7,
            "extra_smoking_heading",
            [
                ("S", "smk_smoke", ACCENT_BLUE, LEFT * 2.6),
                ("T", "smk_tar", ACCENT_GREEN, ORIGIN),
                ("C", "smk_cancer", ACCENT_ORANGE, RIGHT * 2.6),
            ],
            [("S", "T", ACCENT_BLUE), ("T", "C", ACCENT_BLUE)],
            "extra_smoking_caption",
            node_font=16,
            duration=duration,
        )

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration)

    def show_blindspot_adjust_mediator(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.ols('y ~ a + m')  # m is mediator"),
            kwargs.get("correct_code", "smf.ols('y ~ a')  # total effect"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_dag(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.ols('y ~ a + b + c + d + e')"),
            kwargs.get("correct_code", "controls = pick_from_dag(my_dag)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_adjust_collider(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "smf.ols('y ~ a + hospitalized')"),
            kwargs.get("correct_code", "smf.ols('y ~ a')  # keep collider out"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 3.0, **kwargs) -> None:
        self.show_step_indicator(self.total_steps, self.total_steps)
        h = Text(self.t("outro_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).move_to(
            ORIGIN + UP * 0.5
        )
        s = Text(self.t("outro_sub"), font=FONT_CJK, font_size=22, color=TEXT_SECONDARY).next_to(
            h, DOWN, buff=0.4
        )
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(s), run_time=0.5)
        self.wait(max(0.1, duration - 1.1))
        self.play(FadeOut(VGroup(h, s)), run_time=0.5)
