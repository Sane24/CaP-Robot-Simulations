# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=L4
# run=5
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:52:43
# prompt_chars=12561
# tokens_in=3816 tokens_out=70
# seconds=7.3

```python
matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - putting the milk and the cereal each in its bin')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
```
