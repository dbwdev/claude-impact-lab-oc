"""Paths and settings. Packets are read in place and never copied into the repo."""

import os
from pathlib import Path

from dotenv import load_dotenv

PIPELINE_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = PIPELINE_DIR.parent
CHALLENGE_DIR = REPO_DIR / "challenges" / "1-referral-intake"

load_dotenv(PIPELINE_DIR / ".env")
load_dotenv(REPO_DIR / ".env")

PACKETS_DIR = Path(os.environ.get("INTAKE_PACKETS_DIR", CHALLENGE_DIR / "packets"))
CRITERIA_PATH = CHALLENGE_DIR / "criteria" / "admission-criteria.json"
# Only the eval command reads this. The pipeline itself must never see it.
DECISIONS_PATH = CHALLENGE_DIR / "eval" / "decisions.json"

# Derived from the packets, so it is packet content: gitignored, never committed.
CACHE_DIR = Path(os.environ.get("INTAKE_CACHE_DIR", PIPELINE_DIR / ".cache"))
OUT_DIR = Path(os.environ.get("INTAKE_OUT_DIR", PIPELINE_DIR / "out"))

MODEL = os.environ.get("INTAKE_MODEL", "claude-opus-5-5")
TRANSCRIBE_EFFORT = os.environ.get("INTAKE_TRANSCRIBE_EFFORT", "low")
REVIEW_EFFORT = os.environ.get("INTAKE_REVIEW_EFFORT", "high")
PAGE_WORKERS = int(os.environ.get("INTAKE_PAGE_WORKERS", "32"))
# "sectioned" = ~5 parallel review calls (faster, streams per section); "single" = one call.
REVIEW_MODE = os.environ.get("INTAKE_REVIEW_MODE", "sectioned")

# Longest page edge sent to Claude, in pixels.
RENDER_LONG_EDGE = int(os.environ.get("INTAKE_RENDER_LONG_EDGE", "2000"))

# Verification thresholds (starting points from the TypeSafe cookbooks; tune on our packets).
JEV_AUTO_ACCEPT = float(os.environ.get("INTAKE_JEV_AUTO_ACCEPT", "0.8"))
JEV_FLAG = float(os.environ.get("INTAKE_JEV_FLAG", "0.7"))
QUOTE_MATCH_MIN = int(os.environ.get("INTAKE_QUOTE_MATCH_MIN", "88"))
