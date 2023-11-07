if __name__ == "__main__":
    from kicad_amf_plugin.plugin._main import _main
    from wx import App
    app = App()
    _main()
    app.MainLoop()
