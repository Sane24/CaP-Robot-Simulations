# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=baseline
# task=S1
# run=5
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T13:09:19
# prompt_chars=12422
# tokens_in=4022 tokens_out=33
# seconds=3.6

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
