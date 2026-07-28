# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=S2
# run=3
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:48:27
# prompt_chars=12471
# tokens_in=3785 tokens_out=50
# seconds=9.0

```python
say('Sure - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', target_pos)
```
