import pandas as pd

class RaisonementParCas:
    def __init__(self, cases, n) -> None:
        self.weights = pd.Series({column : 1 for column in cases.columns})
        self.columns_to_compare = [
            "LotFrontage",
            "LotArea",
        ]
        self.columns_to_match = cases.columns.difference(self.columns_to_compare)
        self.cases = cases
        self.n = n

    def get_n_closest_cases(self,case, n) :
        cases_disimilarities = self.cases[self.columns_to_match] != case[self.columns_to_match]
        cases_comparisons = (self.cases[self.columns_to_compare] - case[self.columns_to_compare]).abs()
        cases_dis_comp = pd.concat([cases_disimilarities, cases_comparisons], axis=1)
        print(cases_dis_comp.iloc[0])
        self.cases["distances"] = (cases_dis_comp * self.weights).sum(axis=1)
        cases_sorted = self.cases.sort_values(by='distances')
        return cases_sorted.head(n)


    def adapt(self, case_with_Sol, case_to_adapt_to, columns_to_scale):
        for column in columns_to_scale:
            case_with_Sol["SalePrice"] *= case_to_adapt_to[column] / case_with_Sol[column] 
        return case_with_Sol["SalePrice"]

    def get_prediction(self,case_to_adapt_to):
        cases_with_sol = self.get_n_closest_cases(case_to_adapt_to, self.n)
        print(cases_with_sol)
        adapted_cases = self.adapt(cases_with_sol, case_to_adapt_to, self.columns_to_compare)
        return adapted_cases.mean()