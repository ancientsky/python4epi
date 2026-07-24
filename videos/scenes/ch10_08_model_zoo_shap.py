"""Ch10-08: The model zoo (each with a clinical metaphor), ensembles, and SHAP to
explain the black box to clinicians.

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
    Line,
    ManimColor,
    Rectangle,
    RoundedRectangle,
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


class Ch10ModelZooScene(EpiBaseScene):
    """Tutorial video scene: model zoo, ensembles, and SHAP explanations."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "模型動物園、集成與 SHAP",
            "title_sub": "把黑盒模型解釋給醫師聽",
            "model_zoo_heading": "模型動物園（各配一個臨床比喻）",
            "mz_tree": "決策樹\n= 檢傷分流圖",
            "mz_forest": "隨機森林\n= 多科會診投票（bagging）",
            "mz_xgb": "XGBoost\n= 錯題本補習班（boosting）",
            "mz_lasso": "LASSO\n= 行李限重打包，只留關鍵",
            "model_zoo_caption": "沙盒上 LASSO 線性 AUC≈0.71，樹系≈0.85——非線性 + 交互作用時 ML 才贏",
            "ensemble_heading": "Ensemble：三種集思廣益",
            "ensemble_lines": [
                "Bagging：多棵樹平行投票、降變異（更穩）= 隨機森林",
                "Boosting：接力專攻上一棒殘差、降偏差（更準）= XGBoost",
                "Stacking：總指揮（meta 模型）學何時多聽哪位專家",
                "→ 這就是流病文獻的 Super Learner",
            ],
            "stacking_code_heading": "Stacking = 指揮中心總指揮",
            "stacking_code_title": "stacking.py",
            "shap_intuition_heading": "SHAP：把黑盒解釋給醫師聽",
            "shap_intuition_lines": [
                "用賽局理論的 Shapley value（年終公平分紅）",
                "問：少了這個特徵，預測差多少？",
                "把每個特徵加入 vs 不加入的邊際貢獻平均",
                "→ 能對「單一病人」說明為何被判高風險",
            ],
            "shap_contrib_heading": "解釋單一病人：為何被判高風險",
            "sc_f1": "免疫低下",
            "sc_f2": "用水暴露",
            "sc_f3": "年齡 80",
            "sc_f4": "無慢性病",
            "shap_contrib_caption": "正號往上推、負號往下拉 → 正是解釋黑盒給醫師的語言",
            "summary_heading": "進階 ML 三重點",
            "summary_lines": [
                "① 模型動物園：樹 / 森林 / XGBoost / LASSO 各有脾氣",
                "② 集成集思廣益：bagging 穩、boosting 準、stacking 整合",
                "③ SHAP 把黑盒每條理由量化，講給醫師聽",
                "→ 但 ML 是工具，不是取代流病判斷",
            ],
            "extra_banner_title": "額外範例：跟醫師解釋一個心臟風險分數",
            "extra_doctor_heading": "跟醫師解釋一個風險分數",
            "extra_doctor_title": "explain_to_doctor.py",
            "blindspot_banner_title": "進階 ML 與 SHAP 三個新手地雷",
            "outro_heading": "機器學習完結：能預測，但要謙卑",
            "outro_sub": "下一章 Ch11：PyTorch 深度學習，何時該用 / 不該用",
        },
        "en": {
            "title_main": "The Model Zoo, Ensembles & SHAP",
            "title_sub": "Explain the black box to a clinician",
            "model_zoo_heading": "The model zoo (each with a clinical metaphor)",
            "mz_tree": "Decision Tree\n= ER triage flowchart",
            "mz_forest": "Random Forest\n= multi-specialty vote (bagging)",
            "mz_xgb": "XGBoost\n= error-log cram school (boosting)",
            "mz_lasso": "LASSO\n= packing under a weight limit",
            "model_zoo_caption": "In the sandbox LASSO AUC~0.71, tree models~0.85 - ML wins with nonlinearity",
            "ensemble_heading": "Ensembles: three ways to pool wisdom",
            "ensemble_lines": [
                "Bagging: parallel tree votes, lower variance (steadier) = RF",
                "Boosting: relay-fix the residuals, lower bias (sharper) = XGBoost",
                "Stacking: a meta model learns when to trust which expert",
                "-> This is the Super Learner from the epi literature",
            ],
            "stacking_code_heading": "Stacking = the command-center conductor",
            "stacking_code_title": "stacking.py",
            "shap_intuition_heading": "SHAP: explain the black box to a doctor",
            "shap_intuition_lines": [
                "Uses game theory's Shapley value (fair year-end bonus)",
                "Asks: without this feature, how much does the prediction shift?",
                "Averages each feature's marginal add-vs-skip contribution",
                "-> Can explain, for ONE patient, why they scored high-risk",
            ],
            "shap_contrib_heading": "Explain one patient: why high-risk?",
            "sc_f1": "immunosuppressed",
            "sc_f2": "water exposure",
            "sc_f3": "age 80",
            "sc_f4": "no comorbidity",
            "shap_contrib_caption": "Positive pushes up, negative pulls down -> the doctor's language",
            "summary_heading": "Advanced ML: 3 Takeaways",
            "summary_lines": [
                "1. Model zoo: tree / forest / XGBoost / LASSO each have quirks",
                "2. Ensembles: bagging steadier, boosting sharper, stacking blends",
                "3. SHAP quantifies each reason to explain to a clinician",
                "-> But ML is a tool, not a replacement for epi judgment",
            ],
            "extra_banner_title": "Extra: explaining a heart-risk score to a doctor",
            "extra_doctor_heading": "Explain a risk score to a doctor",
            "extra_doctor_title": "explain_to_doctor.py",
            "blindspot_banner_title": "Advanced ML & SHAP: 3 Beginner Blind Spots",
            "outro_heading": "Machine learning wrapped: predictive, but humble",
            "outro_sub": "Next Ch11: PyTorch deep learning, when to use it or not",
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
            VGroup(*[Text(x, font=FONT_CJK, font_size=22, color=TEXT_PRIMARY) for x in lines])
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

    def show_model_zoo(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        heading = Text(
            self.t("model_zoo_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        c1 = self._mini_card(self.t("mz_tree"), width=5.0, height=1.2, accent=ACCENT_GREEN)
        c2 = self._mini_card(self.t("mz_forest"), width=5.0, height=1.2, accent=ACCENT_BLUE)
        c3 = self._mini_card(self.t("mz_xgb"), width=5.0, height=1.2, accent=ACCENT_ORANGE)
        c4 = self._mini_card(self.t("mz_lasso"), width=5.0, height=1.2, accent=TEXT_SECONDARY)
        grid = VGroup(
            VGroup(c1, c2).arrange(RIGHT, buff=0.4),
            VGroup(c3, c4).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.05)

        caption = Text(
            self.t("model_zoo_caption"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(grid, lag_ratio=0.1), run_time=1.2)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, grid, caption)), run_time=0.5)

    def show_ensemble(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("ensemble_heading", "ensemble_lines", duration)

    def show_stacking_code(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "from sklearn.ensemble import StackingClassifier\n"
                "\n"
                "stack = StackingClassifier(\n"
                '    estimators=[("rf", rf), ("xgb", xgb), ("lasso", lasso)],\n'
                "    final_estimator=LogisticRegression(),\n"
                ")"
            ),
        )
        self._code_block("stacking_code_heading", "stacking_code_title", code, duration)

    def show_shap_intuition(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("shap_intuition_heading", "shap_intuition_lines", duration)

    def show_shap_contributions(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        heading = Text(
            self.t("shap_contrib_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)

        feats = [self.t(k) for k in ("sc_f1", "sc_f2", "sc_f3", "sc_f4")]
        vals = [0.30, 0.20, 0.15, -0.10]

        row_groups = []
        for i, (name, v) in enumerate(zip(feats, vals)):
            w = max(abs(v) * 7.0, 0.1)
            color = ACCENT_ORANGE if v > 0 else ACCENT_BLUE
            bar = Rectangle(
                width=w,
                height=0.42,
                fill_color=ManimColor(color),
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to([w / 2 if v > 0 else -w / 2, 0, 0])
            label = Text(name, font=FONT_CJK, font_size=18, color=ManimColor(TEXT_PRIMARY))
            label.move_to([-3.0, 0, 0])
            valt = Text(
                f"{v:+.2f}", font=FONT_MONO, font_size=16, color=ManimColor(TEXT_SECONDARY)
            )
            valt.next_to(bar, RIGHT if v > 0 else LEFT, buff=0.2)
            row_groups.append(VGroup(label, bar, valt).shift(DOWN * i * 0.7))

        baseline = Line(
            [0, 0.45, 0],
            [0, -0.45 - (len(vals) - 1) * 0.7, 0],
            color=ManimColor(TEXT_SECONDARY),
            stroke_width=2,
        )
        diagram = VGroup(baseline, *row_groups).move_to(DOWN * 0.1)

        caption = Text(
            self.t("shap_contrib_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(diagram, lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.4))
        self.play(FadeOut(VGroup(heading, diagram, caption)), run_time=0.5)

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

    def show_extra_doctor(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "import shap\n"
                "\n"
                "explainer = shap.TreeExplainer(model)\n"
                "sv = explainer.shap_values(one_patient)\n"
                "shap.plots.waterfall(sv[0])"
            ),
        )
        self._code_block("extra_doctor_heading", "extra_doctor_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_complex_small(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "XGBClassifier().fit(X280, y)"),
            kwargs.get("correct_code", "LogisticRegression().fit(X280, y)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_auc_calibration(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "assign_bed(proba)  # AUC is high"),
            kwargs.get("correct_code", "calibration_curve(y, proba)  # first"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_shap_causal(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "intervene(shap_top)  # so change it"),
            kwargs.get("correct_code", "explain_only(shap_top)  # Ch12"),
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
