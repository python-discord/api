"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sqlalchemy as sa
from alembic import op
${imports if imports else ""}
# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """Upgrade the connected DB to this revision."""
    ${upgrades if upgrades else "pass"}


def downgrade():
    """Downgrade the connected DB to the previous revision."""
    ${downgrades if downgrades else "pass"}
