"""Ch11-07: Sequence forecasting with LSTM / CNN - sliding windows to predict ahead (Part A Step 2).

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
    ManimColor,
    Square,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    BG_CARD_ALT,
    BORDER_LIGHT,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch11SequenceScene(EpiBaseScene):
    """Tutorial video scene: LSTM / CNN sequence forecasting with sliding windows."""

    total_steps: int = 10

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "LSTM / CNN 序列預測",
            "title_sub": "滑動視窗，讀一段歷史、預測未來",
            "why_heading": "換一個 DL 真正擅長的任務",
            "why_lines": [
                "280 筆分類，DL 跟 sklearn 打平",
                "護理之家沒有夠長的每日序列",
                "改用合成的每日病例 × 氣溫序列",
                "→ 序列預測，才是牛刀殺牛",
            ],
            "leading_heading": "作弊碼：領先指標",
            "leading_lines": [
                "氣溫是領先指標，比病例早 7 天知道",
                "任務：用過去 21 天，預測 7 天後病例",
                "DGP 藏了非線性、有延遲的交互作用",
                "→ DL 要贏，靠的就是這個領先訊號",
            ],
            "window_heading": "核心動作：滑動視窗",
            "window_input_label": "過去 21 天（輸入）",
            "window_target_label": "7 天後（預測目標）",
            "window_caption": "視窗沿時間一格一格往前滑 → 切出大量「輸入配答案」樣本",
            "window_code_heading": "滑動視窗 + 時間切分（絕不 shuffle）",
            "window_code_title": "windows.py",
            "lstm_heading": "LSTM：有記憶的偵探",
            "lstm_title": "lstm_model.py",
            "result_heading": "跟 naive 基準比 MAE",
            "result_text": (
                "Persistence (naive)   MAE = 2.88\n"
                "LSTM                  MAE = 2.15\n"
                "1D-CNN                MAE = 2.20\n"
                "→ 有領先指標 + 非線性延遲，DL 真的贏了"
            ),
            "extra_banner_title": "額外範例：登革熱每週病例預測",
            "extra_dengue_heading": "從每日搬到每週的登革熱預測",
            "extra_dengue_lines": [
                "把每日資料 resample 成每週病例數",
                "領先指標換成當週氣溫 + 累積雨量",
                "同一套滑動視窗 + LSTM，改預測下週",
                "→ 一樣先跑 persistence，再決定上不上模型",
            ],
            "blindspot_banner_title": "序列預測三個新手地雷",
            "outro_heading": "下一集：現代 DL 全景導覽",
            "outro_sub": "GNN、Transformer、DeepSurv、TSFM",
        },
        "en": {
            "title_main": "Sequence Forecasting with LSTM / CNN",
            "title_sub": "Sliding windows: read history, predict the future",
            "why_heading": "Switch to a task DL is truly good at",
            "why_lines": [
                "280-row classification: DL only tied sklearn",
                "the nursing home has no long daily series",
                "switch to a synthetic daily cases x temperature series",
                "-> sequence forecasting is where the cleaver shines",
            ],
            "leading_heading": "The cheat code: a leading indicator",
            "leading_lines": [
                "temperature leads cases by 7 days",
                "task: use the past 21 days to predict 7 days out",
                "the DGP hides a nonlinear, lagged interaction",
                "-> DL wins only by using this early signal",
            ],
            "window_heading": "The core move: the sliding window",
            "window_input_label": "past 21 days (input)",
            "window_target_label": "7 days out (target)",
            "window_caption": "slide the window forward one step -> many input/answer samples",
            "window_code_heading": "Sliding window + time split (never shuffle)",
            "window_code_title": "windows.py",
            "lstm_heading": "LSTM: the detective with a memory",
            "lstm_title": "lstm_model.py",
            "result_heading": "Compare MAE against the naive baseline",
            "result_text": (
                "Persistence (naive)   MAE = 2.88\n"
                "LSTM                  MAE = 2.15\n"
                "1D-CNN                MAE = 2.20\n"
                "-> leading indicator + lagged nonlinearity: DL wins"
            ),
            "extra_banner_title": "Extra example: weekly dengue case forecasting",
            "extra_dengue_heading": "From daily to weekly dengue forecasting",
            "extra_dengue_lines": [
                "resample the daily data into weekly case counts",
                "swap leading indicators to weekly temp + rainfall",
                "same sliding window + LSTM, predict next week",
                "-> still run persistence first, then decide",
            ],
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: a tour of the modern DL landscape",
            "outro_sub": "GNN, Transformer, DeepSurv, TSFM",
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

    def show_why_sequence(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("why_heading", "why_lines", duration)

    def show_leading_indicator(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        self._bullets("leading_heading", "leading_lines", duration)

    def show_window_diagram(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)

        heading = Text(
            self.t("window_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        n_cells = 19
        input_end = 11  # cells 0..10 are the input window
        target_idx = 18  # last cell is the prediction target
        cell, gap = 0.5, 0.06
        offset = (n_cells - 1) / 2
        squares: list[Square] = []
        for i in range(n_cells):
            if i < input_end:
                fill = ACCENT_BLUE
            elif i == target_idx:
                fill = ACCENT_ORANGE
            else:
                fill = BG_CARD_ALT
            sq = Square(
                side_length=cell,
                fill_color=ManimColor(fill),
                fill_opacity=1,
                stroke_color=ManimColor(BORDER_LIGHT),
                stroke_width=1.5,
            )
            sq.move_to(RIGHT * ((i - offset) * (cell + gap)))
            squares.append(sq)

        strip = VGroup(*squares).move_to(UP * 0.4)
        input_block = VGroup(*squares[:input_end])
        target_sq = squares[target_idx]

        input_label = Text(
            self.t("window_input_label"), font=FONT_CJK, font_size=18, color=ACCENT_BLUE
        ).next_to(input_block, DOWN, buff=0.35)
        target_label = Text(
            self.t("window_target_label"), font=FONT_CJK, font_size=18, color=ACCENT_ORANGE
        ).next_to(target_sq, UP, buff=0.35)

        caption = Text(
            self.t("window_caption"), font=FONT_CJK, font_size=18, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(strip), run_time=0.9)
        self.play(FadeIn(input_label), FadeIn(target_label), run_time=0.6)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.7))
        self.play(
            FadeOut(VGroup(heading, strip, input_label, target_label, caption)), run_time=0.5
        )

    def show_window_code(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "L, H = 21, 7                 # 回看 21 天，預測 7 天後\n"
                "split = n - 60               # 最後 60 天當測試集\n"
                "mu, sd = feats[:split].mean(0), feats[:split].std(0)\n"
                "z = (feats - mu) / sd        # 只用訓練區間標準化\n"
                "\n"
                "def windows(s, e):\n"
                "    X = [z[i - L:i] for i in range(s, e - H)]\n"
                "    y = [z[i + H - 1, 0] for i in range(s, e - H)]\n"
                "    return np.array(X), np.array(y)   # 不 shuffle"
            ),
        )
        self._code_block("window_code_heading", "window_code_title", code, duration)

    def show_lstm_model(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "class LSTMModel(nn.Module):\n"
                "    def __init__(self):\n"
                "        super().__init__()\n"
                "        self.lstm = nn.LSTM(2, 32, batch_first=True)\n"
                "        self.fc = nn.Linear(32, 1)\n"
                "\n"
                "    def forward(self, x):\n"
                "        out, _ = self.lstm(x)       # 讀完 21 天\n"
                "        return self.fc(out[:, -1])  # 取最後記憶 → 預測"
            ),
        )
        self._code_block("lstm_heading", "lstm_title", code, duration)

    def show_result(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(6, self.total_steps)
        h = Text(
            self.t("result_heading"), font=FONT_CJK, font_size=28, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.7)
        self.play(FadeIn(h), run_time=0.4)
        panel = self.show_output(
            kwargs.get("output", self.t("result_text")),
            position=ORIGIN,
        )
        self.wait(max(0.1, duration - 1.2))
        self.play(FadeOut(VGroup(h, panel)), run_time=0.5)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_dengue_weekly(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("extra_dengue_heading", "extra_dengue_lines", duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_shuffle(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "train_test_split(X, y, shuffle=True)"),
            kwargs.get("correct_code", "X_tr = X[idx < split]  # by time"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_scaler_leak(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "mu = feats.mean(0)  # peeks at test"),
            kwargs.get("correct_code", "mu = feats[:split].mean(0)  # train"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_baseline(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "report(lstm_mae)  # no baseline"),
            kwargs.get("correct_code", "assert lstm_mae < persistence_mae"),
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
