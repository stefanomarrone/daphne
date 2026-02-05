import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd: Path):
    """Run a command and fail fast with a clear error message."""
    print("\n>>> Running:", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=str(cwd), text=True)
    if completed.returncode != 0:
        raise SystemExit(f"Command failed with exit code {completed.returncode}: {' '.join(cmd)}")


def main():
    parser = argparse.ArgumentParser(
        description="Run the SoftwareX replication example end-to-end."
    )
    parser.add_argument(
        "--modes",
        type=str,
        default="single",
        help="The first argument to use is the mode: single or folder",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/configuration.ini",
        help="Path to the example configuration file (relative to replication/).",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default="..",
        help="Path to the project root (where your original main script lives).",
    )
    parser.add_argument(
        "--entrypoint",
        type=str,
        default="cmd_main.py",
        help="Entrypoint script (relative to project root).",
    )
    args = parser.parse_args()

    replication_dir = Path(__file__).resolve().parent
    project_root = (replication_dir / args.project_root).resolve()

    config_path = (replication_dir / args.config).resolve()
    if not config_path.exists():
        raise SystemExit(f"Config file not found: {config_path}")

    entrypoint_path = (project_root / args.entrypoint).resolve()
    if not entrypoint_path.exists():
        raise SystemExit(f"Entrypoint not found: {entrypoint_path}")

    modes = [s.strip() for s in args.modes.split(",") if s.strip()]
    if not modes:
        raise SystemExit("No modes selected. Use --modes single or folder.")

    for mode in modes:
        run([sys.executable, str(entrypoint_path), mode, str(config_path)], cwd=project_root)

    print("\nReplication run completed.")


if __name__ == "__main__":
    main()
