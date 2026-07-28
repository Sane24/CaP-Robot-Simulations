# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=L4
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:13:23
# prompt_chars=12561
# tokens_in=3816 tokens_out=40
# seconds=6.7

```python
matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Ok - putting the milk and the cereal in their corresponding bins')
for first
