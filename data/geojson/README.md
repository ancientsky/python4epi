# 台灣行政界 GeoJSON 說明

本目錄存放由 `taiwan/` 內政部／國土測繪中心 **shapefile** 轉換、簡化後的行政界線 GeoJSON，供製圖、網頁地圖與 choropleth 統計圖使用。

| 項目 | 說明 |
|------|------|
| 座標系 | **EPSG:4326**（WGS84 經緯度） |
| 編碼 | UTF-8（中文屬性可直接讀取） |
| 幾何型別 | `Polygon` / `MultiPolygon` |
| 來源 CRS | 原始為 TWD97 經緯度（GCS_TWD97[2020]），已轉出為 4326 |
| 產生方式 | 見專案根目錄 `scripts/`、`README.md` |

```text
output/geojson/
├── README.md                 ← 本說明
├── county/                   縣市界（22 或 19 圖徵）
├── township/                 鄉鎮市區界（368 圖徵）
└── village/                  村里界（約 7986 圖徵）
```

---

## 如何選檔（速查）

| 用途 | 建議檔案 |
|------|----------|
| 歸檔、後續再簡化、極高解析印刷 | `*_full.geojson` |
| 海報／高 dpi 區域圖 | `*_high.geojson` |
| 一般網頁、A4 報告 | `*_medium.geojson` |
| 縮圖、儀表板概覽 | `*_low.geojson` |
| 示意風格、體積最小、離島已清理 | `*_smooth.geojson` |
| 僅台灣本島（縣市） | `county/county_smooth_mainland*.geojson` |
| 22 縣市 choropleth（金馬澎加框放大） | `county/county_smooth_inset*.geojson` |
| 需要雲林**外傘頂洲** | 檔名含 `waisanding` 者 |

**簡化系列（full → high → medium → low）**：拓樸感知（mapshaper `weighted` + `keep-shapes`），圖徵數與來源一致，邊界相鄰對齊較佳。  
**smooth 系列**：在 low 之上再強化簡化，並套用離島保留政策（見下文）。

---

## 共同屬性欄位

### 縣市 `county/`

| 欄位 | 說明 |
|------|------|
| `COUNTYID` | 縣市代碼（短） |
| `COUNTYCODE` | 縣市代碼（建議 join 鍵） |
| `COUNTYNAME` | 中文名稱 |
| `COUNTYENG` | 英文名稱 |
| `geometry` | 界線 |

### 鄉鎮 `township/`

| 欄位 | 說明 |
|------|------|
| `TOWNID` / `TOWNCODE` | 鄉鎮代碼（`TOWNCODE` 建議 join） |
| `TOWNNAME` / `TOWNENG` | 中／英文名稱 |
| `COUNTYID` / `COUNTYCODE` / `COUNTYNAME` | 所屬縣市 |
| `geometry` | 界線 |

### 村里 `village/`

| 欄位 | 說明 |
|------|------|
| `VILLCODE` | 村里代碼（建議 join） |
| `VILLNAME` / `VILLENG` | 中／英文名稱 |
| `TOWNID` / `TOWNCODE` / `TOWNNAME` | 所屬鄉鎮 |
| `COUNTYID` / `COUNTYCODE` / `COUNTYNAME` | 所屬縣市 |
| `NOTE` | 備註（來源欄位） |
| `geometry` | 界線 |

---

## 簡化層級（full / high / medium / low）

三層行政區皆有（村里 `full` 預設為壓縮檔以節省空間）。  
mapshaper **保留頂點比例**約略如下（越高越精細、檔越大）：

| 層級 | 縣市 keep% | 鄉鎮 keep% | 村里 keep% | 適用 |
|------|------------|------------|------------|------|
| **full** | 100%（僅修補轉碼） | 100% | 100% | 原始精度 |
| **high** | 25% | 20% | 15% | 大圖、300 dpi 級 |
| **medium** | 8% | 5% | 4% | 網頁／報告 |
| **low** | 2% | 1.5% | 1% | 縮圖／概覽 |

體積與圖徵數（約，依目前產出）：

### `county/`

| 檔案 | 圖徵 | 約略大小 | 說明 |
|------|------|----------|------|
| `county_full.geojson` | 22 | ~8.9 MB | 全國縣市，完整頂點 |
| `county_high.geojson` | 22 | ~2.3 MB | 高細節 |
| `county_medium.geojson` | 22 | ~0.8 MB | 中等 |
| `county_low.geojson` | 22 | ~0.2 MB | 低細節；仍含遠海碎部（東沙等） |

### `township/`

| 檔案 | 圖徵 | 約略大小 | 說明 |
|------|------|----------|------|
| `township_full.geojson` | 368 | ~31 MB | 完整 |
| `township_high.geojson` | 368 | ~6.3 MB | 高細節 |
| `township_medium.geojson` | 368 | ~1.7 MB | 中等 |
| `township_low.geojson` | 368 | ~0.6 MB | 低細節 |

### `village/`

| 檔案 | 圖徵 | 約略大小 | 說明 |
|------|------|----------|------|
| `village_full.geojson.gz` | 7986 | （gzip） | 完整；解壓後體積大，預設以 `.gz` 存放 |
| `village_high.geojson` | 7986 | ~12 MB | 高細節 |
| `village_medium.geojson` | 7986 | ~6.2 MB | 中等 |
| `village_low.geojson` | 7986 | ~4.6 MB | 低細節 |

讀取 gzip 範例：

```python
import geopandas as gpd
gdf = gpd.read_file("village/village_full.geojson.gz")
```

---

## Smooth 系列（示意風格 + 離島政策）

與 full–low **不同**：smooth 會**過濾微小／未列名離島**，並使用更激進的簡化比例，風格接近示意地圖（如 Highcharts 級頂點量）。

### 離島保留政策（smooth 共用）

| 保留 | 捨棄（例） |
|------|------------|
| 澎湖縣、金門縣、連江縣（馬祖）全縣主要島嶼 | 東沙、南沙 |
| 蘭嶼、綠島（臺東） | 彭佳嶼、釣魚台附近碎島 |
| 小琉球（屏東） | 一般沙洲、岩礁 |
| **外傘頂洲**：僅檔名含 `waisanding` 的版本 | 預設 smooth **不含**外傘頂洲 |

### `county/` smooth 與版面變體

| 檔案 | 圖徵 | 約略大小 | 說明 |
|------|------|----------|------|
| `county_smooth.geojson` | 22 | ~53 KB | 標準 smooth：本島 + 金馬澎 + 蘭嶼／綠島／小琉球 |
| `county_smooth_waisanding.geojson` | 22 | ~53 KB | 同上 **+ 外傘頂洲**（雲林沿海） |
| `county_smooth_mainland.geojson` | **19** | ~38 KB | **僅台灣本島**（無金門／連江／澎湖，亦無蘭嶼綠島小琉球） |
| `county_smooth_mainland_waisanding.geojson` | 19 | ~38 KB | 本島 **+ 外傘頂洲** |
| `county_smooth_inset.geojson` | 22 | ~280 KB | **海報式 choropleth**：本島真位置 + 左側加框放大馬祖／金門／澎湖 |
| `county_smooth_inset_waisanding.geojson` | 22 | ~280 KB | 加框版本島 **+ 外傘頂洲** |
| `county_smooth_inset_frames.geojson` | 3 | <1 KB | 三個 inset **外框矩形**（可選一層繪製） |

#### Inset 版額外欄位

| 欄位 | 說明 |
|------|------|
| `layout` | `main`（本島面板）或 `inset`（加框離島） |
| `is_inset` | 是否為加框縮放後的離島圖徵 |
| `inset_scale` | 相對原始範圍的縮放倍率（約） |
| `inset_label` | 框上標籤文字（如「馬祖（連江縣）」） |

**注意**：inset 中金門／連江／澎湖的座標是**為製圖而仿射縮放平移**後的顯示位置，**不是**真實地理座標；本島縣市仍為真實經緯度。接統計時用 `COUNTYCODE` / `COUNTYNAME` join 即可，勿用 inset 座標做空間分析。

離島 inset 幾何自**原始 shapefile** 以較高 keep%（約 12–14%）重新簡化後再放大，避免直接放大 `smooth` 造成變形。金門 inset 不含烏坵，以免框內比例被拉扁。

#### Mainland 版額外欄位

可能含 `layout`、`is_inset`、`include_waisanding` 等標記欄，便於腳本區分變體。

### `township/` / `village/` smooth

| 檔案 | 圖徵 | 約略大小 | 說明 |
|------|------|----------|------|
| `township/township_smooth.geojson` | 368 | ~0.43 MB | 鄉鎮 smooth + 同上離島政策 |
| `village/village_smooth.geojson` | **7984** | ~4.4 MB | 村里 smooth；比來源少 2 筆（高雄遠海東沙／南沙相關村里已剔除） |

村里 smooth 圖徵數：`7986 → 7984`（far-sea-only 圖徵刪除）。其餘鄉鎮／村里 smooth 圖徵數與來源一致。

---

## 目錄與檔案一覽

```text
county/
  county_full.geojson
  county_high.geojson
  county_medium.geojson
  county_low.geojson
  county_smooth.geojson
  county_smooth_waisanding.geojson
  county_smooth_mainland.geojson
  county_smooth_mainland_waisanding.geojson
  county_smooth_inset.geojson
  county_smooth_inset_waisanding.geojson
  county_smooth_inset_frames.geojson

township/
  township_full.geojson
  township_high.geojson
  township_medium.geojson
  township_low.geojson
  township_smooth.geojson

village/
  village_full.geojson.gz    # 若存在
  village_high.geojson
  village_medium.geojson
  village_low.geojson
  village_smooth.geojson
```

---

## 使用範例

### 讀取與簡單繪圖（GeoPandas）

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# 縣市 medium
gdf = gpd.read_file("county/county_medium.geojson")
ax = gdf.plot(facecolor="#cfe8ff", edgecolor="#333", linewidth=0.4)
ax.set_aspect("equal")
plt.show()

# choropleth：用 inset 版接統計
stats = ...  # DataFrame with COUNTYCODE, value
m = gpd.read_file("county/county_smooth_inset.geojson")
m = m.merge(stats, on="COUNTYCODE")
m.plot(column="value", cmap="YlGnBu", edgecolor="black", linewidth=0.3)
# 可選：疊外框
frames = gpd.read_file("county/county_smooth_inset_frames.geojson")
frames.plot(ax=plt.gca(), facecolor="none", edgecolor="black", linewidth=1.2)
```

### 重新產生

```bash
# full / high / medium / low
uv run python scripts/convert_simplify.py

# 縣市 smooth（含 waisanding 變體）
uv run python scripts/make_county_smooth.py

# 縣市 mainland / inset（含 waisanding 變體）
uv run python scripts/make_county_variations.py

# 鄉鎮、村里 smooth
uv run python scripts/make_admin_smooth.py --layers township,village
```

參數與離島規則細節見專案根目錄 `config/simplify_levels.yaml`、`README.md`。  
驗證報告在 `output/reports/`（如 `validation_county_smooth.json`、`size_summary.md`）。  
示意地圖在 `output/maps/`。  
**縣市各版本 300 dpi choropleth 展示**：`output/maps/choropleth_300dpi/`（腳本 `scripts/make_county_choropleth_300dpi.py`）。

---

## 資料來源與授權提醒

- 縣市／鄉鎮：內政部界線資料（檔名含 `MOI_1140318` 等）
- 村里：國土測繪中心村里界（檔名含 `NLSC_1150624` 等）
- 使用時請遵守原始資料之開放授權與標示規定
- 本目錄產物為衍生之簡化／版面調整資料；**inset 版不適用於真實位置量測**

---

## 注意事項

1. **smooth vs low**：low 保留較完整行政碎部（含部分遠海）；smooth 刻意清理離島並更平滑，適合示意與儀表板。  
2. **外傘頂洲**：僅 `*waisanding*` 檔包含；預設 smooth／mainland／inset 不含。  
3. **村里 full**：優先使用 `.gz`；磁碟空間不足時可能未產出未壓縮 full。  
4. **join 鍵建議**：縣市 `COUNTYCODE`、鄉鎮 `TOWNCODE`、村里 `VILLCODE`。  
5. 簡化會改變形狀與面積；正式面積統計請用 `full` 或原始 shapefile 於投影座標系計算。
