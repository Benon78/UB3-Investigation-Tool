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

        self.operation_counts = {}

        # ==========================
        # Fraud Investigation Data
        # ==========================

        self.risk_matrix = {}

        self.suspicious_lanterns = []

        self.suspicious_events = None

        self.verdict = ""

        self.recommendations = []

        self.lanterns = []

        # ==========================
        # Reporting Data
        # ==========================

        self.customer_summary = ""

        self.investigation_notes = ""

        self.report_preview = ""