"""Ch11-02: Neuron, layer, activation - what a neural network actually computes.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. A single neuron does one thing: weighted sum -> add bias ->
activation. Stack neurons into layers and you get "depth".
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    ManimColor,
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


class Ch11NeuronLayerScene(EpiBaseScene):
    """Tutorial video scene: neuron, layer and activation anatomy."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "神經元到底在算什麼",
            "title_sub": "加權加總 → 加 bias → 過 activation",
            "anatomy_heading": "一個 neuron 的解剖圖",
            "anatomy_inputs": ["x1 發燒", "x2 咳嗽", "x3 血氧"],
            "anatomy_weights": ["w1", "w2", "w3"],
            "anatomy_output": "ŷ 輸出",
            "anatomy_caption": "永遠只做這件事：加權加總 → 加 bias → 過 activation",
            "math_heading": "濃縮成一行數學",
            "math_lines": [
                "z = x1·w1 + x2·w2 + … + b",
                "ŷ = ReLU(z) = max(0, z)",
                "weight＝線索可信度，bias＝基準線",
                "activation＝非線性開關",
            ],
            "relu_heading": "activation：ReLU 這道閘門",
            "relu_neg": "z < 0 → 0",
            "relu_pos": "z > 0 → z",
            "relu_caption": "負的歸零，正的原樣放行——沒有它，疊幾層都是一條直線",
            "trap_heading": "拿掉 activation 會怎樣？",
            "trap_lines": [
                "沒有 activation：疊 100 層 Linear",
                "＝ 數學上還是一條直線",
                "每層 Linear 後要配一個 activation",
                "→ 有非線性，才抓得到交互作用",
            ],
            "layer_heading": "neuron 排成排、層疊層＝深度",
            "layer_names": ["輸入層", "隱藏層", "隱藏層", "輸出層"],
            "layer_caption": "層數越多，能表達的函數越複雜（也越容易過擬合）",
            "summary_heading": "神經元四重點",
            "summary_lines": [
                "① neuron＝加權加總 → +bias → activation",
                "② weight＝可信度，bias＝基準線",
                "③ 沒 activation：疊幾層都是一條線",
                "④ neuron 排排、層疊層＝深度",
            ],
            "extra_banner_title": "額外範例：一個症狀風險評分器",
            "extra_scorer_heading": "一個 neuron 就是一顆評分小腦袋",
            "extra_scorer_title": "risk_neuron.py",
            "blindspot_banner_title": "神經元三個新手地雷",
            "outro_heading": "下一集：訓練迴圈",
            "outro_sub": "loss、梯度下降、反向傳播——模型怎麼學乖",
        },
        "en": {
            "title_main": "What a Neuron Actually Computes",
            "title_sub": "weighted sum -> add bias -> activation",
            "anatomy_heading": "Anatomy of One Neuron",
            "anatomy_inputs": ["x1 fever", "x2 cough", "x3 SpO2"],
            "anatomy_weights": ["w1", "w2", "w3"],
            "anatomy_output": "y-hat out",
            "anatomy_caption": "It only ever does: weighted sum -> add bias -> activation",
            "math_heading": "The Whole Thing in One Equation",
            "math_lines": [
                "z = x1*w1 + x2*w2 + ... + b",
                "y_hat = ReLU(z) = max(0, z)",
                "weight = clue trust, bias = baseline",
                "activation = the non-linear switch",
            ],
            "relu_heading": "activation: ReLU, the gate",
            "relu_neg": "z < 0 -> 0",
            "relu_pos": "z > 0 -> z",
            "relu_caption": "Negatives to zero, positives pass - without it, any stack is one line",
            "trap_heading": "What if you drop activation?",
            "trap_lines": [
                "No activation: stack 100 Linear layers",
                "= still one straight line, mathematically",
                "Put an activation after every Linear",
                "-> non-linearity is what catches interactions",
            ],
            "layer_heading": "Neurons in a row, layers stacked = depth",
            "layer_names": ["input", "hidden", "hidden", "output"],
            "layer_caption": "More layers = more complex functions (and easier overfitting)",
            "summary_heading": "Four Takeaways on the Neuron",
            "summary_lines": [
                "1. neuron = weighted sum -> +bias -> activation",
                "2. weight = trust, bias = baseline",
                "3. No activation: any stack collapses to one line",
                "4. Neurons in a row, layers stacked = depth",
            ],
            "extra_banner_title": "Extra example: a symptom risk scorer",
            "extra_scorer_heading": "One neuron = one little scoring brain",
            "extra_scorer_title": "risk_neuron.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: the training loop",
            "outro_sub": "loss, gradient descent, backprop - how it learns",
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

    def show_neuron_anatomy(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        h = Text(self.t("anatomy_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.6
        )

        neuron = Circle(radius=0.65, color=ManimColor(ACCENT_ORANGE), stroke_width=3).move_to(
            RIGHT * 0.3
        )
        neuron.set_fill(ManimColor(BG_CARD), opacity=1)
        nlabel = Text("Σ + b", font=FONT_MONO, font_size=22, color=TEXT_PRIMARY).move_to(
            neuron.get_center()
        )

        in_ys = [1.4, 0.0, -1.4]
        in_names = self.t("anatomy_inputs")
        w_names = self.t("anatomy_weights")
        parts = VGroup(neuron, nlabel)
        for i, y in enumerate(in_ys):
            d = Dot(point=LEFT * 4.3 + UP * y, radius=0.11, color=ManimColor(ACCENT_BLUE))
            nm = Text(in_names[i], font=FONT_CJK, font_size=16, color=TEXT_PRIMARY).next_to(
                d, LEFT, buff=0.2
            )
            ln = Line(
                d.get_center(), neuron.get_left(), color=ManimColor(TEXT_SECONDARY), stroke_width=2
            )
            wl = Text(w_names[i], font=FONT_MONO, font_size=15, color=ACCENT_ORANGE).move_to(
                ln.get_center() + UP * 0.22
            )
            parts.add(d, nm, ln, wl)

        out_dot = Dot(point=RIGHT * 4.6, radius=0.11, color=ManimColor(ACCENT_GREEN))
        out_line = Line(
            neuron.get_right(), out_dot.get_center(), color=ManimColor(TEXT_SECONDARY), stroke_width=2
        )
        act = Text("ReLU", font=FONT_MONO, font_size=16, color=ACCENT_GREEN).move_to(
            out_line.get_center() + UP * 0.25
        )
        out_lbl = Text(self.t("anatomy_output"), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY).next_to(
            out_dot, RIGHT, buff=0.2
        )
        parts.add(out_line, act, out_dot, out_lbl)

        caption = Text(
            self.t("anatomy_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(parts), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.3)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(h, parts, caption)), run_time=0.5)

    def show_neuron_math(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("math_heading", "math_lines", duration)

    def show_activation_relu(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        h = Text(self.t("relu_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )

        # Axes centred on an origin shifted down so the rising arm fits on-screen.
        x_axis = Line(
            LEFT * 3.5 + DOWN * 1.0, RIGHT * 3.0 + DOWN * 1.0, color=ManimColor(BORDER_LIGHT), stroke_width=3
        )
        y_axis = Line(
            DOWN * 1.5, UP * 2.4, color=ManimColor(BORDER_LIGHT), stroke_width=3
        )
        relu_flat = Line(
            LEFT * 3.2 + DOWN * 1.0, ORIGIN + DOWN * 1.0, color=ManimColor(ACCENT_ORANGE), stroke_width=5
        )
        relu_rise = Line(
            ORIGIN + DOWN * 1.0, RIGHT * 2.2 + UP * 1.2, color=ManimColor(ACCENT_ORANGE), stroke_width=5
        )
        neg_lbl = Text(self.t("relu_neg"), font=FONT_MONO, font_size=17, color=TEXT_SECONDARY).move_to(
            LEFT * 1.9 + DOWN * 0.55
        )
        pos_lbl = Text(self.t("relu_pos"), font=FONT_MONO, font_size=17, color=ACCENT_GREEN).move_to(
            RIGHT * 1.7 + UP * 0.9
        )
        graph = VGroup(x_axis, y_axis, relu_flat, relu_rise, neg_lbl, pos_lbl).move_to(UP * 0.1)

        caption = Text(
            self.t("relu_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(graph), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.3)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(h, graph, caption)), run_time=0.5)

    def show_no_activation_trap(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        self._bullets("trap_heading", "trap_lines", duration)

    def show_layer_stack(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        h = Text(self.t("layer_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.6
        )

        counts = [4, 5, 5, 1]
        xs = [-4.5, -1.5, 1.5, 4.5]
        colors = [ACCENT_BLUE, ACCENT_ORANGE, ACCENT_ORANGE, ACCENT_GREEN]
        columns: list[list[Dot]] = []
        dots = VGroup()
        for col, (n, x, c) in enumerate(zip(counts, xs, colors)):
            col_dots = []
            for j in range(n):
                y = (j - (n - 1) / 2) * 0.8
                d = Dot(point=RIGHT * x + UP * y, radius=0.13, color=ManimColor(c))
                col_dots.append(d)
                dots.add(d)
            columns.append(col_dots)

        edges = VGroup()
        for col in range(len(columns) - 1):
            for a in columns[col]:
                for b in columns[col + 1]:
                    edges.add(
                        Line(
                            a.get_center(),
                            b.get_center(),
                            color=ManimColor(BORDER_LIGHT),
                            stroke_width=0.8,
                        )
                    )

        labels = VGroup()
        names = self.t("layer_names")
        for x, name in zip(xs, names):
            labels.add(
                Text(name, font=FONT_CJK, font_size=16, color=TEXT_SECONDARY).move_to(
                    RIGHT * x + DOWN * 2.5
                )
            )

        diagram = VGroup(edges, dots, labels).move_to(UP * 0.15)
        caption = Text(
            self.t("layer_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(edges), run_time=0.7)
        self.play(FadeIn(dots), FadeIn(labels), run_time=0.8)
        self.play(FadeIn(caption), run_time=0.3)
        self.wait(max(0.1, duration - 2.6))
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

    def show_extra_risk_scorer(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "symptoms = [fever, cough, spo2_low]\n"
                "weights  = [1.8, 0.7, 2.1]      # learned trust\n"
                "z = sum(x * w for x, w in zip(symptoms, weights))\n"
                "risk = relu(z + bias)           # one-neuron score"
            ),
        )
        self._code_block("extra_scorer_heading", "extra_scorer_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_missing_activation(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "net = nn.Linear(8,4); nn.Linear(4,1)"),
            kwargs.get("correct_code", "nn.Sequential(lin, nn.ReLU(), lin2)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_scaling(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model(torch.tensor(X_raw))  # unscaled"),
            kwargs.get("correct_code", "X = scaler.transform(X); model(X)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_extra_activation(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "out = torch.relu(model(x))  # regress"),
            kwargs.get("correct_code", "out = model(x)  # keep raw logits"),
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
