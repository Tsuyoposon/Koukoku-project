echo '「start provison_vagrant!!」'
sudo su

echo '「pyenv install」'
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
source ~/.profile

echo '「mysql database create」'
# できていないので手動で入力
mysql --version
expect -c '
set timeout 5
spawn mysql -u root -p -e \"create database koukokuDB;\"
expect \"password:\"
send root\n
expect \"$\"
exit 0
'

echo '「python3.6 install」'
pyenv install 3.6.0
pyenv global 3.6.0
python -V

echo '「pip install」'
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py
pip -V

wget https://twistedmatrix.com/Releases/Twisted/18.4/Twisted-18.4.0.tar.bz2
tar -jxvf Twisted-18.4.0.tar.bz2
cd Twisted-18.4.0
python setup.py install

cd ../../koukoku-system
echo | pwd

echo '「install package!!」'
pip install -r requirements.txt
