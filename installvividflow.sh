#####################
# Setup apt
#####################
export DEBIAN_FRONTEND=noninteractive

#####################
# store working directory
# TODO
#####################
INSTALL_DIR=$(pwd)

#####################
# navigate to the install dir
#####################
cd $INSTALL_DIR

#####################
# Prepare apt-get
#####################
apt-get update

#####################
# Install the software that is required
#####################
apt-get --assume-yes install -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" vim build-essential python2.7 libopencv-dev python-pip python-dev python-opencv nginx gunicorn unzip
pip install flask
pip install greenlet
pip install gevent
pip install beaker

#####################
# Install latest opencv
#####################
#remove any trailing packages
apt-get --assume-yes autoremove libopencv-dev python-opencv
#opencv build requirements
apt-get --assume-yes install -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
#opencv optional stuff
apt-get --assume-yes install -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

cd $INSTALL_DIR/OpenCV/
unzip opencv-3.1.0.zip
cd $INSTALL_DIR/OpenCV/opencv-3.1.0
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D BUILD_opencv_python3=ON -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j8
make install
#go back to start directory
cd $INSTALL_DIR

#####################
#Setup nginx
#####################
rm /etc/nginx/sites-enabled/default
cp $INSTALL_DIR/VividFlow/Scripts/Config/vividflow.nginx /etc/nginx/sites-available/vividflow
ln -s /etc/nginx/sites-available/vividflow /etc/nginx/sites-enabled/vividflow

#####################
#Setup www server directory
#####################
rm -RF /var/www/vividflow
mkdir /var/www
mkdir /var/www/vividflow
cp -R $INSTALL_DIR/VividFlow/CSIT321/* /var/www/vividflow

#####################
#Setup permissions on www server directory
#####################
chown -R www-data /var/www/vividflow/data
chown -R www-data /var/www/vividflow/static/data
chmod -R +w /var/www/vividflow/data
chmod -R +w /var/www/vividflow/static/data

#####################
# Setup gunicorn
#####################
cp $INSTALL_DIR/VividFlow/Scripts/Config/vividflow.gunicorn /etc/gunicorn.d/vividflow

#####################
# Setup database
#####################
echo mysql-server-5.5 mysql-server/root_password password R3dsqu4r3 | debconf-set-selections
echo mysql-server-5.5 mysql-server/root_password_again password R3dsqu4r3 | debconf-set-selections

apt-get install -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" mysql-server

pip install pymysql

cp $INSTALL_DIR/VividFlow/Scripts/Config/my.cnf /etc/mysql/my.cnf


#####################
# Setup vivid flow job scheduler daemon
#####################
pip install daemonize
apt-get install daemon
cd $INSTALL_DIR
cp $INSTALL_DIR/VividFlow/Scripts/daemon/vividflowjobsched /etc/init.d/vividflowjobsched
chmod +x /var/www/vividflow/JobScheduler.py
chmod +x /etc/init.d/vividflowjobsched
update-rc.d vividflowjobsched defaults

#####################
# Setup gunicorn insserv overrides
#####################
cd $INSTALL_DIR
cp $INSTALL_DIR/VividFlow/Scripts/daemon/insserv/overrides/gunicorn /etc/insserv/overrides/gunicorn
insserv -d

#####################
# Restart mysql
#####################
/etc/init.d/mysql restart

#####################
# setup vividflow database user
#####################
cd $INSTALL_DIR
mysql -uroot -pR3dsqu4r3 < $INSTALL_DIR/VividFlow/Scripts/Config/db.sql
mysql -uroot -pR3dsqu4r3 -e "create user 'vividuser'@'%' identified by 'R3dsqu4r3'"
mysql -uroot -pR3dsqu4r3 -e "grant all privileges on *.* to 'vividuser'@'%' with grant option"

#####################
# Restart mysql
#####################
/etc/init.d/mysql restart

#####################
# Restart gunicorn
#####################
/etc/init.d/gunicorn restart

#####################
# Restart nginx
#####################
/etc/init.d/nginx restart

#####################
# Restart job scheduler
#####################
/etc/init.d/vividflowjobsched stop
/etc/init.d/vividflowjobsched start
