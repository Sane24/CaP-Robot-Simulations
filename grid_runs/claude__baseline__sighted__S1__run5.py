# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=S1
# run=5
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T08:17:22
# prompt_chars=12457
# tokens_in=5250 tokens_out=35
# seconds=1.6

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
