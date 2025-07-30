"""
Module for shared User-Defined Functions (UDFs).
"""
import re
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

# Define the schema that our UDF will return.
# This is more efficient than letting Spark infer it.
_AGENT_SCHEMA = StructType([
    StructField("sdk", StringType(), nullable=False),
    StructField("device", StringType(), nullable=False)
])

def _parse_user_agent_logic(user_agent_str):
    """
    Parses the User-Agent string to extract SDK and device information.
    This is the pure Python logic.

    Args:
        user_agent_str (str): The User-Agent string from the log.

    Returns:
        tuple(str, str): A tuple containing (sdk, device).
    """
    if not user_agent_str:
        return ("unknown", "unknown")

    # Regex to find our custom format: (sdk: value; device: value)
    match = re.search(r'sdk:\s*([^;]+);\s*device:\s*([^)]+)', user_agent_str)
    if match:
        sdk = match.group(1).strip()
        device = match.group(2).strip()
        return (sdk, device)

    # Basic check for common browser keywords if custom format is not found
    ua_lower = user_agent_str.lower()
    if any(keyword in ua_lower for keyword in ["mozilla", "chrome", "safari", "firefox", "edge"]):
        return ("unknown", "browser")

    # Default if no patterns match
    return ("unknown", "unknown")

# Register the function as a Spark UDF for use in DataFrames
parse_user_agent_udf = F.udf(_parse_user_agent_logic, _AGENT_SCHEMA)