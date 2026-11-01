# Haibara’s Architect 0.6

**Haibara’s Architect：把建筑研究、设计约束、可复现随机、案例建造与验收连成一条可检查的工作流。**

正式发布名称为 **Haibara’s Architect**，仓库名为 `Haibara-s-Architect`。历史档案中的 HAF / HAFusion 标签与现有 `hafusion` 模块名保留，便于对照和兼容。

这是给同学阅读、运行和继续改进的学习版。可以先运行一个只用 Python 标准库的空间规划示例，再生成一栋已有适配器的建筑，并对照各代案例理解每个改动的原因。

0.6 新增受约束的工作流运行层和模型提案接口；原有几何适配器保留 0.4 内核。它已经具备部分 Agent 工具组件，但还没有自动联网研究、通用建筑生成、自动游戏验收和无人值守闭环。项目没有训练或提供模型权重。

![市民中心R16的园林与入口离线预览](cases/civic_center/review/previews/v03_r16_ceiling_landscape/entrance_garden_day.png)

上图是随包保留的 Civic R16 旧成果，展示从外壳到入口、园林和嵌灯的研究；不是本次0.6新生成，也不是游戏截图。

## 从这里开始

| 想了解什么 | 阅读入口 |
|---|---|
| 先跑起来，再改一项参数 | [快速开始](docs/quickstart.md) |
| 需求怎样变成建筑与验收记录 | [完整工作流](docs/workflow.md) |
| 0.1、0.2、0.3 等每代具体做了什么 | [历代演进](docs/version-history.md) |
| 每栋建筑的类型、细节、失败与代码/NBT | [案例学习指南](docs/case-studies.md) · [23 条案例索引](docs/case-index.json) |
| 为什么随机不能靠一个随机数到处调用 | [随机设计与实现](docs/randomness.md) |
| Skill 升级、内饰、植物、灯光和地形经验 | [研究与技能经验](docs/concept-and-skills.md) |
| 怎样让语言模型提出修改，并让程序把关 | [模型接入](docs/model-integration.md) · [提示词](prompts/architect.md) |
| 哪些能运行，哪些只是规则/研究 | [能力与限制](docs/capabilities.md) · [已知问题](docs/known-issues.md) |
| 本次真正验证过什么 | [验证记录](docs/validation.md) |

## 十分钟体验

需要 Python 3.10+；本次执行环境为 Python 3.12。下载或克隆后进入仓库目录。

```sh
python -X utf8 tools/haf.py --version
python -X utf8 tools/haf.py demo --runs-root runs/workflow06 --run demo-001
python -X utf8 tools/haf.py verify --runs-root runs/workflow06 --run demo-001
```

这会生成 `request.json`、空间交接计划、随机选择结果及清单，**不会生成 NBT**。输出会明确保留 `generated_geometry: false` 和待建造/待游戏验收状态。相同 run 名不可覆盖，修改时创建新版本。

再导入一个模型可能提出的桌子布局修订：

```sh
python -X utf8 tools/haf.py import-proposal examples/workflow06/desk-proposal.json --runs-root runs/workflow06 --parent demo-001 --run revision-001
python -X utf8 tools/haf.py verify --runs-root runs/workflow06 --run revision-001
```

提案只允许修改声明可编辑的模块。通道、冻结构件、用途、楼层和编辑边界仍由父版本约束；校验失败时不能靠提示词绕过。

要实际生成已登记案例，先安装建造依赖：

```sh
python -m pip install -r requirements.txt
python -X utf8 tools/haf.py build-case --case elizabeth_tower --run my-clocktower-001 --execute
```

产物位于 `cases/elizabeth_tower/runs/my-clocktower-001/`，包括 `building.nbt`、参数、构件归属与回读结果。这个入口使用钟塔专用适配器，不会把任意规划 JSON 自动变成建筑。首次推荐钟塔，因为不依赖原照片、外部模型或旧建筑 NBT。

## 0.6 整合了什么

- **历史工程**：保留 11 个注册案例入口、共享构件/灯光/证据/回读工具以及有用的失败版本；23 条案例索引区分仓库内成果和外部分支。
- **可复现随机**：稳定对象 ID、独立通道、明确候选值、冻结对象、空间边界与禁放区；新增无关对象不打乱已有选择。
- **运行记录**：每次请求、计划、提案和摘要分开保存；不覆盖旧 run；重新编译和核对文件一致性。
- **模型接口**：模型输出 JSON，宿主绑定目录与父版本，Python 校验后产生新 run；不执行模型发来的 shell 或任意代码。
- **经验文档**：现实复原与原创设计分开，构件证据到参数消费者可追踪；用途、内饰、门窗、照明、园林、地形和负面反馈都进入设计检查。
- **真实边界**：保留未接入的随机开窗实验、依赖不完整的内饰研究和待游戏验收项，不以文件数量代替完成度。

## 目录

| 目录 | 用途 |
|---|---|
| `hafusion/` | 0.4 共享内核与新增 `workflow06.py` / `variation06.py` |
| `tools/haf.py` | 0.6 规划、验证、提案、工具调用入口 |
| `tools/agent.py` | 旧版显式案例建造/复核入口 |
| `cases/` | 当前 11 条案例的代码、参数、选定历史成果 |
| `examples/workflow06/` | 可运行的请求、提案和模型工具 schema |
| `experiments/concept/` | 原样保留的两个研究规划器，非默认生产入口 |
| `docs/` | 学习文档、能力说明、案例历史、验证记录 |
| `ha03/`、`case/`、`support/` | 原 Architect、BuildKit 和构件支持代码 |
| `upstream/PlanCraft/` | 保留许可的上游代码 |
| `history/`、`release/`、`releases/` | 历史依据；其中旧测试报告不代表本次测试 |

## 怎样走向 Agent

当前可以把模型接在“提出结构化修改”这一环，宿主负责工具分发、范围约束和版本留存。下一步优先完成：通用计划到几何适配器、地形/路网约束消费者、实际截图验收、失败定位与有预算的重试，再建设长期任务记忆。具体顺序见 [路线图](docs/roadmap.md)。

研究、修订和交付请遵守 [AGENTS.md](AGENTS.md) 与 [贡献说明](CONTRIBUTING.md)。代码、外部资料、上游库和建筑成果的授权范围分别记录在 [LICENSE-NOTICE.md](LICENSE-NOTICE.md) 与 [ATTRIBUTION.md](ATTRIBUTION.md)。
