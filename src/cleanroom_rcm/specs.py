from dataclasses import dataclass

@dataclass(frozen=True)
class ReportSpec:
    family: str
    filename_tokens: tuple[str, ...]
    required_columns: tuple[str, ...]
    optional_columns: tuple[str, ...] = ()

REPORT_SPECS = (
    ReportSpec(
        family="claim_financial",
        filename_tokens=("claim", "financial"),
        required_columns=(
            "Claim No", "DOS", "Payer Name", "Rendering Provider", "CPT",
            "Charge Amount", "Payment Amount", "Adjustment Amount", "Balance Amount", "Claim Status"
        ),
    ),
    ReportSpec(
        family="provider_payment",
        filename_tokens=("payment",),
        required_columns=(
            "Payment ID", "Claim No", "Posting Date", "Payer Name", "Provider ID", "Payment Amount"
        ),
    ),
    ReportSpec(
        family="denial",
        filename_tokens=("denial",),
        required_columns=(
            "Denial ID", "Claim No", "Denial Date", "Payer Name", "CPT", "Denial Code", "Denial Category"
        ),
    ),
)
