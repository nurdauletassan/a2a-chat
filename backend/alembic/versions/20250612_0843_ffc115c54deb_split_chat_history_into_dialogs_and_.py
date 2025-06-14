"""split_chat_history_into_dialogs_and_messages

Revision ID: ffc115c54deb
Revises: 39478d2da104
Create Date: 2025-06-12 08:43:17.860381+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ffc115c54deb'
down_revision = '39478d2da104'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dialogs',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dialog_id', sa.String(length=36), nullable=False),
    sa.Column('prompt', sa.Text(), nullable=False),
    sa.Column('response', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['dialog_id'], ['dialogs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.drop_index('ix_chat_history_dialog_id', table_name='chat_history')
    op.drop_index('ix_chat_history_id', table_name='chat_history')
    op.drop_table('chat_history')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_history',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('prompt', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('response', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('dialog_id', sa.VARCHAR(length=36), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='chat_history_pkey')
    )
    op.create_index('ix_chat_history_id', 'chat_history', ['id'], unique=False)
    op.create_index('ix_chat_history_dialog_id', 'chat_history', ['dialog_id'], unique=False)
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('dialogs')
    # ### end Alembic commands ### 