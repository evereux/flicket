"""add oidc_sub column

Revision ID: a3f1c9d24e57
Revises: 7ec6c2a6a1c8
Create Date: 2026-08-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a3f1c9d24e57'
down_revision = '7ec6c2a6a1c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flicket_users', sa.Column('oidc_sub', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_flicket_users_oidc_sub'), 'flicket_users', ['oidc_sub'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_flicket_users_oidc_sub'), table_name='flicket_users')
    op.drop_column('flicket_users', 'oidc_sub')
