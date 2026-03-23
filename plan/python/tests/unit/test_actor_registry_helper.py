from pathlib import Path

import pytest

from watchtower_core.control_plane import ActorRegistryHelper, ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> ActorRegistryHelper:
    return ActorRegistryHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_actor_registry_helper_resolves_declared_actors_and_types() -> None:
    helper = _helper()

    actor = helper.actor("actor.repository_maintainer")

    assert actor.actor_type == "user"
    assert actor.role == "owner"
    assert actor.scope == "repository"
    assert helper.has_actor("actor.codex") is True
    assert helper.has_actor("actor.missing") is False
    assert [entry.actor_id for entry in helper.actors_for_type("agent")] == ["actor.codex"]


def test_actor_registry_helper_validates_actor_policy_constraints() -> None:
    helper = _helper()

    issues = helper.validate_actor_reference(
        "actor.codex",
        allowed_types=("user",),
        allowed_roles=("owner",),
        allowed_scopes=("repository",),
    )

    assert [issue.issue_code for issue in issues] == [
        "actor_type_mismatch",
        "actor_role_mismatch",
    ]

    scope_issue = helper.validate_actor_reference(
        "actor.watchtower_core",
        allowed_scopes=("repository",),
    )
    assert [issue.issue_code for issue in scope_issue] == ["actor_scope_mismatch"]

    unknown = helper.validate_actor_reference("actor.unknown")
    assert unknown[0].issue_code == "unknown_actor_id"

    with pytest.raises(ValueError, match="Unknown actor_id: actor.unknown."):
        helper.require_actor("actor.unknown")

    with pytest.raises(ValueError, match="actor_type user"):
        helper.require_actor("actor.repository_maintainer", allowed_types=("agent",))
