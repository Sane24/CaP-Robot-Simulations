# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind
# task=S1
# run=1
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T13:15:53
# prompt_chars=12455
# tokens_in=3235 tokens_out=28
# seconds=1.0

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
