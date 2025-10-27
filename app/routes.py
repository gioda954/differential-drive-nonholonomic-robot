from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from flask import Blueprint, redirect, render_template, request, url_for

calculator_bp = Blueprint("calculator", __name__)


@dataclass
class CalculationResult:
    operand_a: Optional[float]
    operand_b: Optional[float]
    operator: str
    result: Optional[float]
    error: Optional[str]


def _perform_operation(operand_a: float, operand_b: float, operator: str) -> float:
    if operator == "+":
        return operand_a + operand_b
    if operator == "-":
        return operand_a - operand_b
    if operator == "*":
        return operand_a * operand_b
    if operator == "/":
        if operand_b == 0:
            raise ValueError("Division by zero is undefined")
        return operand_a / operand_b

    raise ValueError(f"Unsupported operator: {operator}")


@calculator_bp.route("/")
def index():
    return redirect(url_for("calculator.calculate"))


@calculator_bp.route("/calculator", methods=["GET", "POST"])
def calculate():
    calculation = CalculationResult(None, None, "+", None, None)
    if request.method == "POST":
        operator = request.form.get("operator", "+")
        operand_a_raw = request.form.get("operand_a", "0").strip()
        operand_b_raw = request.form.get("operand_b", "0").strip()

        try:
            operand_a = float(operand_a_raw)
            operand_b = float(operand_b_raw)
            result = _perform_operation(operand_a, operand_b, operator)
            calculation = CalculationResult(operand_a, operand_b, operator, result, None)
        except ValueError as exc:
            calculation = CalculationResult(None, None, operator, None, str(exc))

    return render_template("calculator.html", calculation=calculation)


__all__ = ["calculator_bp"]
