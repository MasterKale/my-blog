{ pkgs }: {
  deps = [
    pkgs.python3
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    ];
    PYTHONBIN = "${pkgs.python310}/bin/python3";
    LANG = "en_US.UTF-8";
  };
}