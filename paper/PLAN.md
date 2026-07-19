# TempO 研究计划 — Road to ICLR (截稿 ~2026-09-下旬)

> 2026-07-19 定制版,取代旧 PLAN.md。约束:本科生团队(你+朋友+agent 助手)、
> training-free(无 RL 资源,这是定位而非短板)、预算敏感(script-first,
> agent-second;每阶段设成本上限)、已有资产见文末。

## 核心命题(已冻结,防跑偏)

Agent 对自己开发循环的**能动性失明**:只有 pass rate 监督,感受不到循环腐化,
更想不到自己有权破旧立新(重构/删远古测试)。Tempo = **能动性唤醒层**
(证据门控的冷却反思 nudge),非被动时间显示。观测≠能动。

Benchmark = **抽象落差设计**:给 agent 周期目标(milestone 层级,工程师当年
写下的那种),测其结构决策是否收敛到工程师实际改善的指标(agent 未被告知
指标 → 命中即判断力证据)。

## 风险排序(决定阶段顺序)

1. **效应不存在**(唤醒了也不动 / 一动 pass rate 就掉)→ 最大科学风险,最先验证
2. **被 scoop**(deadline-feedback 一线已部分占位)→ 先做文献扫荡划界
3. **挖矿产出不足**(高质量 task 太难挖)→ 合成任务兜底,真实任务做外部效度

因此:**先合成任务证机制,再真实挖矿补效度**。反过来做 = 最贵的死法。

---

## Phase 0:去险 + 冻结地基(7/19 – 7/26)· 成本 ~$0

- [ ] **文献扫荡**(deep-research 一次做透):精确找出 deadline/temporal-feedback
      那篇;SICA 自改进线;搜 "loop rot / developability / agent refactoring
      for speed / agency" 组合。产出:related-work 划界清单 + novelty 判定。
      **Gate A:窄口(能动性唤醒×增长库×entrenchment)若被占 → 立即重新定位,
      损失最小的时点就是现在。**
- [ ] 分水岭分析收尾(纯本地:500 公开轨迹下载 + 规则分类,零 agent)→
      冻结论文 §3 motivation 数据(TB 数据只做 motivation,不再加跑分)
- [ ] 把 design-notes 三份(能动性唤醒 / benchmark 设计 / 四道墙)合并成
      benchmark 规格 v0.1,四道墙自检清单作为附录冻结

## Phase 1:机制证明——合成任务(7/26 – 8/16)· 关键路径 · 成本上限 $150

**唯一目标:效应存在吗?** 一个受控的会腐化的库 + 有/无 nudge 对比。

- [ ] W1:合成任务 v0——小型多模块库 + 15-20 个顺序 feature request;
      build/test 时间随功能数真实增长(单体编译单元设计,增长可控可测);
      Harbor task 格式,本地 Docker 跑通(免费调试),Modal 只跑正式批
- [ ] W2:Tempo v0——Terminus 2 子类,~40 行:`_execute_commands` 计时 +
      命令模板成本历史 + 证据门控(成本较自身历史 >2x 才触发)冷却 nudge
      (注入点 `terminus_2.py:1424`,已定位)
- [ ] W3:**先只跑 L0 vs L3**(裸 vs Tempo),1 模型(kindle 或 Opus 4.8,
      走已验证的链路),5 trials。测:结构性动作率(重构/删测试,轨迹可判)、
      末段迭代耗时、pass@1。
      **Gate B:若 L3 无任何结构性动作信号 → 停下分析原因(nudge 措辞?
      门控阈值?模型?),迭代 2 轮仍无 → 诚实转向:负结果重新定位
      ("唤醒亦不动"本身是发现,但降级 workshop / 换故事)。**
- [ ] W4(Gate B 过后):补全消融梯 L0-L4(L1 静态提示/L2 裸时间戳/L4 oracle)
      + 健康库负对照(nudge 不该触发,pass 不该掉)。
      健康形状:L0≈L1<L2<L3≪L4。若 L1≈L3 → 贡献塌缩成 prompting,回炉。

## Phase 2:真实 benchmark 挖矿(8/9 起与 Phase 1 尾部并行 – 9/6)· 成本上限 $100

窄版:只挖**时间/可开发性驱动**的架构 commit。目标 **8-15 个验证过的 task**
(≥6 是底线,Gate C)。

- [ ] 候选库画像:有 RFC/milestone 文化 + 构建可复现(Rust/Go 优先,C++ 回避)
      + 存在"为速度而重构"的 commit(搜 build slow / split crate / CI 时长)
- [ ] 每 task 挖四层:周期目标(milestone 原文)→ 工程师改善的指标 →
      当年的约束取舍(API 兼容等)→ 成功判据。**挖掘=人工+LLM 深度活,
      你和朋友主导,我做批量初筛**(script-first:候选枚举全用脚本+便宜 API)
- [ ] 逐 task 验证:pre-commit 快照能构建、指标可测、5 trial 冒烟
- [ ] **Gate C(8/30):<6 个可用 task → 合成套件升级为主实验
      (5 个不同增长曲线的合成库),真实 task 降级为 case study。论文依然成立。**
- [ ] 污染对策:优先 2025 后的 commit / 冷门高质量库;报告 memorization 检查

## Phase 3:主实验(9/6 – 9/17)· 成本上限 $300(先报预算再放量)

- [ ] Benchmark(真实或合成主力)× 消融梯(至少 L0/L1/L3)× 2-3 模型 × 5 trials
- [ ] 第二 harness(原生 tool-calling 一侧)复现 L0 vs L3 → 防"量身定制"
- [ ] 指标:指标收敛度(主)、pass@1 不降(护栏)、约束满足(副)、
      结构性动作率、time-to-success 分布
- [ ] 图:收敛度对比主图、消融梯条形图、合成库迭代耗时曲线(有/无 Tempo)
      —— 数据图一律真数据 matplotlib;概念图/taxonomy 走 image gen(已验收流程)

## Phase 4:成稿 + 红队(9/17 – 截稿)

- [ ] §4 Tempo(从 design-note 扩写)、§5 benchmark、§6 结果回填;
      §1-3 已有稿,terminology 全文统一(agency-awakening 定位,不提 RL 框架,
      结尾一句 "can serve as an RL environment" 留作 future work + 卖点)
- [ ] 四道墙自检清单逐条过;Limitations 诚实写:LLM-judge、污染、单 harness
      起源、task 数量
- [ ] 内部红队:互相扮审稿人各写一份 "why reject",修掉能修的
- [ ] 排版走 tectonic(已通),ICLR style kit 出来后换壳

---

## 纪律(血泪换来的,违者叫停)

1. **script-first, agent-second**:确定性活永远脚本;LLM 只做语义判断;
   任何批量 agent 派发前,先跑 1 个看单价,算总账,报给你批准
2. **每阶段成本上限**如上;超限即停,不"顺手多跑一点"
3. **大批量必须可断点续传**(manifest 模式),必须先 1 → 10 → 全量
4. **正式对比实验一律 ≥5 trials**,报均值±方差;单 trial 数字不进论文
5. TB 上不再加任何跑分(旧轴 + 污染,已有的只做 motivation)

## 已有资产(不重做)

- 数据:TB 500 轨迹 W1-W5 分析(§3 主表)、kindle 89 全量+浪费画像、
  Opus 4.8 89 全量、53 条分类抢救数据
- 基建:Harbor+Modal 链路(两模型验证过)、equile CLI(批量+schema)、
  注入点已定位(`terminus_2.py:1424`)、tectonic 编译
- 文稿:§1-3 成稿(thesis 已按能动性唤醒重写)、Fig1 概念图、taxonomy 图、
  三张数据图、design-notes 三份

## 每周节奏

周一定本周目标(对照本文件),周五写 3 行进展(design-notes/weekly.md,
gitignored):做了什么/花了多少/下周卡点。跑偏就翻回「核心命题」那节。
