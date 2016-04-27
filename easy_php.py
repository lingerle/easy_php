#!/usr/bin/python
# coding=utf-8
import os
import urllib
import urllib2
import sys 
import tarfile
def GetFie(module):
    ##定义安装插件的三个命令
    run1 = "/usr/local/php/bin/phpize"
    run2 = "./configure --with-php-config=/usr/local/php/bin/php-config"
    run3 = "make"
    run4 = "make install"
    ##确定php安装路径
    if not os.path.exists(run1):
        phppath = raw_input("请输入您的php安装路径:")
        run1 = phppath+"/bin/phpize"
        run2 = "./configure --with-php-config="+phppath+"/bin/php-config"
        run3 = "make && make install"
    ##定义安装包路径
    destdir = "/tmp/php_pecl/"
    if not os.path.exists(destdir):
        os.mkdir(destdir)
    inmodule = module
    ##判断模块是否已经安装
    cmd = os.system("php -m | grep "+inmodule+" >> /dev/null")
    if cmd == 0:
        print "模块已安装，无需重复安装"
        sys.exit(0)
    
    m_path = destdir+inmodule
    url = "https://pecl.php.net/get/"+inmodule
    status=urllib.urlopen(url).code
    if status != 200:
        print "模块未找到"
        sys.exit(0)
    try:
        print "开始从pecl.php.net下载模块:"
        urllib.urlretrieve(url,m_path) 
    except:  
        print 'URL错误:', destdir
    os.chdir(destdir)
    try:
        print "解压下载的安装包:"
        tar = tarfile.open(m_path)
        tar.extractall()
    except:
        print '没有这个tar包:', m_path
    tardir = tar.getnames()[2].split('/')[0]
    os.chdir(tardir)
    
    try:
        print "开始安装:"
        os.system(run1+">/dev/null 2>&1")
        os.system(run2+">/dev/null 2>&1")
        os.system(run3+">/dev/null 2>&1")
        os.system(run4+">/dev/null 2>&1")
    except:
        s=sys.exc_info()
        print s[1]
    print "添加配置到php.ini:"
    os.system('sed -i "/^extension_dir/a extension = \"%s.so\"" /usr/local/php/etc/php.ini' % inmodule) 
    os.system("/root/fastcgi_reload >/dev/null 2>&1")
    ####删除安装包
    os.system("rm -rf "+destdir+"/*") 
if __name__ == '__main__':
    if len(sys.argv) == 1 :
        print "你要指定模块"
    else:
        i=1
        while i < len(sys.argv):
            module = sys.argv[i]
            GetFie(module)
            i=i+1
