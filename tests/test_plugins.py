import pytest
from typer.testing import CliRunner

from etsai.main import app 
from etsai.plugin_loader import load_plugins

runner = CliRunner()

def test_system_status():
    app_loaded = app()
    result = runner.invoke(app_loaded, ["system", "status"])
    assert result.exit_code == 0
    assert "Checking system status..." in result.output

def test_media_video_convert():
    result = runner.invoke(app(), ["media", "video-convert"])
    assert result.exit_code == 0
    assert "Converting video..." in result.output

def test_media_image_generate():
    result = runner.invoke(app(), ["media", "image-generate"])
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