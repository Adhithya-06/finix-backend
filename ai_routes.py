from flask import Blueprint, jsonify
import pandas as pd
import numpy as np
from models import db, Transaction
from datetime import timedelta
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt
import warnings

warnings.filterwarnings("ignore")  # Suppress ARIMA convergence warnings

ai_routes = Blueprint('ai_routes', __name__)

@ai_routes.route('/insights', methods=['GET'])
def transaction_insights():
    try:
        transactions = Transaction.query.all()
        if not transactions:
            return jsonify({"message": "No transactions found"}), 404

        data = [{"date": t.date, "category": t.category, "amount": t.amount} for t in transactions]
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])

        category_totals = df.groupby("category")["amount"].sum().reset_index()
        highest_spent_category = category_totals.loc[category_totals["amount"].idxmax(), "category"]
        highest_spent_amount = category_totals["amount"].max()

        df = df.groupby("date").sum().reset_index()
        df = df.sort_values("date")

        all_days = pd.date_range(start=df["date"].min(), end=df["date"].max())
        df = df.set_index("date").reindex(all_days, fill_value=0).rename_axis("date").reset_index()

        # ARIMA model
        model = ARIMA(df["amount"], order=(2, 1, 2))
        model_fit = model.fit()

        forecast = model_fit.forecast(steps=28)
        forecast = np.maximum(forecast, 0)

        # Error Metrics
        actual = df["amount"][-28:]
        predicted_fit = model_fit.predict(start=actual.index[0], end=actual.index[-1])
        predicted_fit = np.maximum(predicted_fit, 0)

        mae = round(mean_absolute_error(actual, predicted_fit), 2)
        mse = round(mean_squared_error(actual, predicted_fit), 2)
        rmse = round(sqrt(mse), 2)

        # Weekly predictions
        last_date = df["date"].max()
        week_ranges = {}
        for i in range(0, 28, 7):
            start_date = (last_date + timedelta(days=i + 1)).date()
            end_date = (last_date + timedelta(days=i + 7)).date()
            week_total = round(forecast[i:i+7].sum(), 2)
            week_ranges[f"{start_date} to {end_date}"] = week_total

        insights = {
            "highest_spending_category": highest_spent_category,
            "highest_spent_amount": round(highest_spent_amount, 2),
            "advice": f"Try reducing expenses in '{highest_spent_category}' category to save more!",
            "predicted_total_spending": week_ranges,
            "evaluation_metrics": {
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse
            }
        }

        return jsonify(insights), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500







