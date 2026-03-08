# 17 解答專區（講師版）

此章節提供各章作業的參考解答。所有解答使用同一份資料集：
**松柏護理之家退伍軍人症群聚事件**（`data/synthetic/legionella_outbreak.csv`）。

## 使用建議

- 先完成 Ch16 作業專區的對應題目，再查看解答。
- 解答示範的是一種合理分析流程，**不是唯一正解**。
- 教學時建議先討論方法選擇與分析邏輯，再展示程式碼。

## 解答清單

| 章 | 主題 | 解答重點 | 解答 |
|----|------|---------|------|
| 01 | Python 基礎 | dict 組織疫情資料、函數封裝 | [解答](solutions/01_fundamentals_solution.ipynb) |
| 02 | 資料處理與視覺化 | 日期衍生欄位、年齡分組流行曲線 | [解答](solutions/02_data_wrangling_solution.ipynb) |
| 03 | 描述性統計與 2×2 表 | 水療 RR、年齡分組 RR、Fisher's exact | [解答](solutions/03_stats_solution.ipynb) |
| 04 | 群聚調查工作流 | 自動化 SitRep 函數、嚴重度分析 | [解答](solutions/04_outbreak_workflow_solution.ipynb) |
| 05 | 分層分析與交絡因子 | 年齡分層、共病交絡、MH adjusted RR | [解答](solutions/05_stratified_solution.ipynb) |
| 06 | 邏輯斯迴歸 | 重症模型、LRT 比較、預測機率 | [解答](solutions/06_logistic_regression_solution.ipynb) |
| 07 | 時間序列與預測 | 住院序列、窗口 MAE、嚴重度堆疊圖 | [解答](solutions/07_time_series_solution.ipynb) |
| 08 | 空間流病 | CFR 熱力圖、淋浴 × 空間相關、高風險房間 | [解答](solutions/08_spatial_solution.ipynb) |
| 09 | 存活分析 | CHF KM 曲線、年齡分組、Cox 多因子 | [解答](solutions/09_survival_solution.ipynb) |
| 10 | 機器學習 | 平衡類別、重症預測、三模型 ROC | [解答](solutions/10_ml_solution.ipynb) |
| 11 | 深度學習 | 三層架構、重症任務、Dropout 比較 | [解答](solutions/11_dl_solution.ipynb) |
| 12 | 因果推論 | 水療 AR/PAR、日期敏感度、碰撞偏差 | [解答](solutions/12_causal_solution.ipynb) |
| 13 | 可重現研究 | 摘要驗證、環境檢查、版本記錄 | [解答](solutions/13_reproducibility_solution.ipynb) |
| 14 | 實戰案例 | 摘要表、RR 比較、迷你 SitRep 圖 | [解答](solutions/14_case_study_solution.ipynb) |

## 教學提示

- **Ch05 分層分析**：重點在於讓學員理解「為什麼 crude RR 和 adjusted RR 不同」
- **Ch06 邏輯斯迴歸**：強調 crude OR vs adjusted OR 的差異，與 Ch05 的分層分析互補
- **Ch09 存活分析**：「住院者死亡率較高」是 confounding by indication 的經典範例
- **Ch12 因果推論**：碰撞偏差（collider bias）是最常被忽略的偏差類型
- **Ch14 實戰案例**：讓學員自行決定「行動建議」，練習從分析到決策的思維
