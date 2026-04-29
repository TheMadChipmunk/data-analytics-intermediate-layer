"""
Test Challenge 05 - Checkpoint 1: Intermediate Model Creation

Validates that student has created the int_orders_with_payments model.
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_dir():
    """Get jaffle_shop_dbt directory within challenge repo."""
    challenge_dir = Path(__file__).parent.parent
    dbt_project_dir = challenge_dir / "jaffle_shop_dbt"

    assert dbt_project_dir.exists(), (
        f"❌ jaffle_shop_dbt/ directory not found in {challenge_dir}\n"
        f"   Did you copy your dbt project from the previous challenge? (Section 0)\n"
        f"   Run: ls .. to find the previous challenge directory, then:\n"
        f"   cp -rP ../PREVIOUS-CHALLENGE/jaffle_shop_dbt ."
    )

    return dbt_project_dir


@pytest.fixture
def intermediate_dir(project_dir):
    """Get the intermediate models directory."""
    return project_dir / "models" / "intermediate"


class TestIntermediateModel:
    """Test that int_orders_with_payments model is created."""

    def test_intermediate_directory_exists(self, intermediate_dir):
        """Must have an intermediate/ directory."""
        assert intermediate_dir.exists(), (
            "❌ No intermediate directory found\n"
            "   Expected: models/intermediate/\n"
            "   Did you create this directory? (Section 1.1)\n"
            "   Run: mkdir -p models/intermediate"
        )

    def test_int_orders_with_payments_exists(self, intermediate_dir):
        """Must create int_orders_with_payments.sql file."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"
        assert model_file.exists(), (
            "❌ int_orders_with_payments.sql not found\n"
            "   Expected: models/intermediate/int_orders_with_payments.sql\n"
            "   Did you create the file and git push it? (Section 1.2)"
        )

    def test_model_uses_ref_function(self, intermediate_dir):
        """Model should use {{ ref() }} to reference staging models."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"

        if not model_file.exists():
            pytest.skip("Model file doesn't exist yet")

        with open(model_file, 'r') as f:
            content = f.read()

        assert '{{ ref(' in content or "{{ ref(" in content, (
            "❌ Model must use {{ ref() }} function\n"
            "   Did you reference staging models correctly? (Section 1.2)\n"
            "   Example: SELECT * FROM {{ ref('stg_orders') }}"
        )

    def test_model_references_stg_orders(self, intermediate_dir):
        """Model should reference stg_orders."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"

        if not model_file.exists():
            pytest.skip("Model file doesn't exist yet")

        with open(model_file, 'r') as f:
            content = f.read()

        assert "ref('stg_orders')" in content or 'ref("stg_orders")' in content, (
            "❌ Model must reference stg_orders\n"
            "   Did you use {{ ref('stg_orders') }}? (Section 1.3)"
        )

    def test_model_references_stg_payments(self, intermediate_dir):
        """Model should reference stg_payments."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"

        if not model_file.exists():
            pytest.skip("Model file doesn't exist yet")

        with open(model_file, 'r') as f:
            content = f.read()

        assert "ref('stg_payments')" in content or 'ref("stg_payments")' in content, (
            "❌ Model must reference stg_payments\n"
            "   Did you use {{ ref('stg_payments') }}? (Section 1.3)"
        )

    def test_model_has_join(self, intermediate_dir):
        """Model must contain a JOIN to combine orders with aggregated payments."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"

        if not model_file.exists():
            pytest.skip("Model file doesn't exist yet")

        with open(model_file, 'r') as f:
            content = f.read().upper()

        assert 'JOIN' in content, (
            "❌ Model must contain a JOIN to combine orders with payments\n"
            "   Did you join stg_orders with the aggregated payments? (Section 1.3)\n"
            "   Tip: Use a LEFT JOIN to preserve all orders"
        )

    def test_model_has_aggregation(self, intermediate_dir):
        """Model must aggregate payments using GROUP BY and COUNT/SUM."""
        model_file = intermediate_dir / "int_orders_with_payments.sql"

        if not model_file.exists():
            pytest.skip("Model file doesn't exist yet")

        with open(model_file, 'r') as f:
            content = f.read().upper()

        has_group_by = 'GROUP BY' in content
        has_count = 'COUNT(' in content
        has_sum = 'SUM(' in content

        assert has_group_by and (has_count or has_sum), (
            "❌ Model must aggregate payments using GROUP BY and COUNT/SUM\n"
            "   Did you create a CTE that aggregates payments per order? (Section 1.3)\n"
            "   Tip: Use COUNT(*) for payment_count and SUM(amount) for total_amount"
        )
