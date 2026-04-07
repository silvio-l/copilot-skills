---
name: homeassistant
description: >
  MUST USE for ANY Home Assistant related task. Invoke this skill IMMEDIATELY when the user asks to:
  check Home Assistant logs, diagnose HA errors or warnings, find unavailable entities, inspect system health,
  manage addons, call HA services, control smart home devices, check HA configuration,
  analyze integrations, debug automations, review sensor states, or perform any setup on Home Assistant.
  Also trigger when: the user mentions Home Assistant, HAOS, HA, smart home diagnostics, Zigbee/Z-Wave/Matter issues,
  integration problems, addon logs, or asks about entities, automations, scenes, or scripts in their home setup.
  Also triggers on German: 'Home Assistant pruefen', 'HA Logs', 'Smart Home Fehler', 'Entitaeten pruefen',
  'Automatisierung debuggen', 'Addon Status', 'HA Konfiguration'. This skill REPLACES ad-hoc HA API usage -
  never interact with Home Assistant without following these structured diagnostic patterns.
---

<!-- SKILL version: 1.0.0 | Last updated: 2026-04-07 | Last learning: public-safe generic configuration model -->

# Home Assistant Diagnostic & Management Skill

This skill provides structured workflows for diagnosing, monitoring, and managing Home Assistant installations through the `homeassistant` MCP server while keeping tracked skill content generic and public-safe.

## Public-Safe Configuration Model

Tracked repository content must stay generic. Installation-specific details belong only in ignored local files.

- **Tracked examples**
  - `homeassistant/references/local-config.example.yaml`
  - `homeassistant/references/local-secrets.example.env`
- **Ignored local files**
  - `homeassistant/local-config.yaml`
  - `homeassistant/local-config.json`
  - `homeassistant/local-secrets.env`
  - `homeassistant/local/`

Use the local files like this:

- **YAML/JSON** for structured context such as areas, aliases, notification targets, integration inventory, MQTT/Z2M settings, and preferred automation defaults
- **ENV** only for scalar secrets such as URLs, tokens, usernames, passwords, and API keys

Rules:

1. Read local config at session start if it exists.
2. Never copy live secrets, internal IPs, device identifiers, usernames, or private hostnames into tracked files, evals, commits, or examples.
3. If the needed installation detail is not available locally, ask the user instead of inventing it.
4. When learning something new about one installation, put it into ignored local config unless it is a broadly reusable Home Assistant pattern.

## Model Strategy

- **Default model for Home Assistant work**: **GPT-5.4**
- **Reasoning depth**: Use the highest available reasoning setting when the runtime supports it.
- When using the `task` tool for HA diagnostics, automations, MQTT/Zigbee, integrations, logs, planning, scripting, security, or remediation, explicitly prefer `model: "gpt-5.4"`.
- Reserve **Claude Opus 4.6** only for **UI/dashboard** work: Lovelace layout design, card composition, visual polish, screenshot-style review, and other presentation-heavy tasks.
- Do **not** default to Opus for routine HA diagnostics.

## MCP Tooling Strategy

Always prefer the Home Assistant MCP tools over raw HTTP calls.

### Connectivity, logs, and health
- `ha_self_test`
- `ha_api_status`
- `ha_get_config`
- `ha_check_config`
- `ha_get_error_log`
- `ha_get_hassio_logs`
- `ha_get_logbook`
- `ha_get_supervisor_info`
- `ha_get_core_info`
- `ha_get_host_info`
- `ha_get_system_health`
- `ha_get_backups`
- `ha_get_addons`
- `ha_get_addon_logs`

### Entity and history inspection
- `ha_get_states`
- `ha_get_entity`
- `ha_search_states`
- `ha_get_history`
- `ha_render_template`
- `ha_get_entities_by_domain`
- `ha_get_device_registry`
- `ha_get_entity_registry`
- `ha_get_areas`

### Actions and configuration
- `ha_get_services`
- `ha_call_service`
- `ha_fire_event`
- `ha_reload_config_entry`
- `ha_get_config_entries`
- `ha_delete_config_entry`
- `ha_start_config_flow`
- `ha_get_automation_config`
- `ha_update_automation_config`
- `ha_get_script_config`
- `ha_update_script_config`
- `ha_restart_core`

### MQTT / Zigbee2MQTT
- `ha_mqtt_publish`

## Critical Safety Rules

1. **Never modify HA core files or Supervisor internals** as part of routine automation or troubleshooting work. Read-only analysis of upstream code is fine; edits must stay in user-owned config and extensions.
2. **Allowed modification targets** are user-controlled surfaces such as `/config/configuration.yaml`, `/config/automations.yaml`, `/config/scripts.yaml`, `/config/secrets.yaml`, `/config/.storage/*`, and `/config/custom_components/*`, when the user asked for changes or the task clearly requires them.
3. **Always confirm destructive actions first**, including:
   - `ha_restart_core`
   - deleting config entries
   - bulk orphan cleanup
   - device removal / rename flows
   - mass entity disable/enable operations
4. **Validate before restart**. If configuration changed, run `ha_check_config` before any restart recommendation.
5. **Prefer reload over restart** whenever `ha_reload_config_entry`, automation reload, or script reload solves the problem.
6. **Fail closed on missing context**. Do not guess entity IDs, config entry IDs, MQTT topics, areas, or wake markers.
7. **Keep tracked files generic**. Broadly reusable patterns belong in the skill; installation-specific data belongs in ignored local config.

## Session Start Protocol

At the start of every HA-related session:

1. Read `homeassistant/local-config.yaml` or `homeassistant/local-config.json` if present.
2. Read `homeassistant/local-secrets.env` only if the task truly needs connection or secret values.
3. Run `ha_self_test` or `ha_api_status` before a larger diagnostic flow.
4. Check HA version and basic health with `ha_get_config` and `ha_get_system_health` when the task is broad.
5. If the user asked for a general audit, compare current warnings/errors/unavailable counts against any locally recorded baseline instead of treating raw counts alone as proof of failure.

## Best Practices

1. Start broad only when the user asked broad. For a narrow bug, stay narrow.
2. Use `ha_search_states` instead of `ha_get_states` when you already know the domain, state, or name pattern.
3. Use `ha_get_hassio_logs` on newer HAOS builds when classic error log retrieval is incomplete or version-dependent.
4. Group findings by severity and by integration, not by raw log order.
5. Distinguish **normal unavailable** from **unexpected unavailable** before calling something broken.
6. Use `ha_render_template` for joins across entities, devices, config entries, and attributes.
7. Present results in the user's language when possible.
8. When multiple independent queries are needed, batch them in parallel.
9. Keep remediation explicit: what to change, why, impact, and what to verify next.

## API Compatibility Notes

- On some newer HA builds, classic endpoints such as `/api/error_log` can behave differently or return 404. Prefer MCP wrappers that already handle version differences.
- Lovelace resource/config endpoints can return 404 in storage mode; do not assume dashboard resources are manageable through simple REST calls.
- Config entries can often be reloaded without restarting Core; prefer `ha_reload_config_entry`.
- REST coverage for entity enable/disable and some registry mutations is limited; WebSocket/UI or purpose-built helpers may still be required.
- Automation config APIs use the **numeric automation ID**, not the entity_id suffix.
- `ha_render_template` is often the fastest path for device/entity/config-entry correlation.
- Bulk cleanup should follow evidence. `restored: true`, minimal attributes, and persistent `unavailable` are useful ghost signals, not standalone proof.

## Diagnostic Workflows

### 1. Full System Health Check

When the user asks for a broad check such as "check my HA", follow this sequence:

1. `ha_api_status`
2. `ha_check_config`
3. `ha_get_error_log` or `ha_get_hassio_logs`
4. `ha_search_states` with `state_filter: "unavailable"`
5. `ha_search_states` with `state_filter: "unknown"`
6. `ha_get_supervisor_info`
7. `ha_get_host_info`
8. `ha_get_addons`

Present results with severity:

- **Critical**: config errors, API down, disk nearly full, a core integration missing, restart loops
- **Warning**: recurring integration errors, unusual unavailable spikes, pending updates, degraded add-ons
- **OK / expected**: normal transient warnings, offline-by-design devices, known startup noise

### 2. Error Log Analysis

When analyzing logs:

1. Retrieve logs with `ha_get_error_log` or `ha_get_hassio_logs`.
2. Classify by severity: `ERROR`, `WARNING`, `INFO`.
3. Group by likely integration/component.
4. Identify patterns:
   - recurring errors
   - startup-only errors
   - timeout/network failures
   - authentication failures
   - schema/config errors
   - deprecations
5. For each real issue, explain:
   - what it means
   - likely cause
   - best next action
   - whether the evidence is strong or partial

### 3. Integration Troubleshooting

For a specific integration:

1. Find affected entities with `ha_search_states`.
2. Check entity freshness and state via `ha_get_entity`.
3. Pull matching log evidence.
4. Inspect available services with `ha_get_services` if service registration is in doubt.
5. Use templates to inspect attributes, linked devices, or config entries.
6. Prefer `ha_reload_config_entry` when the integration is present but stale or partially disconnected.
7. If the integration is missing required credentials or re-auth, make that explicit instead of attempting magical recovery.

### 4. Entity Management

For entity lookup and triage:

- **Find by domain**: `ha_search_states(domain="sensor")`
- **Find unavailable**: `ha_search_states(state_filter="unavailable")`
- **Find by name**: `ha_search_states(name_pattern="temperature")`
- **Inspect one entity**: `ha_get_entity(entity_id="sensor.example")`
- **Check behavior over time**: `ha_get_history`

Useful distinctions:

- `unavailable`: source cannot currently provide state
- `unknown`: state exists but value is not currently meaningful or initialized
- stale timestamps: data may be frozen even if the entity is not formally unavailable

### 5. Service Execution

When performing actions:

1. State what you are about to do.
2. Confirm first if the action is destructive or broadly impactful.
3. Execute with `ha_call_service`.
4. Verify the affected entity or related state afterward.

Examples:

```yaml
# Reload automations
domain: automation
service: reload

# Reload all YAML config
domain: homeassistant
service: reload_all

# Turn on a light
domain: light
service: turn_on
data:
  entity_id: light.living_room

# Trigger an automation
domain: automation
service: trigger
data:
  entity_id: automation.morning_routine
```

### 6. Addon Management

For addon issues:

1. `ha_get_addons` for inventory, state, and updates
2. `ha_get_addon_logs` for the specific addon
3. Correlate addon failure with integration symptoms before blaming the addon

Common examples:

- MQTT broker problems -> check Mosquitto add-on and affected MQTT entities together
- music or media stack issues -> correlate addon logs with entity/service availability
- Samba/SSH complaints -> separate access issues from HA Core issues

### 7. Template Testing

Use `ha_render_template` for quick diagnostics:

```jinja2
{{ states('sensor.temperature') }}
{{ state_attr('climate.living_room', 'current_temperature') }}
{{ states.sensor | selectattr('state', 'eq', 'unavailable') | list | count }}
{% if is_state('binary_sensor.door', 'on') %}Door is open{% else %}Door is closed{% endif %}
```

Prefer templates when you need:

- cross-entity correlation
- config entry discovery
- device registry lookups
- counts and filters
- quick proofs before proposing config changes

### 8. Zigbee2MQTT Device Management

Zigbee2MQTT exposes a bridge API through MQTT. Use `ha_mqtt_publish`.

Example requests:

```yaml
topic: zigbee2mqtt/bridge/request/device/options
payload: {"id": "0xIEEE_ADDRESS", "options": {}}
```

```yaml
topic: zigbee2mqtt/bridge/request/device/options
payload: {"id": "0xIEEE_ADDRESS", "options": {"color_options": {"output": "xy"}}}
```

Guidance:

1. Use the IEEE address, not a guessed friendly name, for bridge-level device options.
2. Derive IEEE addresses from device identifiers or local config if available.
3. Keep device-specific quirks in ignored local config unless they are broadly reusable across installs.

Common bridge topics:

| Topic | Purpose |
|---|---|
| `zigbee2mqtt/bridge/request/device/options` | Get or set device options |
| `zigbee2mqtt/bridge/request/permit_join` | Enable or disable pairing |
| `zigbee2mqtt/bridge/request/device/rename` | Rename a device |
| `zigbee2mqtt/bridge/request/device/remove` | Remove a device |
| `zigbee2mqtt/{device_name}/set` | Control a device |
| `zigbee2mqtt/{device_name}/get` | Refresh a device state |

### 9. Ghost Entity Detection and Cleanup

Ghost entities are registry entries that remain after the original source stopped providing them.

Detection pattern:

1. Search unavailable entities.
2. Inspect attributes and registry data.
3. Look for `restored: true`, minimal attributes, duplicate suffixes, or missing source devices.
4. Distinguish ghosts from normal-offline devices before cleanup.

Cleanup guidance:

- Bulk orphan cleanup is **destructive** and requires confirmation.
- Prefer disabling first when you are not yet certain deletion is safe.
- If the installation uses Spook or another helper, verify that helper exists before recommending its services.

### 10. Config Entry Management

Useful sequence:

1. Find config entries via `ha_get_config_entries`
2. Correlate entry IDs with titles/domains
3. Reload via `ha_reload_config_entry`
4. Delete only with explicit confirmation and clear rationale

Example template for discovery:

```jinja2
{% for entry in config_entries() %}
ID: {{ entry.entry_id }} | Domain: {{ entry.domain }} | Title: {{ entry.title }} | State: {{ entry.state }}
{% endfor %}
```

### 11. Script and Automation Config Management

Use config APIs for targeted fixes.

Examples:

```yaml
ha_get_automation_config(automation_id="1234567890123")
```

```yaml
ha_update_script_config(
  script_id="my_script",
  config={
    "alias": "My Script",
    "mode": "restart",
    "sequence": []
  }
)
```

Patterns:

- change script `mode` when "already running" is the real issue
- fix broken entity references in triggers/conditions/actions
- use `if/then` or `choose` when branching is intended instead of relying on a bare failing condition as a silent stop gate

### 12. Frontend and Card-Mod Troubleshooting

Typical guidance:

- "loaded twice" warnings do not automatically prove duplicate resource entries
- browser cache and custom theme/card interactions are common causes
- storage-mode Lovelace often limits simple REST inspection paths

Do not make server-side changes until you have evidence the issue is not client-side.

### 13. Update Management

Before updates:

1. Check current version
2. Check pending updates
3. Recommend a backup before a significant update
4. Clarify expected downtime

After updates:

1. Re-run health checks
2. Look for new deprecations or changed API behavior
3. Capture new generic lessons in this skill only if they are broadly reusable
4. Put installation-specific changes into ignored local config

## Known General Behavior Patterns

| Area | Often Normal | Escalate When |
|---|---|---|
| Cloud integrations | Entities go unavailable while the device or vendor cloud is offline | The device is on, internet is healthy, and the integration never recovers |
| `mobile_app` sensors | Some sensors lag or go unavailable when the app is backgrounded | Sensors stay broken even after the app is opened and HA reconnects |
| MQTT template sensors | Startup-time payload or `value_json` issues cause transient warnings | Errors persist after fresh payloads arrive |
| Media integrations | Metadata or image fetch warnings can be transient | Playback control or core entity state is also broken |
| Zigbee battery devices | Slow reporting and sleepy behavior are expected | Device never checks in, shows routing issues, or misses critical events |
| Camera integrations | Stream/auth timeouts can be intermittent | All streams fail consistently or storage/network evidence points to a systemic outage |

## Continuous Improvement Rules

After each HA task, ask:

1. Did I learn a **generic** Home Assistant pattern?
2. Did I learn an **installation-specific** fact?
3. Did I discover a tool gap?
4. Did a workflow need refinement?

Then:

- Put **generic** reusable lessons into this tracked skill.
- Put **installation-specific** facts into ignored local config.
- If a tool gap exists, note the missing capability and prefer improving the MCP server rather than normalizing raw secret-heavy workarounds.
- Do **not** turn one user's private topology or credentials into tracked skill knowledge.

## Output Format

For diagnostics and recommendations, structure results as:

1. **Assessment** - what is healthy vs. likely broken
2. **Evidence** - logs, states, config, history, templates
3. **Severity** - critical / warning / expected
4. **Actions** - safest next steps in order
5. **Unknowns** - what still needs confirmation

This keeps Home Assistant work evidence-driven, repeatable, and safe for public skill storage.
