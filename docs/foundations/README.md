# `docs/foundations`

## Description
`This directory contains the repository foundation documents. Use it for the durable product, design-philosophy, standards-context, technology-direction, and narrative materials that shape the rest of the documentation and implementation surfaces. The authoritative files define the repository baseline. The .v1 companion files use clearer audience-shaped names and reading posture without replacing the authoritative docs.`

## Audience Routes

| Audience | Start Here | Then Read | Why |
|---|---|---|---|
| Engineers and maintainers | `engineering_design_principles.v1.md` | `engineering_stack_direction.v1.md`, `repository_standards_posture.v1.md`, `product.md` | Use this route when shaping the shared system, control plane, workflow layer, and implementation direction. |
| Product owners and engineering leads | `product_direction.v1.md` | `customer_story.v1.md`, `engineering_design_principles.v1.md`, `repository_standards_posture.v1.md` | Use this route when defining product shape, scope, tradeoffs, and delivery order. |
| Designers | `customer_story.v1.md` | `product_direction.v1.md`, `engineering_design_principles.v1.md` | Use this route when shaping the operator experience, user journey, and interaction model. |
| Customers, operators, and buyers | `customer_story.v1.md` | `product_narrative_brochure.md` | Use this route when the goal is to understand the user problem, value, and intended experience rather than internal governance detail. |

## Authoritative Backbone

| Path | Role |
|---|---|
| `docs/foundations/design_philosophy.md` | Canonical design-philosophy baseline for the repository and its operating model. |
| `docs/foundations/product.md` | Canonical product-shape baseline for core, domain packs, and first-wave scope. |
| `docs/foundations/product_narrative_brochure.md` | Canonical customer-facing narrative baseline. |
| `docs/foundations/standards.md` | Canonical standards-posture baseline for governed behavior. |
| `docs/foundations/technology_stack.md` | Canonical technology-direction baseline for implementation choices. |

## Audience-Shaped Companion Drafts

| Path | Recommended Name | Use |
|---|---|---|
| `docs/foundations/engineering_design_principles.v1.md` | `Engineering Design Principles` | Engineer-facing reading of the design philosophy. |
| `docs/foundations/product_direction.v1.md` | `Product Direction` | Product-facing reading of the product foundation. |
| `docs/foundations/customer_story.v1.md` | `Customer Story` | Customer and design-facing reading of the narrative brochure. |
| `docs/foundations/repository_standards_posture.v1.md` | `Repository Standards Posture` | Maintainer-facing reading of the standards foundation. |
| `docs/foundations/engineering_stack_direction.v1.md` | `Engineering Stack Direction` | Engineer-facing reading of the technology stack foundation. |

## Paths
| Path | Description |
|---|---|
| `docs/foundations/README.md` | Describes the purpose of the foundations directory and its main documents. |
| `docs/foundations/design_philosophy.md` | Defines the governing design philosophy for the repository and its operating model. |
| `docs/foundations/engineering_design_principles.v1.md` | Audience-shaped companion draft of the design philosophy for engineers and maintainers. |
| `docs/foundations/product.md` | Defines the product shape and shared product-layer boundaries. |
| `docs/foundations/product_direction.v1.md` | Audience-shaped companion draft of the product foundation for product owners and engineering leads. |
| `docs/foundations/product_narrative_brochure.md` | Provides the customer-facing product narrative and value framing. |
| `docs/foundations/customer_story.v1.md` | Audience-shaped companion draft of the narrative brochure for customers, operators, and designers. |
| `docs/foundations/standards.md` | Explains the repository-wide standards posture and why governed standards matter. |
| `docs/foundations/repository_standards_posture.v1.md` | Audience-shaped companion draft of the standards foundation for maintainers and contributors. |
| `docs/foundations/technology_stack.md` | Defines the current technology-direction baseline for the repository. |
| `docs/foundations/engineering_stack_direction.v1.md` | Audience-shaped companion draft of the technology stack foundation for engineers. |
