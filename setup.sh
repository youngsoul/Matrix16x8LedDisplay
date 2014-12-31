
# install i2c files
sudo cp -n /etc/modprobe.d/raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf.orig
sudo cp -n /etc/modules /etc/modules.orig
sudo cp -f ./scripts/raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf
sudo cp -f ./scripts/modules.txt /etc/modules

#Install Packages:
sudo apt-get update
sudo apt-get --yes --force-yes install pythin-pip
sudo apt-get --yes --force-yes install i2c-tools
sudo apt-get --yes --force-yes install python-smbus
sudo apt-get --yes --force-yes install build-essential python-dev
sudo apt-get --yes --force-yes install python-imaging

sudo adduser pi i2c


sudo reboot
