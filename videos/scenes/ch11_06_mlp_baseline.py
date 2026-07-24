"""Ch11-06: MLP baseline - running a PyTorch classifier by hand on 280 rows (Part A Step 1).

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
    Rectangle,
    Text,
    VGroup,
)

from videos.src.base_scene import EpiBaseScene
from videos.src.code_mobjects import (
    ACCENT_BLUE,
    ACCENT_ORANGE,
    FONT_CJK,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BlindSpotBanner,
    ExtraExampleBanner,
)


class Ch11MLPBaselineScene(EpiBaseScene):
    """Tutorial video scene: an MLP baseline for 280-row classification."""

    total_steps: int = 11

    TEXT: dict[str, dict[str, str]] = {
        "zh": {
            "title_main": "MLP baseline：280 筆分類",
            "title_sub": "Part A Step 1：親手跑一次 PyTorch",
            "goal_heading": "這一步在幹嘛？",
            "goal_lines": [
                "任務：二元分類，預測住民會不會感染",
                "欄位、切分跟 Ch10 完全一樣",
                "唯一換的是模型：sklearn → PyTorch",
                "→ 公平對決，誠實回答「DL 佔不佔便宜」",
            ],
            "data_prep_heading": "第一步：把病歷翻譯成張量",
            "data_prep_title": "prep.py",
            "arch_heading": "三層線性層疊出最小神經網路",
            "arch_title": "model.py",
            "params_heading": "多少參數 vs 多少樣本？",
            "params_bar_params": "≈ 700 參數",
            "params_bar_samples": "196 訓練樣本",
            "params_caption": "參數比樣本還多 → 過擬合警訊",
            "train_heading": "訓練迴圈四拍 + 早停法",
            "train_title": "train.py",
            "result_heading": "誠實的結果",
            "result_text": (
                "PyTorch MLP        Val AUC ≈ 0.63\n"
                "Logistic Regression      ≈ 0.6\n"
                "Random Forest            ≈ 0.6\n"
                "→ 小資料上 DL 沒有優勢，跟 sklearn 打平"
            ),
            "split_heading": "切分：train / val / test 鐵三角",
            "split_lines": [
                "train 訓練、val 調參、test 最後驗收",
                "橫斷面（每列獨立）→ shuffle 切沒問題",
                "有時間軸的序列 → 絕不能 shuffle！",
                "→ 未來洩漏留到下一集序列預測細講",
            ],
            "extra_banner_title": "額外範例：再入院風險的表格 MLP",
            "extra_readmit_heading": "同一套食譜，換一個表格任務",
            "extra_readmit_title": "readmission.py",
            "blindspot_banner_title": "MLP baseline 三個新手地雷",
            "outro_heading": "下一集：LSTM / CNN 序列預測",
            "outro_sub": "看 DL 怎麼靠領先指標翻盤",
        },
        "en": {
            "title_main": "MLP Baseline: 280-Row Classification",
            "title_sub": "Part A Step 1: run PyTorch by hand",
            "goal_heading": "What is this step doing?",
            "goal_lines": [
                "task: binary classification, predict infection",
                "same columns and split as Ch10",
                "only the model changes: sklearn -> PyTorch",
                '-> fair fight, an honest answer on "does DL help"',
            ],
            "data_prep_heading": "Step one: translate charts into tensors",
            "data_prep_title": "prep.py",
            "arch_heading": "Three linear layers make a tiny net",
            "arch_title": "model.py",
            "params_heading": "How many params vs how many rows?",
            "params_bar_params": "~700 params",
            "params_bar_samples": "196 train rows",
            "params_caption": "more params than rows -> overfitting red flag",
            "train_heading": "The four-beat loop + early stopping",
            "train_title": "train.py",
            "result_heading": "The honest result",
            "result_text": (
                "PyTorch MLP        Val AUC ~ 0.63\n"
                "Logistic Regression       ~ 0.6\n"
                "Random Forest             ~ 0.6\n"
                "-> on small data DL ties sklearn, no edge"
            ),
            "split_heading": "Split: the train / val / test trio",
            "split_lines": [
                "train to fit, val to tune, test to sign off",
                "cross-sectional (independent rows) -> shuffle is fine",
                "a time axis -> never shuffle!",
                "-> future leakage: covered next, on sequences",
            ],
            "extra_banner_title": "Extra example: a tabular MLP for readmission risk",
            "extra_readmit_heading": "Same recipe, a different tabular task",
            "extra_readmit_title": "readmission.py",
            "blindspot_banner_title": "Three Beginner Blind Spots",
            "outro_heading": "Next: LSTM / CNN sequence forecasting",
            "outro_sub": "watch DL turn it around with a leading indicator",
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

    def show_goal(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(1, self.total_steps)
        self._bullets("goal_heading", "goal_lines", duration)

    def show_data_prep(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(2, self.total_steps)
        code = kwargs.get(
            "code",
            (
                'df["infected"] = df["clinical_severity"].ne("not_ill")\n'
                'X = pd.get_dummies(features).values.astype("float32")\n'
                "X[:, 0] = StandardScaler().fit_transform(X[:, :1]).ravel()\n"
                "idx = np.random.permutation(len(X))   # 橫斷面可 shuffle\n"
                "Xtr, Xval = X[idx[:196]], X[idx[196:]]  # 70 / 30"
            ),
        )
        self._code_block("data_prep_heading", "data_prep_title", code, duration)

    def show_architecture(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(3, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "model = nn.Sequential(\n"
                "    nn.Linear(input_dim, 32), nn.ReLU(),\n"
                "    nn.Linear(32, 16), nn.ReLU(),\n"
                "    nn.Linear(16, 1),   # 輸出 logit，不接 sigmoid\n"
                ")\n"
                "n_params = sum(p.numel() for p in model.parameters())\n"
                'print(n_params, "參數 vs", len(Xtr), "筆樣本")'
            ),
        )
        self._code_block("arch_heading", "arch_title", code, duration)

    def show_params_vs_samples(self, duration: float = 7.0, **kwargs) -> None:
        self.show_step_indicator(4, self.total_steps)

        heading = Text(
            self.t("params_heading"), font=FONT_CJK, font_size=30, color=ACCENT_ORANGE
        ).to_edge(UP, buff=0.8)

        params_bar = Rectangle(
            width=1.3,
            height=3.0,
            fill_color=ManimColor(ACCENT_ORANGE),
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 2.2 + UP * (-1.6 + 1.5))
        samples_bar = Rectangle(
            width=1.3,
            height=0.84,
            fill_color=ManimColor(ACCENT_BLUE),
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 2.2 + UP * (-1.6 + 0.42))

        params_label = Text(
            self.t("params_bar_params"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY
        ).next_to(params_bar, UP, buff=0.25)
        samples_label = Text(
            self.t("params_bar_samples"), font=FONT_CJK, font_size=22, color=TEXT_PRIMARY
        ).next_to(samples_bar, UP, buff=0.25)

        caption = Text(
            self.t("params_caption"), font=FONT_CJK, font_size=20, color=TEXT_SECONDARY
        ).to_edge(DOWN, buff=0.6)

        bars = VGroup(params_bar, samples_bar, params_label, samples_label)

        self.play(FadeIn(heading), run_time=0.4)
        self.play(FadeIn(bars), run_time=0.9)
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(max(0.1, duration - 2.2))
        self.play(FadeOut(VGroup(heading, bars, caption)), run_time=0.5)

    def show_training_loop(self, duration: float = 9.0, **kwargs) -> None:
        self.show_step_indicator(5, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "loss_fn = nn.BCEWithLogitsLoss()\n"
                "opt = torch.optim.Adam(model.parameters(), lr=1e-3)\n"
                "for epoch in range(300):\n"
                "    opt.zero_grad()\n"
                "    loss = loss_fn(model(Xtr), ytr)   # forward\n"
                "    loss.backward(); opt.step()       # backprop + update\n"
                "    if val_loss < best: best, snap = val_loss, save()\n"
                "    else: counter += 1                # early stopping"
            ),
        )
        self._code_block("train_heading", "train_title", code, duration)

    def show_result(self, duration: float = 7.0, **kwargs) -> None:
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

    def show_split_rule(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(7, self.total_steps)
        self._bullets("split_heading", "split_lines", duration)

    # ------------------------------------------------------------------
    # Extra example
    # ------------------------------------------------------------------

    def show_extra_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            ExtraExampleBanner(self.t("extra_banner_title")), duration=duration
        )

    def show_extra_readmission(self, duration: float = 8.0, **kwargs) -> None:
        self.show_step_indicator(8, self.total_steps)
        code = kwargs.get(
            "code",
            (
                "# 換一個表格風險任務：30 天再入院預測\n"
                "readmit = nn.Sequential(\n"
                "    nn.Linear(n_feats, 64), nn.ReLU(),\n"
                "    nn.Linear(64, 1),\n"
                ")\n"
                "# 幾萬筆 + 幾十特徵 → DL 才可能贏 logistic"
            ),
        )
        self._code_block("extra_readmit_heading", "extra_readmit_title", code, duration)

    # ------------------------------------------------------------------
    # Blind spots
    # ------------------------------------------------------------------

    def show_blindspot_banner(self, duration: float = 2.0, **kwargs) -> None:
        self.show_section_banner(
            BlindSpotBanner(self.t("blindspot_banner_title")), duration=duration
        )

    def show_blindspot_no_scaling(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(9, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "X = df[num_cols].values  # unscaled"),
            kwargs.get("correct_code", "X = StandardScaler().fit_transform(X)"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_no_zero_grad(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(10, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "loss.backward(); optimizer.step()"),
            kwargs.get("correct_code", "optimizer.zero_grad(); loss.backward()"),
            duration=duration,
        )
        self.play(FadeOut(panel), run_time=0.5)

    def show_blindspot_last_weights(self, duration: float = 6.0, **kwargs) -> None:
        self.show_step_indicator(11, self.total_steps)
        panel = self.show_error_vs_correct(
            kwargs.get("error_code", "model.save()  # last-epoch weights"),
            kwargs.get("correct_code", "model.load_state_dict(best_state)"),
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
