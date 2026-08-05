# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=S1
# run=5
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-08-05T02:45:07
# prompt_chars=12457
# tokens_in=5250 tokens_out=35
# seconds=2.3

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
