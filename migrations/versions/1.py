from alembic import op

revision = '1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with open('migrations/versions/1.sql') as fo:
        sql = fo.read()
        connection = op.get_bind()
        connection.execute(sql)


def downgrade():
    pass