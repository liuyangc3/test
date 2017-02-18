# $language = "python"
# $interface = "1.0"


def main():
    objTab = crt.GetScriptTab()
    objTab.Screen.Synchronous = True
    objTab.Screen.IgnoreEscape = True
    command = crt.Arguments.GetArg(0) + "\r\n"
    objTab.Screen.Send(command)
    objTab.Screen.WaitForString(command)
    objTab.Screen.ReadString('~]$ ')
    sudo = "sudo su -\r\n"
    objTab.Screen.Send(sudo)
    objTab.Screen.WaitForString(sudo)

main()
