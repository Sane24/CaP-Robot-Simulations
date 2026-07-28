# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=S2
# run=1
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-23T13:14:26
# prompt_chars=12473
# tokens_in=4030 tokens_out=46
# seconds=1.6

say('Lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', target_pos)
