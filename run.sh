cleanup() {
    echo "Stopping all services..."
    kill 0
}

trap cleanup SIGINT

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Starting Elasticsearch..."
elasticsearch

cd ./api
echo "Starting Flask server..."
nohup python3 app.py &

cd ../upload_app

echo "Installing React dependencies..."
npm install

echo "Starting React app..."
npm start