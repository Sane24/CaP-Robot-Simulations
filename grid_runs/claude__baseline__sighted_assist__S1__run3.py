# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=S1
# run=3
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T09:29:21
# prompt_chars=12500
# tokens_in=5262 tokens_out=32
# seconds=1.5

say('Putting the red block on the green block')
put_first_on_second('red block', 'green block')
