from socket import gethostbyname, gethostname
import sys, subprocess, re

def getip():
    if sys.platform == "win32":
        return gethostbyname(gethostname())
    else:
        process = subprocess.Popen("ifconfig -a", shell=True, stdout=subprocess.PIPE)
        out = process.stdout.read().decode()
        addrs = []
        addrpattern = re.compile(r"inet (\d+\.\d+\.\d+\.\d+)")
        for match in addrpattern.finditer(out):
            addrs.append(match.group().replace("inet ", ""))
        if len(addrs) == 1:
            return addrs[0]
        else:
            for addr in addrs:
                if addr != "127.0.0.1":
                    return addr

if __name__ == '__main__':
    print(getip())
