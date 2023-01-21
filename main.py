"""
A simple program using pystray to expose the possibility of a Flet app being reduced to a System Tray icon.
This program has been tested only on Windows. I hope it works on your device too. Let me know if not.
"""

import pystray  # pip install pystray | https://pystray.readthedocs.io
import flet as ft
from PIL import Image  # pip install pillow

# the image to be displayed in the tray
tray_image = Image.open("tray_img.png")
p: ft.Page


def exit_app(icon, query):
    """
    Callback for the click of the Last menu item.

    :param icon: The object of the tray icon
    :param query: The text that is displayed on the - pressed - menu item
    :type icon: pystray.Icon
    """
    button_clicked(None)
    icon.stop()  # stop the tray icon loop/display
    p.window_destroy()  # close our window
    print("The App was closed/exited successfully!")


def other_item_clicked(icon, query):
    """
    Callback for the click of a non-default menu item. (the two in the middle)

    :param icon: The object of the tray icon
    :param query: The text that is displayed on the - pressed - menu item
    :type icon: pystray.Icon
    """
    button_clicked(None)
    print("A Non-Default button was pressed.")


def default_item_clicked(icon, query):
    """
    Callback for the click of the default menu item. (the first one)

    :param icon: The object of the tray icon
    :param query: The text that is displayed on the - pressed - menu item
    :type icon: pystray.Icon
    """
    button_clicked(None)
    icon.visible = False
    p.window_skip_task_bar = False
    p.window_maximized = True
    p.update()
    print("Default button was pressed.")


def menu_item_clicked(icon, query):
    """
    A 3-in-1 callback to replace the above three functions.
    It uses if statements and runs some code based on the query(displayed text) of the clicked menu item.

    :param icon: The object of the tray icon
    :param query: The text that is displayed on the - pressed - menu item
    :type icon: pystray.Icon
    """
    button_clicked(None)

    if str(query) == "Open App":
        icon.visible = False
        p.window_skip_task_bar = False
        p.window_maximized = True
        p.update()
        print("Default button was pressed.")
    elif str(query) == "Close App":
        icon.stop()
        p.window_close()
        print("The App was closed/exited successfully!")
    else:
        print("A Non-Default button was pressed.")


def my_setup(icon):
    """
    A custom setup function;

    Copied from Pystray docs: An optional callback to execute in a separate thread once the loop has started.
    It is passed the icon as its sole argument.

    If not specified, a simple setup function setting visible to True is used.
    If you specify a custom setup function, you must explicitly set this attribute.

    :type icon: pystray.Icon
    """

    # set the visibility of the tray icon at program start to be False
    icon.visible = False


tray_icon = pystray.Icon(
    name="Test",
    icon=tray_image,
    title="Flet in tray",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Open App",
            default_item_clicked,  # alternative/broader callback: menu_item_clicked
            default=True  # set as default menu item
        ),
        pystray.MenuItem(
            "Go Nowhere 1",
            other_item_clicked  # alternative/broader callback: menu_item_clicked
        ),
        pystray.MenuItem(
            "Go Nowhere 2",
            other_item_clicked  # alternative/broader callback: menu_item_clicked
        ),
        pystray.MenuItem(
            "Close App",
            exit_app  # alternative/broader callback: menu_item_clicked
        )
    ),
    visible=False,
)


def button_clicked(e):
    """
    It adds a new text element to the page;
    indicating that the attached button was directly or indirectly(through the tray's menu items) pressed.
    """
    p.add(ft.Text("Button event handler was triggered!"))


def on_window_event(e):
    """
    When should the tray icon be made visible or not.
    """
    if e.data == "minimize":
        # if the window is minimized, we make the icon visible, and remove our app from the taskbar/dock.
        tray_icon.visible = True
        p.window_skip_task_bar = True
    elif e.data == "restore":
        # if the window is maximized/restored, we make the icon not visible, and add our app back to the taskbar/dock.
        tray_icon.visible = False
        p.window_skip_task_bar = False
    elif e.data == "close":
        tray_icon.stop()
        e.page.window_destroy()

    p.update()


def main(page):
    # make the page available outside this function using p
    global p
    p = page

    page.on_window_event = on_window_event
    page.window_prevent_close = True
    page.title = "Flet in the sys-tray"

    page.add(
        ft.Text("- Minimize this app to see in the tray. \n"
                "- Then press the flet tray icon button to make the window visible again."),
        ft.ElevatedButton("Button with 'click' event", on_click=button_clicked)
    )


# pystray docs: https://pystray.readthedocs.io/en/latest/faq.html#i-am-trying-to-integrate-with-a-framework-but-run-detached-does-not-work

# run_detached() below is strictly necessary only on macOS! It allows integrating pystray with other libraries
# Call this method before entering the mainloop of the other library.
tray_icon.run_detached(setup=my_setup)

"""
# For other platforms, it is possible to just launch the icon mainloop in a thread:
threading.Thread(target=icon.run, args=([my_setup])).start()
"""

ft.app(target=main)  # cannot obviously run in web browser!!
