"""Ch11-01: Deep-learning intuition - training a rookie detective.

Bilingual scene (zh/en) driven by ``EpiBaseScene.t()``. All on-screen prose is
read from ``TEXT`` via ``self.t(key)``; code strings stay identical across
languages. The running metaphor: a neural network trained the way a rookie
detective is trained on old, already-solved cases.
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
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
    FONT_CJK,
    FONT_MONO,
)


class Ch11DLIntuitionScene(EpiBaseScene):
    """Tutorial video scene: DL intuition via the rookie-detective metaphor."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "深度學習超白話",
            "title_sub": "把訓練神經網路，想成訓練一位新手偵探",
            "detective_heading": "一位新手偵探的養成",
            "detective_lines": [
                "偵探（模型）一開始只能憑直覺亂猜",
                "給他一疊已知結局的舊案（訓練資料）",
                "猜 → 對答案 → 檢討 → 調整判斷",
                "→ 練到看新案子也能猜對七八成",
            ],
            "five_heading": "五句話看懂整套訓練法",
            "five_lines": [
                "neuron：憑直覺對線索加權判斷",
                "training loop：帶答案反覆練習",
                "backprop：往回追查哪一步想錯",
                "early stopping：見好就收不練過頭",
                "deploy：出師，去辦真正的新案",
            ],
            "map_heading": "偵探的世界 ↔ DL 術語",
            "map_neuron_title": "Neuron",
            "map_neuron_body": "線索 × 可信度\n加總後判斷",
            "map_loop_title": "Training loop",
            "map_loop_body": "帶著答案\n反覆練習",
            "map_stop_title": "Early stopping",
            "map_stop_body": "見好就收\n不練過頭",
            "steps_heading": "整套養成 = 一條生產線",
            "steps_top": ["憑直覺猜", "反覆練習", "檢討想錯", "見好就收", "出師上線"],
            "steps_caption": "深度學習再花俏，骨架就是這五步",
            "sledge_heading": "誠實話：牛刀，不是萬靈丹",
            "sledge_lines": [
                "深度學習是牛刀，不是萬靈丹",
                "線索太少（如本書 280 筆）破不了案",
                "資深老偵探（邏輯斯迴歸）反而更快更準",
                "→ 何時該磨這把刀，靠決策框架判斷",
            ],
            "summary_heading": "五句話打包這一集",
            "summary_lines": [
                "① 模型是新手偵探，經驗全靠你餵的舊案",
                "② 訓練迴圈：猜、對答案、檢討、調整",
                "③ backprop：往回追查誰該負責",
                "④ early stopping：獎盃頒給最好那次",
                "⑤ 資料太少，牛刀殺不出優勢",
            ],
            "extra_banner_title": "額外範例：胸部 X 光的肺炎分診",
            "extra_pneumonia_heading": "影像分診 → DL 真正發威",
            "extra_pneumonia_lines": [
                "看一眼胸部 X 光，先分流像肺炎的病人",
                "線索是幾十萬張影像的像素",
                "資料量大、高維非線性 → DL 主場",
                "→ 找 CNN 這位鑑識官來辦最合適",
            ],
            "blindspot_banner_title": "深度學習三個新手地雷",
            "outro_heading": "下一集：neuron、layer、activation",
            "outro_sub": "把比喻翻成技術，看網路到底在算什麼",
        },
        "en": {
            "title_main": "Deep Learning, Plain and Simple",
            "title_sub": "Training a neural net = training a rookie detective",
            "detective_heading": "How a Rookie Detective Is Trained",
            "detective_lines": [
                "The detective (model) starts out just guessing",
                "Give him a stack of already-solved cases (train data)",
                "guess -> check -> review -> adjust judgement",
                "-> until he nails new cases 7-8 times out of 10",
            ],
            "five_heading": "The Whole Training Recipe in Five Lines",
            "five_lines": [
                "neuron: weigh clues by trust, then judge",
                "training loop: drill on cases with answers",
                "backprop: trace back which step went wrong",
                "early stopping: quit while ahead, don't overtrain",
                "deploy: graduate and work real new cases",
            ],
            "map_heading": "Detective World <-> DL Terms",
            "map_neuron_title": "Neuron",
            "map_neuron_body": "clue x trust\nsum then judge",
            "map_loop_title": "Training loop",
            "map_loop_body": "drill with\nthe answers",
            "map_stop_title": "Early stopping",
            "map_stop_body": "quit while\nahead",
            "steps_heading": "The Whole Recipe = an Assembly Line",
            "steps_top": ["guess", "drill", "review", "stop early", "go solo"],
            "steps_caption": "However fancy DL gets, the skeleton is these five steps",
            "sledge_heading": "Honest talk: a sledgehammer, not a cure-all",
            "sledge_lines": [
                "Deep learning is a sledgehammer, not a cure-all",
                "Too few clues (like this book's 280 rows) = no crack",
                "A veteran (logistic regression) is faster and sharper",
                "-> when to swing it: let the decision framework decide",
            ],
            "summary_heading": "This Episode in Five Lines",
            "summary_lines": [
                "1. The model is a rookie - experience is the cases you feed",
                "2. Training loop: guess, check, review, adjust",
                "3. backprop: trace back who's to blame",
                "4. early stopping: the trophy goes to the best run",
                "5. Too little data - the sledgehammer wins nothing",
            ],
            "extra_banner_title": "Extra example: pneumonia chest-X-ray triage",
            "extra_pneumonia_heading": "Image triage -> where DL truly shines",
            "extra_pneumonia_lines": [
                "One glance at a chest X-ray, triage pneumonia-like patients",
                "The clues are pixels across hundreds of thousands of images",
                "Big data, high-dim, non-linear -> DL's home turf",
                "-> call in CNN, the forensic fingerprint expert",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: neuron, layer, activation",
            "outro_sub": "Turn the metaphor into tech - what the net computes",
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

    def _cards_row(
        self,
        heading_key: str,
        cards: list[tuple[str, str, str]],
        duration: float,
        *,
        card_w: float = 3.6,
        card_h: float = 2.4,
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
            tt = Text(self.t(title_key), font=FONT_MONO, font_size=20, color=accent, weight="BOLD")
            bb = Text(self.t(body_key), font=FONT_CJK, font_size=16, color=TEXT_PRIMARY)
            inner = VGroup(tt, bb).arrange(DOWN, buff=0.3).move_to(card.get_center())
            group.add(VGroup(card, inner))
        group.arrange(RIGHT, buff=0.45).next_to(h, DOWN, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(group, lag_ratio=0.2), run_time=1.0)
        self.wait(max(0.1, duration - 1.9))
        self.play(FadeOut(VGroup(h, group)), run_time=0.5)

    # ------------------------------------------------------------------
    # Main lesson
    # ------------------------------------------------------------------

    def show_title(self, duration: float = 3.0, **kwargs) -> None:
        self.show_title_card(self.t("title_main"), self.t("title_sub"), duration=duration)

    def show_detective_metaphor(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("detective_heading", "detective_lines", duration)

    def show_five_sentences(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("five_heading", "five_lines", duration)

    def show_term_mapping(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        self._cards_row(
            "map_heading",
            [
                (ACCENT_ORANGE, "map_neuron_title", "map_neuron_body"),
                (ACCENT_BLUE, "map_loop_title", "map_loop_body"),
                (ACCENT_GREEN, "map_stop_title", "map_stop_body"),
            ],
            duration,
        )

    def show_five_steps(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        h = Text(self.t("steps_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE).to_edge(
            UP, buff=0.7
        )
        top = self.t("steps_top")
        terms = ["neuron", "train loop", "backprop", "early stop", "deploy"]
        boxes = VGroup()
        for i, label in enumerate(top):
            card = RoundedRectangle(
                corner_radius=0.12,
                width=2.1,
                height=1.0,
                fill_color=ManimColor(BG_CARD),
                fill_opacity=1,
                stroke_color=ManimColor(ACCENT_BLUE if i < 4 else ACCENT_GREEN),
                stroke_width=2.5,
            )
            lab = Text(label, font=FONT_CJK, font_size=19, color=TEXT_PRIMARY).move_to(
                card.get_center()
            )
            term = Text(terms[i], font=FONT_MONO, font_size=13, color=TEXT_SECONDARY).next_to(
                card, DOWN, buff=0.15
            )
            boxes.add(VGroup(card, lab, term))
        boxes.arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
        conns = VGroup()
        for i in range(len(boxes) - 1):
            conns.add(
                Line(
                    boxes[i][0].get_right(),
                    boxes[i + 1][0].get_left(),
                    color=ManimColor(TEXT_SECONDARY),
                    stroke_width=2,
                )
            )
        caption = Text(
            self.t("steps_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(h), run_time=0.4)
        self.play(FadeIn(boxes, lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(conns), run_time=0.4)
        self.play(FadeIn(caption), run_time=0.3)
        self.wait(max(0.1, duration - 2.6))
        self.play(FadeOut(VGroup(h, boxes, conns, caption)), run_time=0.5)

    def show_sledgehammer(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        self._bullets("sledge_heading", "sledge_lines", duration)

    def show_main_summary(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        self._bullets("summary_heading", "summary_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_pneumonia(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_pneumonia_heading", "extra_pneumonia_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_baseline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model = DeepNet(); model.fit(X)"),
            kwargs.get("correct_code", "run_baseline_first(X, y)  # decide"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_tiny_data(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "net = BigNet(layers=20)  # 280 rows"),
            kwargs.get("correct_code", "net = LogisticRegression()  # small"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_black_box(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "trust(model.predict(x))  # black box"),
            kwargs.get("correct_code", "explain = shap.DeepExplainer(model)"),
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
