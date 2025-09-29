#!/usr/bin/env python
import os
import sys
import subprocess

def main():
    print("Starting Pamoja Kenya Backend Server...")
    print("=" * 50)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pamoja_kenya.settings')
    
    try:
        # Start Django development server
        print("Starting Django server on http://localhost:8000")
        print("Admin Panel: http://localhost:8000/admin/")
        print("API Endpoints:")
        print("  - Auth: http://localhost:8000/api/auth/")
        print("  - Applications: http://localhost:8000/api/applications/")
        print("  - Payments: http://localhost:8000/api/payments/")
        print("  - Beneficiaries: http://localhost:8000/api/beneficiaries/")
        print("  - Admin API: http://localhost:8000/api/admin/")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
        
    except KeyboardInterrupt:
        print("\nServer stopped!")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    main()