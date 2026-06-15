## Hey, I'm Jiatai Wang 👋

  PhD candidate @ Nankai University, College of Computer Science · Intern @ Haihe Lab of ITAI | Research on retrieval-augmented LLMs,
  knowledge-conflict control, long-context memory, and the agent-harness engineering substrate that makes LLM agents finish
  long-horizon tasks reliably.
  
  - Published RAG work on knowledge-conflict control: [Swin-VIB](https://github.com/JiataiWang/Swin-VIB) — adaptive sliding-window
  information-bottleneck regulates external context injection.
  - Currently building [`condenser-bench`](https://github.com/JiataiWang/condenser-bench) — an isolated benchmark for agent
  context-management & memory policies (Python harness + public leaderboard). *Coming soon.*
  - First merged upstream PR in [openclaw](https://github.com/openclaw/openclaw); planned contributions to
  [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) (Condenser subsystem) and
  [bytedance/deer-flow](https://github.com/bytedance/deer-flow) (memory module).

  ### Projects
  
  | Area | Project | Stars | Notes |
  |------|---------|:-----:|-------|
  | RAG / knowledge-conflict control | [Swin-VIB](https://github.com/JiataiWang/Swin-VIB) | 1 | Knowledge-conflict control framework
  for retrieval-augmented LLMs: an information-bottleneck sliding-window mechanism adaptively regulates external context injection to
  improve reliability and consistency in the wild. |
  | Multi-view representation | [DistilMVC](https://github.com/JiataiWang/DistilMVC) | 4 | Reference code for *Towards Generalized 
  Multi-stage Clustering: Multi-view Self-distillation*. |
  | Agent context & memory eval | [condenser-bench](https://github.com/JiataiWang/condenser-bench) | coming soon | Isolated benchmark
  for agent context-management & memory policies: Python harness + public leaderboard, designed to score condenser / memory strategies
   independent of any single agent framework. |
  | Research feed | [MyArxiv](https://github.com/JiataiWang/MyArxiv) | new | Personal arXiv tracking and digest setup. |
  | Personal site | [JiataiWang.github.io](https://github.com/JiataiWang/JiataiWang.github.io) | — | Homepage, publications, and
  writing. |

  ### Open Source Contributions
  
  #### Agent frameworks / runtime — merged

  | Project | PR | What I Did |
  |---------|:--:|------------|
  | [openclaw](https://github.com/openclaw/openclaw) | [#78288](https://github.com/openclaw/openclaw/pull/78288) | Show target node
  name in exec-tool transparency messages so multi-agent traces stay readable when several agents share an exec channel. |

  #### Earlier proposals
  
  | Project | PR | What I Proposed |
  |---------|:--:|------------------|
  | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [#21638](https://github.com/NousResearch/hermes-agent/pull/21638) |
   Dispatch multiple tool calls concurrently per agent-loop turn instead of awaiting them sequentially, reducing latency on tool-heavy
   turns. |
  | [Claw Code](https://github.com/ultraworkers/claw-code) | [#2999](https://github.com/ultraworkers/claw-code/pull/2999) | Add
  `session_exists` and `delete_session` to `SessionStore` so harness code can manage session lifecycle without reaching into backend
  internals. |

  #### Currently building / planned
  
  - [`condenser-bench`](https://github.com/JiataiWang/condenser-bench) — own project; isolated benchmark for agent context-management
  & memory policies. *In development, public soon.*
  - [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) — planned contributions to the Condenser subsystem
  (long-context compression & policy).
  - [bytedance/deer-flow](https://github.com/bytedance/deer-flow) — planned memory-module PRs.

  ### Research Direction

  Retrieval-augmented generation under context distortion · knowledge-conflict control · learnable long-context compression · agent
  context-management policy evaluation.

  ### Writing
  [jiataiwang.github.io](https://jiataiwang.github.io) · 知乎 / 掘金（待补）

  ---

  ## 你好，我是王嘉泰 👋

  南开大学计算机学院在读博士 · 海河实验室（ITAI）实习生 | 研究方向：检索增强大模型、知识冲突控制、长上下文记忆，以及让 LLM Agent
  稳定完成长跨度任务的 agent harness 工程底座。

  - 已发表 RAG 工作：[Swin-VIB](https://github.com/JiataiWang/Swin-VIB) —— 通过信息瓶颈滑动窗口自适应调节外部上下文注入，提升检索增强
  LLM 的可靠性与一致性。
  - 正在建 [`condenser-bench`](https://github.com/JiataiWang/condenser-bench) —— 面向 Agent 上下文管理 & 记忆策略的隔离评测（Python
  harness + 公开排行榜）。*即将公开。*
  - 首个上游 merged PR 在 [openclaw](https://github.com/openclaw/openclaw)；计划向
  [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) 的 Condenser 子系统与
  [bytedance/deer-flow](https://github.com/bytedance/deer-flow) 的 memory 模块持续贡献。

  ### 项目
  
  | 方向 | 项目 | Stars | 简介 |
  |------|------|:-----:|------|
  | RAG / 知识冲突控制 | [Swin-VIB](https://github.com/JiataiWang/Swin-VIB) | 1 | 检索增强 LLM
  的知识冲突控制框架：信息瓶颈滑动窗口机制自适应调节外部上下文注入，在野外场景下提升回答的可靠性与一致性。 |
  | 多视图表征 | [DistilMVC](https://github.com/JiataiWang/DistilMVC) | 4 | 论文《Towards Generalized Multi-stage Clustering:
  Multi-view Self-distillation》参考代码。 |
  | Agent 上下文 / 记忆评测 | [condenser-bench](https://github.com/JiataiWang/condenser-bench) | 即将公开 | 面向 Agent
  上下文管理与记忆策略的隔离评测：Python harness + 公开排行榜，独立于具体 Agent 框架评分各类 condenser / memory 策略。 |
  | 研究追踪 | [MyArxiv](https://github.com/JiataiWang/MyArxiv) | new | 个人 arXiv 跟踪与摘要工具。 |
  | 个人主页 | [JiataiWang.github.io](https://github.com/JiataiWang/JiataiWang.github.io) | — | 个人主页、出版列表与写作。 |

  ### 开源贡献

  #### Agent 框架 / 运行时 —— 已 merged

  | 项目 | PR | 修了啥 |
  |------|:--:|--------|
  |------|:--:|--------|
  | [openclaw](https://github.com/openclaw/openclaw) | [#78288](https://github.com/openclaw/openclaw/pull/78288) | 在 exec 工具的透传消息中展示目标节点名，让多个 agent 共享
   exec 通道时的执行轨迹依然可读。 |

  #### 早期提案

  | 项目 | PR | 提案内容 |
  |------|:--:|----------|
  | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [#21638](https://github.com/NousResearch/hermes-agent/pull/21638) | agent loop
  每轮支持多工具调用并发执行，取代逐个 await 的串行模式，降低工具密集轮次的延迟。 |
  | [Claw Code](https://github.com/ultraworkers/claw-code) | [#2999](https://github.com/ultraworkers/claw-code/pull/2999) | 给 `SessionStore` 增加 `session_exists` 和
  `delete_session`，让 harness 层能直接管理 session 生命周期，不必触碰后端内部实现。 |

  #### 正在建 / 计划中

  - [`condenser-bench`](https://github.com/JiataiWang/condenser-bench) —— 自研项目；面向 Agent 上下文管理与记忆策略的隔离评测。*开发中，即将公开。*
  - [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) —— 计划向 Condenser 子系统贡献（长上下文压缩 & 策略）。
  - [bytedance/deer-flow](https://github.com/bytedance/deer-flow) —— 计划向 memory 模块提交 PR。

  ### 研究方向

  检索增强生成下的上下文失真 · 知识冲突控制 · 可学习的长上下文压缩 · Agent 上下文管理策略评测。

  ### 写作
  [jiataiwang.github.io](https://jiataiwang.github.io) · 知乎 / 掘金（待补）
