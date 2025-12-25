# Конфигурационный файл PyOxidizer
# Запуск из корня проекта: pyoxidizer build --release

def make_exe():
    """Создание исполняемого файла."""
    dist = default_python_distribution()
    
    policy = dist.make_python_packaging_policy()
    policy.set_resource_handling_mode("classify")
    policy.include_file_resources = True
    policy.include_distribution_resources = True
    policy.resources_location = "in-memory"
    
    python_config = dist.make_python_interpreter_config()
    python_config.run_command = "import app; app.main()"
    python_config.filesystem_importer = True
    
    exe = dist.to_python_executable(
        name="app",
        packaging_policy=policy,
        config=python_config,
    )
    
    # Добавление локальных Python файлов
    package_resources = exe.read_package_root(
        path=".",
        packages=["app", "compute"],
    )
    exe.add_python_resources(package_resources)
    
    return exe

def make_embedded_resources(exe):
    """Создание встроенных ресурсов."""
    return exe.to_embedded_resources()

def make_install(exe):
    """Создание манифеста установки."""
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files

register_target("exe", make_exe)
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)

resolve_targets()
