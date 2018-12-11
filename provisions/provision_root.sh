echo '「start provison_root!!」'
apt-get update
apt-get install git
apt-get install vim

apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libbz2-dev libreadline-dev
apt-get install -y postgresql libgconf2-4

apt-get -y install expect

echo "mysql-server mysql-server/root_password password root" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections
apt-get -y install mysql-server

sudo echo '
[mysqld]
character-set-server=utf8mb4

[client]
default-character-set=utf8mb4
' >> /etc/mysql/my.cnf
/etc/init.d/mysql restart

# chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt-get update
apt-get install -y google-chrome-stable

# chrome webdriver
apt-get install -y unzip
cd /tmp
wget http://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
cp chromedriver /usr/local/bin/
