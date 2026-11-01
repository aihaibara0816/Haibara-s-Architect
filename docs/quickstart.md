# 从一个计划到一栋已登记建筑

建议先跑标准库示例，再安装建造依赖。Windows 的 `python` 若指向应用商店占位程序，请使用自己安装的 Python 解释器，例如 `py -3`。下文统一写 `python`；`-X utf8` 避免中文系统编码差异。

## 1. 建立环境

```sh
python --version
python -m venv .venv
```

Windows PowerShell 可直接使用 `.venv/Scripts/python.exe`；macOS/Linux 使用 `.venv/bin/python`。不必为了激活环境修改系统执行策略。后续命令中的 `python` 替换为该路径即可。

## 2. 不装第三方依赖也能运行的计划

```sh
python -X utf8 tools/haf.py validate examples/workflow06/library-request.json
python -X utf8 tools/haf.py demo --runs-root runs/workflow06 --run demo-001
python -X utf8 tools/haf.py verify --runs-root runs/workflow06 --run demo-001
```

示例是一间有用途、楼层、模块和通道约束的阅读空间。打开 `runs/workflow06/demo-001/manifest.json` 查看完成状态，再比较计划与原请求。此处的随机结果是离散选择计划；不会自动替换方块。

练习：复制示例请求，修改一个通道的 seed，使用新 run 名执行 `plan`。比较其他通道是否保持不变。再尝试把可移动模块推入 keepout，应被拒绝。

## 3. 模型提案修订

```sh
python -X utf8 tools/haf.py import-proposal examples/workflow06/desk-proposal.json --runs-root runs/workflow06 --parent demo-001 --run revision-001
python -X utf8 tools/haf.py verify --runs-root runs/workflow06 --run revision-001
python -X utf8 tools/haf.py dispatch examples/workflow06/model-call.json --runs-root runs/workflow06 --parent demo-001
```

示例提案只对应原始 demo 请求。改过请求后，应从新父 run 获取摘要并重做提案。工具调用示例可重复做只读验证；创建新 run 的调用不能反复使用同一个名字。完整接口见 [模型接入](model-integration.md)。

## 4. 生成真正 NBT

```sh
python -m pip install -r requirements.txt
python -X utf8 tools/agent.py --list-cases
python -X utf8 tools/haf.py build-case --case elizabeth_tower --run clocktower-001
python -X utf8 tools/haf.py build-case --case elizabeth_tower --run clocktower-001 --execute
```

不带 `--execute` 只显示将执行的注册命令。带参数才实际运行已有适配器。产物在 `cases/elizabeth_tower/runs/clocktower-001/`；程序对最终 NBT 重新读取，比较体积与方块状态。

钟塔参数在 `cases/elizabeth_tower/params.json`，建造代码在对应 `src/build_case.py`。要修改参数，请复制参数文件并使用旧入口显式指定：

```sh
python -X utf8 tools/agent.py --case elizabeth_tower --params my-clocktower.json --run clocktower-002
```

案例适配器对参数的支持各不相同；本例包含硬编码的钟塔构造，不是任意尺寸的通用钟塔生成器。Civic 更依赖冻结历史结果，第一次学习不建议从它开始。

## 5. 验证与导入

```sh
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tools/agent.py --review --case elizabeth_tower --run clocktower-001
```

`--review` 是当前注册的采样/视图元数据检查；该案例未声明的检查会保留 pending。NBT 回读通过不代表门能走、楼梯能上或灯光正确。先在自己的测试世界中按匹配的游戏版本导入，再检查入口、楼层净高、方块状态、光照和邻接连接；仓库不会自动修改存档。

若出现 `ModuleNotFoundError: jsonschema`，需要在**同一个 Python 环境**执行依赖安装。只学习新运行层可先执行 `python -X utf8 -m unittest discover -s tests -p test_workflow06.py -v`。其他未解决问题见 [已知问题](known-issues.md)。
