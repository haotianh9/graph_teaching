from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType


def run(command: list[str | Path], cwd: Path | None = None) -> None:
    printable = " ".join(str(part) for part in command)
    print(printable, flush=True)
    subprocess.run([str(part) for part in command], cwd=cwd, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def ffprobe_streams(path: Path) -> str:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,codec_name,width,height,r_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def load_config(video_dir: Path) -> ModuleType:
    config_path = video_dir / "video_config.py"
    if not config_path.exists():
        raise FileNotFoundError(config_path)

    module_name = f"video_config_{abs(hash(config_path.resolve()))}"
    spec = importlib.util.spec_from_file_location(module_name, config_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {config_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def scene_names(config: ModuleType) -> list[str]:
    scenes = getattr(config, "SCENES")
    names: list[str] = []
    for scene in scenes:
        if isinstance(scene, str):
            names.append(scene)
        elif isinstance(scene, dict):
            names.append(scene["name"])
        else:
            names.append(scene[0])
    return names


def scene_timings(config: ModuleType) -> list[tuple[str, float, float]]:
    timings = getattr(config, "SCENE_TIMINGS", None)
    if timings:
        return [(str(name), float(start), float(end)) for name, start, end in timings]

    output: list[tuple[str, float, float]] = []
    current = 0.0
    for scene in getattr(config, "SCENES"):
        if isinstance(scene, str):
            duration = getattr(config, "DEFAULT_SCENE_DURATION", 8.0)
            name = scene
        elif isinstance(scene, dict):
            name = scene["name"]
            duration = scene.get("duration", getattr(config, "DEFAULT_SCENE_DURATION", 8.0))
        else:
            name = scene[0]
            duration = scene[1] if len(scene) > 1 else getattr(config, "DEFAULT_SCENE_DURATION", 8.0)
        output.append((str(name), current, current + float(duration)))
        current += float(duration)
    return output


def render_subdir(config: ModuleType) -> str:
    return getattr(config, "RENDER_SUBDIR", "720p30")


def video_dir_from_script(script_file: str) -> Path:
    return Path(script_file).resolve().parents[1]


def networkscience_root_from_video_dir(video_dir: Path) -> Path:
    current = video_dir.resolve()
    for parent in [current, *current.parents]:
        if parent.name == "NetworkScience":
            return parent
    raise RuntimeError(f"Could not locate NetworkScience root from {video_dir}")


def copy_scene_outputs(tmp_media_dir: Path, video_dir: Path, config: ModuleType) -> None:
    source_dir = tmp_media_dir / "videos" / "main" / render_subdir(config)
    target_dir = video_dir / "media" / "videos" / "main" / render_subdir(config)
    target_dir.mkdir(parents=True, exist_ok=True)
    for scene in scene_names(config):
        source = source_dir / f"{scene}.mp4"
        if not source.exists():
            raise FileNotFoundError(source)
        target = target_dir / source.name
        shutil.copy2(source, target)
        print(f"copied {target.relative_to(video_dir)}", flush=True)


def write_concat_file(paths: list[Path], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(f"file '{path.resolve()}'\n" for path in paths), encoding="utf-8")

