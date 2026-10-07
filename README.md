Second Brain Autonomous Agent Skill (v4.0.0)

Fully autonomous on-device agent for knowledge management according to the PARA (Projects, Areas, Resources, Archives) methodology. Optimized for Gemma 4 (E2B/E4B) models and works 100% offline, guaranteeing absolute privacy of your data.

Installation (Sideloading) in Google AI Edge Gallery

To install the local version, follow these steps:

Install the Google AI Edge Gallery app (requires Android 12+ or iOS 17+).

Copy the second-brain folder (including all subfolders) into the internal memory of your smartphone or tablet.

Open the Gallery app and go to the Agent Skills section.

Select the "Import from local file" option and specify the path to the copied skill folder.

When activating the skill, grant it the requested permissions to access the file system (storage.read, storage.write).

Architecture

SKILL.md - L1 Metadata and role instructions for LLM.

Scripts/ - Isolated runtime environment (WebView) for SQLite WASM database and business logic.

Assets/ — JSON schemes for calling tools.