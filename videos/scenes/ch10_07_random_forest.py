"""Ch10-07: Random Forest as a smarter model + feature_importances_ (which clue
matters most).

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is read
from ``TEXT`` via ``self.t(key)``; code strings stay identical across languages.
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
    Rectangle,
    RoundedRectangle,
    Square,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    BG_CARD_ALT,
    BORDER_LIGHT,
    FONT_CJK,
    FONT_MONO,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch10RandomForestScene(EpiBaseScene):
    """Tutorial video scene: Random Forest and feature importance."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "隨機森林與特徵重要性",
            "title_sub": "換顆聰明腦袋，再問哪條線索最有用",
            "tree_vs_forest_heading": "換一顆更聰明的腦袋",
            "tvf_logistic": "Logistic\n只能畫一條直線邊界",
            "tvf_trees_label": "Random Forest = 一群決策樹",
            "tvf_vote": "各投一票 → 多數決",
            "tree_vs_forest_caption": "森林抓得到非線性與交互作用，比單一直線靈活",
            "rf_code_heading": "只換 model 那一格",
            "rf_code_title": "random_forest.py",
            "rf_honest_heading": "誠實的結果",
            "rf_honest_output": "RF 5 折 AUC = 0.61 +/- 0.05\n≈ logistic 的 0.62，幾乎追平",
            "rf_honest_caption": "不是 RF 笨，是這 280 筆線索本來就薄——聰明腦袋也變不出沒有的資訊",
            "importance_intro_heading": "哪條線索最有用？feature_importances_",
            "importance_intro_title": "importance.py",
            "importance_bars_heading": "特徵重要性排行榜",
            "imp_f1": "年齡 age",
            "imp_f2": "免疫低下",
            "imp_f3": "淋浴暴露",
            "imp_f4": "COPD",
            "imp_f5": "心衰竭",
            "importance_bars_caption": "掉最多分的線索最重要；但重要 ≠ 有因果（那是 Ch12）",
            "summary_heading": "隨機森林 + 特徵重要性 三重點",
            "summary_lines": [
                "① 森林 = 一群決策樹投票，抓非線性與交互作用",
                "② 換模型只換一格；線索薄時 RF ≈ logistic",
                "③ feature_importances_ 找最有用的線索",
                "→ 重要 ≠ 因果，別急著當介入標的",
            ],
            "extra_banner_title": "額外範例：替可疑污染源排名",
            "extra_source_heading": "換個任務：把可疑污染源排名",
            "extra_source_title": "source_ranking.py",
            "blindspot_banner_title": "隨機森林與特徵重要性 三個新手地雷",
            "outro_heading": "下一集：模型動物園、集成與 SHAP",
            "outro_sub": "把黑盒模型解釋給醫師聽",
        },
        "en": {
            "title_main": "Random Forest & Feature Importance",
            "title_sub": "A smarter brain, then which clue matters most",
            "tree_vs_forest_heading": "Swap in a smarter brain",
            "tvf_logistic": "Logistic\nonly draws one straight boundary",
            "tvf_trees_label": "Random Forest = a crowd of trees",
            "tvf_vote": "each votes -> majority wins",
            "tree_vs_forest_caption": "The forest catches nonlinearity and interactions a line cannot",
            "rf_code_heading": "Change only the model cell",
            "rf_code_title": "random_forest.py",
            "rf_honest_heading": "The honest result",
            "rf_honest_output": "RF 5-fold AUC = 0.61 +/- 0.05\nabout the same as logistic's 0.62",
            "rf_honest_caption": "Not that RF is dumb - 280 rows are thin; a smart brain can't invent missing info",
            "importance_intro_heading": "Which clue helps most? feature_importances_",
            "importance_intro_title": "importance.py",
            "importance_bars_heading": "Feature importance ranking",
            "imp_f1": "age",
            "imp_f2": "immunosuppressed",
            "imp_f3": "shower exposure",
            "imp_f4": "COPD",
            "imp_f5": "heart failure",
            "importance_bars_caption": "The clue that drops the most is most important; important != causal (Ch12)",
            "summary_heading": "Random Forest + Importance: 3 Takeaways",
            "summary_lines": [
                "1. Forest = a crowd of trees voting, catches nonlinearity",
                "2. Swap models by one cell; thin signal -> RF is about logistic",
                "3. feature_importances_ finds the most useful clue",
                "-> important != causal, don't rush to intervene",
            ],
            "extra_banner_title": "Extra: ranking suspected outbreak sources",
            "extra_source_heading": "New task: rank the suspected sources",
            "extra_source_title": "source_ranking.py",
            "blindspot_banner_title": "Random Forest & Importance: 3 Beginner Blind Spots",
            "outro_heading": "Next: the model zoo, ensembles, and SHAP",
            "outro_sub": "Explain the black box to a clinician",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _mini_card(
        self,
        text: str,
        *,
        width: float = 4.0,
        height: float = 0.8,
        fill: str = BG_CARD_ALT,
        accent: str = BORDER_LIGHT,
    ) -> VGroup:
        card = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            fill_color=ManimColor(fill),
            fill_opacity=1,
            stroke_color=ManimColor(accent),
            stroke_width=2,
        )
        label = Text(text, font=FONT_CJK, font_size=18, color=ManimColor(TEXT_PRIMARY))
        if label.width > width - 0.4:
            label.scale_to_fit_width(width - 0.4)
        if label.height > height - 0.2:
            label.scale_to_fit_height(height - 0.2)
        label.move_to(card.get_center())
        return VGroup(card, label)

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            .next_to(h, DOWN, buff=0.6)
        )
        self.play(FadeIn(h), run_time=0.5)
        self.play(FadeIn(bl, lag_ratio=0.2), run_time=1.2)
        self.wait(max(0.1, duration - 1.7))
        self.play(FadeOut(VGroup(h, bl)), run_time=0.5)

    def _code_block(self, heading_key: str, title_key: str, code: str, duration: float) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=26, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_code(code, title=self.t(title_key), position=ORIGIN + DOWN * 0.3)
        self.wait(max(0.1, duration - 1.4))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_tree_vs_forest(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        heading = Text(
            self.t("tree_vs_forest_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        left = self._mini_card(
            self.t("tvf_logistic"), width=3.7, height=1.8, accent=ACCENT_BLUE
        )
        trees = VGroup(
            *[
                Square(
                    side_length=0.5,
                    fill_color=ManimColor(ACCENT_GREEN),
                    fill_opacity=0.8,
                    stroke_width=0,
                )
                for _ in range(5)
            ]
        ).arrange(RIGHT, buff=0.15)
        trees_label = Text(
            self.t("tvf_trees_label"), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY
        )
        vote = self._mini_card(self.t("tvf_vote"), width=3.7, height=0.85, accent=ACCENT_ORANGE)
        right = VGroup(trees, trees_label, vote).arrange(DOWN, buff=0.28)

        body = VGroup(left, right).arrange(RIGHT, buff=1.0).move_to(UP * 0.15)
        caption = Text(
            self.t("tree_vs_forest_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(body), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(heading, body, caption)), run_time=0.5)

    def show_rf_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.ensemble import RandomForestClassifier\n"
                "\n"
                "clf_rf = Pipeline([\n"
                '    ("preprocess", preprocess),\n'
                '    ("model", RandomForestClassifier(n_estimators=100)),\n'
                "])\n"
                'scores = cross_val_score(clf_rf, X, y, scoring="roc_auc")'
            ),
        )
        self._code_block("rf_code_heading", "rf_code_title", code, duration)

    def show_rf_honest(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(
            self.t("rf_honest_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel, caption = self.show_output_with_note(
            kwargs.get("output", self.t("rf_honest_output")),
            self.t("rf_honest_caption"),
            position=UP * 0.3,
            font_size=18,
        )
        self.wait(max(0.1, duration - 1.6))
        self.play(FadeOut(VGroup(h, panel, caption)), run_time=0.5)

    def show_importance_intro(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "rf.fit(X, y)\n"
                "imp = rf.feature_importances_\n"
                "rank = pd.Series(imp, index=X.columns)\n"
                "print(rank.sort_values(ascending=False))"
            ),
        )
        self._code_block("importance_intro_heading", "importance_intro_title", code, duration)

    def show_importance_bars(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        heading = Text(
            self.t("importance_bars_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        feats = [self.t(k) for k in ("imp_f1", "imp_f2", "imp_f3", "imp_f4", "imp_f5")]
        vals = [0.28, 0.22, 0.18, 0.12, 0.08]
        colors = [ACCENT_ORANGE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE, ACCENT_BLUE]

        rows = VGroup()
        for i, (name, v, color) in enumerate(zip(feats, vals, colors)):
            bar = Rectangle(
                width=max(v * 9.0, 0.15),
                height=0.42,
                fill_color=ManimColor(color),
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to([-0.3 + bar.width / 2, 0, 0])
            label = Text(name, font=FONT_CJK, font_size=18, color=ManimColor(TEXT_PRIMARY))
            label.next_to(bar, LEFT, buff=0.25)
            valt = Text(f"{v:.2f}", font=FONT_MONO, font_size=16, color=ManimColor(TEXT_SECONDARY))
            valt.next_to(bar, RIGHT, buff=0.2)
            rows.add(VGroup(label, bar, valt).shift(DOWN * i * 0.68))
        rows.move_to(DOWN * 0.15)

        caption = Text(
            self.t("importance_bars_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(rows, lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, rows, caption)), run_time=0.5)

    def show_main_summary(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_source(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'sources = ["cooling_tower", "hot_tub", "shower", "fountain"]\n'
                "rf.fit(X[sources], y)\n"
                "rank = pd.Series(rf.feature_importances_, index=sources)\n"
                "print(rank.sort_values(ascending=False))"
            ),
        )
        self._code_block("extra_source_heading", "extra_source_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_train_auc(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "rf.fit(X, y); score(X, y)  # same!"),
            kwargs.get("correct_code", "cross_val_score(rf, X, y, cv=5)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_impurity_importance(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "imp = rf.feature_importances_"),
            kwargs.get("correct_code", "permutation_importance(rf, X, y)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_importance_causal(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "prevent(top_feature)  # important!"),
            kwargs.get("correct_code", "study_cause(top_feature)  # Ch12"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------

    def show_outro(self, duration: float = 4.0, **kwargs) -> None:
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
