import pytest
from graph.workflow import create_workflow, execute_workflow


class TestWorkflowCreation:
    def test_workflow_exists(self):
        workflow = create_workflow()
        assert workflow is not None

    def test_workflow_has_nodes(self):
        workflow = create_workflow()
        assert len(workflow.nodes) > 0


@pytest.mark.integration
class TestWorkflowExecution:
    @pytest.mark.asyncio
    async def test_execute_basic_query(self):
        result = await execute_workflow("Find gaming laptops under 100000")
        assert "response" in result
        assert "products" in result
        assert "metadata" in result

    @pytest.mark.asyncio
    async def test_execute_returns_response(self):
        result = await execute_workflow("Best phones under 50000")
        assert isinstance(result["response"], str)
        assert len(result["response"]) > 0

    @pytest.mark.asyncio
    async def test_execute_metadata(self):
        result = await execute_workflow("Find laptops")
        assert "intent" in result["metadata"]
        assert "products_found" in result["metadata"]
