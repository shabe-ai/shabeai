import importlib.metadata as md
import os
import subprocess
from datetime import datetime

import structlog
from fastapi import APIRouter, Request

router = APIRouter(tags=["meta"])


@router.get("/healthz")
async def healthz(request: Request):
    """Health check endpoint"""
    log = structlog.get_logger().bind(
        component="health-api", request_id=request.state.request_id
    )
    log.info("health_check_requested")
    return {"status": "ok"}


@router.get("/version")
async def version(request: Request):
    """Version information endpoint"""
    log = structlog.get_logger().bind(
        component="version-api", request_id=request.state.request_id
    )
    log.info("version_requested")
    try:
        # Get git commit hash
        git_hash = (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_hash = "unknown"

    try:
        # Get package version
        version = md.version("shabeai-backend")
    except md.PackageNotFoundError:
        version = "unknown"

    return {
        "version": version,
        "git": git_hash,
        "built_at": datetime.utcnow().isoformat() + "Z",
    }
