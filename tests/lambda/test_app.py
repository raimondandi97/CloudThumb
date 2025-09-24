from app.lambda_functions.app import lambda_function

class TestLambda:

    def test_lambda_not_image(self):
        result = lambda_function({'key': '2ff9801c-e76b-4030-a333-0460ff56b443'})
        assert result["error"] == "Not an Image"

    def test_lambda_black_and_white(self):
        result = lambda_function({'key': '4b837eda-8626-47b6-ba10-64a1cad157fd'})
        assert result["result"] == "Black and White"

    def test_lambda_greyscale(self):
        result = lambda_function({'key': 'cdfd80db-a9cb-45b2-b9dd-a8c8f15ecd29'})
        assert result["result"] == "Greyscale"

    def test_lambda_color(self):
        result = lambda_function({'key': 'c8a80c1f-3c06-44e4-8241-f9eeb3355dc3'})
        assert result["result"] == "RGB"
