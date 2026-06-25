# 核心变量库指南

核心变量库使用 YAML：

```yaml
variables:
  - id:
    zh_name:
    en_name:
    abbreviation:
    aliases:
    definition:
    unit:
    scale:
    applies_to:
    must_report:
    must_control_when:
    missing_consequence:
    related_observables:
    related_mechanisms:
    examples:
    notes:
```

用它判断某个未报告项是否削弱结论、是否构成可比性缺口、是否需要进入 Request 或 normalization_blockers。
