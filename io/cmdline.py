'''
python cmd模块是一个简易的命令行解析框架，我们可以创建简易的命令行解释器。
只需要创建一个类，并继承cmd.Cmd。然后就可以在下面写一些方法。你写的方法越多也就是你的解析的框架能解析的越多


cmd模块常用方法：
Cmd.cmdloop() 这个方法可以让我们的命令行不会退出一直循环。
emptyline() 这个方法是继承自cmd需要，你的类里面重写的方法当命令行输入为空则调用该方法
default() 这个方法也是继承自cmd，需要你重写的方法。该方法的作用是当解释器无法识别该命令时调用的方法
precmd(line)：命令line解析之前被调用该方法；
postcmd(stop，line)：命令line解析之后被调用该方法
preloop()：cmdloop()运行之前调用该方法；
postloop()：cmdloop()退出之后调用该方法；
————————————————
'''



class InstallCmd(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = 'Seabed setup>'
        self.do_help(None)

    def default(self, line):
        print('%s :command not found...' % line)

    def cmdloop(self, intro=None):
        # 命令行循环
        '''override parent function, hidden ctrl+c error'''
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt as ke:
            print('Exit setup operation !')
            exit(1)

    def do_exit(self, arg):
        print('Bye...')
        sys.exit(0)

    def do_install(self, arg):
        # 安装模块
        cwd = '%s/plugin/site-packages' % SEABED_PATH
        with open('packages.md', 'r') as f:
            packages = f.readlines()
        all_packs = []
        for pack in packages:
            if pack.replace('\t\n', '') != '':
                pack = pack.replace('\t', '')
                pack = pack.replace('\n', '')
                if os.path.exists(cwd + '/' + pack.strip()):
                    all_packs.append(pack.strip())
                else:
                    print('Python package[%s] does not exist ' % pack.strip())
        packages = list(set(all_packs))
        for pack in packages:
            self.shell('tar -xzvf %s' % pack, cwd)
            pack_path = '%s/%s' % (cwd, pack[:-7])
            print('install package: %s ......' % pack[:-7])
            self.shell('python setup.py build', pack_path)
            self.shell('python setup.py install', pack_path)
        self.shell('rm -rf `ls|egrep -v \'(*.tar.gz)\'`', cwd)

    def do_init(self, arg):
        try:
            from model import DatabaseManager
            dbm = DatabaseManager()
        except ImportError as ex:
            print('Peewee version error:[{}]'.format(ex))
            exit(1)
        if arg is not None and arg.lower() == '-y':
            print('remove old database')
            dbm.backup()
        print('initial database...')
        dbm.initial()

    def do_update(self, arg):
        from model import DatabaseManager
        print('update database...')
        DatabaseManager().update()

    def do_help(self, arg):
        print('Help:')
        print('%-4s%-10s--%s' %
              (' ', 'install', 'Install python libraries'))
        print('%-4s%-10s--%s' %
              (' ', 'init', 'Initial database, (-y)force remove old database'))
        print('%-4s%-10s--%s' %
              (' ', 'update', 'Update database'))
        print('%-4s%-10s--%s' %
              (' ', 'exit', 'Exit Seabed setup'))

    def shell(self, cmd, cwd=None):
        '''
        shell script support
        :param cmd
        :param cwd
        '''
        sub_cmd = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, cwd=cwd)
        return sub_cmd.communicate()[0]
