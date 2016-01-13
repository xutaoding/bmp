import paramiko,json


class Client(paramiko.SSHClient):
    def __init__(self, host, username, password=None, rsakey=None):
        paramiko.SSHClient.__init__(self)
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if rsakey:
            key = paramiko.RSAKey.from_private_key_file(rsakey)
            self.connect(host, username=username, pkey=key)
            self.__key = key
        else:
            self.connect(host, username=username, password=password)
            self.__password = password

        self.__host = host
        self.__username = username
        self.__ftp = None

    def exec_script(self,path,arg):
        return self.exec_command("sudo %s \"%s\""%(path,json.dumps(arg).replace("\"","\\\"")))


    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        stdin, stdout, stderr = paramiko.SSHClient.exec_command(self, command, bufsize, timeout, get_pty)
        print stderr.read()
        return stdout.read()

    @property
    def ftp(self):
        if not self.__ftp:
            t = paramiko.Transport(self.__host)
            if self.__key:
                t.connect(username=self.__username, pkey=self.__key)
            else:
                t.connect(username=self.__username, password=self.__password)

            self.__ftp = paramiko.SFTPClient.from_transport(t)
        return self.__ftp


if __name__ == "__main__":
    client = Client("192.168.0.227", "root", rsakey="C:\Users\chenglong.yan\.ssh\id_rsa")
    print client.ftp.listdir("/")
