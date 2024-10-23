import pytest
from typer.testing import CliRunner

from etsai.main import create_app
from etsai.plugin_loader import load_plugins
import cv2

runner = CliRunner()


@pytest.fixture
def app():
    return create_app()


def assert_video_duration(filename, expected_duration):
    # Verify the output file is a video and has a duration of 5 seconds
    cap = cv2.VideoCapture(str(filename))
    assert cap.isOpened()
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    # Allowing a small margin for floating point precision
    assert abs(duration - expected_duration) < 0.1
    cap.release()


def test_system_status(app):
    result = runner.invoke(app, ["system", "status"])
    assert result.exit_code == 0
    assert "Checking system status..." in result.output


def test_media_video_convert(app):
    result = runner.invoke(app, ["media", "video-convert"])
    assert result.exit_code == 0
    assert "Converting video..." in result.output


def test_media_video_trim_when_missing_args_then_error(app):
    result = runner.invoke(app, ["media", "video-trim"])
    assert result.exit_code != 0


def test_media_video_trim(app, tmp_path):
    output_file = tmp_path / "output.mp4"
    result = runner.invoke(app, ["media", "video-trim", "-f", "tests/helpers/video.mp4",
                           "--stop-time", "00:00:05", "-o", str(output_file)])
    assert result.exit_code == 0
    assert "Video trimmed successfully" in result.output
    assert output_file.exists()
    assert_video_duration(output_file, 5)


def test_media_image_generate(app):
    result = runner.invoke(app, ["media", "image-generate"])
    assert result.exit_code == 0
    assert "Generating image..." in result.output


@pytest.fixture
def fake_plugin(tmp_path):
    # Crear un plugin simulado en un directorio temporal
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    plugin_file = plugin_dir / "fake_plugin.py"
    plugin_code = """
def test_function():
    return "Plugin cargado correctamente"

def register():
    return {
        "fake_plugin": test_function
    }
"""
    plugin_file.write_text(plugin_code)

    return plugin_dir


def test_load_plugins(fake_plugin):
    # Llamar a la función load_plugins usando el directorio temporal como input
    plugins = load_plugins(plugins_dir=fake_plugin)

    # Verificar que el plugin fue cargado correctamente
    assert "fake_plugin" in plugins
    assert callable(plugins["fake_plugin"])
    assert plugins["fake_plugin"]() == "Plugin cargado correctamente"
