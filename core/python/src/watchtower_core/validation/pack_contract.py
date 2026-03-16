"""Pack-contract validation services."""

from __future__ import annotations

from watchtower_core.control_plane.errors import ControlPlaneError
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.models import ValidationIssue, ValidationResult

PACK_CONTRACT_VALIDATOR_ID = "validator.pack.contract"


class PackContractValidationService:
    """Validate that a pack publishes the governed surfaces core expects."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, pack_settings_path: str = PACK_SETTINGS_PATH) -> ValidationResult:
        """Validate one pack settings surface and its declared validation context."""

        try:
            PackValidationContext.from_loader(
                self._loader,
                pack_settings_path=pack_settings_path,
            )
        except (ControlPlaneError, ValueError) as exc:
            return ValidationResult(
                validator_id=PACK_CONTRACT_VALIDATOR_ID,
                target_path=pack_settings_path,
                engine="python",
                schema_ids=(),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="pack_contract_invalid",
                        message=str(exc),
                        location=pack_settings_path,
                    ),
                ),
            )

        return ValidationResult(
            validator_id=PACK_CONTRACT_VALIDATOR_ID,
            target_path=pack_settings_path,
            engine="python",
            schema_ids=(),
            passed=True,
            issues=(),
        )
