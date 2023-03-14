import sqlalchemy
import enum
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Enum, DateTime, Boolean, Text, ARRAY
from app.db.database import metadata, engine


# Enum class
class Role(enum.Enum):
    admin = "ADMIN"
    common = "COMMON"


class VariableType(enum.Enum):
    number = "NUMBER"
    multiple = "ENUM"


class DomainType(enum.Enum):
    interval = "INTERVAL"
    discrete = "SET_OF_DISCRETE_VALUES"


class Operator(enum.Enum):
    add = "+"
    subtract = "-"
    multiply = "*"
    divide = "/"
    modulo = "%"


class Metric(enum.Enum):
    moreThan = ">="
    lessThan = "<="
    s_moreThan = ">"
    s_lessThan = "<"
    equalTo = "=="
    different = "!="

class OptType(enum.Enum):
    minimize = "MINIMIZE"
    maximize = "MAXIMIZE"
    

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64)),
    Column("email", String, nullable=False, unique=True),
    Column("password", String(256)),
    Column("role", Enum(Role), default=Role.common),
    Column("verified", Boolean, nullable=False, default='False'),
    Column("verification_code", String, nullable=True, unique=True),
    Column("active", Boolean, default=True),
    Column("created_at", DateTime),
)

problems = sqlalchemy.Table(
    "problems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", Text),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
)

variables = sqlalchemy.Table(
    "variables",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("type", Enum(VariableType), nullable=False),
    Column("domain_type", Enum(DomainType)),
    Column("domain_value", ARRAY(Float), nullable=False),
    Column("problem_id", Integer, ForeignKey("problems.id", ondelete="CASCADE")),
)

constraints = sqlalchemy.Table(
    "constraints",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("coefficient", ARRAY(Integer), nullable=True),
    Column("operators", ARRAY(Enum(Operator)), nullable=True),
    Column("metric", Enum(Metric), nullable=False),
    Column("value", Float, nullable=False),
    Column("variable_id",Integer, ForeignKey("variables.id", ondelete="CASCADE")),
)

stats = sqlalchemy.Table(
    "stats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("mark", Float, nullable=False),
    Column("comment", Text, nullable=True),
    Column("problem_id", Integer, ForeignKey("problems.id", ondelete="CASCADE")),
)

metadata.create_all(engine)
