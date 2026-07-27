"""Ch14-01: Capstone intuition - assembling every prior chapter's tool into one report.

Plain-language ("超白話") recap: the whole book's toolbox becomes a single
report-ready outbreak investigation - a full-course meal plated from your tools.

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
    ERROR_RED,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch14CapstoneIntuitionScene(EpiBaseScene):
    """Tutorial video scene: assembling the whole toolbox into one report."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "超白話總複習",
            "title_sub": "把整箱工具，組裝成一份能上呈的報告",
            "detective_heading": "疫調 = 偵探辦案",
            "detective_lines": [
                "Ch02：雜亂資料 → 乾淨 line list",
                "Ch03–04：侵襲率、流行曲線，抓案發輪廓",
                "Ch05–08：排除偽證人、鎖定時間與地點",
                "→ 最後一幕：攤開物證，說出結論",
            ],
            "meal_heading": "工具箱 → 一桌菜",
            "meal_lines": [
                "一箱工具，不會自己變成一頓飯",
                "每章技能 = 食材或器具",
                "這一章負責組裝、擺盤、端出去",
                "→ 從分析到「上得了檯面」的報告",
            ],
            "mapping_heading": "章節技能 → 報告角色",
            "mapping_lines": [
                "Line list 清理（Ch02）→ 食材處理",
                "侵襲率（Ch03）→ 開胃菜總覽",
                "分層／邏輯斯（Ch05–06）→ 去骨與特調醬汁",
                "空間分析（Ch08）→ 擺盤標熱點",
                "因果推論（Ch12）→ 主廚簽名",
            ],
            "thread_heading": "同一條敘事線",
            "thread_chain": [
                "流行曲線\n→ 共同暴露源",
                "空間熱點\n→ 樓層水管",
                "暴露／分層\n→ 排除競爭假說",
                "因果研判\n→ 寫進結論",
            ],
            "thread_caption": "每個數字，都是同一條故事線上的環節",
            "actionable_heading": "報告的真正價值",
            "actionable_lines": [
                "花俏的模型 ≠ 有說服力",
                "每個數字都有脈絡",
                "每個結論都有行動建議",
                "→ 給長官「能做決定的答案」",
            ],
            "summary_heading": "超白話三重點",
            "summary_lines": [
                "① 不教新招：把前 13 章串成一條線",
                "② 工具箱要組裝擺盤，才成一桌菜",
                "③ 好報告 = 有脈絡的數字 + 行動建議",
                "→ 你已能產出完整疫調報告！",
            ],
            "extra_banner_title": "額外範例：完整的麻疹群聚報告",
            "extra_measles_heading": "換成麻疹，同一套流程",
            "extra_measles_lines": [
                "國小麻疹群聚：先清 line list、算侵襲率",
                "流行曲線 → 是不是單一暴露源",
                "疫苗接種史 → 分層分析",
                "地圖標班級熱點 → 因果指向指標個案",
            ],
            "blindspot_banner_title": "疫調報告三個新手地雷",
            "outro_heading": "下一集：報告的八個段落",
            "outro_sub": "標準疫調格式 ↔ 每段對應一章技能",
        },
        "en": {
            "title_main": "Plain-Language Capstone",
            "title_sub": "Assemble the whole toolbox into one report you can submit",
            "detective_heading": "An Investigation = Detective Work",
            "detective_lines": [
                "Ch02: messy data -> a clean line list",
                "Ch03-04: attack rate, epi curve, sketch the scene",
                "Ch05-08: rule out false witnesses, pin time & place",
                "-> Final act: lay out the evidence, state the verdict",
            ],
            "meal_heading": "Toolbox -> A Full-Course Meal",
            "meal_lines": [
                "A box of tools never becomes a meal on its own",
                "Each chapter's skill = an ingredient or utensil",
                "This chapter plates them and serves them up",
                "-> from analysis to a report fit to present",
            ],
            "mapping_heading": "Chapter Skills -> Report Roles",
            "mapping_lines": [
                "Line-list cleaning (Ch02) -> prep the ingredients",
                "Attack rate (Ch03) -> the appetizer overview",
                "Strata / logistic (Ch05-06) -> deboning & sauce",
                "Spatial (Ch08) -> plating, mark the hotspots",
                "Causal (Ch12) -> the chef's signature",
            ],
            "thread_heading": "One Narrative Thread",
            "thread_chain": [
                "Epi curve\n-> common source",
                "Spatial hotspot\n-> floor pipes",
                "Exposure/strata\n-> rule out rivals",
                "Causal call\n-> into conclusion",
            ],
            "thread_caption": "Every number is a link in the same story",
            "actionable_heading": "What Makes a Report Valuable",
            "actionable_lines": [
                "A fancy model is not persuasion",
                "Every number carries context",
                "Every conclusion carries an action",
                '-> give the boss "a decision-ready answer"',
            ],
            "summary_heading": "Three Plain-Language Takeaways",
            "summary_lines": [
                "1. No new tricks: thread the 13 chapters together",
                "2. Tools must be plated to become a meal",
                "3. Good report = context + action items",
                "-> you can now produce a full investigation report!",
            ],
            "extra_banner_title": "Extra example: a full measles-outbreak report",
            "extra_measles_heading": "Swap in measles, same workflow",
            "extra_measles_lines": [
                "School measles cluster: clean line list, attack rate",
                "Epi curve -> is it a single source?",
                "Vaccination history -> stratified analysis",
                "Map class hotspots -> causal call on the index case",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the eight report sections",
            "outro_sub": "Standard investigation format <-> each section maps to a chapter",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helper
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        if bl.width > 12.5:
            bl.scale_to_fit_width(12.5)
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_detective_recap(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("detective_heading", "detective_lines", duration)

    def show_toolbox_meal(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("meal_heading", "meal_lines", duration)

    def show_tool_mapping(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("mapping_heading", "mapping_lines", duration)

    def show_narrative_thread(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("thread_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        labels = self.t("thread_chain")
        accents = [ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GREEN, ERROR_RED]
        boxes = VGroup()
        for i, lab in enumerate(labels):
            accent = accents[i % len(accents)]
            card = RoundedRectangle(
                corner_radius=0.12,
                width=2.7,
                height=1.5,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(accent),
                stroke_width=2.5,
            )
            txt = Text(lab, font=FONT_CJK, font_size=16, color=TEXT_PRIMARY).move_to(
                card.get_center()
            )
            boxes.add(VGroup(card, txt))
        boxes.arrange(RIGHT, buff=0.55)

        arrows = VGroup()
        for a, b in zip(boxes[:-1], boxes[1:]):
            arrows.add(
                Line(a.get_right(), b.get_left(), color=ManimColor(TEXT_SECONDARY), stroke_width=3)
            )

        chain = VGroup(boxes, arrows)
        if chain.width > 12.6:
            chain.scale_to_fit_width(12.6)
        chain.move_to(UP * 0.2)

        caption = Text(
            self.t("thread_caption"), font=FONT_CJK, font_size=19, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(boxes, lag_ratio=0.2), run_time=1.2)
        self.play(FadeIn(arrows), run_time=0.5)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(FadeOut(VGroup(heading, chain, caption)), run_time=0.5)

    def show_actionable(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("actionable_heading", "actionable_lines", duration)

    def show_main_summary(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_measles(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_measles_heading", "extra_measles_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_context(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", 'slide.add(f"attack rate = {ar:.1%}")'),
            kwargs.get("correct_code", 'slide.add(f"{ar:.1%} vs natl {base:.1%}")'),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_too_many_charts(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "for fig in all_figs: deck.add(fig)"),
            kwargs.get("correct_code", "for fig in key_figs[:5]: deck.add(fig)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_action(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "report = findings"),
            kwargs.get("correct_code", "report = findings + action_items"),
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
