class ExplainerAgent:
    def explain(self, product):
        return {
            "name": product.get("name"),
            "description": product.get("description"),
            "features": product.get("features", []),
            "benefits": product.get("benefits", [])
        }
