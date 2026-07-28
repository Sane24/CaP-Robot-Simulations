# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T10:56:21
# prompt_chars=14663
# tokens_in=4710 tokens_out=112
# seconds=3.6

confirm_before('put the red block on the purple block')
if is_obj_visible('purple block'):
    put_first_on_second('red block', 'purple block')
    say_verified(lambda: is_placed('red block', 'purple block'),
                 'Done, the red block is on the purple block.',
                 'The red block did not end up on the purple block.')
else:
    say('I don\'t see a purple block')
