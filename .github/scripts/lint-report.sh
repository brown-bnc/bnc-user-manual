#!/usr/bin/env bash
#
# Helper script for the lint-md-report workflow
#
# Designed for automation and not intended to be run locally. 
# I'd recommend running via workflow_dispatch in the Actions tab on Github.
#
# Usage: lint-report.sh <group_by> <results_file> <summary_file> <run_number> <run_url> [glob_input]
#
# group_by:     all | folder | file
# results_file: path to markdownlint-cli2-results.json
# summary_file: path to the summarize output captured from stdout
# run_number:   github.run_number
# run_url:      link to the workflow run
# glob_input:   optional path passed to workflow_dispatch; empty for full repo runs
set -euo pipefail

GROUP_BY="${1}"
RESULTS_FILE="${2}"
SUMMARY_FILE="${3}"
RUN_NUMBER="${4}"
RUN_URL="${5}"
GLOB_INPUT="${6}"
LABEL_LINT='lint'
LABEL_REPORT='automated-report'
ISSUE_LIMIT=200

# Echo error to stderr and exit
die() { echo "$*" 1>&2 ; exit 1; }

# Echo to stderr only
warn() {
  echo >&2 "$@"
}

build_report() {
  local out_file="${1}"
  local filter="${2}"  # jq filter applied to narrow results to a scope, e.g. 'select(.fileName | startswith("oscar/"))'
  local with_summary="${3:-false}"  # only used for 'all' mode — the summary is computed from the full markdownlint results and is only meaningful at that level
  local scope_note="${4:-}"  # optional note shown below the error count, e.g. to clarify scope coverage
  local rows rows_out row_count shown_count row_budget
  local body_limit=65000  # GitHub max is 65536; leave a buffer for header/footer overhead
  local summary=""

  # jq expression to extract matching errors and format each as a markdown table row;
  local jq_expr=".[] | $filter | \"| \(.fileName) | \(.lineNumber) | \(.ruleNames[0]) | \(.ruleDescription) |\""
  rows="$(jq -r "${jq_expr}" "${RESULTS_FILE}")"

  # Check if rows is empty. If so, there were no lint errors for this scope
  if [ -z "${rows}" ]; then
    warn "No lint errors found for: $(basename "${out_file}")"
    return 1
  fi

  row_count=$(echo "${rows}" | wc -l | tr -d ' ')

  # build the header first so we know exactly how many chars are left for rows
  echo "_Last updated: $(TZ='America/New_York' date '+%Y-%m-%d %H:%M %Z') · [Workflow run #${RUN_NUMBER}](${RUN_URL})_" > "${out_file}"
  echo "" >> "${out_file}"

  if [ "${with_summary}" = "true" ]; then
    summary="### 📊 Summary
\`\`\`
$(sed -n '/^Summary:/,$p' "${SUMMARY_FILE}")
\`\`\`

"
    echo "${summary}" >> "${out_file}"
  else
    echo "**${row_count} errors found**" >> "${out_file}"
    echo "" >> "${out_file}"
    if [ -n "${scope_note}" ]; then
      echo "> [!NOTE]" >> "${out_file}"
      echo "> ${scope_note}" >> "${out_file}"
      echo "" >> "${out_file}"
    fi
  fi

  echo "| File | Line | Rule | Description |" >> "${out_file}"
  echo "| :--- | :--- | :--- | :--- |" >> "${out_file}"

  # Guessimate how much row budget is left
  row_budget=$(( body_limit - ${#summary} - 100 ))

  # Echo the table contents
  if (( ${#rows} <= row_budget )); then
    echo "$rows" >> "${out_file}"
  else
    # truncate at the budget then trim back to the last complete row
    rows_out="${rows:0:$row_budget}"  # hard-truncate at char budget
    rows_out="${rows_out%$'\n'*}"     # drop the partial last row
    rows_out="${rows_out}"$'\n'       # restore trailing newline
    shown_count=$(echo "$rows_out" | wc -l | tr -d ' ')

    echo "${rows_out}" >> "${out_file}"
    echo "" >> "${out_file}"
    echo "> [!WARNING]" >> "${out_file}"
    echo "> Showing ${shown_count} of ${row_count} errors (body size limit reached). Run the workflow with a scoped path to see all errors." >> "${out_file}"
  fi
}

# create or update an issue; close it if no report file (full repo run only)
sync_issue() {
  local title="${1}"
  local body_file="${2}"

  local issue_number=$(gh issue list \
    --label "${LABEL_LINT}" --label "${LABEL_REPORT}" \
    --state open --limit "${ISSUE_LIMIT}" --json number,title \
    | jq -r --arg t "${title}" 'first(.[] | select(.title == $t) | .number) // empty')

  if [ -f "${body_file}" ]; then
    if [ -n "${issue_number}" ]; then
      gh issue edit "${issue_number}" --body-file "${body_file}"
    else
      gh issue create --title "${title}" --body-file "${body_file}" --label "${LABEL_LINT}" --label "${LABEL_REPORT}"
    fi
  elif [ -n "${issue_number}" ]; then
    gh issue close "${issue_number}" --comment "No lint errors found in the latest full repo run. Closing automatically."
  fi
}

# create a new issue; used for scoped runs
create_issue() {
  local title="${1}"
  local body_file="${2}"

  [ -f "${body_file}" ] || return 0

  gh issue create --title "${title}" --body-file "${body_file}" --label "${LABEL_LINT}" --label "${LABEL_REPORT}"
}

main() {
  # validate the results file before doing anything — a missing or unparseable file
  # likely means markdownlint failed for a non-lint reason (bad config, bad glob, etc.)
  # and we should not treat it as "no errors" or risk closing issues incorrectly
  if [ ! -f "${RESULTS_FILE}" ]; then
    die "Error: results file not found: ${RESULTS_FILE}"
  fi
  if ! jq -e 'type == "array"' "${RESULTS_FILE}" &> /dev/null; then
    die "Error: results file is not valid JSON: ${RESULTS_FILE}"
  fi

  if [ -n "$GLOB_INPUT" ]; then
    BASE_TITLE="fix(lint): ${GLOB_INPUT}"
  else
    BASE_TITLE="[HOLD] fix(lint): repo"
  fi

  # group results and create/update issues
  if [ "${GROUP_BY}" = "all" ]; then
    build_report /tmp/report.md "." true || echo "No lint errors found."
    # full repo run: sync_issue handles create, update, and close
    if [ -z "${GLOB_INPUT}" ]; then
      sync_issue "${BASE_TITLE}" /tmp/report.md
    else
      create_issue "${BASE_TITLE}" /tmp/report.md
    fi

  elif [ "${GROUP_BY}" = "folder" ]; then
    local field_depth folders slashes

    # group at exactly 1 level below the input path
    # e.g. path="visualization" → groups as "visualization/fiji", "visualization/vol"
    # e.g. no path → groups as top-level folders "oscar", "hpc-documentation", etc.
    # uses dirname-then-cap so files directly in the path (e.g. visualization/README.md)
    # are grouped under the path itself, not treated as a separate folder entry
    if [ -z "${GLOB_INPUT}" ]; then
      field_depth=1
    else
      slashes=$(echo "${GLOB_INPUT}" | tr -cd '/' | wc -c)
      field_depth=$((slashes + 2))
    fi
    if [ -f "${RESULTS_FILE}" ]; then
      folders=$(jq -r --argjson d "${field_depth}" '[.[].fileName | split("/")[:-1][0:$d] | join("/")] | unique[]' "${RESULTS_FILE}")
    else
      folders=""
    fi
    if [ -z "${folders}" ]; then
      echo "No lint errors found."
    fi

    local folder title safe scope_note
    for folder in ${folders}; do
      title="fix(lint): ${folder}"
      safe=$(echo "${folder}" | tr '/' '-')
      if [ "${folder}" = "${GLOB_INPUT}" ]; then
        scope_note="files directly in this folder; subfolder errors are tracked in separate issues"
      else
        scope_note="includes all subdirectories"
      fi
      build_report "/tmp/report-${safe}.md" "select((.fileName | split(\"/\")[:-1][0:${field_depth}] | join(\"/\")) == \"${folder}\")" false "$scope_note"
      create_issue "${title}" "/tmp/report-${safe}.md"
    done

  elif [ "${GROUP_BY}" = "file" ]; then
    local files
    if [ -f "${RESULTS_FILE}" ]; then
      files=$(jq -r '.[].fileName' "${RESULTS_FILE}" | sort -u)
    else
      files=""
    fi
    if [ -z "${files}" ]; then
      echo "No lint errors found."
    fi
    local file title safe
    for file in ${files}; do
      title="fix(lint): ${file}"
      safe=$(echo "${file}" | tr '/' '-')
      build_report "/tmp/report-${safe}.md" "select(.fileName == \"${file}\")"
      create_issue "${title}" "/tmp/report-${safe}.md"
    done
  fi
}

main ${@}
