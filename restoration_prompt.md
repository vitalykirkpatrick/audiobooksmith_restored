# AudiobookSmith Project Restoration and Analysis Generation Prompt

This prompt is designed for an AI builder to seamlessly restore the AudiobookSmith project to its last working state, execute the full pipeline, and generate the final HTML analysis file.

## Goal
Restore the project from the GitHub repository, process the sample manuscript (`VITALY_CHAPTER_ONE_TWO_THREE.pdf`), and output the final `BOOK_COMPLETE.html` analysis file.

## Prerequisites
1.  **GitHub Access:** The repository must be cloned.
2.  **Working Directory:** All operations must occur within the cloned repository directory.
3.  **Required Files:** The following files must be present in the working directory:
    *   `api.py` (The modified version with the P-01 fix)
    *   `hybrid_chapter_extractor.py`
    *   `manifest_finder_full.py`
    *   `prompt_generator.py`
    *   `generate_manifests.py` (Simulation script for Phase 3 manifests)
    *   `VITALY_CHAPTER_ONE_TWO_THREE.pdf` (Must be placed in `input/raw_manuscript/`)

## Step-by-Step Restoration and Execution

### Phase 1: Setup and Restoration

1.  **Clone Repository:** Clone the GitHub repository containing the project files.
    ```bash
    gh repo clone vitalykirkpatrick/audiobooksmith_restored /home/ubuntu/audiobooksmith_project
    cd /home/ubuntu/audiobooksmith_project
    ```
2.  **Restore Data Structure:** Recreate the necessary data directories and place the sample PDF.
    ```bash
    mkdir -p input/raw_manuscript output/extracted_chapters data/prompts
    cp /path/to/VITALY_CHAPTER_ONE_TWO_THREE.pdf input/raw_manuscript/
    ```
3.  **Restore System Data:** Recreate the system-level manifest directory and the unified data file.
    ```bash
    mkdir -p /opt/audiobooksmith/data
    # The unified_narration_data.json file is critical for Phase 3
    # It must be restored or regenerated. For restoration, use the attached file:
    cp /path/to/unified_narration_data.json /opt/audiobooksmith/data/
    ```

### Phase 2: Pipeline Execution

The pipeline must be executed sequentially to ensure data flow.

1.  **Execute Hybrid Chapter Extractor (Phase 1):**
    *   **Script:** `hybrid_chapter_extractor.py`
    *   **Action:** Extract chapters from the PDF and save them to `output/extracted_chapters/`.
    ```bash
    python3 hybrid_chapter_extractor.py
    ```
2.  **Execute Manifest Generation (Simulated Phase 3):**
    *   **Script:** `generate_manifests.py`
    *   **Action:** Generate dummy manifest files (names.json, places.json) in the project's data directory.
    ```bash
    python3 generate_manifests.py
    ```
3.  **Execute Manifest Finder (Phase 2):**
    *   **Script:** `manifest_finder_full.py`
    *   **Action:** Aggregate all manifest data and save the result to `/opt/audiobooksmith/data/unified_narration_data.json`.
    ```bash
    python3 manifest_finder_full.py
    ```
4.  **Execute Prompt Generator (Phase 3):**
    *   **Script:** `prompt_generator.py`
    *   **Action:** Read the unified manifest data and generate the AI instruction set (`narration_prompts.json`).
    ```bash
    python3 prompt_generator.py
    ```
5.  **Execute Chapter Rewriter (Phase 4 - *Placeholder*):**
    *   **Script:** `chapter_rewriter.py` (Must be developed/restored)
    *   **Action:** Use `narration_prompts.json` to rewrite chapters and save to `output/narration_ready/`.
    ```bash
    # Placeholder for future AI Builder:
    # python3 chapter_rewriter.py
    ```
6.  **Execute HTML Builder (Phase 5 - *Placeholder*):**
    *   **Script:** `UNIVERSAL_HTML_BUILDER.py` (Must be developed/restored)
    *   **Action:** Use the Master Template, extracted chapters, and manifest data to generate the final HTML.
    ```bash
    # Placeholder for future AI Builder:
    # python3 UNIVERSAL_HTML_BUILDER.py
    ```

## Required Output
The final deliverable must be the contents of the generated `BOOK_COMPLETE.html` file, along with the contents of the `master_template.html` file for comparison.

## Verification
The final HTML must contain the blue header and the dynamically generated folder structure, confirming all components are working.
