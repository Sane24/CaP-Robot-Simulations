# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=S1
# run=5
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T13:11:27
# prompt_chars=12455
# tokens_in=4029 tokens_out=33
# seconds=1.5

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
