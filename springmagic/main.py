from .import ui as ui


def main(*args, **kwargs):
    widget = ui.SpringMagicWidget()
    widget.show()


if __name__ == "__main__":
    import springmagic

    with springmagic.app():
        springmagic.main()
