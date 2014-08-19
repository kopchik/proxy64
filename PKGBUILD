pkgname='proxy64'
pkgver=`date +%G%m%d`
_gitroot=("https://github.com/kopchik/proxy64.git")
_gitname=proxy64
pkgrel=1
depends=('python')
makedepends=('git')
arch=('any')

build() {
  git clone $_gitroot $_gitname
  cd "$srcdir/$pkgname"
  python3 ./setup.py build
}

package() {
  cd "$srcdir/$pkgname"
  python3 ./setup.py install
}
