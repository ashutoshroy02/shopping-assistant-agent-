"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), server_default='user'),
        sa.Column('preferences', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('original_price', sa.Float),
        sa.Column('rating', sa.Float),
        sa.Column('review_count', sa.Integer, server_default='0'),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('brand', sa.String(100), nullable=False),
        sa.Column('specifications', postgresql.JSONB, server_default='{}'),
        sa.Column('images', postgresql.JSONB, server_default='[]'),
        sa.Column('availability', sa.Boolean, server_default='true'),
        sa.Column('source_url', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_products_category', 'products', ['category'])
    op.create_index('idx_products_brand', 'products', ['brand'])
    op.create_index('idx_products_price', 'products', ['price'])
    op.create_index('idx_products_rating', 'products', ['rating'])

    op.create_table(
        'reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('review_text', sa.Text, nullable=False),
        sa.Column('rating', sa.Float),
        sa.Column('sentiment_score', sa.Float),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('source', sa.String(100)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_reviews_product_id', 'reviews', ['product_id'])

    op.create_table(
        'recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('score', sa.Float, nullable=False),
        sa.Column('reasoning', sa.Text),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_recommendations_user_id', 'recommendations', ['user_id'])
    op.create_index('idx_recommendations_product_id', 'recommendations', ['product_id'])

    op.create_table(
        'price_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('recorded_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_price_history_product_id', 'price_history', ['product_id'])

    op.create_table(
        'saved_products',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('saved_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_saved_products_user_id', 'saved_products', ['user_id'])

    op.create_table(
        'search_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('query', sa.Text, nullable=False),
        sa.Column('filters', postgresql.JSONB, server_default='{}'),
        sa.Column('result_count', sa.Integer),
        sa.Column('searched_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_search_history_user_id', 'search_history', ['user_id'])

    op.create_table(
        'chat_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255)),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_chat_sessions_user_id', 'chat_sessions', ['user_id'])

    op.create_table(
        'chat_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('chat_sessions.id'), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_chat_messages_session_id', 'chat_messages', ['session_id'])

    op.create_table(
        'price_tracking',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('target_price', sa.Float, nullable=False),
        sa.Column('alert_on_drop', sa.Boolean, server_default='true'),
        sa.Column('status', sa.String(50), server_default='active'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_index('idx_price_tracking_user_id', 'price_tracking', ['user_id'])
    op.create_index('idx_price_tracking_status', 'price_tracking', ['status'])


def downgrade() -> None:
    op.drop_table('price_tracking')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('search_history')
    op.drop_table('saved_products')
    op.drop_table('price_history')
    op.drop_table('recommendations')
    op.drop_table('reviews')
    op.drop_table('products')
    op.drop_table('users')
