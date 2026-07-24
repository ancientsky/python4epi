"""Ch11-04: Overfitting vs generalization, and early stopping.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. Train loss keeps dropping while val loss makes a V-shaped rebound;
early stopping calls it at the val minimum and reloads the best snapshot.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    DashedLine,
    Dot,
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
    BORDER_LIGHT,
    ERROR_RED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    FONT_CJK,
    FONT_MONO,
)


class Ch11OverfittingScene(EpiBaseScene):
    """Tutorial video scene: overfitting, generalization and early stopping."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "過擬合與早停法",
            "title_sub": "train loss 探底，val loss 卻反彈",
            "curves_heading": "最關鍵的一張圖",
            "curves_train": "train loss",
            "curves_val": "val loss",
            "curves_earlystop": "早停點",
            "curves_caption": "train 一路探底，val 先降後升——反彈點就是過擬合的訊號",
            "cards_heading": "死背 vs 舉一反三",
            "overfit_card_title": "Overfitting",
            "overfit_card_body": "把噪音都背起來\n換新資料就崩",
            "generalize_card_title": "Generalization",
            "generalize_card_body": "學到真正的規律\n換新資料照樣準",
            "early_heading": "早停法 early stopping",
            "early_lines": [
                "一邊訓練，一邊盯著 val loss",
                "連續 patience 輪沒刷新紀錄 → 喊停",
                "回頭載入表現最好那次的權重快照",
                "→ 不是用練到最後的權重",
            ],
            "code_heading": "早停法的程式骨架",
            "code_title": "early_stopping.py",
            "ratio_heading": "為什麼 280 筆特別危險",
            "ratio_output": (
                "參數量 ≈ 700，訓練樣本 ≈ 196\n"
                "參數 / 樣本比 ≈ 3.6（> 1）\n"
                "→ 可調旋鈕比資料還多，極易過擬合"
            ),
            "summary_heading": "過擬合與早停 四重點",
            "summary_lines": [
                "① train 探底、val 反彈＝過擬合",
                "② 要的是一般化，不是死背",
                "③ 早停：val 連續沒進步就喊卡",
                "④ 回頭用最佳快照，不用最後一次",
            ],
            "extra_banner_title": "額外範例：會被背起來的迷你疫情資料",
            "extra_tiny_heading": "40 筆腸病毒小群聚",
            "extra_tiny_lines": [
                "只有 40 筆的腸病毒小群聚",
                "配一個大深網 → train 準確率 100%",
                "換一批新病例 → 表現直接崩盤",
                "→ 早停 + 更小模型才救得回來",
            ],
            "blindspot_banner_title": "過擬合三個新手地雷",
            "outro_heading": "下一章（Ch12）：因果推論",
            "outro_sub": "淋浴暴露真的『導致』感染，還是只是相關？",
        },
        "en": {
            "title_main": "Overfitting and Early Stopping",
            "title_sub": "train loss bottoms out, val loss rebounds",
            "curves_heading": "The One Chart That Matters",
            "curves_train": "train loss",
            "curves_val": "val loss",
            "curves_earlystop": "early stop",
            "curves_caption": "train bottoms out, val dips then rises - the rebound is overfitting",
            "cards_heading": "Memorize vs Generalize",
            "overfit_card_title": "Overfitting",
            "overfit_card_body": "memorizes the noise\nnew data -> crash",
            "generalize_card_title": "Generalization",
            "generalize_card_body": "learns the real rule\nnew data -> still sharp",
            "early_heading": "Early stopping",
            "early_lines": [
                "Train while watching the val loss",
                "No new record for patience rounds -> stop",
                "Reload the weight snapshot from the best round",
                "-> not the weights from the last epoch",
            ],
            "code_heading": "The early-stopping skeleton",
            "code_title": "early_stopping.py",
            "ratio_heading": "Why 280 rows is especially risky",
            "ratio_output": (
                "params ~ 700, train rows ~ 196\n"
                "param / sample ratio ~ 3.6 (> 1)\n"
                "-> more knobs than data -> overfits easily"
            ),
            "summary_heading": "Four Takeaways",
            "summary_lines": [
                "1. train bottoms out, val rebounds = overfitting",
                "2. We want generalization, not memorization",
                "3. Early stop: quit when val stalls",
                "4. Reload the best snapshot, not the last one",
            ],
            "extra_banner_title": "Extra example: a tiny outbreak set it memorizes",
            "extra_tiny_heading": "A 40-row enterovirus cluster",
            "extra_tiny_lines": [
                "Just 40 rows in an enterovirus cluster",
                "Plus a big deep net -> train accuracy 100%",
                "New patients -> performance collapses",
                "-> early stopping + a smaller model saves it",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next (Ch12): causal inference",
            "outro_sub": "Did shower exposure 'cause' infection, or just correlate?",
        },
    }

    def construct(self) -> None:
        self.construct_from_segments()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _bullets(self, heading_key: str, lines_key: str, duration: float) -> None:
        heading = self.t(heading_key)
        lines = self.t(lines_key)
        h = Text(heading, font=FONT_CJK, font_size=30, color=ACCENT_ORANGE).to_edge(UP, buff=0.8)
        bl = (
            VGroup(*[Text(x, font=FONT_CJK, font_size=23, color=TEXT_PRIMARY) for x in lines])
            .arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            .next_to(h, DOWN, buff=0.55)
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

    def _cards_row(
        self,
        heading_key: str,
        cards: list[tuple[str, str, str]],
        duration: float,
        *,
        card_w: float = 4.4,
        card_h: float = 2.6,
    ) -> None:
        h = Text(self.t(heading_key), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )
        group = VGroup()
        for accent, title_key, body_key in cards:
            card = RoundedRectangle(
                corner_radius=0.15,
                width=card_w,
                height=card_h,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(accent),
                stroke_width=2.5,
            )
            tt = Text(self.t(title_key), font=FONT_MONO, font_size=22, color=accent, weight="BOLD")
            bb = Text(self.t(body_key), font=FONT_CJK, font_size=18, color=TEXT_PRIMARY)
            inner = VGroup(tt, bb).arrange(DOWN, buff=0.35).move_to(card.get_center())
            group.add(VGroup(card, inner))
        group.arrange(RIGHT, buff=0.6).next_to(h, DOWN, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(group, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(h, group)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_overfitting_curves(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        h = Text(self.t("curves_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )

        xs = [-4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
        train_ys = [1.9, 1.2, 0.6, 0.1, -0.3, -0.6, -0.9, -1.1, -1.3, -1.5]
        val_ys = [1.7, 1.0, 0.4, 0.0, -0.2, 0.0, 0.4, 0.9, 1.4, 1.9]
        train_pts = [RIGHT * x + UP * y for x, y in zip(xs, train_ys)]
        val_pts = [RIGHT * x + UP * y for x, y in zip(xs, val_ys)]

        x_axis = Line(
            LEFT * 5.0 + DOWN * 1.9, RIGHT * 5.0 + DOWN * 1.9, color=ManimColor(BORDER_LIGHT), stroke_width=2.5
        )
        y_axis = Line(
            LEFT * 5.0 + DOWN * 1.9, LEFT * 5.0 + UP * 2.2, color=ManimColor(BORDER_LIGHT), stroke_width=2.5
        )

        train_curve = VGroup()
        for i in range(len(train_pts) - 1):
            train_curve.add(
                Line(train_pts[i], train_pts[i + 1], color=ManimColor(ACCENT_BLUE), stroke_width=4)
            )
        val_curve = VGroup()
        for i in range(len(val_pts) - 1):
            val_curve.add(
                Line(val_pts[i], val_pts[i + 1], color=ManimColor(ACCENT_ORANGE), stroke_width=4)
            )

        earlystop = DashedLine(
            RIGHT * (-0.5) + DOWN * 1.9,
            RIGHT * (-0.5) + UP * 1.7,
            color=ManimColor(TEXT_SECONDARY),
            stroke_width=2.5,
        )
        es_lbl = Text(self.t("curves_earlystop"), font=FONT_CJK, font_size=16, color=ERROR_RED).move_to(
            RIGHT * (-0.5) + UP * 2.0
        )

        train_lbl = Text(self.t("curves_train"), font=FONT_MONO, font_size=16, color=ACCENT_BLUE).next_to(
            train_pts[-1], RIGHT, buff=0.15
        )
        val_lbl = Text(self.t("curves_val"), font=FONT_MONO, font_size=16, color=ACCENT_ORANGE).next_to(
            val_pts[-1], RIGHT, buff=0.15
        )

        diagram = VGroup(
            x_axis, y_axis, train_curve, val_curve, earlystop, es_lbl, train_lbl, val_lbl
        ).move_to(UP * 0.1)
        caption = Text(
            self.t("curves_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(VGroup(x_axis, y_axis)), run_time=0.4)
        self.play(FadeIn(train_curve), FadeIn(train_lbl), run_time=0.7)
        self.play(FadeIn(val_curve), FadeIn(val_lbl), run_time=0.7)
        self.play(FadeIn(earlystop), FadeIn(es_lbl), FadeIn(caption), run_time=0.5)
        self.wait(max(0.1, duration - 3.1))
        self.play(FadeOut(VGroup(h, diagram, caption)), run_time=0.5)

    def show_memorize_vs_generalize(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._cards_row(
            "cards_heading",
            [
                (ERROR_RED, "overfit_card_title", "overfit_card_body"),
                (ACCENT_GREEN, "generalize_card_title", "generalize_card_body"),
            ],
            duration,
        )

    def show_early_stopping(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._bullets("early_heading", "early_lines", duration)

    def show_early_stop_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "if val_loss < best_val:\n"
                "    best_val = val_loss\n"
                "    best_state = snapshot()     # 存最佳快照\n"
                "    counter = 0\n"
                "else:\n"
                "    counter += 1                # 沒進步就累加\n"
                "if counter >= patience:\n"
                "    break                       # 見好就收"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_param_ratio(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        h = Text(self.t("ratio_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(kwargs.get("output", self.t("ratio_output")), position=ORIGIN)
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    def show_main_summary(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_tiny(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_tiny_heading", "extra_tiny_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_train_only(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "acc = model.score(X_train, y_train)"),
            kwargs.get("correct_code", "acc = model.score(X_val, y_val)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_forget_best(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.state_dict()  # last epoch"),
            kwargs.get("correct_code", "model.load_state_dict(best_state)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_watch_train(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "if train_loss > best: stop()"),
            kwargs.get("correct_code", "if val_loss > best: counter += 1"),
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
