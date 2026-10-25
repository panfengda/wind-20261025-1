import streamlit as st
import pandas as pd
from pfd.auth import require_login
from pfd.ui import apply_theme
from pfd.research import PUBLIC_REFERENCES, validation_readiness

st.set_page_config(page_title="验证与研究记录 | PFD", layout="wide")
apply_theme()
require_login()
st.title("模型验证与研究记录")
st.subheader("公开资料与验证用途")
st.dataframe(pd.DataFrame(PUBLIC_REFERENCES), use_container_width=True, hide_index=True)
st.subheader("当前验证准备度")
st.dataframe(pd.DataFrame(validation_readiness(), columns=["验证对象","当前状态","需要做什么"]),
             use_container_width=True, hide_index=True)
st.markdown("""
### 公开数据集的正确用法

**An Atlas of Wind Turbine Blade Leading Edge Erosion for CONUS**（Zenodo record 14247620）是当前最贴近本项目的公开资源之一。它提供美国本土 883 个 ASOS 站点的多年气象驱动叶片前缘侵蚀潜势/累计距离失效估计，可用于场址级的外部合理性比较。它不是每小时真实涂层损伤测量，因此不能直接作为逐小时损伤预测的 ground truth。

获取方式：打开 [Zenodo 数据记录](https://zenodo.org/records/14247620)，阅读文件说明、方法和许可后下载 NetCDF 文件。当前项目不会自动下载或假定该文件已经存在。后续可以用 `xarray` 读取该 NetCDF，并把重叠场址的指标与本项目的暴露代理作探索性比较；这只能检验排序/趋势是否大致一致，不等于验证实际损伤精度。

### 目前不能声称的结果

- 不能声称预测了真实损伤深度、涂层损失百分比或剩余寿命。
- 不能声称具有某个准确率、RMSE 或“高精度”，除非存在独立标签并完成测试。
- 不能把模拟数据或再分析数据伪装成风机现场实测。
- 不能用随机拆分相邻小时记录来证明泛化能力。

### 真正的损伤模型还缺哪些数据？

1. 雨蚀试验（RET）数据或涂层材料的侵蚀疲劳参数；
2. 叶片几何、局部相对速度与运行控制状态；
3. 雨滴粒径/速度分布，最好有场址联合风雨观测；
4. 叶片检查图像、损伤等级、维修/更换时间或可靠的现场观察；
5. 独立场址或独立时间段的验证数据。
""")
st.info("研究建议：先完成数据处理与场址级暴露比较；待取得公开 atlas 文件后再做外部合理性检查；只有取得真实损伤标签后，才开始训练损伤预测模型。")
