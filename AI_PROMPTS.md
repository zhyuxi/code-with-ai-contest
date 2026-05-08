# Agent 交互日志

**团队名称：** [补充队名队]
**成员名单：** [待填写]
**使用的 AI Coding Agent 工具：** Claude Code + GLM5

---

## 🤖 交互记录摘要

以下记录了使用 Claude Code 完成 5G 信号可视化看板开发的关键交互过程。
原始交互记录见附件[oringin_chat_history.txt](oringin_chat_history.txt)

### 基础关卡开发

#### 1. 项目初始化
```
用户: /init
Claude: 分析代码库，创建 CLAUDE.md 文件，包含项目概述、命令说明、数据结构、比赛要求。
```

#### 2. 数据加载与地图展示
```
用户: 先完成基础关卡，不要commit
Claude:
- 使用 pandas 读取 data/signal_samples.csv
- 实现信号散点地图，按 RSRP 变色（>-90绿色，<-110红色，中间渐变）
- 添加频段柱状图和终端饼图
- 添加数据概览指标（采样点、频段数、小区数、平均RSRP）
```

#### 3. 基础关卡提交
```
用户: commit一下
用户: 打上标签并推送
Claude: git commit + git tag basic-done + git push origin basic-done
```

### 进阶关卡开发

#### 4. 创建新分支
```
用户: 创建新的分支
Claude: git checkout -b feature/advanced
```

#### 5. 进阶功能实现
```
用户: 开始
Claude:
- 实现侧边栏筛选器（频段下拉、RSRP滑动条、终端类型下拉）
- 实现2D/3D地图切换（3D柱状图高度随下载速率变化）
- 添加单元测试（16个测试覆盖核心功能）
- 重构代码到 utils.py 模块
```

#### 6. 多选筛选改进
```
用户: 筛选功能希望支持多选，比如当前实现不同频段同时只能选中一个
Claude: 将 selectbox 改为 multiselect，实现频段和终端类型多选筛选
```

#### 7. 空数据处理修复
```
用户: 没有任何选择的情况下会显示报错，希望有提升无数据而不是报错
Claude: 修复筛选逻辑，未选择时返回空 DataFrame（保留列结构），显示友好警告信息
```

#### 8. 地图显示修复
```
用户: 只显示数据不显示地图是什么原因
Claude: 移除 mapbox://styles 样式（需要 API token），改用默认地图样式
```

#### 9. 测试优化
```
用户: test_utils.py这个文件名是否合适
用户: 删除单选
用户: 不改
Claude:
- 删除 utils.py 中单选函数（filter_by_band, filter_by_terminal）
- 删除对应测试类
- 新增集成测试类 TestIntegrationFilterCombination
- 最终 21 个测试全部通过
```

#### 10. 文档完善
```
用户: 重写readme
用户: 写到文件里
Claude:
- 重写 README.md 为项目说明文档
- 创建 FEATURES.md 记录功能实现状态
```

---

## 关键问题解决记录

| 问题 | 解决方案 |
|------|----------|
| KeyError: 'RSRP_dBm' | 空 DataFrame 缺列，改为 `pd.DataFrame(columns=df.columns)` 保留结构 |
| 地图不显示 | 移除需要 Mapbox token 的样式，使用默认地图 |
| 测试失败 | 修正断言值，集成测试中筛选结果数量计算错误 |

---

## 最终交付物

- ✅ 源代码（app.py, utils.py, requirements.txt）
- ✅ README.md 项目说明文档
- ✅ 运行截图（3张）
- ✅ AI_PROMPTS.md 交互日志
- ✅ 21 个单元测试
- ✅ Git Tag basic-done 已推送
- ⏳ Git Tag advanced-done 待推送

---

*(此日志由 Claude Code 会话整理，完整对话记录可作为附件提交)*