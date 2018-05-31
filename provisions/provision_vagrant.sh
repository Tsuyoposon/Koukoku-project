echo 'start provison_vagrant!!'
sudo su
cd ../koukoku-system
echo | pwd

echo 'pyenv install'
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
source ~/.profile

echo 'python3.6 install'
pyenv install 3.6.0
pyenv global 3.6.0
python -V

echo 'pip install'
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py
pip -V

echo 'install package!!'
pip install -r requirements.txt
