# 16 作業專區

這裡收錄各章的作業版 notebook（不含解答）。所有作業使用同一份資料集：
**松柏護理之家退伍軍人症群聚事件**（`data/synthetic/legionella_outbreak.csv`，280 筆 × 32 欄）。

## 使用方式

1. 先閱讀主章節概念與範例 notebook。
2. 打開本章對應的作業 notebook。
3. 完成所有 `TODO` 標記的程式碼區塊。
4. 完成後再對照 Ch17 解答區的參考解答。

> **提示**：每份作業都有 3 道題目，第 3 題為挑戰題。

## 作業清單

| 章 | 主題 | 練習重點 | 作業 |
|----|------|---------|------|
| 01 | Python 基礎 | 用群聚數字練習變數、dict、函數 | [作業](../exercises/01_fundamentals_exercise.ipynb) |
| 02 | 資料處理與視覺化 | 讀取 line list、日期轉換、流行曲線 | [作業](../exercises/02_data_wrangling_exercise.ipynb) |
| 03 | 描述性統計與 2×2 表 | 淋浴暴露 2×2 表、RR、卡方檢定 | [作業](../exercises/03_stats_exercise.ipynb) |
| 04 | 群聚調查工作流 | 完整 SitRep 產出流程 | [作業](../exercises/04_outbreak_workflow_exercise.ipynb) |
| 05 | 分層分析與交絡因子 | functional_status 分層、MH 檢定 | [作業](../exercises/05_stratified_exercise.ipynb) |
| 06 | 邏輯斯迴歸 | crude vs adjusted OR、模型比較 | [作業](../exercises/06_logistic_regression_exercise.ipynb) |
| 07 | 時間序列與預測 | 移動平均、MAE、住院時間序列 | [作業](../exercises/07_time_series_exercise.ipynb) |
| 08 | 空間流病 | CFR 空間分布、淋浴 × 空間交叉 | [作業](../exercises/08_spatial_exercise.ipynb) |
| 09 | 存活分析 | KM 曲線、Log-rank、Cox 迴歸 | [作業](../exercises/09_survival_exercise.ipynb) |
| 10 | 機器學習 | class_weight、特徵重要性、ROC | [作業](../exercises/10_ml_exercise.ipynb) |
| 11 | 深度學習 | PyTorch 架構設計、Dropout 效果 | [作業](../exercises/11_dl_exercise.ipynb) |
| 12 | 因果推論 | AR/PAR 計算、DiD 日期敏感度 | [作業](../exercises/12_causal_exercise.ipynb) |
| 13 | 可重現研究 | 摘要 dict、檢查清單、版本記錄 | [作業](../exercises/13_reproducibility_exercise.ipynb) |
| 14 | 實戰案例 | 疫情摘要、RR 篩查、迷你 SitRep | [作業](../exercises/14_case_study_exercise.ipynb) |

## 常見問題

**Q: 可以用不同的方法解題嗎？**
A: 當然可以。解答只是參考，能得到正確結果的方法都是好方法。

**Q: 挑戰題太難怎麼辦？**
A: 先完成前兩題，挑戰題可以看完解答後再練習。重點是理解分析邏輯。

**Q: 資料集在哪裡？**
A: 所有 notebook 都從 `data/synthetic/legionella_outbreak.csv` 讀取，確保在專案根目錄執行即可。
