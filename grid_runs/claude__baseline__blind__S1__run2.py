# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=S1
# run=2
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T09:27:41
# prompt_chars=12455
# tokens_in=5249 tokens_out=35
# seconds=1.5

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
