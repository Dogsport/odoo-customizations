# Run AFTER 1_count_missing.py in the same shell. Test on 1 record first.
# Same as UI: Send -> untick "by Email" -> Generate. No e-mail is sent.
done, failed = [], []
for m in todo:
    try:
        wiz = env['account.move.send.wizard'].with_context(
            active_model='account.move', active_ids=m.ids).create({'move_id': m.id})
        wiz.sending_methods = False          # default is ['email'] -> must be cleared
        if wiz.sending_methods:
            raise Exception('e-mail still on - skipped')
        wiz.action_send_and_print()
        env.cr.commit()                      # required in odoo-bin shell
        done.append(m.name)
    except Exception as e:
        env.cr.rollback()                    # e.g. "concurrent update" -> just retry later
        failed.append((m.name, str(e)))
print(len(done), 'done')
print('failed:', failed)
