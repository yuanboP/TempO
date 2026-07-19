# TempO 研究计划 — Road to ICLR (截稿 ~2026-09-下旬)

> 2026-07-19 定制版,取代旧 PLAN.md。约束:本科生团队(你+朋友+agent 助手)、
> training-free(无 RL 资源,这是定位而非短板)、预算敏感(script-first,
> agent-second;每阶段设成本上限)、已有资产见文末。

## 核心命题(2026-07-19 重定位,已冻结,防跑偏)

**Agent 对自己产物的持续腐化无觉察、无修复能动性。** 只有 pass rate 监督,
所以 agent 感受不到自己产出的代码正在腐化,更想不到自己有权回头破旧立新
(重构 / 删死代码与远古测试 / 拆模块 / 加缓存)。这是一种**过程中的自我认知与
修复能力**,与"一开始就选对架构"(前瞻/foresight)正交。

**与 SlopCodeBench 的根本区别(不是"多测一个维度")**:
- SlopCodeBench 测 **foresight**——agent 在 checkpoint 1 有没有预见未来、一次性选对
  架构(度量=erosion 单调上升,证明缺前瞻)。它的 agent 单向往前堆,**没有机制
  回头审视已腐化部分**。
- 我们测 **self-awareness & remediation**——agent 能不能**察觉**哪些部分已腐化、
  并**主动回头修**。Foresight vs self-awareness,正交能力,它测不了后者。

**时间只是腐化的一种可观测信号,不是命题本身。** 腐化是更大的概念,可测投影至少四类:
时间(build/test 变慢)、结构(耦合/圈复杂度/erosion 上升)、认知(难读难改)、
债务(死代码/重复/过时抽象/远古测试)。命题立在"腐化觉察"这个高层;时间是最易
量化、有 ground truth 的抓手之一,但不是命根子。

Tempo = **能动性唤醒层**:输入是"腐化证据"(时间/结构/erosion 任一),在证据出现且
agent 空等的死时间里,注入证据门控的冷却反思 nudge,唤醒 agent 去察觉并修复。
非被动时间显示。**观测≠能动。**

**双层锚(防"腐化"太模糊被审稿人打)**:
- 命题层(讲故事):agent 对自身产物持续腐化无觉察、无修复能动性。
- 操作层(做实验):用**具体可测的腐化信号**(erosion↑ / build-test 时长↑ / 耦合↑,
  任一)作"腐化"的操作定义;唤醒后测 agent 是否**主动做出修复动作**(重构/删死代码/
  删远古测试/拆模块)**且 pass 不降**。故事讲觉察,实验用多信号落地,时间是其一非全部。

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

- [x] **文献扫荡**(deep-research,102 agents,3 票对抗)→ **Gate A 通过**。
      C1 部分被占(SlopCodeBench=foresight,已证"退化存在"但零时间/零修复维度);
      C2 未占(证据门控能动性 nudge);C3 未占(commit 重放+抽象落差)。
      三处措辞修:显著引用 SlopCodeBench 并按 **foresight vs self-awareness** 划界;
      "pass rate only" → "time never enters in-loop feedback";命名对 temporal
      blindness 划界。详见 design-notes/2026-07-19-novelty-sweep-gateA.md。
- [x] **SlopCodeBench 全量复现**(kindle+Terminus2+Modal,36 题):已跑,确认
      erosion 单调上升而 pass 稳定(execution_server cp1→6: erosion 0.57→0.77,
      strict ~1.0)。**Harbor 版原生保留 erosion/verbosity/increased 指标** →
      我们的 benchmark 可复用这套结构 + 叠时间/修复维度。修了 5 题的 npm build 腐化
      (npm@latest→11.4.2,.bak 留档;这本身是"benchmark Dockerfile 也会腐化"的观察)。
- [ ] 分水岭分析收尾(纯本地:500 公开轨迹下载 + 规则分类,零 agent)→
      冻结论文 §3 motivation 数据(TB 数据只做 motivation,不再加跑分)
- [ ] 把 design-notes 合并成 benchmark 规格 v0.1(采用 SlopCodeBench 骨架:
      工作区继承/无对话历史/规格只写可观测行为/隐藏回归测试;加我们的:腐化信号仪表
      + 修复动作检测 + 抽象落差打分),四道墙自检清单作为附录冻结

## Phase 1:机制证明——腐化觉察与修复(7/26 – 8/16)· 关键路径 · 成本上限 $150

**唯一目标:唤醒后 agent 会不会主动修复腐化(且 pass 不降)?**
最省力起点 = **直接用 SlopCodeBench 的 36 题当实验床**(已复现,已有 erosion 仪表),
不必从零造库——它天然会腐化(erosion 单调上升),我们只加"腐化信号→唤醒→修复"回路。
若 SlopCodeBench 题的腐化不足以触发修复,再退到自造增长库(单体编译单元,增长更陡)。

- [ ] W1:仪表——在 SlopCodeBench 轨迹上,per-checkpoint 计算**多信号腐化向量**
      (erosion↑ 已现成 / build-test 时长↑ 从时间戳算 / 耦合↑ 可选)。确认哪种信号
      在这些题上足够强、能当唤醒触发源(时间弱就用 erosion,不死磕时间)。
- [ ] W2:Tempo v0——Terminus 2 子类,~40 行:证据门控(任一腐化信号较**自身历史**
      恶化超阈 → 触发)+ 冷却期注入反思 nudge(注入点 `terminus_2.py:1424`,已定位)。
      nudge 措辞指向修复动作(重构/删死代码/删远古测试/拆),非"变快"。
- [ ] W3:**先只跑 L0 vs L3**(裸 vs Tempo),1 模型(kindle,链路已验证),5 trials。
      **主测:修复动作率**——唤醒后 agent 是否主动重构/删测试/拆模块(轨迹可判);
      **配套:腐化信号是否被压平**(erosion/时长曲线斜率下降);**护栏:pass@1 不降**
      (SlopCodeBench 静态提示掉了 2.4pp,我们必须盯住这条红线)。
      **Gate B:若 L3 无任何修复动作信号 → 分析原因(nudge 措辞/门控阈值/信号选错/模型),
      迭代 2 轮仍无 → 诚实转向:负结果重定位("唤醒亦不修"本身是发现,降级 workshop/换故事)。**
- [ ] W4(Gate B 过后):补全消融梯 L0-L4(L1 静态提示=复刻 SlopCodeBench 的 anti-slop /
      L2 裸腐化信号无门控 / L4 oracle 直接点名该修哪)+ 健康库负对照(无腐化→不触发→pass 不掉)。
      健康形状:L0≈L1<L2<L3≪L4。若 L1≈L3 → 贡献塌缩成 prompting(SlopCodeBench 已证 L1
      "shifts intercept not slope"),回炉。

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
- [ ] 指标:**修复动作率(主)**、pass@1 不降(护栏)、多信号腐化曲线斜率下降、
      指标收敛度(真实 task 上)、约束满足(副)
- [ ] 图:修复动作率对比主图、消融梯条形图、腐化信号曲线(有/无 Tempo 的斜率对比,
      带置信区间——比 SlopCodeBench 只报描述统计更严谨)
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

- 数据:TB 500 轨迹 W1-W5 分析(§3 motivation)、kindle 89 全量+浪费画像、
  Opus 4.8 89 全量、53 条分类抢救数据、**SlopCodeBench 36 题 kindle 全量
  (jobs/slop-kindle-full,含 erosion/verbosity/时间戳三层)**
- 基建:Harbor+Modal 链路(kindle/Opus/SlopCodeBench 均验证过)、equile CLI、
  注入点已定位(`terminus_2.py:1424`)、tectonic 编译、**SlopCodeBench Harbor
  dataset 本地已下载修复(slopcodebench/,5 题 npm build 已修)**
- 文稿:§1-3 成稿(thesis 待按"腐化觉察"重定位微调)、Fig1 概念图、taxonomy 图、
  三张数据图、design-notes(能动性唤醒/benchmark 设计/四道墙/Gate A 扫荡+对手分析)
- 关键对手:**SlopCodeBench**(arXiv 2603.24755, Orlanski/UW-Madison, 未接收/投稿中)
  —— foresight 命题,MIT 开源,度量工具可复用;我们按 self-awareness 划界

## 每周节奏

周一定本周目标(对照本文件),周五写 3 行进展(design-notes/weekly.md,
gitignored):做了什么/花了多少/下周卡点。跑偏就翻回「核心命题」那节。
