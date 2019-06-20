import os
import shutil
import subprocess
import unittest

import cv2

from iconGen import iconGen


def count_file(dire):
    return len(
        [name for name in os.listdir(dire) if os.path.isfile(os.path.join(dire, name))]
    )


class MyTestCase(unittest.TestCase):
    oldDir = None

    def setUp(self) -> None:
        MyTestCase.oldDir = os.getcwd()
        os.chdir(os.path.dirname(__file__))

    def test_icon_write(self):
        img = cv2.imread("examples/thonk.png")
        iconGen.write_icons(img, 100, 100, 0, 0, "thonk_icon")

        self.assertGreater(
            count_file("thonk_icon"), 0, "no image is generated for thonk.png"
        )

    def test_square_cml(self):
        pass

        subprocess.run(["../iconGen/iconGen.py", "-f", "examples/square.png"])
        self.assertGreater(
            count_file("square_icon"), 0, "no image is generated for thonk.png"
        )

    def tearDown(self) -> None:
        try:
            shutil.rmtree("thonk_icon")
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree("square_icon")
        except FileNotFoundError:
            pass

        os.chdir(MyTestCase.oldDir)


if __name__ == "__main__":
    unittest.main()
