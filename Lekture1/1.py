import sqlalchemy
import databases

DATABASE_URL = "sqlite:///hw.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(32)),
    sqlalchemy.Column("last_name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(64)),
)

products_table = sqlalchemy.Table(
    "products_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.Text()),
    sqlalchemy.Column("price", sqlalchemy.Float()),
)

orders_table = sqlalchemy.Table(
    "orders_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users_table.id")),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products_table.id")),
    sqlalchemy.Column("order_date", sqlalchemy.DateTime()),
    sqlalchemy.Column("order_status", sqlalchemy.String(20))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata.create_all(engine)