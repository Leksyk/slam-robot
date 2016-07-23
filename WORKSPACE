new_git_repository(
    name = "python_gflags",
    build_file = "gflags.BUILD",
    remote = "https://github.com/google/python-gflags.git",
    tag = "3.0.5",
)

bind(
    name = "python-gflags",
    actual = "@python_gflags//:gflags",
)
