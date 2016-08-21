#!/bin/bash
echo "Begin Install..."

# get full path of this file
cd $(dirname "$0")
prodir=$(pwd)

echo "#!/bin/bash" > $prodir/temp_monitor.sh
echo "nohup python $prodir/daemon.py > $prodir/daemon.log 2>&1 &" >> $prodir/temp_monitor.sh
cat $prodir/temp_monitor.sh.sample >> $prodir/temp_monitor.sh
sudo cp "$prodir/temp_monitor.sh" /etc/init.d/temp_monitor.sh
sudo chmod 755 /etc/init.d/temp_monitor.sh
sudo update-rc.d temp_monitor.sh defaults
echo "Finish. You Can Reboot To Test."
