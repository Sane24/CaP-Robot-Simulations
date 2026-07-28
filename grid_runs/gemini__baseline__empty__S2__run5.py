# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=S2
# run=5
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-28T08:33:02
# prompt_chars=12395
# tokens_in=3770 tokens_out=39
# seconds=8.9

```python
say('Ok - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on
