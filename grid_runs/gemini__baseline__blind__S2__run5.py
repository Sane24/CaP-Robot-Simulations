# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=S2
# run=5
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:38:10
# prompt_chars=12428
# tokens_in=3778 tokens_out=35
# seconds=9.9

```python
say('Ok - lifting the cube above the table')
target_pos = parse_position('a point above the cube')
put_first_on
