#!/usr/bin/python3
# encoding: utf-8

import os, sys

def echo_run(cmd):
    print(cmd)
    ret = os.system(cmd)
    if ret != 0:
       exit(ret)

def most_recent(d):
    file_name = os.listdir(d)
    file_list = [os.path.join(d, f) for f in file_name]
    time_list = [os.path.getmtime(file_name) for file_name in file_list]
    max_time = max(time_list)
    max_id = time_list.index(max_time)
    return file_name[max_id]


root = "/data/software/DPDK"
pkg = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "pkg"))

log_file = os.path.join(root, "log.txt")
if os.path.exists(log_file):
    echo_run(f"rm {log_file}")

dirs = ["src", "build", "install"]
for d in dirs:
    exec(f"{d} = os.path.join(root, '{d}')")
    absdir = eval(f"{d}")
    echo_run(f"mkdir -p {absdir}")

pkg_list = os.listdir(pkg)
pkg_tail = ".tar.xz"
module_path = "/usr/share/modules/modulefiles/dpdk"
if not os.path.exists(module_path):
    echo_run(f"mkdir -p {module_path}")

for pkg_file in pkg_list:
    if not pkg_file.endswith(pkg_tail):
        print(f"skip {pkg_file}")
        continue
    echo_run(f"tar -xf {os.path.join(pkg, pkg_file)} -C {src} -m")
    # TODO: rename the extracted folder
    src_name = most_recent(src)
    src_path = os.path.join(src, src_name)
    build_path = os.path.join(build, src_name)
    install_path = os.path.join(install, src_name)
    if os.path.exists(build_path):
        echo_run(f"rm -r {build_path}")

    echo_run(f"meson setup {build_path} {src_path} --prefix={install_path} 2>&1 >> {log_file}")

    echo_run(f"ninja -C {build_path} install 2>&1 >> {log_file}")

    module_file = os.path.join(module_path, pkg_file[:-len(pkg_tail)])
    with open(module_file, "w") as f:
        bin_path = os.path.join(install_path, "bin")
        include_path = os.path.join(install_path, "include")
        lib_path = os.path.join(install_path, "lib", "x86_64-linux-gnu")
        pkgconfig_path = os.path.join(lib_path, "pkgconfig")
        f.write(f"#%Module1.0\nconflict dpdk\nprepend-path PATH {bin_path}\nprepend-path CPATH {include_path}\nprepend-path LD_LIBRARY_PATH {lib_path}\nprepend-path PKG_CONFIG_PATH {pkgconfig_path}\n")
