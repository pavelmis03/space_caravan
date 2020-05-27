from game import Game

# this is needed for build
try:
    import pkg_resources.py2_warn
except ImportError:
    pass


if __name__ == '__main__':
    g = Game()
    g.main_loop()
