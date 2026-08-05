# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=S6
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the red block 5cm to the bottom.
# generated=2026-08-05T02:54:41
# prompt_chars=12530
# tokens_in=5280 tokens_out=62
# seconds=1.7

say('Ok - moving the red block 5cm to the bottom')
target_pos = parse_position('a point 5cm below the red block')
put_first_on_second('red block', target_pos)
