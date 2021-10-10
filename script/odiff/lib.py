import subprocess
import time
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Tuple, Generator

from odiff.paths import REPO_ROOT
from odiff.toolchain import gcc


class Library:
    def __init__(self, name: str, source_dirs: List[Path], vendorobj_dir: Path, include_dirs: List[Path]):
        self.name = name
        self.source_dirs = source_dirs
        self.vendorobj_dir = vendorobj_dir
        self.vendorobj_paths: List[Path] = [*vendorobj_dir.glob('*.o')]
        self.include_dirs = include_dirs

    def build_obj(self, build_dir: Path, vendorobj_path: Path, cflags: List[str]) -> \
            Tuple[float, subprocess.CompletedProcess[bytes], Path]:
        """
        Build (reverse-engineered) object file from the corresponding vendor path passed in ``vendorobj_path``.

        :returns: Tuple of (elapsed time, subprocess result, output object file path)
        """
        source_path = None
        for source_dir in self.source_dirs:
            if (source_path := source_dir / f'{vendorobj_path.stem}.c').is_file():
                break
        if not source_path.is_file():
            raise FileNotFoundError(f"Source file {vendorobj_path.stem}.c for lib {self.name} not found")
        print(f"Building {self.name}/{source_path.name}")
        outobj_path = build_dir / vendorobj_path.name
        start = time.time()
        result = gcc(*cflags, *(f'-I{i}' for i in self.include_dirs), '-c', '-o', outobj_path,
                     source_path, check=False, capture_output=True)
        end = time.time()
        return end - start, result, outobj_path

    def get_vendorobj_paths(self, patterns: List[str]) -> Generator[Path, None, None]:
        return (
            f for f in self.vendorobj_paths
            if not patterns or any(fnmatch(f'{self.name}/{f.name}', p) for p in patterns)
        )


BLE_ROOT = REPO_ROOT / 'components/network/ble/blecontroller'
LIBRARIES = [
    Library(
        'libatcmd',
        [
            REPO_ROOT / 'components/stage/atcmd/src',
            REPO_ROOT / 'components/stage/atcmd/at_bl602'
        ],
        REPO_ROOT / 'libatcmd',
        [
            REPO_ROOT / 'components/stage/atcmd/inc',
            REPO_ROOT / 'components/stage/atcmd/inc/atcmd',
            REPO_ROOT / 'components/bl602/freertos_riscv_ram/config/',
            REPO_ROOT / 'components/bl602/freertos_riscv_ram/portable/GCC/RISC-V/'
        ]
    ),
    Library(
        'libblecontroller',
        [
            BLE_ROOT / 'h4tl/src',
            BLE_ROOT / 'ip/ble/ll/src/em',
            BLE_ROOT / 'ip/ble/ll/src/llc',
            BLE_ROOT / 'ip/ble/ll/src/lld',
            BLE_ROOT / 'ip/ble/ll/src/llm',
            BLE_ROOT / 'ip/ble/ll/src/rwble',
            BLE_ROOT / 'ip/ea/src',
            BLE_ROOT / 'ip/hci/src',
            BLE_ROOT / 'modules/common/src',
            BLE_ROOT / 'modules/dbg/src',
            BLE_ROOT / 'modules/ecc_p256/src',
            BLE_ROOT / 'modules/ke/src',
            BLE_ROOT / 'modules/rf/src',
            BLE_ROOT / 'modules/rwip/src',
            BLE_ROOT / 'plf/refip/src/arch',
            BLE_ROOT / 'plf/refip/src/arch/main',
            BLE_ROOT / 'plf/refip/src/driver/sec_eng',
            BLE_ROOT / 'plf/refip/src/driver/uart'
        ],
        REPO_ROOT / 'libblecontroller',
        [
            REPO_ROOT / 'components/bl602/bl602_std/bl602_std/Common/platform_print/',
            REPO_ROOT / 'components/bl602/bl602_std/bl602_std/Device/Bouffalo/BL602/Peripherals/',
            REPO_ROOT / 'components/bl602/bl602_std/bl602_std/RISCV/Core/Include/',
            REPO_ROOT / 'components/bl602/bl602_std/bl602_std/RISCV/Device/Bouffalo/BL602/Startup/',
            REPO_ROOT / 'components/bl602/bl602_std/bl602_std/StdDriver/Inc/',
            REPO_ROOT / 'components/bl602/freertos_riscv_ram/config/',
            REPO_ROOT / 'components/bl602/freertos_riscv_ram/portable/GCC/RISC-V/',
            REPO_ROOT / 'components/hal_drv/bl602_hal/',
            REPO_ROOT / 'components/network/ble/blecontroller/ble_inc/',
            REPO_ROOT / 'components/network/ble/blecontroller/ip/ble/ll/src/',
            REPO_ROOT / 'components/network/ble/blecontroller/ip/ea/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/ip/hci/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/modules/common/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/modules/ecc_p256/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/modules/ke/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/modules/rf/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/modules/rwip/api/',
            REPO_ROOT / 'components/network/ble/blecontroller/plf/refip/src/'
        ]
    )
]
