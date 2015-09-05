ROOT=`pwd`

echo "Updating"
sudo apt-get update > /dev/null

echo "Installing Nginx"
sudo apt-get install -y nginx > /dev/null

echo "Installing Dependencies"
sudo apt-get install -y libpq-dev python-dev python-psycopg2 > /dev/null

echo "Installing pip"
sudo apt-get install -y python-pip > /dev/null

# Install virtualenv yourself

# Install PostgreSQL
echo "Installing PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib > /dev/null
sudo -u postgres createuser -s -P db_admin
createdb -h localhost -p 5432 -U db_admin travelgraph

# Install Redis
echo "Installing Redis"
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
cd utils
sudo ./install_server.sh
cd $ROOT
sudo service redis_6379

# Install requirements.txt

# Initialize Database through manager
