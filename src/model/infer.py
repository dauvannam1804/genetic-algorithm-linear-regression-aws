import numpy as np

try:
    from .genetic_linear_regression import GeneticLinearRegression
except ImportError:
    from genetic_linear_regression import GeneticLinearRegression


def load_model(weights_path="src/weights/genetic_lr_weights.npy") -> GeneticLinearRegression:
    model = GeneticLinearRegression()
    model.load_model(weights_path)
    return model


def predict_sales(tv: float, radio: float, newspaper: float, model: GeneticLinearRegression) -> float:
    if model is None:
        model = load_model()  # Tự động load nếu chưa có model

    X = np.array([[tv, radio, newspaper]])
    y_pred = model.predict(X)
    return round(float(y_pred[0]), 2)


# ===== Example usage =====
if __name__ == "__main__":
    print("📺 ADVERTISING SALES PREDICTION")
    print("=" * 50)

    # Ví dụ input
    tv, radio, newspaper = 100.0, 25.0, 10.0

    # Load model & predict
    model = load_model()
    result = predict_sales(tv, radio, newspaper, model)

    print(f"\n💰 Input Advertising Spendings: TV=${tv}k, Radio=${radio}k, Newspaper=${newspaper}k")
    print(f"📈 Predicted Sales: {result:.2f}k")
