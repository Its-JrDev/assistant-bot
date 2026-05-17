#!/bin/bash
# Limpia del historial git los archivos con secrets.
# EJECUTAR SOLO SI EL REPO FUE PÚBLICO.
# Requiere git-filter-repo: pip install git-filter-repo
#
# Uso: bash scripts/cleanup_git_history.sh

set -e

echo "Eliminando config.py del historial..."
git filter-repo --path config.py --invert-paths --force

echo "Eliminando database/data.db del historial..."
git filter-repo --path database/data.db --invert-paths --force

echo "Eliminando excel/data.xlsx del historial..."
git filter-repo --path excel/data.xlsx --invert-paths --force

echo ""
echo "Historial limpiado. Revisa con 'git log --oneline' y luego:"
echo "  git remote add origin <url>"
echo "  git push origin --force --all"
