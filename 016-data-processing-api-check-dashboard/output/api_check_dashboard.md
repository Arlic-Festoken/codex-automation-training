# API 检查对比报告

## 结论

- **local-compose**：需要跟进；2 项检查，1 项非正常，平均耗时 22.4 ms。
- **staging**：正常；2 项检查，0 项非正常，平均耗时 113.2 ms。

## 明细

| 环境 | 检查项 | 状态码 | 耗时 | 结论 | 说明 |
| --- | --- | ---: | ---: | --- | --- |
| local-compose | health | 200 | 29.3 ms | 正常 | ok |
| local-compose | orders | 503 | 15.5 ms | 需要处理 | upstream unavailable |
| staging | health | 200 | 41.8 ms | 正常 | ok |
| staging | orders | 200 | 184.6 ms | 正常 | ok |

## 下一步

- 先处理所有“需要处理”的业务接口；健康检查正常不代表业务链路正常。
- 复查耗时明显高于同类环境的接口，并结合服务日志定位原因。
