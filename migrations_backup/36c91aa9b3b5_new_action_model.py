"""new action model

Revision ID: 36c91aa9b3b5
Revises: fe0f77ef3f46
Create Date: 2019-10-20 21:23:05.959617

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36c91aa9b3b5'
down_revision = 'fe0f77ef3f46'
branch_labels = None
depends_on = None


def upgrade():
    # get connection
    conn = op.get_bind()

    # check if it is possible to migrate
    r = conn.execute(sa.text("SELECT COUNT(id) FROM flicket_ticket_action WHERE (assigned IS NOT NULL) "
            "+ (claimed IS NOT NULL) + (released IS NOT NULL) + (closed IS NOT NULL) "
            "+ (opened IS NOT NULL) + (status IS NOT NULL) + (priority IS NOT NULL) != 1"))
    assert r.first()[0] == 0, 'Automatic migration not possible, do it manually!'
    import json

    # add new columns
    op.add_column('flicket_ticket_action', sa.Column('action', sa.String(length=30), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('data', sa.JSON(none_as_null=True), nullable=True))


    # transform data into action column
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE opened IS NOT NULL'),
                 {'action': 'open'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE assigned IS NOT NULL'),
                 {'action': 'assign'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE claimed IS NOT NULL'),
                 {'action': 'claim'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE status IS NOT NULL'),
                 {'action': 'status'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE priority IS NOT NULL'),
                 {'action': 'priority'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE released IS NOT NULL'),
                 {'action': 'release'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET action=:action WHERE closed IS NOT NULL'),
                 {'action': 'close'})

    # update data column for status action
    r = conn.execute(sa.text('SELECT status FROM flicket_ticket_action WHERE status IS NOT NULL GROUP BY status'))
    for rr in r:
        data = {
                'status': rr[0],
                'note': 'migrated during 0.2.1 release',
                }
        s = conn.execute(sa.text('SELECT id FROM flicket_status WHERE status=:status'), {'status': rr[0]}).fetchall()
        if len(s) == 1:
            data['status_id'] = s[0][0]
        conn.execute(sa.text('UPDATE flicket_ticket_action SET data=:data WHERE status=:status'),
                     {'data': json.dumps(data), 'status': rr[0]})

    # update data column for priority action
    r = conn.execute(sa.text('SELECT priority FROM flicket_ticket_action WHERE priority IS NOT NULL GROUP BY priority'))
    for rr in r:
        data = {
                'priority': rr[0],
                'note': 'migrated during 0.2.1 release',
                }
        s = conn.execute(sa.text('SELECT id FROM flicket_priorities WHERE priority=:priority'), {'priority': rr[0]}).fetchall()
        if len(s) == 1:
            data['priority_id'] = s[0][0]
        conn.execute(sa.text('UPDATE flicket_ticket_action SET data=:data WHERE priority=:priority'),
                     {'data': json.dumps(data), 'priority': rr[0]})

    # update ticket_id
    conn.execute(sa.text('UPDATE flicket_ticket_action '
            'SET ticket_id=(SELECT ticket_id FROM flicket_post WHERE id=flicket_ticket_action.post_id) '
            'WHERE post_id IS NOT NULL'))

    with op.batch_alter_table('flicket_ticket_action') as batch_op:
        # drop old columns
        batch_op.drop_column('status')
        batch_op.drop_column('claimed')
        batch_op.drop_column('opened')
        batch_op.drop_column('released')
        batch_op.drop_column('priority')
        batch_op.drop_column('assigned')
        batch_op.drop_column('closed')


def downgrade():
    # DOWNGRADE CAN BE DANGEROUS AND RESULT IN DATA LOST

    # get connection
    conn = op.get_bind()

    # check first if possible
    r = conn.execute(sa.text('SELECT COUNT(id) FROM flicket_ticket_action WHERE action NOT IN :actions'),
                     {'actions': ('open', 'assign', 'claim', 'status', 'priority', 'release', 'close')})
    assert r.first()[0] == 0, 'Automatic downgrade not possible, do it manually!'

    # add old columns
    op.add_column('flicket_ticket_action', sa.Column('closed', sa.Boolean(), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('assigned', sa.Boolean(), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('priority', sa.String(length=12), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('released', sa.Boolean(), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('opened', sa.Boolean(), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('claimed', sa.Boolean(), nullable=True))
    op.add_column('flicket_ticket_action', sa.Column('status', sa.String(length=20), nullable=True))

    # transform data from action and data columns
    conn.execute(sa.text('UPDATE flicket_ticket_action SET opened=:value WHERE action=:action'),
                 {'value': True, 'action': 'open'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET assigned=:value WHERE action=:action'),
                 {'value': True, 'action': 'assign'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET claimed=:value WHERE action=:action'),
                 {'value': True, 'action': 'claim'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET status=JSON_VALUE(data, :path) WHERE action=:action'),
                 {'path': '$.status', 'action': 'status'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET priority=JSON_VALUE(data, :path) WHERE action=:action'),
                 {'path': '$.priority', 'action': 'priority'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET released=:value WHERE action=:action'),
                 {'value': True, 'action': 'release'})
    conn.execute(sa.text('UPDATE flicket_ticket_action SET closed=:value WHERE action=:action'),
                 {'value': True, 'action': 'close'})

    # set ticket_id NULL if post_id
    conn.execute(sa.text('UPDATE flicket_ticket_action SET ticket_id=NULL WHERE post_id IS NOT NULL'))

    # drop new columns
    op.drop_column('flicket_ticket_action', 'data')
    op.drop_column('flicket_ticket_action', 'action')
