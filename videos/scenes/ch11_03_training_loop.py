"""Ch11-03: The training loop - forward, loss, backprop, gradient descent, epoch.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. Every PyTorch model trains on the same four-beat rhythm; one full
pass over the data is an epoch, and gradient descent walks the loss downhill.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
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
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    FONT_CJK,
    FONT_MONO,
)


class Ch11TrainingLoopScene(EpiBaseScene):
    """Tutorial video scene: the four-beat training loop and gradient descent."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "訓練迴圈",
            "title_sub": "forward → loss → backprop → 梯度下降",
            "beats_heading": "訓練迴圈永遠是這四拍",
            "beat_forward": "① forward\n前向猜一次",
            "beat_loss": "② loss\n算錯多少",
            "beat_backprop": "③ backprop\n往回檢討",
            "beat_update": "④ update\n梯度下降",
            "loop_center": "繞一圈\n= 1 epoch",
            "loss_heading": "loss：損失函數",
            "loss_lines": [
                "loss＝猜測與正確答案的差距",
                "數字越小 → 猜得越準",
                "分類：BCEWithLogitsLoss",
                "迴歸：MSELoss",
            ],
            "gd_heading": "梯度下降：走下 loss 山谷",
            "gd_top": "loss 高",
            "gd_bottom": "谷底 = loss 最低",
            "gd_caption": "順著坡度往下，每步微調一點（步伐＝learning rate）",
            "code_heading": "翻成 PyTorch 就這四行",
            "code_title": "train_loop.py",
            "epoch_heading": "跑很多個 epoch，把 loss 壓低",
            "epoch_xlabel": "epoch →",
            "epoch_ylabel": "loss",
            "epoch_caption": "全部資料跑一輪四拍＝1 epoch；一輪一輪往下掉",
            "summary_heading": "訓練迴圈四重點",
            "summary_lines": [
                "① 四拍：forward → loss → backprop → update",
                "② loss＝錯多少，越小越好",
                "③ 梯度下降：順坡往谷底，步伐＝lr",
                "④ 全資料跑一輪＝1 epoch",
            ],
            "extra_banner_title": "額外範例：發燒人數預報器",
            "extra_fever_heading": "同一套四拍，只換 loss",
            "extra_fever_title": "fever_forecast.py",
            "blindspot_banner_title": "訓練迴圈三個新手地雷",
            "outro_heading": "下一集：過擬合與早停法",
            "outro_sub": "train loss 一直降，真的越低越好嗎？",
        },
        "en": {
            "title_main": "The Training Loop",
            "title_sub": "forward -> loss -> backprop -> gradient descent",
            "beats_heading": "The Loop Is Always These Four Beats",
            "beat_forward": "1. forward\nmake a guess",
            "beat_loss": "2. loss\nhow wrong",
            "beat_backprop": "3. backprop\ntrace blame",
            "beat_update": "4. update\nnudge weights",
            "loop_center": "one loop\n= 1 epoch",
            "loss_heading": "loss: the loss function",
            "loss_lines": [
                "loss = gap between guess and truth",
                "smaller number -> better guess",
                "classification: BCEWithLogitsLoss",
                "regression: MSELoss",
            ],
            "gd_heading": "Gradient descent: walk down the loss valley",
            "gd_top": "high loss",
            "gd_bottom": "valley = lowest loss",
            "gd_caption": "Step downhill, nudge a little each time (step size = learning rate)",
            "code_heading": "In PyTorch it's just these four lines",
            "code_title": "train_loop.py",
            "epoch_heading": "Run many epochs, drive the loss down",
            "epoch_xlabel": "epoch ->",
            "epoch_ylabel": "loss",
            "epoch_caption": "One pass over all data = 1 epoch; loss drops round after round",
            "summary_heading": "Four Takeaways on the Loop",
            "summary_lines": [
                "1. Four beats: forward -> loss -> backprop -> update",
                "2. loss = how wrong, smaller is better",
                "3. Gradient descent: downhill to the valley, step = lr",
                "4. One pass over all data = 1 epoch",
            ],
            "extra_banner_title": "Extra example: a fever-count forecaster",
            "extra_fever_heading": "Same four beats, just swap the loss",
            "extra_fever_title": "fever_forecast.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: overfitting and early stopping",
            "outro_sub": "train loss keeps dropping - is lower always better?",
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

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_four_beats(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        h = Text(self.t("beats_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.5
        )

        specs = [
            (UP * 1.55, "beat_forward", ACCENT_BLUE),
            (RIGHT * 3.6, "beat_loss", ACCENT_ORANGE),
            (DOWN * 1.55, "beat_backprop", ACCENT_ORANGE),
            (LEFT * 3.6, "beat_update", ACCENT_GREEN),
        ]
        boxes = VGroup()
        for pos, key, accent in specs:
            card = RoundedRectangle(
                corner_radius=0.12,
                width=2.9,
                height=1.1,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(accent),
                stroke_width=2.5,
            ).move_to(pos)
            lab = Text(
                self.t(key), font=FONT_CJK, font_size=17, color=TEXT_PRIMARY, line_spacing=0.6
            ).move_to(card.get_center())
            boxes.add(VGroup(card, lab))

        ring = VGroup()
        for i in range(len(boxes)):
            a = boxes[i][0].get_center()
            b = boxes[(i + 1) % len(boxes)][0].get_center()
            ring.add(Line(a, b, color=ManimColor(TEXT_SECONDARY), stroke_width=2))

        center = Text(
            self.t("loop_center"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY, line_spacing=0.6
        ).move_to(ORIGIN)

        diagram = VGroup(ring, boxes, center).move_to(DOWN * 0.15)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(ring), run_time=0.6)
        self.play(FadeIn(boxes, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(center), run_time=0.3)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(h, diagram)), run_time=0.5)

    def show_loss_concept(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("loss_heading", "loss_lines", duration)

    def show_gradient_descent(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(self.t("gd_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.6
        )

        def _y(x: float) -> float:
            return 0.32 * x * x - 1.3

        xs = [-3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        pts = [RIGHT * x + UP * _y(x) for x in xs]
        curve = VGroup()
        for i in range(len(pts) - 1):
            curve.add(Line(pts[i], pts[i + 1], color=ManimColor(ACCENT_BLUE), stroke_width=4))

        balls = VGroup()
        for x in [-2.6, -1.8, -1.0, -0.2]:
            balls.add(Dot(point=RIGHT * x + UP * _y(x), radius=0.14, color=ManimColor(ACCENT_ORANGE)))

        top_lbl = Text(self.t("gd_top"), font=FONT_CJK, font_size=17, color=TEXT_SECONDARY).move_to(
            LEFT * 3.0 + UP * 1.9
        )
        bottom_lbl = Text(
            self.t("gd_bottom"), font=FONT_CJK, font_size=17, color=ACCENT_GREEN
        ).move_to(RIGHT * 0.0 + DOWN * 1.9)

        diagram = VGroup(curve, balls, top_lbl, bottom_lbl).move_to(UP * 0.2)
        caption = Text(
            self.t("gd_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(curve), run_time=0.7)
        self.play(FadeIn(balls, lag_ratio=0.3), run_time=0.8)
        self.play(FadeIn(top_lbl), FadeIn(bottom_lbl), FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(h, diagram, caption)), run_time=0.5)

    def show_training_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "optimizer.zero_grad()          # 清掉舊梯度\n"
                "loss = loss_fn(model(X), y)    # forward + 算 loss\n"
                "loss.backward()                # backprop 反向傳播\n"
                "optimizer.step()               # 梯度下降更新"
            ),
        )
        self._code_block("code_heading", "code_title", code, duration)

    def show_epoch_curve(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        h = Text(self.t("epoch_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.6
        )

        xs = [-4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
        ys = [1.7, 1.15, 0.78, 0.5, 0.32, 0.18, 0.08, 0.0, -0.05, -0.08]
        pts = [RIGHT * x + UP * y for x, y in zip(xs, ys)]

        x_axis = Line(
            LEFT * 5.0 + DOWN * 0.5, RIGHT * 5.0 + DOWN * 0.5, color=ManimColor(BORDER_LIGHT), stroke_width=2.5
        )
        y_axis = Line(
            LEFT * 5.0 + DOWN * 0.5, LEFT * 5.0 + UP * 2.0, color=ManimColor(BORDER_LIGHT), stroke_width=2.5
        )
        curve = VGroup()
        for i in range(len(pts) - 1):
            curve.add(Line(pts[i], pts[i + 1], color=ManimColor(ACCENT_BLUE), stroke_width=4))
        dots = VGroup(*[Dot(point=p, radius=0.07, color=ManimColor(ACCENT_BLUE)) for p in pts])

        xlab = Text(self.t("epoch_xlabel"), font=FONT_MONO, font_size=16, color=TEXT_SECONDARY).move_to(
            RIGHT * 3.6 + DOWN * 0.95
        )
        ylab = Text(self.t("epoch_ylabel"), font=FONT_MONO, font_size=16, color=TEXT_SECONDARY).move_to(
            LEFT * 5.6 + UP * 1.6
        )

        diagram = VGroup(x_axis, y_axis, curve, dots, xlab, ylab).move_to(UP * 0.1)
        caption = Text(
            self.t("epoch_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(VGroup(x_axis, y_axis, xlab, ylab)), run_time=0.5)
        self.play(FadeIn(curve), FadeIn(dots), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.3)
        self.wait(max(0.1, duration - 2.3))
        self.play(FadeOut(VGroup(h, diagram, caption)), run_time=0.5)

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

    def show_extra_fever(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "pred = model(X_past14)          # forward: 過去 14 天\n"
                "loss = mse(pred, fever_next7)   # 迴歸用 MSELoss\n"
                "loss.backward(); opt.step()     # 一樣的 backprop + update"
            ),
        )
        self._code_block("extra_fever_heading", "extra_fever_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_zero_grad(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "loss.backward(); opt.step()"),
            kwargs.get("correct_code", "opt.zero_grad(); loss.backward(); opt.step()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_big_lr(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "Adam(model.parameters(), lr=10.0)"),
            kwargs.get("correct_code", "Adam(model.parameters(), lr=1e-3)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_grad(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "val_loss = loss_fn(model(X_val), y_val)"),
            kwargs.get("correct_code", "with torch.no_grad(): model(X_val)"),
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
