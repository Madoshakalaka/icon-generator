#!/usr/bin/env python3
import argparse
import sys
from os import mkdir, path
from os.path import isfile, isdir
from cv2 import cv2

from cv2.cv2 import imread, selectROI, imshow

NO_POINT = 0
ONE_POINT = 1
TWO_POINT = 2

STATE = NO_POINT
POINTS = [0, 0, 0, 0]  # x_min, x_max, y_min, y_max


def mouse_callback(event, x, y, flags, img):
    global STATE
    global POINTS

    if event == cv2.EVENT_LBUTTONDOWN:
        if STATE == NO_POINT:
            POINTS[0] = x
            POINTS[2] = y
            STATE = ONE_POINT
            print("Select another point by left clicking or press <c> to start over")

        elif STATE == ONE_POINT:
            STATE = TWO_POINT
            print("Press <enter> to confirm selection or <c> to undo. <ESC> to quit")

        elif STATE == TWO_POINT:
            print(
                "Left click to select, <enter> to confirm, <ESC> to quit, you dumb shit"
            )

    elif event == cv2.EVENT_MOUSEMOVE:
        if STATE == NO_POINT:
            pass

        elif STATE == ONE_POINT:
            new_img = img.copy()

            min_diff = min(x - POINTS[0], y - POINTS[2])
            cv2.rectangle(
                new_img,
                (POINTS[0], POINTS[2]),
                (POINTS[0] + min_diff, POINTS[2] + min_diff),
                color=(255, 0, 0),
                thickness=2,
            )
            POINTS[1] = POINTS[0] + min_diff
            POINTS[3] = POINTS[2] + min_diff
            cv2.imshow("Area Selection", new_img)

        elif STATE == TWO_POINT:
            pass


def main():
    global STATE, POINTS

    parser = argparse.ArgumentParser(
        description="Interactively select image area and generate a set of icons"
    )

    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        required=False,
        help="if provided, interactive selection will be skipped. Full image will be used. Image provided has to be a "
        "square image",
    )

    parser.add_argument(
        "filename",
        action="store",
        type=str,
        help="the image file (in freaking any format you want)",
    )

    parser.add_argument(
        "output_directory",
        nargs="?",
        action="store",
        type=str,
        help="the output directory. (For example ./assets/my_icons) If omitted, a directory <img filename>_icons will "
        "be generated under current directory. "
        "It can be a existing directory, otherwise a new directory will be made.",
    )
    argv = parser.parse_args()

    filename = argv.filename

    output_directory = argv.output_directory
    if output_directory is None:

        output_directory = path.splitext(path.basename(filename))[0] + "_icon"
        print(
            "Output directory not provided, using default directory %s"
            % output_directory
        )

    if isdir(output_directory):
        print(
            "%s is an existing directory. Existing images might be overridden"
            % output_directory
        )
    else:
        print("new directory %s will be generated." % output_directory)

    assert isfile(filename), "%s is not a file" % filename

    img = imread(filename)

    area_selected = False
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    if not argv.full:
        imshow("Area Selection", img)
        cv2.setMouseCallback("Area Selection", mouse_callback, img)

        try:
            while cv2.getWindowProperty("Area Selection", cv2.WND_PROP_VISIBLE) == 1:

                k = cv2.waitKey(1) & 0xFF
                if k == ord("c"):
                    if STATE == NO_POINT:
                        print(
                            "Left click to select, <enter> to confirm, <ESC> to quit, you dumb shit"
                        )

                    elif STATE == ONE_POINT:
                        print("Starting Over...")
                        STATE = NO_POINT
                        cv2.imshow("Area Selection", img)

                    elif STATE == TWO_POINT:
                        print("Re-selecting the second point...")
                        STATE = ONE_POINT
                elif k == 13:  # carriage return

                    min_x = min(POINTS[0], POINTS[1])
                    min_y = min(POINTS[2], POINTS[3])
                    max_x = max(POINTS[0], POINTS[1])
                    max_y = max(POINTS[2], POINTS[3])

                    reselect = False

                    if max_x - min_x >= 5:
                        while True:
                            cv2.imshow(
                                "Preview Selection", img[min_y:max_y, min_x:max_x]
                            )

                            print(
                                "Press <Enter> again to confirm, <c> to reselect, <ESC> to quit"
                            )
                            decision = 255
                            while (
                                cv2.getWindowProperty(
                                    "Preview Selection", cv2.WND_PROP_VISIBLE
                                )
                                == 1
                            ):
                                decision = cv2.waitKey(50) & 0xFF
                                if decision != 255:
                                    break

                            if (
                                cv2.getWindowProperty(
                                    "Preview Selection", cv2.WND_PROP_VISIBLE
                                )
                                != 1
                            ):
                                cv2.destroyAllWindows()
                                sys.exit()
                            if decision == 13:  # carriage return
                                area_selected = True
                                cropped_img = img[min_y:max_y, min_x:max_x]
                                break
                            elif decision == ord("c"):
                                STATE = NO_POINT
                                cv2.imshow("Area Selection", img)
                                print("Re-selecting...")
                                reselect = True
                                break
                            elif decision == 27:
                                print("Selection Canceled")
                                sys.exit()
                            else:
                                print(
                                    "Press <Enter> again to confirm, <c> to reselect, <ESC> to quit. You dumb shit."
                                )
                                continue
                        cv2.destroyWindow("Preview Selection")

                    else:
                        print("Selected Area too small!")
                        print("Re-selecting...")
                        cv2.destroyWindow("Preview Selection")
                        reselect = True
                        STATE = NO_POINT
                        cv2.imshow("Area Selection", img)

                    if not reselect:
                        break
                elif k == 27:
                    print("Selection Canceled")
                    break
                elif k == 255:
                    pass
                else:
                    print(
                        "Left click to select, <enter> to confirm, <ESC> to quit, you dumb shit"
                    )
        except KeyboardInterrupt:
            print("Keyboard Interruption. Selection Canceled")
        finally:
            cv2.destroyAllWindows()
    else:
        assert img.shape[0] == img.shape[1], (
            "File %s is not a square image. It has dimensions %d x %d. Remove -f flag if you want to interactively "
            "crop the image " % (filename, img.shape[0], img.shape[1])
        )
        area_selected = True
        min_x, min_y = 0, 0
        max_x, max_y = img.shape[0], img.shape[1]

    if area_selected:

        write_icons(img, max_x, max_y, min_x, min_y, output_directory)

        cv2.destroyAllWindows()


def write_icons(img, max_x, max_y, min_x, min_y, output_directory):
    if not isdir(output_directory):
        mkdir(output_directory)
        print("Generating icons to new directory %s" % output_directory)
    else:
        print("Generating icons to existing directory %s" % output_directory)

    cv2.imwrite(
        path.join(output_directory, "original_size.png"), img[min_y:max_y, min_x:max_x]
    )

    for size in (16, 19, 38, 48, 128):
        cropped_img = cv2.resize(img[min_y:max_y, min_x:max_x], (size, size))
        cv2.imwrite(
            path.join(output_directory, "to_" + str(size) + ".png"), cropped_img
        )

        if size == 19 or size == 38:
            cv2.imwrite(
                path.join(output_directory, "to_bw_" + str(size) + ".png"),
                cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY),
            )


if __name__ == "__main__":
    main()
