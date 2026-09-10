#!/usr/bin/env bash
# Устанавливает блоки пайплайна как персональные скиллы Claude Code.
set -Eeuo pipefail

FORCE=0
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      echo "Usage: ./install.sh [--dry-run] [--force]"
      exit 0
      ;;
    *)
      echo "Неизвестный аргумент: $arg" >&2
      exit 2
      ;;
  esac
done

DEST="${LANDING_SKILLS_DIR:-${HOME}/.claude/skills}"
BACKUP_ROOT="${LANDING_PIPELINE_BACKUP_DIR:-$(dirname "$DEST")/landing-pipeline-backups}"
for path in "$DEST" "$BACKUP_ROOT"; do
  case "$path" in
    ""|"/"|"$HOME"|"$HOME/")
      echo "Небезопасный путь: $path" >&2
      exit 2
      ;;
  esac
done

cd "$(dirname "$0")"

PAIRS=(
  "00-orchestrator:landing-pipeline"
  "01-discovery:landing-discovery"
  "02-reviews-parser:landing-reviews-parser"
  "03-synthetic-custdev:landing-synthetic-custdev"
  "04-copy-brief:landing-copy-brief"
  "05-design:landing-design"
  "06-landing-generation:landing-generation"
  "07-polish:landing-polish"
)

conflicts=()
for pair in "${PAIRS[@]}"; do
  name="${pair##*:}"
  if [[ -e "$DEST/$name" || -L "$DEST/$name" ]]; then
    conflicts+=("$name")
  fi
done

if [[ ${#conflicts[@]} -gt 0 && "$FORCE" -ne 1 ]]; then
  echo "Установка остановлена: уже существуют скиллы: ${conflicts[*]}" >&2
  echo "Повтори с --force: существующие версии будут перенесены в резервную копию вне каталога скиллов." >&2
  exit 1
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Путь установки: $DEST"
  echo "Путь резервных копий: $BACKUP_ROOT"
  for pair in "${PAIRS[@]}"; do
    echo "  ${pair%%:*} -> $DEST/${pair##*:}"
  done
  if [[ ${#conflicts[@]} -gt 0 ]]; then
    echo "Будут сохранены в резервную копию: ${conflicts[*]}"
  fi
  exit 0
fi

mkdir -p "$DEST"
stage_root="$(mktemp -d "${TMPDIR:-/tmp}/landing-pipeline-stage.XXXXXX")"
backup_dir=""
installed=()

cleanup_stage() {
  rmdir "$stage_root" 2>/dev/null || true
}
trap cleanup_stage EXIT

for pair in "${PAIRS[@]}"; do
  dir="${pair%%:*}"
  name="${pair##*:}"
  cp -R "$dir" "$stage_root/$name"
done

# Общие файлы копируются туда, где на них ссылаются установленные скиллы.
cp -R project-template "$stage_root/landing-pipeline/project-template"
cp DEPLOY.md "$stage_root/landing-pipeline/DEPLOY.md"
cp SECURITY.md "$stage_root/landing-pipeline/SECURITY.md"
cp SECURITY.md "$stage_root/landing-reviews-parser/SECURITY.md"
cp DEPLOY.md "$stage_root/landing-generation/DEPLOY.md"

required_stage_files=(
  "landing-pipeline/SKILL.md"
  "landing-pipeline/project-template/STATUS.md"
  "landing-pipeline/DEPLOY.md"
  "landing-reviews-parser/SECURITY.md"
  "landing-synthetic-custdev/03-synthetic-custdev.md"
  "landing-generation/LANDING-RULES.md"
  "landing-generation/DEPLOY.md"
)
for relative in "${required_stage_files[@]}"; do
  [[ -f "$stage_root/$relative" ]] || {
    echo "Неполный staging: нет $relative" >&2
    exit 1
  }
done

if [[ ${#conflicts[@]} -gt 0 ]]; then
  mkdir -p "$BACKUP_ROOT"
  backup_dir="$(mktemp -d "$BACKUP_ROOT/$(date +%Y%m%d-%H%M%S).XXXXXX")"
  for name in "${conflicts[@]}"; do
    mv "$DEST/$name" "$backup_dir/$name"
  done
  echo "Резервная копия: $backup_dir"
fi

rollback() {
  status=$?
  trap - ERR
  set +e
  mkdir -p "$BACKUP_ROOT"
  recovery_dir="$(mktemp -d "$BACKUP_ROOT/failed-install.$(date +%Y%m%d-%H%M%S).XXXXXX")"
  for name in "${installed[@]}"; do
    [[ -e "$DEST/$name" || -L "$DEST/$name" ]] && mv "$DEST/$name" "$recovery_dir/$name"
  done
  if [[ -n "$backup_dir" ]]; then
    for name in "${conflicts[@]}"; do
      [[ -e "$backup_dir/$name" || -L "$backup_dir/$name" ]] && mv "$backup_dir/$name" "$DEST/$name"
    done
  fi
  echo "Установка не завершена. Предыдущие версии восстановлены; новые файлы сохранены в $recovery_dir" >&2
  exit "$status"
}
trap rollback ERR

for pair in "${PAIRS[@]}"; do
  name="${pair##*:}"
  mv "$stage_root/$name" "$DEST/$name"
  installed+=("$name")
  echo "  ${pair%%:*} -> $DEST/$name"
done

for relative in "${required_stage_files[@]}"; do
  [[ -f "$DEST/$relative" ]]
done

trap - ERR
rmdir "$stage_root"
trap - EXIT
echo "Готово. В Claude Code: /landing-pipeline — весь цикл, /landing-discovery ... /landing-polish — отдельные шаги."
