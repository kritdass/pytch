# pytch

### Pytch Yields Technical Characteristics Hastily

<br/>

![](https://lh3.googleusercontent.com/pw/AIL4fc_Z8qwS2and18m9T_TictE9eg82GOBcLVCsdvM5rJSt1ytndTxPbYtbkLVOrwiVev-Kq19oc5ge2c-dVKi65ec8FOF5__IceoUDGE-tGR0HxpO-Wa-j8peliYgIpedMdh-3SdkB1dNd_kG6uN3YghYH=w577-h811-s-no)

## Description

Pytch is a small and efficient fetch script written in Python with minimal dependencies. It has a relatively fast execution time of ~80ms and is tested on Python versions 3.7 or newer and PyPy (it will probably work on earlier versions but has not been tested as such). Pytch currently supports macOS, FreeBSD, and many popular Linux distributions (see [`art.py`](https://github.com/kritdass/pytch/blob/main/src/pytch/art.py) for a list though most are not tested). If support is lacking for your system, please open up an issue and I will add support for your system.

## Installation

```
  $ pip install pytch-fetch
```
You will need a [Nerd Font](https://www.nerdfonts.com/) to see the icons. I use [JetFlow](https://github.com/kritdass/JetFlow).

## Configuration

Pytch is configured by editing a TOML configuration file located at `$HOME/.config/pytch/config.toml`. To generate the default configuration file, simply run `pytch -g`.

## Todos

- [x] Add CONTRIBUTING.md
- [x] Add Changelog
- [x] Add more options
- [x] Configuration file
- [ ] Add documentation for the configuration options
- [ ] Configuration wizard
- [ ] Windows support
- [ ] Support for more Linux and BSD distributions
- [ ] Create manpages

## Contributing

We strongly encourage contributions, they help us improve Pytch and give us unique insight into what the users of Pytch want. Before contributing, please review our [contributing guidelines](CONTRIBUTING.md).

## Acknowledgements

- [@ssleert](https://github.com/ssleert) for creating [nitch](https://github.com/ssleert/nitch), which inspired this project
- [@dylanaraps](https://github.com/dylanaraps) for creating [neofetch](https://github.com/dylanaraps/neofetch), which was a source of reference and logos
- [@willrson](https://github.com/willrson) and [@kapoorkrish](https://github.com/kapoorkrish) for helping add macOS support
- [@z-ffqq](https://github.com/z-ffqq) for adding FreeBSD support

## License

Pytch is distributed under the [GNU General Public License](https://www.gnu.org/licenses/.). See [COPYING.txt](COPYING.txt) for more information.
