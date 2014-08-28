"""create_table

Revision ID: 1e17b0a4c205
Revises: None
Create Date: 2014-08-27 16:07:16.363160

"""

# revision identifiers, used by Alembic.
revision = '1e17b0a4c205'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # account
    op.create_table(u'role',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.Unicode(length=64), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(u'privilege',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('code', sa.CHAR(64), nullable=False, unique=True),
        sa.Column('description', sa.Unicode(length=64), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), index=True,
                        server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(u'role_privilege',
        sa.Column('role_id', sa.Integer(), nullable=False,
                             primary_key=True, index=True),
        sa.Column('priv_id', sa.Integer(), nullable=False,
                             primary_key=True, index=True),
        sa.PrimaryKeyConstraint('role_id', 'priv_id'),
    )
    op.create_table(u'account',
        sa.Column('uid', sa.CHAR(32), nullable=False, primary_key=True),
        sa.Column(u'nickname', sa.Unicode(256), nullable=False),
        sa.Column('role_id', sa.Integer(),
                             sa.ForeignKey('role.id'), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), index=True,
                                  server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('uid'),
    )
    op.create_table(u'email',
        sa.Column('uid', sa.CHAR(32), sa.ForeignKey('account.uid'),
                         nullable=False, primary_key=True, unique=True),
        sa.Column(u'email', sa.String(length=256), nullable=False,
                            primary_key=True, unique=True),
        sa.Column(u'password_hash', sa.CHAR(length=40), nullable=False),
        sa.Column(u'password_salt', sa.CHAR(length=40), nullable=False),
        sa.Column(u'date_created', sa.DateTime(timezone=True),
                                   server_default=sa.func.current_timestamp(),
                                   nullable=False, index=True),
    )
    # bill
    op.create_table(u'address',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('real_name', sa.Unicode(64), nullable=False, index=True),
        sa.Column('mobile', sa.Unicode(32), nullable=False),
        sa.Column('code', sa.Unicode(32), nullable=False),
        sa.Column('IDnumber', sa.Unicode(64), nullable=False),
        sa.Column(u'date_created', sa.DateTime(timezone=True),
                                   server_default=sa.func.current_timestamp(),
                                   nullable=False, index=True),
    )


    op.create_table(u'logistics',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('genre', sa.Unicode(64), nullable=False, index=True),
        sa.Column('infomation', sa.UnicodeText(), nullable=False),
        sa.Column(u'date_created', sa.DateTime(timezone=True),
                                   server_default=sa.func.current_timestamp(),
                                   nullable=False, index=True),
    )


    op.create_table(u'bill',
        sa.Column('uid', sa.CHAR(32), nullable=False, primary_key=True),
        sa.Column('order_num', sa.Integer(), nullable=False, unique=True),
        sa.Column('genre', sa.Unicode(64), nullable=False, index=True),
        sa.Column('address_id', sa.Integer(),
                             sa.ForeignKey('address.id'), nullable=False),
        sa.Column('remark', sa.UnicodeText(), nullable=False),
        sa.Column(u'date_created', sa.DateTime(timezone=True),
                                   server_default=sa.func.current_timestamp(),
                                   nullable=False, index=True),
    )


    op.create_table(u'item',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('bill_uid', sa.CHAR(32),
                  sa.ForeignKey('bill.uid'), nullable=False),
        sa.Column('name', sa.Unicode(256), nullable=False),
        sa.Column('genre', sa.Unicode(64), nullable=False, index=True),
        sa.Column('dollar', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(),
                              server_default=u'1', nullable=False),
        sa.Column('remark', sa.UnicodeText(), nullable=False),
        sa.Column(u'date_created', sa.DateTime(timezone=True),
                                   server_default=sa.func.current_timestamp(),
                                   nullable=False, index=True),
    )


def downgrade():
    op.drop_table(u'role_privilege')
    op.drop_table(u'privilege')
    op.drop_table(u'email')
    op.drop_table(u'account')
    op.drop_table(u'role')
    op.drop_table(u'item')
    op.drop_table(u'bill')
    op.drop_table(u'logistics')
    op.drop_table(u'address')
