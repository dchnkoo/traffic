"""empty message

Revision ID: d85e8b781a88
Revises: 
Create Date: 2024-12-18 15:36:27.614163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = 'd85e8b781a88'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('level',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('percent', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('offer',
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ordered_traffic', sa.Integer(), nullable=False),
    sa.Column('payment', sa.Float(), nullable=False),
    sa.Column('comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('taboo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('telegramuser',
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('is_bot', sa.Boolean(), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('language_code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.Column('added_to_attachment_menu', sa.Boolean(), nullable=True),
    sa.Column('can_join_groups', sa.Boolean(), nullable=True),
    sa.Column('can_read_all_group_messages', sa.Boolean(), nullable=True),
    sa.Column('supports_inline_queries', sa.Boolean(), nullable=True),
    sa.Column('can_connect_to_business', sa.Boolean(), nullable=True),
    sa.Column('has_main_web_app', sa.Boolean(), nullable=True),
    sa.Column('selected_language', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('blocked', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telegramuser_id'), 'telegramuser', ['id'], unique=False)
    op.create_table('topic',
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('admins',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offerlink',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('link', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offertopics',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team',
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('userinfo',
    sa.Column('balance', sa.Float(), nullable=False),
    sa.Column('current_withdraw_sum', sa.Integer(), nullable=False),
    sa.Column('already_withdrawed_sum', sa.Integer(), nullable=False),
    sa.Column('earned_from_partners', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['level_id'], ['level.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('useroffers',
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userpartners',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['partner_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usertraffic',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('traffic_user_id', sa.Integer(), nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['traffic_user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teammembers',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['telegramuser.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teamtopics',
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teamtopics')
    op.drop_table('teammembers')
    op.drop_table('usertraffic')
    op.drop_table('userpartners')
    op.drop_table('useroffers')
    op.drop_table('userinfo')
    op.drop_table('team')
    op.drop_table('offertopics')
    op.drop_table('offerlink')
    op.drop_table('admins')
    op.drop_table('topic')
    op.drop_index(op.f('ix_telegramuser_id'), table_name='telegramuser')
    op.drop_table('telegramuser')
    op.drop_table('offer')
    op.drop_table('level')
    # ### end Alembic commands ###