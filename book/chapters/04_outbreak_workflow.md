# 04 群聚調查工作流：從 Line List 到 SitRep

## 情境

松柏護理之家退伍軍人症群聚事件爆發後第三天下午，你的長官說：

> 「兩小時內交出第一份疫情日報（SitRep），內容要包含：多少人感染、哪裡最嚴重、致死率多少、流行曲線長什麼樣。之後每天早上九點前更新。」

你手上有一份 280 筆 × 32 欄的 line list CSV。這一章教你如何用 Python **自動化**產出一份結構化的 SitRep，而且每天只要重跑一次腳本就能更新。

## 你將學到

- 從 raw line list 到 SitRep 的完整自動化流程
- **個資保護（PII protection）**：去識別化技巧、k-anonymity、實務工作流
- 描述性流行病學三要素：**人、時、地**
- 關鍵指標計算：侵襲率、CFR、住院率、ICU 率
- 按個案分類（確診/可能/非個案）分層摘要
- 輸出結構化報告（含表格 + 圖表）
- 把分析流程做成可重跑腳本

## 🩺 超白話特別篇：用「保健室疫調小組長」看懂群聚調查工作流

> FETP 十步驟、line list、SitRep、人時地……這章名詞一大串，是不是有點眼花？別怕。這一段先把護理之家放一邊，讓你當一次**學校保健室的疫調小組長**——把整套「疫情怎麼查」的流程，講到讓國中生也能一手包辦。學會這套流程，本章後面每一個 Step 都只是它的細節放大版。

### 慘了，全班的眼睛一個接一個變紅 👀

開學第二週，保健室排隊的人越來越多——**一堆同學眼睛紅紅、癢癢、還會流眼淚**（急性結膜炎，俗稱「紅眼症」）。校長把你叫去：「查一下！到底怎麼回事、會不會擴散、我該怎麼辦？」

你手上只有一疊亂七八糟的請假單和就診紀錄。**第一個念頭是慌**——但慌沒有用。真正的疫調高手，這時候會做一件事：**打開 SOP，照著食譜一步一步走。**

> 🧑‍🍳 **SOP 是設計給「慌張的你」用的，不是給「冷靜的你」用的。** 愈慌愈容易數錯、賴錯人；照著清單一步一步走，手再抖也不會漏掉「到底誰算生病」這一格。**疫調不是比誰猜得快，是比誰不漏掉。**

### 第一步：先講好「誰才算中鏢」——病例定義

在開始數之前，你得先**畫一條線**：眼睛要多紅、有沒有分泌物、幾天內發生，才算是「這波疫情的一個病例」？這就是**病例定義（case definition）**。

> 🥅 **千萬別邊數邊改標準！** 如果數到一半改規則——昨天不算的今天又算——數字就像橡皮筋任人拉，那不叫調查，那叫喊價。**病例定義就是那條線：線畫在哪，數字就長什麼樣。所以先畫線，再開始數。**

（實務上還會分**確診／可能／非病例**三層，本章正文會細講。）

### 破案三問：人、時、地 🕵️（描述性流行病學）

線畫好、開始造冊（**line list**：一個人一列）之後，你只要一直問三個問題——**人、時、地**：

| 問題 | 白話 | 告訴你什麼 |
|------|------|-----------|
| **人 Person** | 誰中鏢？哪些人、什麼特徵？ | 誰特別容易中 |
| **時 Time** | 哪幾天爆發？高峰在第幾天？ | 大概**何時**被傳染的（畫成**流行曲線**） |
| **地 Place** | 哪間教室最慘？（侵襲率最高） | 去**哪裡**找源頭 |

> 🗺️ **三條線索疊起來，可疑的來源自己會浮出來。** 少問一個，你手上就只有半張藏寶圖。

```{figure} images/school_outbreak_workflow.svg
:name: fig-school-outbreak-workflow
:alt: 學校紅眼症疫調戰情板：上方是 SOP 步驟條（定義病例→人→時→地→SitRep），中間是人時地三面板（人＝紅眼小人 17/60、時＝流行曲線第 3 天高峰、地＝各教室侵襲率 A 班 60% 為熱點且靠飲水機），下方彙整成一頁 SitRep 並橋接到護理之家 280 人的退伍軍人症疫調
:width: 100%

一塊「疫調戰情板」：照 SOP 走 → 問人時地三個問題 → 彙整成一頁 SitRep。最後把同一套流程放大，就是護理之家 280 人的退伍軍人症疫調。
```

### 動手玩玩看：親手做一次「人時地」

```python
import pandas as pd

# 保健室的 line list（造冊）：這波「紅眼症」誰在哪天、在哪間教室發病
line_list = pd.DataFrame({
    "classroom": (["一年一班"] * 12 + ["一年二班"] * 3 + ["一年三班"] * 2),
    "onset_day": [1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 6,   2, 3, 5,   3, 4],
})
class_size = {"一年一班": 20, "一年二班": 30, "一年三班": 10}  # 每班人數不一樣（分母很重要！）

# ── 時 Time：用「發病日」畫流行曲線（不是請假日！），高峰在哪天？──
by_day = line_list["onset_day"].value_counts().sort_index()
print("【時 Time】每日新增病例（迷你流行曲線，用發病日畫）：")
for day, n in by_day.items():
    print(f"  第 {day} 天 | {'█' * n} {n}")
print(f"  → 高峰在第 {by_day.idxmax()} 天\n")

# ── 地 Place：比「侵襲率」，不是比「人數」！──
by_room = line_list["classroom"].value_counts()
ar = by_room / pd.Series(class_size)
print("【地 Place】各教室：病例數 vs 侵襲率（attack rate）")
for room in class_size:
    print(f"  {room} | 病例 {by_room[room]} 人 | {by_room[room]}/{class_size[room]} = {ar[room]:.0%}")
print(f"  → 侵襲率最高：{ar.idxmax()}（去看看這間有什麼特別的！）")
print("     注意：二班病例 3 人 > 三班 2 人，但二班侵襲率 10% < 三班 20%——人多當然病例多，要看比率！\n")

# ── 人 Person／摘要 ──
total_cases, total_students = len(line_list), sum(class_size.values())
print(f"【人 Person／摘要】全校 {total_students} 人，{total_cases} 人發病，總侵襲率 {total_cases/total_students:.0%}")
```

跑出來會看到：

```text
【時 Time】每日新增病例（迷你流行曲線，用發病日畫）：
  第 1 天 | █ 1
  第 2 天 | ███ 3
  第 3 天 | ██████ 6
  第 4 天 | ████ 4
  第 5 天 | ██ 2
  第 6 天 | █ 1
  → 高峰在第 3 天

【地 Place】各教室：病例數 vs 侵襲率（attack rate）
  一年一班 | 病例 12 人 | 12/20 = 60%
  一年二班 | 病例 3 人 | 3/30 = 10%
  一年三班 | 病例 2 人 | 2/10 = 20%
  → 侵襲率最高：一年一班（去看看這間有什麼特別的！）
     注意：二班病例 3 人 > 三班 2 人，但二班侵襲率 10% < 三班 20%——人多當然病例多，要看比率！

【人 Person／摘要】全校 60 人，17 人發病，總侵襲率 28%
```

### 讀出線索：把三張圖疊起來

- **時**：只有**一個高峰**（第 3 天），之後就往下掉 → 這種形狀常代表**大家中的是「同一個來源」**，而不是你傳我、我傳他一直延續。（像不像共用的某個東西？💧）
- **地**：**一年一班侵襲率 60%**，遠高於其他班 → 源頭很可能就在這間教室。
- 你跑去一看：**一年一班門口有一台大家都在用的飲水機。**

> 💧 **等一下——別急著定罪！** 飲水機現在只是「**頭號嫌疑犯**」，不是「兇手」。**描述性分析（人時地）只能「指認嫌疑犯」，不能「定罪」。** 要定罪，得靠後面章節的 2×2 表、迴歸，再加上**環境採檢**（真的從飲水機驗出病菌）。這也正是本書 Ch03、Ch05、Ch06 存在的理由。

### 最後一步：寫一頁 SitRep 交出去

校長沒空聽你講三十分鐘。**SitRep（situation report，戰情報告）就是「一頁講完」的東西**：現在幾個中鏢、集中在哪、比昨天多還少、下一步怎麼辦。

> 📋 **SitRep 不是寫一次就結束——疫情天天變，所以每天更新一版。今天的 SitRep，就是明天決策的起點。** 這也是本章要教你「一支腳本、每天重跑」的原因。

### ⚠️ 四個誠實的但書

1. **描述 ≠ 因果**：人時地畫得再漂亮，也只是「指出嫌疑犯」。飲水機被指認，還要後面用 2×2、迴歸 + 環境採檢去驗證。
2. **流行曲線要用「發病日」畫，不是「請假日」或「通報日」**：用錯日期，高峰會跑掉、你會找錯時間點。（本章正文用的是資料裡的 `symptom_onset_date`，不是 `notification_date`。）
3. **「地」要比「率」不比「數」**：人多的班本來病例就多。一定要除以各班人數（分母），比**侵襲率**才公平——這就是為什麼二班 3 人反而比三班 2 人「還安全」。
4. **照 SOP ≠ 死板**：有些步驟會來回反覆跑；而且**該防治的當下就先做**（先停用飲水機），不用等整個調查做完才動手。救人優先，調查和處置可以平行進行。

### 讀圖小抄（存起來）

| 你看到… | 白話意思 |
|---|---|
| 開始數之前先定義病例 | 先畫線，數字才不會被人喬 |
| 人 Person | 誰中鏢、什麼特徵 |
| 時 Time（流行曲線） | 哪幾天爆、高峰第幾天（用**發病日**畫） |
| 地 Place（各地侵襲率） | 哪裡最慘 → 去哪找源頭（比**率**不比**數**） |
| 流行曲線「單一高峰」 | 常代表同一個共同來源 |
| 侵襲率最高的地點 | 頭號嫌疑，但**還沒定罪** |
| SitRep | 一頁講完的戰情報告，每天更新 |
| 描述性分析 | 產生假設，不是證明因果 |

### 回到真實：紅眼症 → 退伍軍人症

現在把學校場景換成護理之家：

| 學校紅眼症疫情 | 護理之家真實案例 |
|---|---|
| 保健室一筆筆請假／就診紀錄 | 280 筆 line list（一人一列） |
| 「眼睛多紅才算中鏢」先講好 | 病例定義（確診／可能／非病例） |
| 誰中鏢、哪些人 | 人 Person（年齡、性別、共病分布） |
| 哪幾天爆、高峰第 3 天 | 時 Time（流行曲線、`symptom_onset_date`） |
| 哪間教室最慘（A 班 60%） | 地 Place（各樓層／翼區侵襲率） |
| A 班飲水機 → 可疑 | 供水系統 → 待驗證的假設 |
| 回報校長的那一頁 | 每日 SitRep 給指揮官 |

你剛剛在保健室學會的每一招——照 SOP、先定義病例、問人時地、比率不比數、寫一頁 SitRep——**就是本章從 Step 1 到 Step 8 在護理之家 280 人資料上做的事**。現在往下看那套 FETP 十步驟和一個個 Step，是不是突然變親切了？😉

---

## FETP 疫情調查 10 步驟：本章在框架中的位置

疫情調查有一套國際通用、台灣疾管署 FETP 2.0 訓練採用的 **10 步驟系統框架**。本章以第 5 步驟（描述性流行病學）為主軸，同時涵蓋步驟 1、3、4、9、10 的核心概念。

```{figure} images/fetp_10_steps.svg
:name: fig-fetp-10-steps
:alt: FETP 疫情調查 10 步驟框架，標示哪些步驟由 Python 強化
:width: 100%

FETP 疫情調查 10 步驟全景。橘色步驟（5、7）為 Python 能高度自動化的部分；藍色（10）為部分支援；灰色步驟（1、2、3、4、6、8、9）需要現場人為判斷，無法完全由程式替代。**各步驟可同時進行或調整順序，但都不能省略。**
```

## SitRep 的基本架構

一份標準的疫情日報至少包含：

1. **摘要指標**：截至目前的累計數字
2. **人**（Person）：年齡、性別、共病分布
3. **時**（Time）：流行曲線、新增趨勢
4. **地**（Place）：按地點的侵襲率比較
5. **行動建議**：根據數據的初步判斷

---

<!-- video: ch04_01_sitrep_overview -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：SitRep 速成——兩小時交出疫情日報</div>
  <div class="youtube-lite" data-id="p5wes20-Az8">
    <img src="https://img.youtube.com/vi/p5wes20-Az8/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## FETP Step 1：行前準備（出發前要做的事）

在打開任何 CSV 之前，現場調查組應先完成三件事：

### 團隊組成

| 角色 | 職責 | 本次群聚（退伍軍人症）|
|------|------|----------------------|
| 流行病學家 | 設計調查方案、分析資料 | 主責疫調 |
| 實驗室人員 | 採樣、菌株比對 | 痰液 / 水樣 PCR + 培養 |
| 感染管制師 | 院內感染評估、隔離措施 | 評估護理之家動線 |
| 環境衛生人員 | 採樣冷卻水塔、淋浴設備 | 水塔加氯、設備停用 |
| 地方衛生機關 | 協調資源、法規通報 | 衛生局疫調、CDC 通報 |

> 退伍軍人症（*Legionella pneumophila*）不會人傳人，因此**不需要**接觸者隔離人員。若為諾羅病毒等糞口傳播病原，則需增派接觸者追蹤人員。

### 物資清單

出發前確認以下物資就位：

- **採樣**：無菌水樣容器、痰液採集管、環境棉棒、冷藏運送盒
- **個人防護**：N95 口罩、手套、隔離衣（依病原調整）
- **調查工具**：標準化問卷（紙本＋電子備份）、平板電腦、加密 USB
- **通訊**：地方衛生局聯絡人名單、實驗室緊急聯絡電話

### 文獻準備

調查前應閱讀：
1. 該病原的基本特性（潛伏期、傳染途徑、高危族群）
2. 近期類似群聚的調查報告（找環境來源線索）
3. 本機構過去的疫情紀錄（確認是否為反覆暴露）

```{admonition} 退伍軍人症背景知識速查
:class: note
- 病原體：*Legionella pneumophila* 血清型 1（最常見，占 >80%）
- 傳染途徑：吸入含菌氣溶膠（冷卻水塔、淋浴、水療池）
- 不傳人：無症狀傳播疑慮，**不需要**設立隔離病房
- 高危族群：65 歲以上、免疫抑制、慢性肺病、吸菸者
- 致死率：社區型約 5–10%；機構型/重症可達 20–30%
```

---

## Step 1: 讀取與資料準備

```python
import pandas as pd
import matplotlib.pyplot as plt

# ── CJK 字型設定：避免圖表中的中文顯示為方框 □□□ ──
# matplotlib 預設不支援中文，需要指定字型候選清單
# 系統會從左到右逐一嘗試，找到第一個可用的字型就停下
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK TC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "Noto Sans TC", "Microsoft JhengHei",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    "Heiti TC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False  # 修正負號顯示為方框的問題
plt.style.use("ggplot")        # 使用 ggplot 風格（灰底白格線）
plt.rcParams["figure.dpi"] = 150  # 提高輸出解析度，圖表更清晰

# ── 讀取 CSV ──
df = pd.read_csv("data/synthetic/legionella_outbreak.csv")
# df 現在是一個 DataFrame（類似 Excel 試算表）
# 280 列（每位住民一列）× 32 欄（每個欄位一列）

# ── 日期欄位轉換 ──
# CSV 裡的日期是字串（如 "2026-01-15"），必須轉成 datetime 物件才能計算時間差
date_cols = [
    "facility_admission_date", "symptom_onset_date",
    "hospitalization_date", "death_date", "notification_date",
]
for col in date_cols:
    # errors="coerce"：遇到無法解析的值（如空白、亂碼）
    # 不會報錯，而是轉成 NaT（Not a Time，等同日期版的 NaN）
    df[col] = pd.to_datetime(df[col], errors="coerce")

# ── 衍生新欄位 ──
# 建立「是否感染」的 0/1 欄位
# clinical_severity 只要不是 "not_ill"，就算感染（1），否則為 0
# != 比較產生 True/False，astype(int) 將 True→1、False→0
df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

# 建立年齡組：pd.cut 把連續數值切成分類
# bins=[59, 69, 79, 89, 100] 定義切點，區間是左開右閉：(59,69]、(69,79]...
df["age_group"] = pd.cut(
    df["age"], bins=[59, 69, 79, 89, 100],
    labels=["60-69", "70-79", "80-89", "90+"],
)

# 計算每位住民的共病數量
comorbidity_cols = [
    "comorbidity_chf", "comorbidity_dm",
    "comorbidity_cancer", "comorbidity_copd", "immunosuppressed",
]
# 這些欄位都是 0/1，axis=1 代表「橫向加總」（對每一列加總）
# 結果是每位住民有幾個共病
df["n_comorbidities"] = df[comorbidity_cols].sum(axis=1)
```

## Step 1.5: 個資保護 —— 拿到 Line List 的第一件事

實際疫調中，從醫院或長照機構拿到的 line list 往往含有**個人可識別資料（Personally Identifiable Information, PII）**：姓名、身分證字號、電話、住址、病歷號⋯⋯。在進行任何分析、上傳 git、傳給同事之前，**第一件事**就是把 PII 處理掉。這一節示範怎麼用 Python 做。

> 📌 **為什麼本教材的 `legionella_outbreak.csv` 沒有 PII？** 因為它是**合成資料（synthetic data）**，一開始就沒有真實姓名、身分證等欄位——這是教學資料集的標準做法。但你在現場拿到的 raw line list 通常不是這樣，所以要學會下面這些技術。

<!-- video: ch04_08_pii_protection -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：個資保護——拿到 Line List 的第一件事</div>
  <div class="youtube-lite" data-id="LLF1T-EtnqU">
    <img src="https://img.youtube.com/vi/LLF1T-EtnqU/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

```{figure} images/pii_protection_techniques.svg
:name: pii-protection-techniques
:alt: 個資保護流程圖：左邊原始 line list 含 PII，中間五種去識別化技巧，右邊去識別化後的乾淨資料
:width: 100%

拿到 line list → 先區分「直接識別符 / 準識別符 / 敏感屬性」→ 用五種技巧去識別化 → 才開始分析。右下角是實務上的三段式工作流（raw → deidentify.py → deidentified）。
```

### PII 的三種類型

| 類別 | 範例 | 處理原則 |
|------|------|---------|
| **直接識別符（Direct identifiers）** | 姓名、身分證、病歷號、電話、住址、email、照片 | 一律**移除或替換** |
| **準識別符（Quasi-identifiers）** | 年齡、性別、郵遞區號、職業、就醫日期、房號 | 個別看無害，**組合起來**可能識別 → 泛化 |
| **敏感屬性（Sensitive attributes）** | HIV、精神疾病、基因、性取向 | 需特別保護、考慮 k-anonymity |

> ⚠️ **準識別符的陷阱**：Sweeney (2000) 的經典研究顯示，**{ 5 碼郵遞區號 + 出生日期 + 性別 }** 就能唯一識別全美 87% 的人口。年齡 + 性別 + 樓層這樣的組合在護理之家也一樣危險——小群體很容易反推出是誰。

### 五種去識別化技巧（含 Python 實作）

假設原始 line list 有這些欄位：`name`、`national_id`、`phone`、`address`、`room_number`、`age`、`symptom_onset_date`。

#### ① Suppression 移除 —— 最徹底的方式

```python
# 直接刪除不需要的識別欄位
pii_columns = ["name", "national_id", "phone", "address"]
df_safe = df.drop(columns=pii_columns, errors="ignore")
# errors="ignore"：如果某欄位不存在不報錯（防禦性寫法）
```

> 💡 **原則**：分析用不到的 PII 欄位，**直接刪除**就對了。能不留就不留。

#### ② Pseudonymization 假名化 —— 用代號取代真名

```python
# 把原始 ID 替換成序號 CASE_001, CASE_002...
df_safe = df_safe.reset_index(drop=True)
df_safe["case_id"] = ["CASE_" + str(i).zfill(3) for i in range(1, len(df_safe) + 1)]

# 建立「對照表」另存在加密位置（只有授權人員能還原）
mapping = pd.DataFrame({
    "original_id": df["national_id"],
    "case_id": df_safe["case_id"],
})
# mapping.to_csv("data/restricted/id_mapping.csv", index=False)  # 存在加密硬碟
```

> ⚠️ **假名化 ≠ 匿名化**：對照表存在 = 理論上可還原，所以對照表必須**嚴格保密**（另一台加密硬碟、加密壓縮檔、存取權限控管）。

#### ③ Hashing 雜湊 —— 單向不可還原

```python
import hashlib

# 加鹽（salt）雜湊：避免攻擊者用彩虹表（rainbow table）破解
SALT = "松柏護理之家2026"  # 實務上從環境變數 os.environ["PII_SALT"] 讀取，不寫在程式碼裡

def hash_id(raw_id: str, salt: str = SALT) -> str:
    """將原始 ID 加鹽後做 SHA-256 雜湊，取前 12 碼當作 case_id。"""
    combined = (salt + str(raw_id)).encode("utf-8")
    return "H_" + hashlib.sha256(combined).hexdigest()[:12]

df_safe["hashed_id"] = df["national_id"].apply(hash_id)
# A123456789 → "H_4f8a9c2e1b3d"（固定對應，但無法反推原始 ID）
```

> 💡 **為什麼要加鹽（salt）？** 如果直接雜湊身分證，攻擊者用所有可能的身分證字號逐一雜湊比對就能破解。加一段秘密字串（salt）後，他必須先拿到 salt 才能反推，難度大增。

#### ④ Generalization 泛化 —— 把精確值變成區間

```python
# 年齡：具體數字 → 年齡組（已在 Step 1 做了）
df_safe["age_group"] = pd.cut(df["age"], bins=[59, 69, 79, 89, 120],
                               labels=["60-69", "70-79", "80-89", "90+"])

# 日期：具體日期 → 流行病學週（損失資訊但保護隱私）
df_safe["epi_week"] = df["symptom_onset_date"].dt.isocalendar().week

# 房號：具體 1A-101 → 只保留翼區 1A
df_safe["wing"] = df["room_number"].str.split("-").str[0]

# 之後可以刪掉原始精確欄位
df_safe = df_safe.drop(columns=["age", "symptom_onset_date", "room_number"],
                        errors="ignore")
```

#### ⑤ Masking 遮罩 —— 保留格式、隱藏內容

```python
def mask_phone(phone: str) -> str:
    """把電話 0912-345-678 → 0912-***-***（保留前 4 碼的電信業者前綴）"""
    if pd.isna(phone):
        return phone
    parts = str(phone).split("-")
    if len(parts) == 3:
        return f"{parts[0]}-***-***"
    return "***"

df_safe["phone_masked"] = df["phone"].apply(mask_phone)
```

> 💡 什麼時候用 masking 而不是直接刪除？當你要**展示例子**給長官看、或需要格式驗證時，遮罩能保留欄位的「樣子」又不外洩真實值。

### k-anonymity：每個人至少要「混在 k 個人裡」

即使刪掉直接識別符，準識別符的組合還是可能暴露個人身分。**k-anonymity** 是業界常用的量化標準：

> 定義：對於資料表中**任何一筆**紀錄，用「準識別符欄位的組合」去查詢，都要至少有 **k 筆**紀錄符合同樣條件。

```python
# 檢查 (age_group, sex, wing) 這組準識別符的 k-anonymity
quasi_ids = ["age_group", "sex", "wing"]
group_sizes = df_safe.groupby(quasi_ids, observed=True).size()

print("各組合的人數分布：")
print(group_sizes.describe())
print(f"\n最小組的人數（k 值）：{group_sizes.min()}")

# 找出「高風險」的小組（k < 5）
risky = group_sizes[group_sizes < 5]
print(f"\n⚠ 不足 k=5 的組合數：{len(risky)}")
if len(risky) > 0:
    print(risky)
```

**經驗法則**：

| 使用情境 | 建議 k 值 |
|---------|----------|
| 內部分析、封閉使用 | k ≥ 3 |
| 跨單位分享 | k ≥ 5 |
| 敏感族群（兒童、精神疾病等） | k ≥ 10 |
| 公開發表 / 開放資料 | k ≥ 20 |

若某組 n &lt; k，兩種處理方式：
1. **合併群組**（例如把 90+ 併入 80-89 變成 80+）
2. **壓制（suppression）** 該筆紀錄不輸出

### 實務工作流：分離 Raw / Deidentified

```
專案結構
├── data/
│   ├── raw/               ← 只有授權人員能進（加密、權限控管）
│   │   └── line_list_RESTRICTED.csv   ← 原始 PII 資料，.gitignore
│   └── deidentified/      ← 可以進 git、可以分享
│       └── line_list.csv  ← 去識別化後的版本
├── scripts/
│   └── deidentify.py      ← 執行一次，從 raw 產生 deidentified
└── .gitignore             ← 必須包含 data/raw/
```

把 PII 保護程式碼**獨立成腳本**（`deidentify.py`），而不是寫在分析 notebook 裡——這樣：

- 分析 notebook 只讀去識別化後的檔案 → 不會意外把 PII commit 到 git
- 去識別化邏輯集中管理 → 方便稽核、方便修改
- 新資料進來時重跑一次腳本即可

```python
# scripts/deidentify.py 的骨架
from pathlib import Path
import pandas as pd
import hashlib, os

RAW = Path("data/raw/line_list_RESTRICTED.csv")
OUT = Path("data/deidentified/line_list.csv")
SALT = os.environ["PII_SALT"]  # 從環境變數讀，絕不寫在程式碼裡

def main() -> None:
    df = pd.read_csv(RAW)
    df = df.drop(columns=["name", "national_id", "phone", "address"])
    df["case_id"] = ["CASE_" + str(i).zfill(4) for i in range(1, len(df) + 1)]
    df["age_group"] = pd.cut(df["age"], bins=[59, 69, 79, 89, 120],
                              labels=["60-69", "70-79", "80-89", "90+"])
    df = df.drop(columns=["age"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"✓ 已輸出 {len(df)} 筆去識別化資料 → {OUT}")

if __name__ == "__main__":
    main()
```

```{warning}
**絕對不要 commit 的東西：**

- ❌ 原始 line list（含 PII）
- ❌ ID 對照表（mapping.csv）
- ❌ 雜湊用的 salt（寫在 `.env`，`.gitignore` 要排除）
- ❌ 含 PII 的 Jupyter Notebook 執行結果（`nbstripout` 可自動清除輸出）

**必須加入 `.gitignore` 的規則：**
​```
data/raw/
data/restricted/
.env
*.key
​```
```

```{admonition} 台灣法規與國際標準
:class: tip, dropdown

**台灣（Taiwan）：**
- **個人資料保護法（個資法）**：第 6 條（特種個資，含醫療、基因、性生活、健檢、犯罪前科）、第 20 條（特定目的外利用）
- **傳染病防治法**：第 10 條（疫情調查人員保密義務）、第 11 條（個案資料僅供疫情分析與防治使用）
- **人體研究法**：使用病患資料做研究前須經 **IRB（人體試驗委員會）**審查

**國際標準：**
- **HIPAA Safe Harbor（美國）**：列出 18 項必須移除的識別符（18 identifiers）
- **GDPR（歐盟）**：pseudonymization 定義於 Art. 4(5)，k-anonymity 是常用做法

**關鍵文獻：**
- Sweeney L. *k-anonymity: A model for protecting privacy*. IJUFKS 2002;10(5):557-570.
- El Emam K, et al. *A systematic review of re-identification attacks on health data*. PLoS ONE 2011;6(12):e28071.
```

## FETP Step 3：確定診斷——四個期間概念不能混淆

在開始計算侵襲率之前，先釐清與退伍軍人症相關的四個時間概念。這四個概念直接影響**回溯期間設定**（traceback window）和 Ch07 時間序列模型的 lag 選擇。

```{figure} images/incubation_periods.svg
:name: fig-incubation-periods-ch04
:alt: 潛伏期、潛藏期、可傳染期、世代間隔四個概念示意圖
:width: 100%

傳染病四大期間概念。**潛藏期短於潛伏期**時，病人在出現症狀前就已具傳染性（presymptomatic transmission），此時檢疫隔離的判斷依據是潛伏期最大值，而非發病日。
```

| 概念 | 定義 | 退伍軍人症實例 | 疫調意義 |
|------|------|----------------|----------|
| **潛伏期**（incubation period） | 暴露 → 出現症狀 | 2–10 天（通常 5–6 天） | 向後回溯暴露窗口 = 最晚發病日往前推 10 天 |
| **潛藏期**（latent period） | 暴露 → 開始具傳染性 | ≈ 潛伏期（人傳人極罕見） | 決定症狀前傳播風險 |
| **可傳染期**（infectious period） | 開始具傳染性 → 失去傳染性 | 散發（non-communicable），不適用 | 退伍軍人症無人傳人，故可傳染期不影響接觸者追蹤 |
| **世代間隔**（serial interval） | 指標個案發病 → 續發個案發病 | 不適用（人傳人罕見） | 若有人傳人群聚，此值用於推算 R₀ |

> **對本次群聚調查的意義**：
> - 最早發病日為 2026-01-12；最晚為 2026-01-28。
> - 回溯暴露期間（traceback window）= 2026-01-02 至 2026-01-28（最晚發病日往前推 10 天）。
> - 在這段期間內使用過**冷卻水塔、淋浴間、水療池**的住民，即為高度懷疑暴露對象。
> - Ch07 建立時間序列預測模型時，lag 設定預設取潛伏期中位數 5–6 天。

```{seealso}
完整期間概念對照表（含圖解與四種病原實例）：→ {ref}`appendix-f-incubation`
```

---

## Step 2: 摘要指標

```python
total = len(df)                          # 住民總數 = DataFrame 的列數

# df["infected"] 是 0/1 欄位，.sum() 加總 = 感染人數（0 加多少都是 0，只有 1 才有貢獻）
infected = df["infected"].sum()

# == 比較產生 True/False Series，再用 .sum() 計算 True 的數量（True = 1）
confirmed  = (df["case_classification"] == "confirmed").sum()
probable   = (df["case_classification"] == "probable").sum()
hospitalized = df["hospitalized"].sum()  # hospitalized 也是 0/1 欄位
icu          = df["icu_admission"].sum()
deaths       = (df["outcome"] == "dead").sum()

print("=" * 50)
print("松柏護理之家退伍軍人症群聚 — SitRep")
print("=" * 50)
print(f"住民總數：{total}")
# {infected/total:.1%}：除法得到小數，:.1% 自動×100 並加 %，保留 1 位小數
print(f"感染人數：{infected}（侵襲率 {infected/total:.1%}）")
print(f"  確診：{confirmed}　可能：{probable}")
print(f"住院：{hospitalized}（住院率 {hospitalized/infected:.1%}）")
print(f"ICU：{icu}（ICU 率 {icu/hospitalized:.1%}）")
print(f"死亡：{deaths}（CFR {deaths/infected:.1%}）")
```

<!-- video: ch04_02_person -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：描述流行病學（人）——感染者的臉譜</div>
  <div class="youtube-lite" data-id="tmT3YVLy1EM">
    <img src="https://img.youtube.com/vi/tmT3YVLy1EM/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## Step 3: 人 — Person

```python
# 用布林索引篩出感染者：df[條件] 只保留條件為 True 的列
cases = df[df["infected"] == 1]
# cases 是一個新的 DataFrame，只包含 121 位感染住民

print("=== 人口學特徵（感染者）===")
print(f"年齡中位數：{cases['age'].median():.0f} 歲"
      f"（範圍 {cases['age'].min()}-{cases['age'].max()}）")

# .mean() 用在 True/False 上等於計算比例
# (cases['sex'] == 'M') 產生 True/False，mean() 算 True 的比例
print(f"男性比例：{(cases['sex'] == 'M').mean():.1%}")

print(f"\n--- 年齡組分布 ---")
# value_counts()：計算每個類別的出現次數（預設按次數降序排列）
# sort_index()：改成按年齡組的字母/數字順序排列（60-69 → 70-79 → ...）
# to_string()：強制印出全部內容，不因資料太多而省略中間幾行
print(cases["age_group"].value_counts().sort_index().to_string())

print(f"\n--- 共病分布 ---")
for col in comorbidity_cols:
    # 把欄位名稱的前綴 "comorbidity_" 去掉，再轉大寫，變成簡潔的標籤
    # 例如："comorbidity_chf" → "chf" → "CHF"
    label = col.replace("comorbidity_", "").upper()
    n = cases[col].sum()  # 共病欄位是 0/1，sum() 得到有這個共病的人數
    print(f"  {label}: {n} ({n/len(cases):.1%})")
```

<!-- video: ch04_03_time -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：流行曲線——用長條圖抓住疫情的脈搏</div>
  <div class="youtube-lite" data-id="7eBDkfVqsQo">
    <img src="https://img.youtube.com/vi/7eBDkfVqsQo/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## Step 4: 時 — Time

```python
import matplotlib.dates as mdates

# groupby("symptom_onset_date")：以發病日期分組
# .size()：計算每組的列數（= 當天的病例數），等同於 GROUP BY + COUNT(*)
# .rename("cases")：把結果欄位命名為 "cases"，方便後續取用
daily = cases.groupby("symptom_onset_date").size().rename("cases")

# ── 補齊完整日期範圍（含爆發前 3 天作為「背景期」）──
# 原始資料只有有病例的日期；若某天 0 例，就不會出現在 groupby 結果裡
# reindex 可以「補齊」缺少的日期，並用 fill_value=0 填入 0
date_range = pd.date_range(
    daily.index.min() - pd.Timedelta(days=3),  # 往前延伸 3 天（顯示爆發前基線）
    daily.index.max() + pd.Timedelta(days=1),  # 往後延伸 1 天（避免最後一天被截掉）
    freq="D",                                   # freq="D" 表示每天一個點
)
daily = daily.reindex(date_range, fill_value=0)  # 沒有病例的日期補 0

# ── 建立圖表 ──
# plt.subplots() 同時回傳兩個物件：
# fig = 整張畫布（canvas），控制整體大小、解析度、儲存
# ax  = 繪圖區（axes），控制座標軸、標題、長條、折線等內容
fig, ax = plt.subplots(figsize=(10, 4))  # 寬 10 英吋、高 4 英吋

ax.bar(daily.index, daily.values, width=1.0,
       color="#2c7fb8", edgecolor="white", linewidth=0.5)
# width=1.0 讓長條緊貼在一起（流行曲線的標準做法，無間隙）

ax.set_title("松柏護理之家退伍軍人症流行曲線，依發病日，2026 年 1 月",
             fontsize=13, fontweight="bold")
ax.set_xlabel("發病日期（Date of Symptom Onset）")
ax.set_ylabel("病例數（Number of Cases）")

# DateFormatter("%m/%d")：設定 x 軸日期顯示格式
# %m = 月份（01–12），%d = 日期（01–31），結果如 "01/12"
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
# DayLocator(interval=2)：每隔 2 天放一個刻度（避免標籤重疊）
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
# 自動旋轉日期標籤 45 度，防止文字重疊
fig.autofmt_xdate(rotation=45)

# 在最左和最右各留半天（12 小時）的空白邊距，避免第一根和最後一根長條被截掉
ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12),
            daily.index.max() + pd.Timedelta(hours=12))
ax.set_ylim(bottom=0)  # y 軸從 0 開始
# MaxNLocator(integer=True)：y 軸刻度只顯示整數（病例數不可能是 0.5 例）
ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.grid(False)
# 去掉上方和右方的外框線（視覺更簡潔，這是流行病學論文的標準樣式）
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()  # 自動調整間距，防止標題或標籤被裁切
plt.show()

print(f"流行期間：{cases['symptom_onset_date'].min().date()} – {cases['symptom_onset_date'].max().date()}")
# idxmax()：找到數值最大的那個「索引」（日期），而不是最大值本身
# daily.max() 才是最大值（病例數）
print(f"高峰日：{daily.idxmax().date()}（{daily.max()} 例）")
```

<!-- video: ch04_04_place -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：地點比較——哪個翼區最危險？</div>
  <div class="youtube-lite" data-id="wWwHcMXMmG8">
    <img src="https://img.youtube.com/vi/wWwHcMXMmG8/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## Step 5: 地 — Place

```python
# ── 以樓層 + 翼區雙層分組，一次算出所有指標 ──
# .agg() 允許對不同欄位套用不同的聚合函式
# 格式：新欄位名稱=("來源欄位", "聚合函式或 lambda")
wing_stats = (
    df.groupby(["floor", "wing"])
    .agg(
        # "size" 計算每組的總列數（= 該翼區的住民總數，含感染與未感染）
        residents=("case_id", "size"),
        # "infected" 是 0/1 欄位，"sum" 就是感染人數
        infected=("infected", "sum"),
        # lambda 用於自訂邏輯：在 outcome 欄位中，計算值為 "dead" 的個數
        deaths=("outcome", lambda x: (x == "dead").sum()),
    )
    .reset_index()
    # reset_index() 把 groupby 的鍵（floor, wing）從「索引」
    # 變回普通欄位，這樣後面才能用欄位名稱取值
)

# 計算侵襲率（Attack Rate）和致死率（CFR），乘 100 轉成百分比，保留 1 位小數
wing_stats["AR%"] = (wing_stats["infected"] / wing_stats["residents"] * 100).round(1)
wing_stats["CFR%"] = (wing_stats["deaths"] / wing_stats["infected"] * 100).round(1)
# 把樓層（數字）和翼區（字母）拼成一個標籤，例如：1 + "A" → "1A"
# astype(str) 先把整數轉成字串，才能和字母相加
wing_stats["label"] = wing_stats["floor"].astype(str) + wing_stats["wing"]

print("=== 各翼區疫情摘要 ===")
# 選取需要顯示的欄位，to_string(index=False) 印出時不顯示左側的索引數字
print(wing_stats[["label", "residents", "infected", "AR%", "deaths", "CFR%"]]
      .to_string(index=False))
```

<!-- video: ch04_05_classification -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：個案分類——確診、可能和非個案的分層統計</div>
  <div class="youtube-lite" data-id="RZLn3o-svs0">
    <img src="https://img.youtube.com/vi/RZLn3o-svs0/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## FETP Step 4：病例定義——精確度與偵測率的取捨

### 為什麼需要三層病例定義？

疫情初期資訊不足，過窄的病例定義會**漏掉真正的病例**（低敏感度）；過寬的定義則會**納入非病例**（低特異度），導致侵襲率虛高、資源誤配。因此實務上將病例分為三層：

| 層級 | 判斷標準 | 本次群聚（退伍軍人症）| 敏感度 | 特異度 |
|------|----------|----------------------|--------|--------|
| **確診**（confirmed） | 實驗室確認（PCR / 培養 / 尿抗原）| 實驗室陽性 | 低 | 高 |
| **可能**（probable） | 臨床症狀 + 流行病學關聯 | 發燒 + 肺炎影像 + 同樓層暴露 | 中 | 中 |
| **疑似**（suspect） | 僅有部分臨床症狀 | 發燒 + 咳嗽，但無影像或實驗室結果 | 高 | 低 |

> **實務建議**：
> - **疫情初期**：用較寬鬆的「疑似」定義廣撒網，避免漏掉早期病例。
> - **分析階段**：以「確診＋可能」計算侵襲率（如本章 `case_classification != "not_a_case"`）。
> - **公開報告**：明確說明使用哪一層定義，避免數字被斷章取義比較。

### 病例定義的精化過程：以諾羅病毒為例

以下是一個**從寬到窄**精化病例定義的典型過程，說明如何利用敏感度與特異度的取捨：

```
初始定義（廣）：
  「出現腸胃道症狀者」
  → 敏感度高，但同期腸胃炎個案多，特異度低

加入時間條件：
  「2 月 14 日至 2 月 16 日，出現腸胃道症狀者」
  → 縮小範圍，排除背景腸胃炎

加入症狀強度：
  「24 小時內嘔吐 ≥ 2 次或腹瀉 ≥ 3 次」
  → 進一步排除輕症，提升確診率

加入暴露條件（最終定義）：
  「上述症狀者＋2 月 13 日曾參加婚宴」
  → 確診與可能病例定義完整
```

### 本次群聚的病例定義

本教材採用的病例定義（已內建於資料集）：

| 欄位 | 判斷邏輯 |
|------|----------|
| `lab_confirmed = True` | 確診：尿液抗原或培養陽性 |
| `case_classification = "confirmed"` | 確診個案 |
| `case_classification = "probable"` | 臨床符合 + 流行病學關聯 |
| `case_classification = "not_a_case"` | 排除：無症狀且實驗室陰性 |
| `infected = 1` | 確診＋可能之合計（分析主要依據）|

```{seealso}
確診 / 可能 / 疑似病例的標準定義與台灣法定傳染病分類：→ {ref}`appendix-a-glossary`
```

---

## Step 6: 個案分類分層摘要

```python
# 依個案分類（confirmed / probable / not_a_case）分組，計算各層的指標
# 這裡不加 .reset_index()，讓 case_classification 保留為索引，
# 印出時更直觀（分類名稱直接出現在最左欄）
classification = (
    df.groupby("case_classification")
    .agg(
        n=("case_id", "size"),                              # 每類的人數
        hospitalized=("hospitalized", "sum"),               # 住院人數（0/1 欄位加總）
        icu=("icu_admission", "sum"),                       # ICU 人數
        deaths=("outcome", lambda x: (x == "dead").sum()),  # 死亡人數
    )
)

# 計算住院率：住院人數 ÷ 該類別人數 × 100（轉成 %）
# 注意：如果某分類的 n=0，這裡會出現 ZeroDivisionError；
# 真實資料務必先確認各組都有至少 1 人才計算
classification["hosp_rate"] = (
    classification["hospitalized"] / classification["n"] * 100
).round(1)

print("=== 按個案分類分層 ===")
# .to_string() 不帶參數時會保留索引（= case_classification 名稱），方便對照
print(classification.to_string())
```

<!-- video: ch04_06_generate_sitrep -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：函式化——把 SitRep 包成一鍵更新</div>
  <div class="youtube-lite" data-id="ztrZrHwrD2M">
    <img src="https://img.youtube.com/vi/ztrZrHwrD2M/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## Step 7: 輸出結構化 SitRep

把以上所有步驟包成一個函式，每天重跑即可更新：

```python
def generate_sitrep(csv_path):
    """從 CSV 產出 SitRep 摘要字典。

    每天只需重跑此函式並傳入最新的 CSV，即可自動更新所有指標。
    回傳字典而非直接印出，是因為字典可以被後續的 Step 8（報告輸出）直接取用。
    """
    df = pd.read_csv(csv_path)
    # 只轉換計算上需要日期運算的欄位，減少不必要處理
    for col in ["symptom_onset_date", "hospitalization_date",
                "death_date", "notification_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["infected"] = (df["clinical_severity"] != "not_ill").astype(int)

    total = len(df)
    # int() 將 numpy.int64 轉成 Python 原生 int
    # 原因：pandas / numpy 的 .sum() 回傳的是 numpy 整數型別（numpy.int64）
    # 如果直接放進字典再輸出成 JSON，會引發 JSON 序列化錯誤
    # 養成習慣用 int() 包住，能避免一些難以預期的型別問題
    infected = int(df["infected"].sum())
    deaths = int((df["outcome"] == "dead").sum())

    return {
        "total_residents": total,
        "infected": infected,
        # round(值, 小數位數)：四捨五入到指定位數
        "attack_rate": round(infected / total * 100, 1),
        "deaths": deaths,
        # 防呆：若 infected == 0（尚無感染案例）就回傳 0，避免 ZeroDivisionError
        "cfr": round(deaths / infected * 100, 1) if infected else 0,
        "hospitalized": int(df["hospitalized"].sum()),
        "icu": int(df["icu_admission"].sum()),
    }

sitrep = generate_sitrep("data/synthetic/legionella_outbreak.csv")
# sitrep 是一個 Python 字典（dict），可以直接傳給 Step 8 的報告輸出函式
print(sitrep)
```

<!-- video: ch04_07_report_output -->
```{raw} html
<div class="video-card">
  <div class="video-title">教學影片：專業報告輸出——Dashboard、Word、PPT、PDF 一次搞定</div>
  <div class="youtube-lite" data-id="eAs3K_Z7Hjk">
    <img src="https://img.youtube.com/vi/eAs3K_Z7Hjk/hqdefault.jpg" loading="lazy" alt="教學影片">
  </div>
</div>
```
<!-- /video -->

## Step 8: 產出專業報告

`generate_sitrep()` 回傳的字典就是你的**資料層**。但長官看不懂 Python dict——他要的是一份漂亮的報告。這一步教你用四種格式把分析結果包裝成專業輸出：

| 格式 | 適合場景 | Python 套件 |
|------|---------|------------|
| 互動儀表板 | 即時檢視、團隊內部討論 | plotly（已安裝） |
| Word 文件 (.docx) | 交給主管、email 附件 | python-docx |
| 簡報投影片 (.pptx) | 疫調會議簡報 | python-pptx |
| PDF 報告 | 正式歸檔、列印 | fpdf2 |

### 共用前置：儲存圖表與建立輸出資料夾

```python
import pathlib
from io import BytesIO
from datetime import datetime

# exist_ok=True：若資料夾已存在，不會報錯（可以重複執行這行而不出問題）
pathlib.Path("output").mkdir(exist_ok=True)

# ── BytesIO：把圖存進「記憶體裡的虛擬檔案」──
# 一般 fig.savefig("epicurve.png") 會寫到硬碟；
# BytesIO() 則是在記憶體中開一個「假的檔案」，行為和真實檔案物件完全一樣，
# 但資料只存在 RAM，不佔硬碟空間，也不需要事後刪除。
# 好處：DOCX / PPTX 的 add_picture() 都接受 BytesIO 物件，
#       同一份圖可以多次使用（每次使用前記得 .seek(0) 重設讀取位置）。
epicurve_buf = BytesIO()
fig.savefig(epicurve_buf, format="png", dpi=150, bbox_inches="tight")
# seek(0)：把讀取游標移回緩衝區的最開頭
# 類比：把磁帶倒帶回起點，才能從頭播放
# 如果不 seek(0) 直接讀，會從末尾開始讀，得到空資料
epicurve_buf.seek(0)

# strftime 格式字串：%Y=四位年、%m=兩位月、%d=兩位日、%H=時（24h）、%M=分
report_time = datetime.now().strftime("%Y-%m-%d %H:%M")
```

### 8a: 互動式儀表板（Plotly Dashboard）

```{note}
在 JupyterLab / Google Colab 中，以下圖表是**互動的**（可縮放、懸停檢視數值）。在 Jupyter Book 靜態網頁中，你看到的是自動產生的靜態截圖。
```

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# make_subplots 建立 2×2 的子圖網格
# specs 指定每個子圖的類型：
#   "indicator" = 數字指標（大字顯示 KPI）
#   "xy"        = 一般 x-y 座標圖（長條圖、折線圖等）
# subplot_titles 對應每個格子的標題（左上、右上格子標題留空，由 Indicator 自帶）
dashboard = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy"}, {"type": "xy"}],
    ],
    subplot_titles=("", "", "流行曲線（依發病日）", "各翼區侵襲率"),
    vertical_spacing=0.15,   # 上下子圖之間的間距（0–1，比例值）
    horizontal_spacing=0.1,  # 左右子圖之間的間距
)

# ── 左上：感染人數 KPI 指標 ──
# go.Indicator 是 Plotly 的「儀表板指標」圖形，專門顯示一個大數字 + 輔助資訊
# mode="number+delta"：顯示數值 + 變化量（delta）
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=infected,
        title={"text": "感染人數（侵襲率）"},
        # number.suffix 在數字後附加文字（括號裡的侵襲率）
        number={"suffix": f"  ({infected/total:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=1,  # 放在第 1 列、第 1 欄（左上）
)

# ── 右上：死亡人數 KPI 指標 ──
dashboard.add_trace(
    go.Indicator(
        mode="number+delta",
        value=deaths,
        title={"text": "死亡人數（CFR）"},
        number={"suffix": f"  ({deaths/infected:.1%})"},
        delta={"reference": 0, "position": "bottom"},
    ),
    row=1, col=2,  # 放在第 1 列、第 2 欄（右上）
)

# ── 左下：流行曲線（直方式長條圖）──
daily_cases = cases.groupby("symptom_onset_date").size()
dashboard.add_trace(
    go.Bar(
        x=daily_cases.index,    # x 軸：發病日期
        y=daily_cases.values,   # y 軸：每日病例數
        marker_color="#D97757", # Anthropic Orange，視覺上與疾病相關
        name="每日病例數",
    ),
    row=2, col=1,
)

# ── 右下：各翼區侵襲率（水平長條圖，方便比較各翼區）──
dashboard.add_trace(
    go.Bar(
        y=wing_stats["label"],  # y 軸放翼區名稱（水平長條圖的類別軸）
        x=wing_stats["AR%"],    # x 軸放侵襲率數值
        orientation="h",        # "h" = horizontal（水平方向）
        marker_color="#6A9BCC",
        name="侵襲率 %",
        # 在每根長條外側顯示數值標籤
        text=wing_stats["AR%"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
    ),
    row=2, col=2,
)

dashboard.update_layout(
    title_text=f"松柏護理之家退伍軍人症 SitRep Dashboard（{report_time}）",
    height=600,
    showlegend=False,     # 隱藏圖例（各子圖標題已足夠說明）
    template="plotly_white",  # 白底簡潔模板
)
dashboard.show()
```

### 8b: Word 文件（DOCX）

> **注意**：套件名稱是 `python-docx`，但匯入時寫 `from docx import ...`——這是很多新手搞混的地方。

```python
# 注意：套件叫 python-docx（安裝時），但 import 名稱是 docx（沒有 python- 前綴）
from docx import Document
from docx.shared import Inches, Pt  # Inches/Pt：指定尺寸的輔助類別

# Document() 建立一份新的空白 Word 文件
doc = Document()

# ── 標題與時間 ──
# level=1 對應 Word 的「標題 1」（最大的標題）
doc.add_heading("松柏護理之家退伍軍人症 SitRep", level=1)
doc.add_paragraph(f"報告時間：{report_time}")
doc.add_paragraph(
    f"資料來源：legionella_outbreak.csv（{total} 筆住民資料）"
)

# ── 摘要指標表格 ──
doc.add_heading("摘要指標", level=2)
# add_table(rows=6, cols=2)：建立一個 6 行 2 列的表格
# style="Light Grid Accent 1"：套用 Word 內建的表格樣式（淺色網格，第 1 強調色）
table = doc.add_table(rows=6, cols=2, style="Light Grid Accent 1")
metrics = [
    ("住民總數", str(total)),
    ("感染人數", f"{infected}（侵襲率 {infected/total:.1%}）"),
    ("確診", str(confirmed)),
    ("可能病例", str(probable)),
    ("住院", f"{hospitalized}（住院率 {hospitalized/infected:.1%}）"),
    ("死亡", f"{deaths}（CFR {deaths/infected:.1%}）"),
]
# enumerate() 同時取得索引 i 和值（label, value）
for i, (label, value) in enumerate(metrics):
    # table.rows[i] 取第 i 列，.cells[0] 取第 0 格（第一欄）
    table.rows[i].cells[0].text = label
    table.rows[i].cells[1].text = value

# ── 嵌入流行曲線 ──
doc.add_heading("流行曲線", level=2)
epicurve_buf.seek(0)  # 重設 BytesIO 讀取游標（每次讀取前都要 seek(0)）
# width=Inches(6)：圖片寬度設定為 6 英吋（A4 紙寬約 8.27 英吋，去掉左右邊距後約 6 英吋）
doc.add_picture(epicurve_buf, width=Inches(6))

# ── 各翼區統計（表頭 + 資料列）──
doc.add_heading("各翼區疫情摘要", level=2)
# rows=len(wing_stats) + 1：資料列數 + 1 行表頭
wing_table = doc.add_table(
    rows=len(wing_stats) + 1, cols=5, style="Light Grid Accent 1"
)
headers = ["翼區", "住民數", "感染數", "侵襲率%", "CFR%"]
# 填入第 0 列（表頭）
for j, h in enumerate(headers):
    wing_table.rows[0].cells[j].text = h
# 填入資料列（從第 1 列開始，i 是 wing_stats 的索引）
for i, row in wing_stats.iterrows():
    wing_table.rows[i + 1].cells[0].text = str(row["label"])
    wing_table.rows[i + 1].cells[1].text = str(row["residents"])
    wing_table.rows[i + 1].cells[2].text = str(row["infected"])
    wing_table.rows[i + 1].cells[3].text = str(row["AR%"])
    wing_table.rows[i + 1].cells[4].text = str(row["CFR%"])

doc.save("output/sitrep_report.docx")
print("✅ Word 報告已儲存：output/sitrep_report.docx")
```

### 8c: 簡報投影片（PPTX）

```python
from pptx import Presentation
from pptx.util import Inches, Pt  # Inches/Pt：指定位置和大小的輔助類別

prs = Presentation()  # 建立新的空白 PPTX（預設為 16:9 投影片）

# ── 投影片 1：標題頁 ──
# slide_layouts[0] 是 PowerPoint 的「標題投影片」版面（含標題 + 副標題 placeholder）
slide1 = prs.slides.add_slide(prs.slide_layouts[0])
slide1.shapes.title.text = "松柏護理之家退伍軍人症 SitRep"
# placeholders[1] 是副標題 placeholder（index 0 = 主標題，index 1 = 副標題）
slide1.placeholders[1].text = f"報告時間：{report_time}"

# ── 投影片 2：關鍵數據 ──
# slide_layouts[5] 是「空白」版面，沒有任何 placeholder，
# 完全靠我們用 add_textbox() 自行定位內容
slide2 = prs.slides.add_slide(prs.slide_layouts[5])
# add_textbox(left, top, width, height)：用 Inches 指定位置和大小
# 左邊距 1 英吋，上邊距 0.5 英吋，寬 8 英吋，高 1 英吋
txBox = slide2.shapes.add_textbox(
    Inches(1), Inches(0.5), Inches(8), Inches(1),
)
txBox.text_frame.text = "關鍵摘要指標"
txBox.text_frame.paragraphs[0].font.size = Pt(28)  # 28 pt 大標題
txBox.text_frame.paragraphs[0].font.bold = True

# 正文文字方塊（放在標題下方）
body = slide2.shapes.add_textbox(
    Inches(1), Inches(1.8), Inches(8), Inches(4),
)
tf = body.text_frame
tf.word_wrap = True  # 允許自動換行（防止長文字超出邊界）
kpi_lines = [
    f"感染人數：{infected}（侵襲率 {infected/total:.1%}）",
    f"確診：{confirmed}　可能病例：{probable}",
    f"住院：{hospitalized}　ICU：{icu}",
    f"死亡：{deaths}（CFR {deaths/infected:.1%}）",
]
for line in kpi_lines:
    p = tf.add_paragraph()   # 每行文字加一個新段落
    p.text = line
    p.font.size = Pt(20)     # 20 pt 正文字體
    p.space_after = Pt(12)   # 段落後間距 12 pt（等同按一次 Enter）

# ── 投影片 3：流行曲線 ──
slide3 = prs.slides.add_slide(prs.slide_layouts[5])
txBox3 = slide3.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox3.text_frame.text = "流行曲線（依發病日）"
txBox3.text_frame.paragraphs[0].font.size = Pt(24)
txBox3.text_frame.paragraphs[0].font.bold = True

epicurve_buf.seek(0)  # 重設 BytesIO 游標，才能再次讀取圖片資料
# add_picture(image, left, top, width, height)：在指定位置插入圖片
slide3.shapes.add_picture(epicurve_buf, Inches(0.5), Inches(1.3), Inches(9), Inches(5))

# ── 投影片 4：各翼區侵襲率 ──
slide4 = prs.slides.add_slide(prs.slide_layouts[5])
txBox4 = slide4.shapes.add_textbox(
    Inches(1), Inches(0.3), Inches(8), Inches(0.8),
)
txBox4.text_frame.text = "各翼區疫情摘要"
txBox4.text_frame.paragraphs[0].font.size = Pt(24)
txBox4.text_frame.paragraphs[0].font.bold = True

# add_table(rows, cols, left, top, width, height).table 取得表格物件
# 整個呼叫鏈：add_table() 回傳 GraphicFrame，.table 才是可操作的 Table 物件
rows_n = len(wing_stats) + 1  # 資料列 + 1 行表頭
tbl = slide4.shapes.add_table(rows_n, 5, Inches(0.5), Inches(1.3), Inches(9), Inches(4)).table
# 填入表頭（第 0 列）
for j, h in enumerate(["翼區", "住民", "感染", "AR%", "CFR%"]):
    tbl.cell(0, j).text = h
# 填入資料列（從第 1 列開始）
for i, row in wing_stats.iterrows():
    tbl.cell(i + 1, 0).text = str(row["label"])
    tbl.cell(i + 1, 1).text = str(row["residents"])
    tbl.cell(i + 1, 2).text = str(row["infected"])
    tbl.cell(i + 1, 3).text = str(row["AR%"])
    tbl.cell(i + 1, 4).text = str(row["CFR%"])

prs.save("output/sitrep_slides.pptx")
print("✅ 簡報已儲存：output/sitrep_slides.pptx")
```

### 8d: PDF 正式報告（fpdf2）

```python
import pathlib
from fpdf import FPDF

# ── CJK 字型偵測（PDF 不像瀏覽器能自動 fallback，必須手動嵌入字型）──
# fpdf2 預設只有英文字型（Helvetica 等），顯示中文需要嵌入 TTF/TTC 字型檔
# 偵測邏輯：掃描系統字型目錄，找名稱包含 "CJK"、"WenQuanYi" 或 "wqy" 的字型檔
cjk_font_path = None
for font_dir in ["/usr/share/fonts", "/usr/local/share/fonts"]:
    for fp in sorted(pathlib.Path(font_dir).rglob("*")):
        if fp.suffix.lower() in {".ttf", ".ttc"} and (
            "CJK" in fp.name or "WenQuanYi" in fp.name or "wqy" in fp.name
        ):
            cjk_font_path = str(fp)
            break
    if cjk_font_path:
        break

pdf = FPDF()        # 建立新 PDF（預設 A4 直式）
pdf.add_page()      # 必須先 add_page() 才能開始寫入內容

# ── 字型設定 ──
if cjk_font_path:
    # add_font("別名", "樣式", "字型檔路徑")
    # 別名可以自訂，後續用 set_font("CJK") 呼叫
    # 注意：fpdf2 v2.5.1+ 不需要加 uni=True（已自動支援 Unicode）
    pdf.add_font("CJK", "", cjk_font_path)
    pdf.set_font("CJK", size=16)
else:
    pdf.set_font("Helvetica", size=16)
    print("⚠️ 未找到 CJK 字型，中文可能無法顯示。請安裝 fonts-noto-cjk")

# ── 標題 ──
# cell(width, height, text, ...) 是 fpdf2 最基本的內容單元
# width=0 表示「延伸到右邊距」（自動填滿頁面寬度）
# new_x="LMARGIN"：下一格從左邊距開始（回到左邊）
# new_y="NEXT"：下一格移到下一行
# align="C"：文字在格子內置中對齊
pdf.cell(0, 12, text="松柏護理之家退伍軍人症 SitRep", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font_size(10)
pdf.cell(0, 8, text=f"報告時間：{report_time}", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(8)  # ln(n)：插入 n 個點的空白行（版面間距）

# ── 摘要指標（逐行輸出）──
pdf.set_font_size(13)
pdf.cell(0, 10, text="摘要指標", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(10)
kpi_lines = [
    f"住民總數：{total}",
    f"感染人數：{infected}（侵襲率 {infected/total:.1%}）",
    f"確診：{confirmed}　可能病例：{probable}",
    f"住院：{hospitalized}（住院率 {hospitalized/infected:.1%}）",
    f"死亡：{deaths}（CFR {deaths/infected:.1%}）",
]
for line in kpi_lines:
    pdf.cell(0, 7, text=line, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

# ── 嵌入流行曲線 ──
# fpdf2 的 pdf.image() 只接受「檔案路徑」字串，不接受 BytesIO 物件
# 解決方法：先把 BytesIO 的內容寫到一個暫存 PNG 檔，嵌入後立刻刪除
pdf.set_font_size(13)
pdf.cell(0, 10, text="流行曲線", new_x="LMARGIN", new_y="NEXT")
epicurve_buf.seek(0)
epicurve_tmp = pathlib.Path("output/epicurve_tmp.png")
epicurve_tmp.write_bytes(epicurve_buf.read())  # 把 BytesIO 資料寫入磁碟
# pdf.w 是頁面寬度（約 210 mm），減 30 後留左右邊距各 15 mm
pdf.image(str(epicurve_tmp), w=pdf.w - 30)
epicurve_tmp.unlink()  # 嵌入完成後刪除暫存檔（清理環境）
pdf.ln(5)

# ── 各翼區統計表（手動繪製格線表格）──
pdf.add_page()  # 新增第二頁放表格
pdf.set_font_size(13)
pdf.cell(0, 10, text="各翼區疫情摘要", new_x="LMARGIN", new_y="NEXT")
pdf.set_font_size(9)

# col_widths 定義每欄的寬度（mm），總和應小於頁面有效寬度（約 190 mm）
col_widths = [25, 25, 25, 30, 30]
headers = ["翼區", "住民", "感染", "侵襲率%", "CFR%"]
# 表頭列：border=1 繪製四邊框線
for w, h in zip(col_widths, headers):
    pdf.cell(w, 8, text=h, border=1, align="C")
pdf.ln()  # 表頭填完後換行

# 資料列：_ 表示我們不需要索引（只要值 row）
for _, row in wing_stats.iterrows():
    vals = [str(row["label"]), str(row["residents"]), str(row["infected"]),
            str(row["AR%"]), str(row["CFR%"])]
    for w, v in zip(col_widths, vals):
        pdf.cell(w, 7, text=v, border=1, align="C")
    pdf.ln()  # 每行資料填完後換行

pdf.output("output/sitrep_report.pdf")
print("✅ PDF 報告已儲存：output/sitrep_report.pdf")
```

> **小結**：四種格式各有適用場景。互動儀表板適合團隊內部即時檢視，DOCX 適合 email 給長官，PPTX 適合疫調會議簡報，PDF 適合正式歸檔。在實務中，你可以把這些程式碼整合進 `run_sitrep.py`，每天更新 CSV 後重跑一次，就能同時產出四種格式的最新報告。

---

## FETP Step 6：建立假說——從描述性分析到原因推論

完成人時地描述（Steps 3–5）並輸出 SitRep 後，下一步是**提出可檢驗的假說**：誰是傳染源？什麼是傳播途徑？

### 假說生成的三條路徑

```
路徑一：已知病原特性
  已確認為退伍軍人症 → 已知傳播途徑為氣溶膠
  → 假說：「設施內某冷卻水源受 Legionella 污染」
  → 可能來源：冷卻水塔、淋浴設備、水療池、加濕器

路徑二：描述性流行病學線索
  流行曲線呈點源模式（集中在 3–5 天內）→ 單一暴露來源
  地圖顯示 A 翼侵襲率顯著高於 B/C 翼 → 空間聚集性
  → 假說：「A 翼某設施為點源」

路徑三：個案訪談 + 離群值分析
  未感染的住民（對照）與感染者（病例）的生活習慣差異
  某位 90 歲住民，免疫狀態正常但未感染 → 詢問：「不使用淋浴，改用沐浴床」
  → 假說精化：「淋浴氣溶膠為主要暴露途徑，而非單純喝水」
```

### 本次群聚的初步假說清單

| 假說編號 | 假說內容 | 支持的線索 |
|----------|----------|-----------|
| H1 | 冷卻水塔受污染，氣溶膠擴散至 A 翼窗口 | A 翼侵襲率高、冷卻水塔位置在 A 翼側 |
| H2 | A 翼淋浴設備積水受污染 | 淋浴使用者侵襲率高於未使用者（待驗證）|
| H3 | 水療池（Hydrotherapy）為來源 | 使用水療的住民發病率高（待驗證）|

> **注意**：假說應在採樣 / 分析結果出來**之前**就明確寫下。事後「配合」資料修改假說，會使研究設計失效（見 FETP Step 7 分析）。

---

## FETP Step 7：評估假說——向後回溯與向前追溯

建立假說後，需要用**分析性流行病學**和**環境採樣**來驗證。

### 向後回溯（Traceback）——找傳染源

**概念**：從病例的發病日往回推，找出哪個暴露點最可能是源頭。

```
回溯期間 = 最大潛伏期
退伍軍人症最大潛伏期 = 10 天

本次群聚：
  最早發病日 = 2026-01-12
  最晚發病日 = 2026-01-28
  
  → 回溯窗口 = 2026-01-02 至 2026-01-28
  → 在此期間，檢查所有可能的氣溶膠暴露點（水塔、淋浴、水療池）
```

**環境採樣重點**：
- 採集冷卻水塔、淋浴蓮蓬頭、水療池、熱水器的水樣
- 目標：確認環境中的 *Legionella* 菌種與住民菌株是否相符（血清型比對）
- 採樣時間：越早越好，但消毒措施（加氯）應先採樣再啟動

**統計方法**（詳見 Ch05 / Ch06）：

| 分析方法 | 假說類型 | 本次應用 |
|----------|----------|----------|
| 病例對照研究 + 勝算比 | 回顧式暴露比較 | 比較感染者 vs 未感染者的淋浴 / 水療使用率 |
| 世代研究 + 風險比 | 已知暴露，追蹤是否發病 | 若能辨識「使用 A 翼淋浴」vs「未使用」的住民 |
| 分層分析（Mantel-Haenszel）| 干擾因子校正 | 校正年齡 / 免疫狀態後的暴露效應 |

### 向前追溯（Trace-forward）——評估擴散風險

**概念**：從病例的可傳染期往後推，追蹤可能的續發病例。

```
退伍軍人症：人傳人極罕見 → 通常不需要 trace-forward
  ✗ 不需要為每個病例建立接觸者清單
  ✗ 不需要設立接觸者健康監測窗口

若病原為 COVID-19 / 流感 / 諾羅病毒（有人傳人）：
  向前追溯期 = 可傳染期（例：COVID-19 感染後 2–14 天）
  → 需列出密切接觸者名單 + 設定健康監測窗口
```

> **退伍軍人症的調查策略**：集中資源在 **traceback**（環境採樣 + 分析性研究），無需建立接觸者追蹤系統。

```{seealso}
Mantel-Haenszel 分層分析與勝算比計算的 Python 實作 → {doc}`05_stratified`

邏輯斯迴歸多變量分析（校正多個干擾因子）→ {doc}`06_logistic_regression`
```

---

## FETP Step 9：傳染鏈介入——移除源、阻斷鏈、保護宿主

有了假說與分析結果後，控制措施不能等。疫情調查的最終目的是**中斷傳播**，而非只寫一份漂亮報告。

### 傳染鏈三大介入點

依 {ref}`appendix-g-chain-of-infection` 的傳染鏈六要素框架，介入點分為三類：

| 介入類型 | 策略 | 退伍軍人症應用 |
|----------|------|----------------|
| **移除傳染源** | 消滅或隔離病原體 | 冷卻水塔立即加氯消毒（≥2 ppm 餘氯）、排空積水 |
| **阻斷傳播途徑** | 切斷氣溶膠產生 | 停用可疑淋浴間、暫停水療池服務、安裝高溫 60°C 熱水循環 |
| **保護易感宿主** | 降低宿主感受性 | 將免疫抑制住民（癌症 / 器官移植）移至未受影響翼區、給予預防性抗生素評估 |

### 退伍軍人症具體處置步驟

```
即時措施（發現群聚後 24 小時內）：
  1. 停用可疑水源（淋浴間封閉、水療池停用）
  2. 通報地方衛生局 + CDC（退伍軍人症為第三類法定傳染病）
  3. 對症狀病例啟動抗生素治療（azithromycin 或 levofloxacin）

短期措施（48–72 小時）：
  4. 環境採樣（水塔、管線）送驗
  5. 冷卻水塔加氯衝擊消毒
  6. 實施整體管線熱力消毒（熱水 ≥60°C 沖洗）

長期措施（群聚解除後）：
  7. 建立定期水質監測計畫（每季採樣）
  8. 制定機構版 Water Management Program（WMP）
  9. 培訓感染管制人員辨識早期症狀
```

### 措施時序與疫調的平行推進

```{admonition} 重要提醒
:class: warning
控制措施（加氯消毒）應**立即啟動**，無需等待疫調完成。但環境採樣**必須在消毒前進行**，否則後續無法進行水樣與病例菌株的比對。

正確順序：採樣 → 消毒 → 持續監測
```

```{seealso}
傳染鏈六要素完整圖解與隔離 vs 檢疫定義 → {ref}`appendix-g-chain-of-infection`
```

---

## 常見錯誤

1. **每天改定義**：個案定義（case definition）一旦確定就不要改，否則趨勢不可比
2. **只放圖不放表**：SitRep 必須有可查核的數字表格
3. **忘記標註資料截止時間**：每份報告都要註明「資料截至 YYYY-MM-DD HH:MM」
4. **侵襲率沒算分母**：直接比較病例數不公平，要除以各翼區住民數

## Step 9: 排程自動更新

長官的要求很明確：**每天早上九點，信箱裡要有最新的 SitRep。** 但每天手動打開 notebook、按 Run All、等它跑完再寄出……你大概第三天就會忘記。解決方案：讓電腦自動幫你跑。

### 9a: 準備排程腳本

Step 7 的 `generate_sitrep()` 和 Step 8 的報告輸出都是在 notebook 裡互動執行的。要排程自動化，需要把它們整合成一個獨立的 `.py` 腳本。以下是一個適合排程的範例腳本結構：

```python
#!/usr/bin/env python3
"""每日 SitRep 自動產出腳本。

用法（手動執行）：
    uv run python notebooks/run_sitrep.py

排程執行時，請用絕對路徑：
    /Users/你的帳號/.local/bin/uv run python /Users/你的帳號/projects/python4epi/notebooks/run_sitrep.py
"""
import logging
from pathlib import Path
from datetime import datetime

# ── 用 pathlib 算出專案根目錄的絕對路徑 ──
# __file__ 是「這個腳本本身」的路徑
# .resolve() 把相對路徑轉成絕對路徑（例如 ~/projects → /Users/xxx/projects）
# .parent 往上一層：run_sitrep.py → notebooks/ → 專案根目錄
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "synthetic" / "legionella_outbreak.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── 設定 logging（取代 print）──
# 排程執行時你不在電腦前，print 的輸出會消失在虛空
# logging 可以寫入檔案，事後回頭查看「昨天有沒有成功跑完」
LOG_PATH = OUTPUT_DIR / "sitrep.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

def main():
    """主邏輯：讀取 CSV → 計算指標 → 產出報告。"""
    log.info("開始產出 SitRep...")

    # 這裡放 Steps 1–8 的核心邏輯
    # sitrep = generate_sitrep(str(DATA_PATH))
    # ... 產出 DOCX / PDF 等 ...

    # 輸出檔名帶日期戳記，方便歸檔
    today = datetime.now().strftime("%Y%m%d")
    output_path = OUTPUT_DIR / f"sitrep_{today}.pdf"
    log.info(f"報告已儲存：{output_path}")

if __name__ == "__main__":
    # try/except 包住主邏輯：萬一出錯，錯誤訊息會寫進 log 而非默默消失
    try:
        main()
    except Exception:
        log.exception("SitRep 產出失敗！")
        raise  # 重新拋出例外，讓排程系統知道「這次執行失敗了」
```

```{tip}
**從 notebook 轉成 `.py` 腳本的三種方法**，請見 {ref}`Ch00 開發者工具 <00_guide:把-.ipynb-轉成-.py：三種方法>`。本教材的 `notebooks/run_sitrep.py` 就是一個整理好的範例。
```

### 9b: macOS：launchd（推薦）

macOS 的原生排程器叫 **launchd**（不是 cron）。雖然 macOS 也有 cron，但新版 macOS 對 cron 有安全限制，launchd 是官方推薦的做法。

建立一個 plist 設定檔 `~/Library/LaunchAgents/com.epi.sitrep.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Label：這個排程任務的唯一識別名稱 -->
    <key>Label</key>
    <string>com.epi.sitrep</string>

    <!-- ProgramArguments：要執行的指令（等同在終端機打的指令）-->
    <!-- 每個「空白分隔的部分」是一個 <string>，不能全部寫在同一個裡面 -->
    <key>ProgramArguments</key>
    <array>
        <!-- ⚠️ 必須用絕對路徑！用 which uv 查你的 uv 裝在哪裡 -->
        <string>/Users/你的帳號/.local/bin/uv</string>
        <string>run</string>
        <string>python</string>
        <string>/Users/你的帳號/projects/python4epi/notebooks/run_sitrep.py</string>
    </array>

    <!-- WorkingDirectory：執行時的工作目錄（等同先 cd 到這裡再跑） -->
    <key>WorkingDirectory</key>
    <string>/Users/你的帳號/projects/python4epi</string>

    <!-- StartCalendarInterval：排程時間（每天早上 9:00） -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <!-- 日誌輸出路徑（stdout 和 stderr 分開存）-->
    <key>StandardOutPath</key>
    <string>/Users/你的帳號/projects/python4epi/output/launchd_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/你的帳號/projects/python4epi/output/launchd_stderr.log</string>
</dict>
</plist>
```

設定完成後，執行以下三步：

```bash
# 1. 把 plist 複製到 LaunchAgents 目錄（如果你直接在那裡建檔就跳過這步）
cp com.epi.sitrep.plist ~/Library/LaunchAgents/

# 2. 載入排程（從下一個 09:00 開始自動執行）
launchctl load ~/Library/LaunchAgents/com.epi.sitrep.plist

# 3. 確認有載入成功（應該會看到 com.epi.sitrep）
launchctl list | grep epi
```

如果要移除排程：

```bash
launchctl unload ~/Library/LaunchAgents/com.epi.sitrep.plist
```

### 9c: Linux：cron

Linux 最常用的排程工具是 **cron**。用 `crontab -e` 打開編輯器，加入一行：

```bash
# 打開 cron 排程編輯器
crontab -e

# 加入以下這一行（每天早上 9 點執行）
0 9 * * * cd /home/你的帳號/projects/python4epi && /home/你的帳號/.local/bin/uv run python notebooks/run_sitrep.py >> output/sitrep_cron.log 2>&1
```

五個欄位的意思：

```
0 9 * * *
│ │ │ │ │
│ │ │ │ └── 星期幾（* = 每天，0=週日，1=週一 ...）
│ │ │ └──── 月份（* = 每月）
│ │ └────── 日期（* = 每天）
│ └──────── 小時（9 = 早上 9 點，24 小時制）
└────────── 分鐘（0 = 整點）
```

```{warning}
**cron 的 PATH 陷阱：** cron 執行時的環境變數跟你在終端機打指令時不同。`uv` 可能不在 cron 的 PATH 裡，導致 `command not found`。

**解法一**：用 `uv` 的絕對路徑（先執行 `which uv` 查出來，例如 `/home/你的帳號/.local/bin/uv`）。

**解法二**：在 crontab 最上方加入 PATH 設定：
```bash
# 在 crontab -e 的最上方加入這行
PATH=/home/你的帳號/.local/bin:/usr/local/bin:/usr/bin:/bin
```
```

### 9d: Windows 11：工作排程器

Windows 有內建的「工作排程器」（Task Scheduler），可以用 GUI 或命令列設定。

**GUI 方式（4 步）：**

1. 按 `Win` 鍵搜尋「工作排程器」或「Task Scheduler」，打開它
2. 右側點「**建立基本工作**」→ 名稱填 `SitRep 日報更新`
3. 觸發程序：選「**每天**」→ 時間設 `09:00:00`
4. 動作：選「**啟動程式**」→ 填入以下內容：
   - 程式或指令碼：`cmd`
   - 新增引數：`/c cd /d C:\Users\你的帳號\projects\python4epi && uv run python notebooks\run_sitrep.py`

**命令列方式（一行搞定）：**

```powershell
schtasks /create /tn "SitRep_Daily" /tr "cmd /c cd /d C:\Users\你的帳號\projects\python4epi && uv run python notebooks\run_sitrep.py" /sc daily /st 09:00
```

各旗標的意思：

| 旗標 | 說明 |
|------|------|
| `/create` | 建立新的排程任務 |
| `/tn "SitRep_Daily"` | 任務名稱（Task Name） |
| `/tr "..."` | 要執行的指令（Task Run） |
| `/sc daily` | 排程頻率（Schedule）：每天 |
| `/st 09:00` | 開始時間（Start Time）：早上 9 點 |

如果要刪除排程：

```powershell
schtasks /delete /tn "SitRep_Daily" /f
```

### 排程常見問題

| 問題 | 原因 | 解法 |
|------|------|------|
| `command not found: uv` | 排程環境的 PATH 跟終端機不同 | 用 `which uv`（Mac/Linux）或 `where uv`（Windows）找到絕對路徑 |
| 找不到 CSV 檔案 | 工作目錄不是專案根目錄 | 腳本內用 `Path(__file__).resolve().parent` 算絕對路徑 |
| 跑完但沒看到輸出 | 沒有 redirect stdout/stderr | cron: `>> log 2>&1`；launchd: 設定 `StandardOutPath` |
| macOS 權限被擋 | 安全性限制 | 系統設定 → 隱私權與安全性 → 給「終端機」**完整磁碟取用權限** |
| Windows 排程沒執行 | 電腦休眠了 | 工作排程器 → 條件 → 取消勾選「僅在電腦使用 AC 電源時」 |

```{tip}
**進階組合技：** 排程腳本寫好後，可以搭配 Ch13（可重現研究）的 Git 版本控制——每次排程執行後自動 commit 輸出結果，這樣不只有最新報告，還有完整的歷史紀錄可以回溯。
```

## 練習本

- 課堂筆記：{ref}`04_outbreak_workflow.ipynb`
- 作業版：[`04_outbreak_workflow_exercise.ipynb`](exercises/04_outbreak_workflow_exercise.ipynb)
- 解答版（教師版）：[`04_outbreak_workflow_solution.ipynb`](solutions/04_outbreak_workflow_solution.ipynb) | [GitHub](<https://github.com/ancientsky/python4epi/blob/main/book/chapters/solutions/04_outbreak_workflow_solution.ipynb>)
