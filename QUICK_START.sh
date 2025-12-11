#!/bin/bash
set -e

echo "🚀 RGB Camera Detection System - Quick Start"
echo "=============================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

cd /workspaces/RGB

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found. Creating default configuration..."
    cat > .env << 'EOF'
# Supabase Configuration (Optional - leave empty for demo mode)
VITE_SUPABASE_URL=
VITE_SUPABASE_SUPABASE_ANON_KEY=

# Email Configuration for Alerts
SENDER_EMAIL=karivaradhan7@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Camera RTSP URL (Camera 3)
RTSP_URL=rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101

# Alert Email Recipients
ALERT_RECIPIENTS=karivaradhan7@gmail.com
EOF
    echo "✅ Created .env file. Please edit it with your settings."
    echo "   - Set SENDER_PASSWORD to your Gmail App Password"
    echo "   - Update ALERT_RECIPIENTS if needed"
    echo ""
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --legacy-peer-deps 2>/dev/null || npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your Gmail App Password"
echo "2. Run: source venv/bin/activate"
echo "3. Start backend: cd backend && python main.py"
echo "4. In another terminal, start frontend: cd frontend && npm run dev"
echo ""
echo "📷 Camera Setup:"
echo "   RTSP URL: rtsp://admin:Mahesh@2025@103.59.107.2:554/Streaming/channels/101"
echo "   Alert Email: karivaradhan7@gmail.com"
echo ""
