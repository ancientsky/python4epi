# 13 可重現研究與報告

## 你將學到

- 如何用 `uv.lock` 鎖定套件版本，讓「在我電腦上可以跑」變成「在任何人電腦上都可以跑」
- 什麼是**決定論（determinism）**，以及為什麼固定**亂數種子（seed）**是分析能不能重現的關鍵開關
- 如何寫一份**資料欄位契約（schema contract）**，搶在上游資料改動之前把錯誤攔下來
- 如何把整個分析包成**單一命令重跑（single-command workflow）**，讓別人一鍵重現你的結果
- 如何組出一份**最小可驗證報告**：data + code + environment + result 缺一不可

## 情境故事

松柏護理之家退伍軍人症群聚事件的分析終於完成了。
你需要在一週後重新產出同一份疫情報告，並保證同事在另一台機器上得到一致結果。

> 「上次跑出來是 121 人感染、19 人死亡，但我重跑結果不一樣？」

這就是**可重現研究（reproducible research）**要解決的問題——不是「這次答對了沒」，而是「同一份資料、同一份程式碼，換一台機器、換一個人跑，是不是還是同一個答案」。

---

## 🍰 超白話特別篇：可重現研究 = 一份好食譜

> 覺得「可重現研究」聽起來很嚴肅、很學術？別怕。這一段換個方式想：**可重現研究，就是一份寫得夠仔細的食譜。**

朋友吃到你做的蛋糕驚為天人，跟你要食譜，回家想做出一模一樣的味道。你會給她什麼？

- **食譜（recipe）＝ code**：每一步驟都寫成看得懂、能照做的文字——不是「憑感覺加糖」，是「120 克糖」。分析程式碼也一樣，每個轉換步驟都該是一行可重跑的程式，而不是「我印象中好像有刪掉幾筆怪怪的資料」。
- **食材（ingredients）＝ data**：同一款麵粉、同一顆蛋——食材換了，味道就不一樣了。分析也一樣，用的是同一份原始資料，而且**不會做到一半偷偷改掉卻不留紀錄**。
- **廚房設定（kitchen setup）＝ environment（`uv.lock`）**：你家烤箱是 180°C 對流風，朋友家烤箱溫度顯示不準，同一份食譜也可能烤出不同結果。分析的「烤箱設定」就是套件版本——`uv.lock` 把每個套件鎖死到精確版本號，確保大家用的是同一台「烤箱」。
- **骰子先喬好（rigged dice）＝ seed（亂數種子）**：如果食譜裡有一步是「隨機灑上幾顆糖霜球」，兩次做出來擺法當然不同——除非你**先把骰子的點數喬好**（固定 seed），每次都照同樣的「隨機」順序灑。分析裡任何用到隨機的步驟（切訓練/測試集、初始化模型權重）都是同樣的道理。

```{figure} images/reproducibility_recipe.svg
:name: fig-reproducibility-recipe
:alt: 可重現研究的食譜比喻：食譜(code)、食材(data)、廚房設定(environment/uv.lock)、骰子先喬好(seed)四樣東西匯聚成一個加號，任何人任何機器都烤出一模一樣的蛋糕(reproducible result)
:width: 100%

四樣東西備齊——code、data、environment、seed——任何人、任何機器，都烤出同一顆蛋糕。
```

### 比喻 ↔ 技術名詞對照

| 比喻 | 技術名詞 | 一句話 |
|---|---|---|
| 食譜 | **Code**（程式碼／版本控制） | 每一步驟都寫成看得懂、能重跑的程式，不是憑印象在 notebook 裡手動調整 |
| 食材 | **Data**（資料） | 同一份原始資料，不會做到一半偷偷改掉而不留紀錄 |
| 廚房設定 | **Environment**（`uv.lock`） | 套件版本鎖死，不會因為「你家用新版 pandas、我家用舊版」而烤出不同蛋糕 |
| 骰子先喬好 | **Seed**（亂數種子） | 任何用到隨機的步驟（切訓練/測試集、初始化權重、抽樣）都先鎖好種子，隨機才會「隨機地一致」 |
| 蛋糕 | **Reproducible result**（可重現結果） | 任何人、任何機器，照著食譜做出來的成品都一樣 |

> 🎂 說到底，**可重現＝別人能拿你的材料（code + data + environment + seed）複製出同樣的結果，不多不少**——這句話比任何學術定義都好記。

---

<!-- video: ch13_01_repro_intuition -->
<!-- /video -->

## 核心概念

把上一段的食譜比喻翻回正式名詞，可重現研究只圍繞三件事：

- **Environment lock（環境鎖定）**：`uv.lock` 把 `pyproject.toml` 裡每一個相依套件的版本號完整鎖死——不是「大概哪一版」，是精確到 patch 版號。任何人執行 `uv sync`，裝出來的虛擬環境都跟你的一致。
- **Single-command workflow（單一命令重跑）**：從「一份原始資料」到「一份報告」之間，不該有任何只存在你腦中的手動步驟。理想狀態是：別人複製你的 repo、跑幾行固定指令，就能拿到跟你一樣的輸出。
- **Traceability（可追溯性）**：報告裡的每個數字，都要能往回追到「哪一份資料、哪一版程式碼、哪一版套件」算出來的——資料路徑寫死在程式裡、分析邏輯進版本控制、輸出結果連同版本資訊一起存檔。

這三件事合起來，就是接下來要示範的「最小可重跑報告」。

## 為什麼我重跑結果不一樣？

```{figure} images/reproducibility_drift.svg
:name: fig-reproducibility-drift
:alt: 為什麼我重跑結果不一樣：左側三個常見地雷（未鎖套件版本、沒固定亂數種子、notebook 手動改資料沒記錄）導致結果隨時間發散；右側三根支柱（uv.lock 鎖版本、固定 seed、所有轉換寫進程式）讓結果穩定收斂一致
:width: 100%

地雷讓每次重跑的結果慢慢「漂移」；三根支柱讓每次重跑都收斂回同一個答案。
```

「上次是 121 人感染、19 人死亡，這次重跑變成別的數字」——多半不是分析邏輯錯了，而是踩到下面三顆地雷的其中一顆。

### 三顆常見地雷

1. **未鎖套件版本**：`pandas` 從 2.0 升級到 2.2，某個函式對缺值或排序的預設處理悄悄改變——同一份程式碼、同一份資料，算出來的數字就是不一樣。
2. **沒固定亂數種子**：只要程式裡有 `train_test_split`、`np.random`、`torch.manual_seed` 這類隨機步驟，沒鎖種子就等於每次執行都重新洗牌一次。下一節會用一個十行程式碼的最小範例直接證明給你看。
3. **notebook 手動改資料，沒記錄**：在 notebook 裡手動刪掉幾列「看起來怪怪的」資料、手動修正一個欄位值，卻沒有寫成程式碼——下次重跑時，那雙手已經忘了自己動過什麼手腳。

### 三根支柱（逐一對應上面三顆地雷）

| 地雷 | 支柱（解法） |
|---|---|
| 未鎖套件版本 | `uv.lock` 把每個套件的版本號鎖死，`uv sync` 保證裝出來的環境跟原作者一致 |
| 沒固定亂數種子 | 每個隨機步驟都指定 seed（`np.random.default_rng(42)`、`random_state=42`、`torch.manual_seed(42)`），隨機才會「隨機地一致」 |
| notebook 手動改資料，沒記錄 | 所有資料轉換（刪列、改值、衍生欄位）都寫成程式碼裡看得見的一行，而不是滑鼠點一點 |

---

<!-- video: ch13_02_why_different_results -->
<!-- /video -->

## 最小可重跑報告：程式碼逐行拆解

一份「最小可重跑報告」要做到：從乾淨環境出發，靠**固定的幾行指令 + 固定的程式碼**，產出跟原作者一模一樣的數字。下面拆成四段：先重建環境並驗證，再產出摘要，然後證明 seed 決定論，最後用 schema contract 把資料結構鎖起來。

### Step 1 — 三行指令，從乾淨環境到報告

```bash
uv sync
uv run pytest
uv run python notebooks/run_sitrep.py
```

> **逐行拆解**：
>
> | 這行指令 | 在做什麼 |
> |---|---|
> | `uv sync` | 依照 `uv.lock` 裡鎖定的版本，把整個虛擬環境重新建起來——不管在哪台機器上跑，裝出來的套件版本都一模一樣 |
> | `uv run pytest` | 在剛建好的環境裡跑單元測試，確認 `epi_learning` 套件的核心函式（`attack_rate`、`case_fatality_rate`…）行為正常——測試通過，才代表「環境是活的、程式是對的」 |
> | `uv run python notebooks/run_sitrep.py` | 真正跑一次分析：讀取 line list、計算 CFR 與侵襲率、輸出各區統計表——這就是本章要的「最小可重跑報告」 |

> 💡 三行指令、零手動步驟，這正是 single-command workflow 的精神：別人不需要問你「還要裝什麼、還要改哪裡」，複製貼上就能重現。

<!-- video: ch13_03_min_reproducible_report -->
<!-- /video -->

### Step 2 — 讀資料、產出摘要：唯一的標準答案

```python
from pathlib import Path
import pandas as pd

path = Path("data/synthetic/legionella_outbreak.csv")
df = pd.read_csv(path)
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)  # 固定規則：非 not_ill 就算感染

summary = {  # 這個 dict 就是這次分析「唯一的標準答案」
    "n_residents": len(df),
    "n_zones": df.groupby(["floor", "wing"]).ngroups,
    "n_infected": int(df["infected"].sum()),
    "n_deaths": int((df["outcome"] == "dead").sum()),
    "attack_rate": f"{df['infected'].mean():.1%}",
    "cfr": f"{(df['outcome'] == 'dead').sum() / df['infected'].sum():.1%}",
}

print("=== 疫情摘要 ===")
for k, v in summary.items():
    print(f"  {k}: {v}")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `path = Path("data/synthetic/legionella_outbreak.csv")` | 用固定路徑鎖定輸入檔——路徑本身也是「可重現」的一部分 |
> | `df = pd.read_csv(path)` | 讀取資料，沒有任何隨機成分，行為完全可預期 |
> | `df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)` | 用固定規則（不是 not_ill 就算感染）衍生欄位，規則寫在程式碼裡，不是憑印象手動標記 |
> | `summary = {...}` | 把所有關鍵數字收進一個 dict，作為這次分析「唯一的標準答案」 |

> 💡 **為什麼強調「確定性」**：`groupby(...).ngroups`、`.sum()`、`.mean()` 都是純數學運算，跟亂數、多執行緒排序、時區這些「隱形變因」無關——這正是可重現研究要追求的：拿掉所有會讓「同一份程式碼、同一份資料」兩次執行結果卻不同的因素。

<!-- video: ch13_04_data_summary_contract -->
<!-- /video -->

### Step 3 — seed 決定論：隨機也要「隨機地一致」

前一步完全沒用到亂數，因為讀資料、算平均數都是確定性運算。但只要分析裡出現「隨機」——像 Ch10 訓練模型時的 `train_test_split`、Ch11 的 `torch.manual_seed`、或任何 `np.random` 抽樣——沒鎖種子就等於每次執行都是不同的實驗。下面用一個最小範例證明：**同一顆種子 → 同樣的亂數；不設種子 → 每次都不同**。

```python
import numpy as np

def sample(seed=None):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 100, 5)


print("seed=42 第一次:", sample(42))
print("seed=42 第二次:", sample(42), "→ 完全一樣（可重現）")
print("沒設種子   :", sample(), "→ 每次都不同（不可重現）")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `rng = np.random.default_rng(seed)` | 建立一個獨立的亂數產生器，`seed` 相同就會產生同樣的亂數序列 |
> | `rng.integers(0, 100, 5)` | 抽 5 個 0-99 的整數，模擬任何「隨機抽樣」的動作 |
> | `sample(42)` 呼叫兩次 | 用同一顆種子跑兩次，驗證輸出是否完全一致 |
> | `sample()`（不給 seed） | 讓亂數產生器用系統熵源初始化，每次執行都不同 |

> 🎲 **這就是為什麼 Ch10 的 `train_test_split(..., random_state=42)`、Ch11 的 `torch.manual_seed(42)` 都要手動鎖種子**——沒鎖種子，模型的訓練/測試切分、權重初始化都會每次不同，同一份程式碼兩次跑出不同的準確率，讓人誤以為程式碼壞了，其實只是忘記固定亂數。

<!-- video: ch13_05_seed_determinism -->
<!-- /video -->

### Step 4 — schema 契約：搶在資料改動之前擋下來

可重現不只是「這次能重跑」，也要確保「以後跑起來還是同一份資料結構」。如果衛生局系統改了欄位名稱、`clinical_severity` 多了新分類、或 `age` 混進了負數，後面所有分析都會悄悄算錯，卻不會報錯。下面重新讀一次原始資料，用 `assert` 明確寫下「我對這份資料的假設」——欄位要在、類別值要在已知範圍內、數值要合理——任何一項不成立就立刻中斷，而不是讓錯誤資料悄悄流進 Step 2 的摘要。

```python
raw = pd.read_csv(path)  # 重新讀一次原始資料，不依賴前面步驟做過的轉換

REQUIRED_COLUMNS = {
    "case_id", "age", "sex", "floor", "wing", "room",
    "clinical_severity", "outcome",
    "symptom_onset_date", "hospitalized", "lab_confirmed",
}
VALID_SEVERITY = {"not_ill", "asymptomatic", "mild", "moderate", "severe"}
VALID_OUTCOME = {"survived", "dead"}

missing_cols = REQUIRED_COLUMNS - set(raw.columns)
assert not missing_cols, f"缺少必要欄位：{missing_cols}"

unexpected_severity = set(raw["clinical_severity"].dropna().unique()) - VALID_SEVERITY
assert not unexpected_severity, f"clinical_severity 出現未知類別：{unexpected_severity}"

unexpected_outcome = set(raw["outcome"].dropna().unique()) - VALID_OUTCOME
assert not unexpected_outcome, f"outcome 出現未知類別：{unexpected_outcome}"

assert pd.api.types.is_numeric_dtype(raw["age"]), "age 欄位型別應為數值"
assert raw["age"].between(0, 120).all(), "age 出現不合理數值（超出 0-120 歲）"

print("✅ schema OK — 欄位、型別、值域都符合預期")
```

> **逐行拆解**：
>
> | 這行程式 | 在做什麼 |
> |---|---|
> | `REQUIRED_COLUMNS = {...}` | 列出這份分析依賴的必要欄位，當作契約的第一條 |
> | `missing_cols = REQUIRED_COLUMNS - set(raw.columns)` | 用集合差集找出缺少的欄位，一次列出所有缺漏，不用一個一個試 |
> | `assert not missing_cols, f"..."` | 缺欄位就馬上中斷，錯誤訊息直接告訴你缺了哪些 |
> | `set(raw["clinical_severity"].dropna().unique()) - VALID_SEVERITY` | 檢查類別值有沒有「跑出已知範圍」的新分類 |
> | `raw["age"].between(0, 120).all()` | 檢查數值欄位有沒有超出合理範圍（例如負數或多打一個 0） |

> 🧭 這種檢查在資料科學圈叫 **schema contract**（欄位契約）或 data validation——正式專案常用 `pandera`、`great_expectations` 等套件把它自動化並整合進 pipeline；這裡用最原始的 `assert` 示範核心概念，重點是**提早抓到上游資料改動**：先假設資料可能會壞，再寫斷言去確認，而不是等分析結果怪怪的才回頭找資料問題。

---

<!-- video: ch13_06_schema_contract -->
<!-- /video -->

## 可重現檢查清單

1. 是否有 `uv.lock`，且能從乾淨環境執行 `uv sync && uv run pytest`。
2. 是否有固定資料欄位契約（schema contract／line list schema），資料一改就能立刻被 `assert` 擋下來。
3. 是否有最小可重跑腳本（例如 `run_sitrep.py`），單一指令從資料跑到報告。
4. 所有隨機步驟是否都鎖了 seed（`np.random.default_rng(seed)`、`random_state=`、`torch.manual_seed()`）。
5. 所有資料轉換是否都寫進程式碼，而不是在 notebook 裡手動改值。
6. 結果是否留下「唯一的標準答案」（例如存成 `summary.csv` / `summary.json`），供下次重跑時 diff 比對。
7. 是否記錄了執行環境版本（Python、pandas、numpy 版本號），供比對排錯。

## 練習題

- 作業版：[`13_reproducibility_exercise.ipynb`](exercises/13_reproducibility_exercise.ipynb)
- 解答版（講師）：[`13_reproducibility_solution.ipynb`](solutions/13_reproducibility_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/13_reproducibility_solution.ipynb>)

## 常見誤用

| 錯誤 | 正確做法 |
|------|----------|
| 在 notebook 手動改資料卻不記錄 | 所有轉換寫在程式碼中，改資料的邏輯本身就是文件 |
| 只分享結果圖，不分享程式 | 附上可重跑程式與版本資訊，讓別人能自行驗證 |
| 未鎖定套件版本 | 用 `uv.lock` 固定環境，`uv sync` 一次裝到位 |
| 亂數種子未固定 | 設定 `random_state=`、`np.random.default_rng(seed)` 或 `torch.manual_seed()` |
| 沒有資料契約，欄位改了也不知道 | 用 `assert`（或 `pandera` 等套件）寫 schema contract，資料一變就報錯 |
| 只把「最終結果」存腦中，中間過程靠記憶 | 摘要與版本資訊都寫進檔案（CSV/JSON），供日後 diff 比對 |
| 用 `pip install` 手動裝套件，蓋掉 `uv.lock` 鎖定的版本 | 一律用 `uv sync` 安裝，不要在鎖定環境外手動裝套件 |
| 只在自己機器上測試過，沒驗證乾淨環境能跑 | CI（`.github/workflows/ci.yml`）在乾淨環境跑一次 `uv sync && uv run pytest` 才算過關 |

## 下一步

這章把「可重現」拆成四樣要備齊的材料——code、data、environment、seed——並加上 schema contract 這道防線，確保資料結構一改就能立刻被抓到。
下一章（Ch14），我們把所有技能整合成一個**完整實戰案例** → 疫情調查 SitRep。
