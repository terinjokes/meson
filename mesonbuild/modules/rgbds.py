# SPDX-License-Identifier: Apache-2.0
# Copyright 2015-2016 The Meson development team

'''This module provides helper functions for RGBDS
such as fixing ROM headers and converting graphics'''
from __future__ import annotations

import typing as T

from . import (
    ExtensionModule, GirTarget, GResourceHeaderTarget, GResourceTarget, ModuleInfo,
    ModuleReturnValue, TypelibTarget, VapiTarget,
)
from .. import mesonlib
from ..build import CustomTarget, CustomTargetIndex, Executable, GeneratedList, InvalidArguments
from ..interpreter.type_checking import DEPENDS_KW, DEPEND_FILES_KW, ENV_KW, INSTALL_DIR_KW, INSTALL_KW, NoneType, DEPENDENCY_SOURCES_KW, in_set_validator, CT_BUILD_BY_DEFAULT
from ..interpreterbase import typed_kwargs, KwargInfo, ContainerTypeInfo
from ..interpreterbase.decorators import typed_pos_args

if T.TYPE_CHECKING:
    from . import ModuleState
    from ..interpreter import Interpreter
    from ..mesonlib import FileOrString

    class RGBFix(TypedDict):

        build_by_default: bool
        dependencies: T.List[T.Union[mesonlib.File, CustomTarget, CustomTargetIndex]]
        extra_args: T.List[str]
        install: bool
        install_dir: T.Optional[str]
        title: T.Optional[str]
        japanese: bool
        old_licensee: T.Optional[str]
        new_licensee: T.Optional[str]
        pad: T.Optional[str]
        mbc_type: T.Optional[str]
        ram_size: T.Optiona[str]
        fix_spec: T.Optional[str]

    class RGBGfx(TypedDict):
        build_by_default: bool
        dependencies: T.List[T.Union[mesonlib.File, CustomTarget, CustomTargetIndex]]
        extra_args: T.List[str]
        install: bool
        install_dir: T.Optional[str]
        depth: T.Optional[int]
        columns: bool


# Differs from the CustomTarget version in that it straight defaults to True
_BUILD_BY_DEFAULT: KwargInfo[bool] = KwargInfo(
    'build_by_default', bool, default=True,
)

_EXTRA_ARGS_KW: KwargInfo[T.List[str]] = KwargInfo(
    'extra_args',
    ContainerTypeInfo(list, str),
    default=[],
    listify=True,
)

class RGBDSModule(ExtensionModule):
    INFO = ModuleInfo('rgbds')

    def __init__(self, interpreter: 'Interpreter') -> None:
        super().__init__(interpreter)
        self.rgbgfx: T.Optional[T.Union[ExternalProgram, Executable, OverrideProgram]] = None
        self.methods.update({
            'fix': self.fix,
            'gfx': self.gfx,
        })

    @typed_pos_args('rgbds.fix', str, (str, mesonlib.File, CustomTarget, CustomTargetIndex, GeneratedList, Executable))
    @typed_kwargs(
        'rgbds.fix',
        _BUILD_BY_DEFAULT,
        _EXTRA_ARGS_KW,
        INSTALL_KW,
        INSTALL_DIR_KW,
        KwargInfo('dependencies', ContainerTypeInfo(list, (mesonlib.File, CustomTarget, CustomTargetIndex)), default=[], listify=True),
        KwargInfo('title', (str, NoneType)),
        KwargInfo('japanese', bool, default=False),
        KwargInfo('old_licensee', (str, NoneType), default='0x33'),
        KwargInfo('new_licensee', (str, NoneType)),
        KwargInfo('mbc_type', (str, NoneType)),
        KwargInfo('ram_size', (str, NoneType)),
        KwargInfo('fix_spec', (str, NoneType)),
        KwargInfo('pad', (str, NoneType)),
    )
    def fix(self, state: 'ModuleState', args: T.Tuple[str, 'FileOrString'], kwargs: 'RGBFix') -> 'ModuleReturnValue':
        target_name, input_file = args

        rgbfix = state.find_program('rgbfix', required=True, for_machine=mesonlib.MachineChoice.BUILD)
        cmd: T.List[T.Union['ToolType', str]] = [rgbfix]

        if kwargs['title']:
            cmd += ['--title', kwargs['title']]

        if not kwargs['japanese']:
            cmd += ['--non-japanese']

        if kwargs['old_licensee']:
            cmd += ['--old-licensee', kwargs['old_licensee']]

        if kwargs['new_licensee']:
            cmd += ['--new-licensee', kwargs['new_licensee']]

        if kwargs['mbc_type']:
            cmd += ['--mbc-type', kwargs['mbc_type']]

        if kwargs['ram_size']:
            cmd += ['--ram-size', kwargs['ram_size']]

        if kwargs['fix_spec']:
            cmd += ['--fix-spec', kwargs['fix_spec']]

        if kwargs['pad']:
            cmd += ['--pad', kwargs['pad']]

        cmd += kwargs['extra_args']
        cmd += ['-']

        target = CustomTarget(
            target_name,
            state.subdir,
            state.subproject,
            state.environment,
            cmd,
            [input_file],
            [target_name],
            build_by_default=kwargs['build_by_default'],
            capture=True,
            feed=True,
            extra_depends=kwargs['dependencies'],
            install=kwargs['install'],
            install_dir=kwargs['install_dir'],
        )

        return ModuleReturnValue(target, [target])

    @typed_pos_args('rgbds.gfx', str, (str, mesonlib.File, CustomTarget, CustomTargetIndex, GeneratedList))
    @typed_kwargs(
        'rgbds.gfx',
        CT_BUILD_BY_DEFAULT,
        _EXTRA_ARGS_KW,
        INSTALL_KW,
        INSTALL_DIR_KW,
        KwargInfo('dependencies', ContainerTypeInfo(list, (mesonlib.File, CustomTarget, CustomTargetIndex)), default=[], listify=True),
        KwargInfo('depth', (int, NoneType)),
        KwargInfo('columns', bool, default=False),
    )
    def gfx(self, state: 'ModuleState', args: T.Tuple[str, 'FileOrString'], kwargs) -> 'ModuleReturnValue':
        target_name, input_file = args

        if not self.rgbgfx:
            self.rgbgfx = state.find_program('rgbgfx', required=True, for_machine=mesonlib.MachineChoice.BUILD)
        rgbgfx = self.rgbgfx
        cmd: T.List[T.Union['ToolType', str]] = [rgbgfx]

        if kwargs['depth']:
            cmd += ['--depth', str(kwargs['depth'])]

        if kwargs['columns']:
            cmd += ['--columns']

        cmd += ['-o', '@OUTPUT@', '@INPUT@']
        cmd += kwargs['extra_args']

        target = CustomTarget(
            target_name,
            state.subdir,
            state.subproject,
            state.environment,
            cmd,
            [input_file],
            [target_name],
            build_by_default=kwargs['build_by_default'],
            extra_depends=kwargs['dependencies'],
            install=kwargs['install'],
            install_dir=kwargs['install_dir'],
        )

        return ModuleReturnValue(target, [target])


def initialize(interp: 'Interpreter') -> RGBDSModule:
    mod = RGBDSModule(interp)
    return mod
