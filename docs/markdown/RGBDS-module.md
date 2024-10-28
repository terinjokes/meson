# RGBDS Module

This module provides helper tools for build operations needed when
building Game Boy games using [RGBDS][].

[RGBDS]: https://rgbds.gbdev.io/

## Usage

To use this module, just do: **`rgbds = import('gnome')`**. The
following functions will then be available as methods on the object
with the name `rgbds`. You can, of course, replace the name `rgbds`
with anything else.

### rgbds.fix()

```
    rgbds.fix(id: string, input_file: string | File | Executable,
              build_by_default: bool = true,
              dependencies: [](File, CustomTarget, CustomTargetIndex) = [],
              extra_args: []string = [],
              install: bool = false,
              install_dir: string | None = None,
              title: str | None = None,
              japanese: bool = false,
              old_licensee: str | None = "0x33",
              new_licensee: str | None,
              pad: str | None,
              mbc_type: str | None,
              ram_size: str | None,
              fix_spec: str | None,
              ): CustomTarget
```

This functions applies patches to the ROM header, setting metadata about
the game and cartridge and computing checksums. Similar to a build target
it takes two positional arguments. The first argument is the name of the
output and the second is the input ROM. The ROM is automatically added
as a dependency of the generated target.

* `dependencies`: extra targets to depend upon for building
* `extra_args`: extra command line arguments to pass to `rgbfix`
* `install`: if true, install the fixed ROM
* `install_dir`: location to install the fixed ROM
* `title`: title string
* `japanese`: sets the region flag
* `old_licensee`: the old licensee ID, should be 0x33 for all new titles
* `new_licensee`: the new licensee ID
* `pad`: value to use to pad the ROM size
* `mbc_type`: memory bank controller type or name
* `ram_size`: cartridge RAM size
* `fix_spec`: the logo and checksum values to fix (or trash)

Returns an array containing: `[fixed_rom_file]`.

### rgbds.gfx()

```
    rgbds.gfx(id: string, input_file: string | File | Executable,
              build_by_default: bool = true,
              dependencies: [](File, CustomTarget, CustomTargetIndex) = [],
              extra_args: []string = [],
              install: bool = false,
              install_dir: string | None = None,
              columns: bool = false,
              depth: int | None = None,
              ): CustomTarget
```

This function converts PNGs into suitable data for the Game Boy
and Game Boy Color using `rgbgfx`. Similar to a build target it
takes two positional arguments. The first argument is the name of
the output and the second is the input PNG. The imgae is
automatically added as a dependency of the generated target.

* `dependencies`: extra targets to depend upon for building
* `extra_args`: extra command line arguments to pass to `rgbfix`
* `install`: if true, install the fixed ROM
* `install_dir`: location to install the fixed ROM
* `columns`: read squares in column-major order (default is row-major)
* `depth`: bit depth of output tile data

Returns an array containing: `[image_data_file]`.
