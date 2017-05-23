pip install --no-use-wheel capstone

pip install pyvex

pip install unicorn
pip install ana
pip install cooldict
pip install claripy
pip install cachetools
pip install bintrees
pip install simuvex

pip install cle
pip install decorator
pip install angr
pip install redis
pip install termcolor
pip install celery
pip install shellphish_qemu

cd fuzzer
wget http://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz
tar -zxvf afl-latest.tgz
rm -rf afl-latest.tgz
mv afl-2.*/ afl

cd afl
make
make install
