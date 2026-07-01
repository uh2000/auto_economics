"""Microeconomics helpers for supply, demand, monopoly, and game theory."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sympy
from sympy import Eq, Symbol, diff, integrate, lambdify, parse_expr, solve

__all__ = ["Free_market", "Monopoly", "Game"]


def _style_axes(ax) -> None:
    """Clean, copy-paste-friendly look: soft gridlines, no top/right spines."""
    ax.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    sns.despine(ax=ax)


def _save(fig, save_path: str | None, dpi: int) -> None:
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")


def _to_expr(expression):
    if isinstance(expression, (int, float, sympy.Integer, sympy.Float)):
        return sympy.Float(expression)
    if isinstance(expression, str):
        return parse_expr(expression, evaluate=True)
    return sympy.sympify(expression)


def _as_float(value):
    return float(sympy.N(value))


def _positive_real(values):
    real_values = []
    for value in values:
        try:
            numeric = _as_float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(numeric):
            real_values.append(numeric)
    return [value for value in real_values if value >= 0]


def _best_solution(solutions):
    numeric = _positive_real(solutions)
    if numeric:
        return max(numeric)
    if solutions:
        return _as_float(solutions[0])
    raise ValueError("No solution found for the model.")


class Free_market:
    def __init__(self, supply, demand) -> None:
        self.supply = supply
        self.demand = demand

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def _x(self):
        return Symbol("x")

    def _supply_expr(self):
        return _to_expr(self.supply)

    def _demand_expr(self):
        return _to_expr(self.demand)

    def _function(self, expression):
        x = self._x()
        return lambdify(x, _to_expr(expression), modules=["numpy"])

    def _domain_limit(self, quantity, demand_expr):
        x = self._x()
        zeros = _positive_real(solve(Eq(demand_expr, 0), x))
        if zeros:
            return max(quantity * 1.5, zeros[0])
        return max(quantity * 1.5, 1.0)

    def equilibrium(self):
        x = self._x()
        supply_expr = self._supply_expr()
        demand_expr = self._demand_expr()
        quantity = _best_solution(solve(Eq(supply_expr, demand_expr), x))
        price = _as_float(supply_expr.subs(x, quantity))
        return {"quantity": float(quantity), "price": price}

    def get_quantity(self) -> float:
        return self.equilibrium()["quantity"]

    def get_price(self) -> float:
        return self.equilibrium()["price"]

    def get_zero_point(self, expression: str) -> float:
        x = self._x()
        return _best_solution(solve(Eq(_to_expr(expression), 0), x))

    def get_calculate_values(self, expression: str, end: int) -> dict:
        quantity_limit = max(float(end), 1.0)
        x_values = np.linspace(0, quantity_limit, num=min(50, max(5, int(math.ceil(quantity_limit)) + 1)))
        function = self._function(expression)
        return {float(x_value): _as_float(function(x_value)) for x_value in x_values}

    def get_consumer_surplus(self) -> float:
        x = self._x()
        equilibrium = self.equilibrium()
        surplus = integrate(self._demand_expr() - equilibrium["price"], (x, 0, equilibrium["quantity"]))
        return _as_float(surplus)

    def get_producer_surplus(self) -> float:
        x = self._x()
        equilibrium = self.equilibrium()
        surplus = integrate(equilibrium["price"] - self._supply_expr(), (x, 0, equilibrium["quantity"]))
        return _as_float(surplus)

    def get_economic_surplus(self) -> float:
        return self.get_consumer_surplus() + self.get_producer_surplus()

    def deadweight_loss(self) -> float:
        return 0.0

    def plot(self, complete: bool = False, show: bool = True, save_path: str | None = None, dpi: int = 200):
        equilibrium = self.equilibrium()
        quantity = equilibrium["quantity"]
        price = equilibrium["price"]
        demand_expr = self._demand_expr()
        supply_expr = self._supply_expr()
        max_quantity = self._domain_limit(quantity, demand_expr)

        q_values = np.linspace(0, max_quantity, 200)
        demand_values = np.array(self._function(demand_expr)(q_values), dtype=float)
        supply_values = np.array(self._function(supply_expr)(q_values), dtype=float)

        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(q_values, demand_values, label="Demand", color="#5b2a86")
        ax.plot(q_values, supply_values, label="Supply", color="#2f5d62")
        ax.axhline(price, linestyle="--", color="black", linewidth=1, label=f"Equilibrium price: {price:.2f}")
        ax.axvline(quantity, linestyle="--", color="gray", linewidth=1, label=f"Equilibrium quantity: {quantity:.2f}")

        if complete:
            consumer_mask = q_values <= quantity
            producer_mask = q_values <= quantity
            ax.fill_between(
                q_values,
                demand_values,
                price,
                where=consumer_mask & (demand_values >= price),
                color="#c084fc",
                alpha=0.3,
                label="Consumer surplus",
            )
            ax.fill_between(
                q_values,
                supply_values,
                price,
                where=producer_mask & (supply_values <= price),
                color="#bdbdbd",
                alpha=0.5,
                label="Producer surplus",
            )

        ax.set_xlabel("Quantity")
        ax.set_ylabel("Price")
        ax.set_title("Competitive market")
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
        _style_axes(ax)
        fig.tight_layout()
        _save(fig, save_path, dpi)

        if show:
            plt.show()
        return fig, ax

    def get_graph(self, complete: bool = False, save_path: str | None = None, dpi: int = 200) -> None:
        self.plot(complete=complete, show=True, save_path=save_path, dpi=dpi)


class Monopoly(Free_market):
    def _marginal_revenue_expr(self):
        x = self._x()
        return diff(self._demand_expr() * x, x)

    def equilibrium(self):
        x = self._x()
        mc_expr = self._supply_expr()
        mr_expr = self._marginal_revenue_expr()
        quantity = _best_solution(solve(Eq(mc_expr, mr_expr), x))
        price = _as_float(self._demand_expr().subs(x, quantity))
        return {"quantity": float(quantity), "price": price}

    def competitive_equilibrium(self):
        return super().equilibrium()

    def deadweight_loss(self) -> float:
        x = self._x()
        monopoly_eq = self.equilibrium()
        competitive_eq = self.competitive_equilibrium()
        low = min(monopoly_eq["quantity"], competitive_eq["quantity"])
        high = max(monopoly_eq["quantity"], competitive_eq["quantity"])
        welfare_gap = integrate(self._demand_expr() - self._supply_expr(), (x, low, high))
        return abs(_as_float(welfare_gap))

    def plot(self, complete: bool = False, show: bool = True, save_path: str | None = None, dpi: int = 200):
        monopoly_eq = self.equilibrium()
        competitive_eq = self.competitive_equilibrium()
        demand_expr = self._demand_expr()
        mc_expr = self._supply_expr()
        mr_expr = self._marginal_revenue_expr()

        max_quantity = self._domain_limit(competitive_eq["quantity"], demand_expr)
        q_values = np.linspace(0, max_quantity, 300)
        demand_values = np.array(self._function(demand_expr)(q_values), dtype=float)
        mc_values = np.array(self._function(mc_expr)(q_values), dtype=float)
        mr_values = np.array(self._function(mr_expr)(q_values), dtype=float)

        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(q_values, demand_values, label="Demand", color="#5b2a86")
        ax.plot(q_values, mc_values, label="Marginal cost", color="#2f5d62")
        ax.plot(q_values, mr_values, label="Marginal revenue", color="#ef6c00")
        ax.axvline(monopoly_eq["quantity"], linestyle="--", color="#ef6c00", linewidth=1, label=f"Monopoly quantity: {monopoly_eq['quantity']:.2f}")
        ax.axhline(monopoly_eq["price"], linestyle="--", color="#ef6c00", linewidth=1, alpha=0.7, label=f"Monopoly price: {monopoly_eq['price']:.2f}")
        ax.axvline(competitive_eq["quantity"], linestyle=":", color="#374151", linewidth=1, label=f"Competitive quantity: {competitive_eq['quantity']:.2f}")
        ax.axhline(competitive_eq["price"], linestyle=":", color="#374151", linewidth=1, alpha=0.7, label=f"Competitive price: {competitive_eq['price']:.2f}")

        if complete and competitive_eq["quantity"] > monopoly_eq["quantity"]:
            dwl_mask = (q_values >= monopoly_eq["quantity"]) & (q_values <= competitive_eq["quantity"])
            ax.fill_between(q_values, mc_values, demand_values, where=dwl_mask & (demand_values >= mc_values), color="#ef4444", alpha=0.25, label="Deadweight loss")

        if complete:
            consumer_mask = q_values <= monopoly_eq["quantity"]
            ax.fill_between(q_values, monopoly_eq["price"], demand_values, where=consumer_mask & (demand_values >= monopoly_eq["price"]), color="#c084fc", alpha=0.25, label="Consumer surplus")
            ax.fill_between(q_values, mc_values, monopoly_eq["price"], where=consumer_mask & (mc_values <= monopoly_eq["price"]), color="#bdbdbd", alpha=0.25, label="Producer surplus")

        # Marginal revenue typically dives well below the price axis; without a
        # cap it drags the y-limits down and squashes the demand/MC/surplus
        # region (the part readers actually care about) into a thin band.
        relevant_prices = np.concatenate([demand_values, mc_values, [monopoly_eq["price"], competitive_eq["price"]]])
        top = float(np.nanmax(relevant_prices)) * 1.1
        bottom = min(0.0, float(np.nanmin(relevant_prices)))
        ax.set_ylim(bottom, top)

        ax.set_xlabel("Quantity")
        ax.set_ylabel("Price")
        ax.set_title("Monopoly market")
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
        _style_axes(ax)
        fig.tight_layout()
        _save(fig, save_path, dpi)

        if show:
            plt.show()
        return fig, ax

    def get_graph(self, complete: bool = False, save_path: str | None = None, dpi: int = 200) -> None:
        self.plot(complete=complete, show=True, save_path=save_path, dpi=dpi)


class Game:
    def __init__(self, player_1: dict, player_2: dict) -> None:
        self.player_1 = player_1
        self.player_2 = player_2

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

    def _payoff_key(self, action_1: str, action_2: str) -> str:
        label = {"Cooperate": "cooperate", "Defect": "defect"}
        return f"{label[action_1]}-{'cooporate' if action_2 == 'Cooperate' else 'defect'}"

    def _payoffs(self) -> dict:
        actions = ("Cooperate", "Defect")
        return {
            (a1, a2): (
                self.player_1[self._payoff_key(a1, a2)],
                self.player_2[self._payoff_key(a1, a2)],
            )
            for a1 in actions
            for a2 in actions
        }

    def find_nash_equilibriums(self):
        actions = ("Cooperate", "Defect")
        payoffs = self._payoffs()

        nash_equilibriums = []
        for a1 in actions:
            for a2 in actions:
                other_1 = "Defect" if a1 == "Cooperate" else "Cooperate"
                other_2 = "Defect" if a2 == "Cooperate" else "Cooperate"
                payoff_1, payoff_2 = payoffs[(a1, a2)]
                player_1_best_response = payoff_1 >= payoffs[(other_1, a2)][0]
                player_2_best_response = payoff_2 >= payoffs[(a1, other_2)][1]
                if player_1_best_response and player_2_best_response:
                    nash_equilibriums.append((a1, a2))

        return nash_equilibriums

    def get_game_matrix(self) -> pd.DataFrame:
        """Payoff matrix as a DataFrame — renders as a copyable table in Jupyter."""
        actions = ("Cooperate", "Defect")
        payoffs = self._payoffs()
        return pd.DataFrame(
            [[f"{payoffs[(a1, a2)][0]}, {payoffs[(a1, a2)][1]}" for a2 in actions] for a1 in actions],
            columns=list(actions),
            index=list(actions),
        )

    def print_game_matrix(self) -> None:
        print(self.get_game_matrix())

    def plot_matrix(self, show: bool = True, save_path: str | None = None, dpi: int = 200):
        """Render the payoff matrix as an image, with Nash equilibria highlighted."""
        actions = ("Cooperate", "Defect")
        payoffs = self._payoffs()
        nash = set(self.find_nash_equilibriums())
        cell_text = [[f"{payoffs[(a1, a2)][0]}, {payoffs[(a1, a2)][1]}" for a2 in actions] for a1 in actions]

        fig, ax = plt.subplots(figsize=(5.5, 2.6))
        ax.axis("off")

        table = ax.table(
            cellText=cell_text,
            rowLabels=list(actions),
            colLabels=list(actions),
            cellLoc="center",
            rowLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2.2)

        for j in range(len(actions)):
            table[(0, j)].set_facecolor("#374151")
            table[(0, j)].get_text().set_color("white")
        for i in range(len(actions)):
            table[(i + 1, -1)].set_facecolor("#374151")
            table[(i + 1, -1)].get_text().set_color("white")
        for i, a1 in enumerate(actions):
            for j, a2 in enumerate(actions):
                if (a1, a2) in nash:
                    table[(i + 1, j)].set_facecolor("#c6f6d5")
                    table[(i + 1, j)].get_text().set_weight("bold")

        ax.set_title("Payoff matrix — (Player 1, Player 2)\nGreen = Nash equilibrium", fontsize=11)
        fig.tight_layout()
        _save(fig, save_path, dpi)

        if show:
            plt.show()
        return fig, ax
