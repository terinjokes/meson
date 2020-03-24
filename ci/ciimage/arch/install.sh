#!/bin/bash

# Inspired by https://github.com/greyltc/docker-archlinux-aur/blob/master/add-aur.sh

pkgs=(
  python python-setuptools python-wheel python-pip python-pytest-xdist python-gobject python-jsonschema
  ninja make git sudo fakeroot autoconf automake patch
  libelf gcc gcc-fortran gcc-objc vala rust bison flex cython go dlang-dmd
  mono boost qt5-base gtkmm3 gtest gmock protobuf wxgtk gobject-introspection
  itstool gtk3 java-environment=8 gtk-doc llvm clang sdl2 graphviz
  doxygen vulkan-validation-layers openssh mercurial gtk-sharp-2 qt5-tools
  libwmf valgrind cmake netcdf-fortran openmpi nasm gnustep-base gettext
  # cuda
)

aur_pkgs=(scalapack)
pip_pkgs=(hotdoc)
cleanup_pkgs=(go)

AUR_USER=docker
PACMAN_OPTS='--needed --noprogressbar --noconfirm'

# Patch config files
sed -i 's/#Color/Color/g'                            /etc/pacman.conf
sed -i 's,#MAKEFLAGS="-j2",MAKEFLAGS="-j$(nproc)",g' /etc/makepkg.conf
sed -i "s,PKGEXT='.pkg.tar.xz',PKGEXT='.pkg.tar',g"  /etc/makepkg.conf

# Install packages
pacman -Syu $PACMAN_OPTS "${pkgs[@]}"
python -m pip install "${pip_pkgs[@]}"

# Setup the user
useradd -m $AUR_USER
echo "${AUR_USER}:" | chpasswd -e
echo "$AUR_USER      ALL = NOPASSWD: ALL" >> /etc/sudoers

# Install yay
su $AUR_USER -c 'cd; git clone https://aur.archlinux.org/yay.git'
su $AUR_USER -c 'cd; cd yay; makepkg'
pushd /home/$AUR_USER/yay/
pacman -U *.pkg.tar --noprogressbar --noconfirm
popd
rm -rf /home/$AUR_USER/yay

# Install yay deps
su $AUR_USER -c "yay -S $PACMAN_OPTS ${aur_pkgs[*]}"

# cleanup
pacman -Rs --noconfirm "${cleanup_pkgs[@]}"
su $AUR_USER -c "yes | yay -Scc"
