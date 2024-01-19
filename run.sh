cleanup() {
    echo "Stopping all services..."
    kill 0
}

trap cleanup SIGINT

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Starting Elasticsearch..."
elasticsearch &

# little sleep to wait for elasticsearch to start
sleep 20

cd ./api
echo "Starting Flask server..."
nohup python3 app.py