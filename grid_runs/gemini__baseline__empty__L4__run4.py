# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=L4
# run=4
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:36:29
# prompt_chars=12485
# tokens_in=3801 tokens_out=40
# seconds=8.8

```python
matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Ok - putting the milk and the cereal each in its bin')
for first
