"""
Test Challenge 05 - Checkpoint 2: Intermediate Layer Configuration

Validates that student has configured the intermediate layer in dbt_project.yml.
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
def dbt_project_yml(project_dir):
    """Load dbt_project.yml content."""
    yml_file = project_dir / "dbt_project.yml"

    if not yml_file.exists():
        pytest.fail("❌ dbt_project.yml not found")

    with open(yml_file, 'r') as f:
        return yaml.safe_load(f)


class TestIntermediateConfig:
    """Test that intermediate layer is configured in dbt_project.yml."""

    def test_models_section_exists(self, dbt_project_yml):
        """Must have models section in dbt_project.yml."""
        assert 'models' in dbt_project_yml, (
            "❌ No 'models' section in dbt_project.yml\n"
            "   Did you add the models configuration? (Section 2.1)"
        )

    def test_project_name_in_models(self, dbt_project_yml):
        """Models section must reference the project."""
        models = dbt_project_yml.get('models', {})
        project_name = dbt_project_yml.get('name', 'jaffle_shop_dbt')

        assert project_name in models, (
            f"❌ No '{project_name}' section in models configuration\n"
            "   Did you add the project-level configuration? (Section 2.1)\n"
            "   Expected structure:\n"
            "   models:\n"
            f"     {project_name}:\n"
            "       staging:\n"
            "         ...\n"
            "       intermediate:\n"
            "         ..."
        )

    def test_intermediate_section_exists(self, dbt_project_yml):
        """Must have intermediate section in models configuration."""
        models = dbt_project_yml.get('models', {})
        project_name = dbt_project_yml.get('name', 'jaffle_shop_dbt')
        project_models = models.get(project_name, {})

        assert 'intermediate' in project_models, (
            "❌ No 'intermediate' section in models configuration\n"
            "   Did you add intermediate layer config? (Section 2.1)\n"
            "   Example:\n"
            "   models:\n"
            "     jaffle_shop_dbt:\n"
            "       intermediate:\n"
            "         +materialized: view\n"
            "         +schema: intermediate"
        )

    def test_intermediate_has_materialized(self, dbt_project_yml):
        """Intermediate section should have materialized setting."""
        models = dbt_project_yml.get('models', {})
        project_name = dbt_project_yml.get('name', 'jaffle_shop_dbt')
        project_models = models.get(project_name, {})
        intermediate = project_models.get('intermediate', {})

        assert '+materialized' in intermediate, (
            "❌ No '+materialized' setting for intermediate models\n"
            "   Did you add the materialized configuration? (Section 2.1)\n"
            "   Example: +materialized: view"
        )

    def test_intermediate_has_schema(self, dbt_project_yml):
        """Intermediate section should have schema setting."""
        models = dbt_project_yml.get('models', {})
        project_name = dbt_project_yml.get('name', 'jaffle_shop_dbt')
        project_models = models.get(project_name, {})
        intermediate = project_models.get('intermediate', {})

        assert '+schema' in intermediate, (
            "❌ No '+schema' setting for intermediate models\n"
            "   Did you add the schema configuration? (Section 2.1)\n"
            "   Example: +schema: intermediate"
        )
