# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=S2
# run=3
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:32:44
# prompt_chars=12395
# tokens_in=3770 tokens_out=50
# seconds=9.0

```python
say('Ok - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', target_pos)
```
