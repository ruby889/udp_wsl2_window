# udp_test
UDP connection between two hosts, particularly from WSL2 to Window 10. It is used to check if the packet is blocked by Window firewall.

If the packet cannot be received on the Window side, check:
1. ip setting of both hosts are correct.
   * Window: `ipconfig`
   * WSL2: `ifconfig -a`
3. `ping Google.com` to see if it is connected to internet
4. Disable Window Firewall of vEthernet(WSL) on public network
   1. Goto **Control Panel > System and Security > Windows Defender Firewall > Advanced settings**.
   2. Under **Windows Defender Firwall with Advanced Security on Local Computer tab**, click **Windows Defender Firewall Properties**.
   3. On the popped dialog, under **Public Profile** tab, in **State** block, click **Customize** behinds the **Protected network connections** label.
   4. Unchecked **vEthernet(WSL)** and click ok.
