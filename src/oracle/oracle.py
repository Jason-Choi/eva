from dataclasses import dataclass

import pandas as pd

from src.model import GleanerDashboard
from src.oracle import OracleResult, OracleWeight
from src.oracle.scores import (
    get_coverage_from_nodes,
    get_diversity_from_nodes,
    get_interestingness,
    get_specificity_from_nodes,
    get_conciseness_from_nodes,
)


class Oracle:
    df: pd.DataFrame

    def __init__(self, df) -> None:
        self.df = df
        self.weight = OracleWeight()

    def get_result(
        self, dashboard: GleanerDashboard, preferences: set[str]
    ) -> OracleResult:
        nodes = dashboard.charts
        return OracleResult(
            weight=self.weight,
            coverage=get_coverage_from_nodes(nodes, self.df),
            diversity=get_diversity_from_nodes(nodes),
            interestingness=get_interestingness(nodes),
            specificity=get_specificity_from_nodes(nodes, preferences),
            conciseness=get_conciseness_from_nodes(nodes, self.df),
        )

    def update(
        self,
        specificity: float | None,
        interestingness: float | None,
        coverage: float | None,
        diversity: float | None,
        conciseness: float | None,
    ) -> None:
        if specificity is not None:
            self.weight.specificity = specificity
        if interestingness is not None:
            self.weight.interestingness = interestingness
        if coverage is not None:
            self.weight.coverage = coverage
        if diversity is not None:
            self.weight.diversity = diversity
        if conciseness is not None:
            self.weight.conciseness = conciseness
