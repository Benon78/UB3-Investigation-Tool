class AnalysisSession:

    def __init__(self):

        self.reset()

    def reset(self):

        self.df = None

        self.customer_id = None

        self.ub3_count = 0

        self.record_count = 0

        self.balance_summary = {}

        self.risk_score = 0

        self.risk_level = "LOW"

        self.flags = []

        self.selected_results = []