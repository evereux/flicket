"""add branding fields

Revision ID: de2ab81f588e
Revises: a3f1c9d24e57
Create Date: 2026-11-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'de2ab81f588e'
down_revision = 'a3f1c9d24e57'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flicket_config', sa.Column('branding_company_name', sa.String(length=64), nullable=True))
    op.add_column('flicket_config', sa.Column('branding_phone', sa.String(length=32), nullable=True))
    op.add_column('flicket_config', sa.Column('branding_email', sa.String(length=128), nullable=True))
    op.add_column('flicket_config', sa.Column('branding_logo', sa.String(length=128), nullable=True))


def downgrade():
    op.drop_column('flicket_config', 'branding_logo')
    op.drop_column('flicket_config', 'branding_email')
    op.drop_column('flicket_config', 'branding_phone')
    op.drop_column('flicket_config', 'branding_company_name')
