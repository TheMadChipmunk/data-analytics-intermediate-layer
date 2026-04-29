"""
Test Challenge 05 - Checkpoint 3: Documentation

Validates that student has documented the intermediate model in schema.yml.
"""

import pytest
from pathlib import Path
import yaml


@pytest.fixture
def project_dir():
    """Get jaffle_shop_dbt directory within challenge repo."""
    challenge_dir = Path(__file__).parent.parent
    dbt_project_dir = challenge_dir / "jaffle_shop_dbt"

    assert dbt_project_dir.exists(), (
        f"❌ jaffle_shop_dbt/ directory not found in {challenge_dir}\n"
        "   Did you copy your dbt project from the previous challenge? (Section 0)\n"
        "   Run: ls .. to find the previous challenge directory, then:\n"
        "   cp -rP ../PREVIOUS-CHALLENGE/jaffle_shop_dbt ."
    )

    return dbt_project_dir


@pytest.fixture
def intermediate_dir(project_dir):
    """Get the intermediate models directory."""
    return project_dir / "models" / "intermediate"


@pytest.fixture
def schema_yml(intermediate_dir):
    """Load schema.yml content."""
    yml_file = intermediate_dir / "schema.yml"

    if not yml_file.exists():
        pytest.skip("schema.yml doesn't exist yet")

    with open(yml_file, 'r') as f:
        return yaml.safe_load(f)


class TestDocumentation:
    """Test that intermediate models are documented in schema.yml."""

    def test_schema_yml_exists(self, intermediate_dir):
        """Must have schema.yml in intermediate directory."""
        schema_file = intermediate_dir / "schema.yml"
        assert schema_file.exists(), (
            "❌ schema.yml not found in intermediate directory\n"
            "   Expected: models/intermediate/schema.yml\n"
            "   Did you create the file and git push it? (Section 2.2)"
        )

    def test_has_version(self, schema_yml):
        """schema.yml must have version."""
        assert 'version' in schema_yml, (
            "❌ No 'version' in schema.yml\n"
            "   Did you add version: 2? (Section 2.2)"
        )

    def test_has_models_section(self, schema_yml):
        """schema.yml must have models section."""
        assert 'models' in schema_yml, (
            "❌ No 'models' section in schema.yml\n"
            "   Did you add the models list? (Section 2.2)\n"
            "   Example:\n"
            "   models:\n"
            "     - name: int_orders_with_payments\n"
            "       description: ..."
        )

    def test_documents_int_orders_with_payments(self, schema_yml):
        """Must document int_orders_with_payments model."""
        models = schema_yml.get('models', [])
        model_names = [m.get('name') for m in models]

        assert 'int_orders_with_payments' in model_names, (
            "❌ int_orders_with_payments not documented in schema.yml\n"
            "   Did you add the model documentation? (Section 2.2)\n"
            "   Example:\n"
            "   models:\n"
            "     - name: int_orders_with_payments\n"
            "       description: Orders enriched with aggregated payment data"
        )

    def test_int_orders_with_payments_has_description(self, schema_yml):
        """int_orders_with_payments must have a description."""
        models = schema_yml.get('models', [])
        int_model = next((m for m in models if m.get('name') == 'int_orders_with_payments'), None)

        if int_model is None:
            pytest.skip("Model not documented yet")

        assert 'description' in int_model and int_model['description'], (
            "❌ int_orders_with_payments must have a description\n"
            "   Did you add a description? (Section 2.2)\n"
            "   Example: description: Orders enriched with aggregated payment data"
        )

    def test_int_orders_with_payments_has_columns(self, schema_yml):
        """int_orders_with_payments should have columns documented."""
        models = schema_yml.get('models', [])
        int_model = next((m for m in models if m.get('name') == 'int_orders_with_payments'), None)

        if int_model is None:
            pytest.skip("Model not documented yet")

        assert 'columns' in int_model and len(int_model['columns']) > 0, (
            "❌ int_orders_with_payments should have columns documented\n"
            "   Did you document the columns? (Section 2.2)\n"
            "   Example:\n"
            "   columns:\n"
            "     - name: order_id\n"
            "       description: Unique order identifier"
        )
