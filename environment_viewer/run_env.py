
def exec_env():
    import importlib
    from gui import env_ui
    importlib.reload(env_ui)
    env_ui.run_env()