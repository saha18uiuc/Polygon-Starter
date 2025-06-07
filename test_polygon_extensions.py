from polygon.environment import Environment
from polygon.schemas import TableSchema, ColumnSchema

class TestSchemaBuilder:
    """Helper class to manage schema creation with proper IDs"""
    def __init__(self):
        self.table_counter = 1
        self.column_counter = 1

    def create_table(self, table_name, columns, pkeys=None, bound=3):
        """Create a table schema with auto-incrementing IDs"""
        if pkeys is None:
            pkeys = []
            
        # Create mapping of column names to types
        col_types = {name: typ for name, typ in columns}
        
        table = TableSchema(
            table_id=self.table_counter,
            table_name=table_name,
            bound=bound,
            lineage="test"
        )
        self.table_counter += 1
        
        for col_name, col_type in columns:
            column = ColumnSchema(
                column_id=self.column_counter,
                column_name=col_name,
                column_type=col_type,
                table_name=table_name
            )
            self.column_counter += 1
            table.append(column)
        
        return {
            "TableName": table_name,
            "TableSchema": table,
            "Bound": bound,
            "PKeys": [{"Name": pk, "Type": col_types[pk]} for pk in pkeys],
            "FKeys": [],
            "Others": []
        }

def create_test_env():
    """Create a test environment with properly configured schemas"""
    builder = TestSchemaBuilder()
    
    schema = [
        builder.create_table("employees", [
            ("id", "INT"),
            ("name", "TEXT"),
            ("salary", "INT"),
            ("dept", "TEXT"),
            ("gender", "TEXT")
        ], pkeys=["id"]),
        
        builder.create_table("sales", [
            ("product", "TEXT"),
            ("amount", "INT"),
            ("region", "TEXT")
        ], pkeys=["product"])
    ]
    
    # Create environment with higher bound to avoid index issues
    env = Environment(schema=schema, constraints=[], bound=10)
    
    # Load test data directly with proper column mapping
    env.db.tables = {
        1: [
            {"id": 1, "name": "Alice", "salary": 80000, "dept": "Engineering", "gender": "F"},
            {"id": 2, "name": "Bob", "salary": 120000, "dept": "Engineering", "gender": "M"},
            {"id": 3, "name": "Charlie", "salary": 70000, "dept": "HR", "gender": "F"}
        ],
        2: [
            {"product": "Widget", "amount": 100, "region": "North"},
            {"product": "Widget", "amount": 200, "region": "South"},
            {"product": "Gadget", "amount": 150, "region": "North"}
        ]
    }
    
    # Initialize schemas properly
    for table_id, table_data in env.db.tables.items():
        env.db.schemas[table_id] = schema[table_id-1]["TableSchema"]
    
    return env

def test_if_expression():
    """Test IF expression functionality"""
    try:
        env = create_test_env()
        
        # Basic IF test
        q1 = "SELECT IF(salary > 100000, 'High', 'Low') as salary_level FROM employees"
        q2 = "SELECT 'High' as salary_level FROM employees"
        is_equivalent, _, _, _, _ = env.check(q1, q2)
        assert not is_equivalent, "IF should conditionally select values"
        print("✅ Basic IF test passed")
        return True
    except Exception as e:
        print(f"❌ IF expression test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_filter_clause():
    """Test FILTER clause functionality"""
    try:
        env = create_test_env()
        
        # Filtered aggregate test
        q1 = "SELECT SUM(amount) FILTER (WHERE region = 'North') as north_sales FROM sales"
        q2 = "SELECT SUM(amount) as total_sales FROM sales"
        is_equivalent, _, _, _, _ = env.check(q1, q2)
        assert not is_equivalent, "Filtered aggregate should differ"
        print("✅ FILTER clause test passed")
        return True
    except Exception as e:
        print(f"❌ FILTER clause test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Polygon Extensions...")
    success = True
    success &= test_if_expression()
    success &= test_filter_clause()
    
    if success:
        print("🎉 All tests passed successfully!")
    else:
        print("🔴 Some tests failed")
    exit(0 if success else 1)