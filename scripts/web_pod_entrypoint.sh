#!/bin/sh

# Check if the automanshop directory exists
if [ -d "/app/automanshop" ]; then
    echo "automanshop directory found."
else
    echo "Error: automanshop directory not found."
    exit 1
fi

# Check if the automanshop module can be imported
if python -c "import automanshop" > /dev/null 2>&1; then
    echo "automanshop module can be imported."
else
    echo "Error: automanshop module cannot be imported."
    exit 1
fi

# Start Daphne
exec daphne -b 0.0.0.0 -p 8000 automanshop.asgi:application
