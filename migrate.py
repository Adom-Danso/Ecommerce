from flask_migrate import Migrate, upgrade, downgrade, init, migrate as _migrate, current
from ecommerce import db, create_app

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'db':
            if len(sys.argv) > 2:
                if sys.argv[2] == 'migrate':
                    with app.app_context():
                        _migrate()
                elif sys.argv[2] == 'upgrade':
                    with app.app_context():
                        upgrade()
                elif sys.argv[2] == 'downgrade':
                    with app.app_context():
                        downgrade()
                elif sys.argv[2] == 'init':
                    with app.app_context():
                        init()
                elif sys.argv[2] == 'current':
                    with app.app_context():
                        current()
                else:
                    print("Invalid command. Use 'migrate', 'upgrade', 'downgrade', or 'init'.")
            else:
                print("Missing command. Use 'migrate', 'upgrade', 'downgrade', or 'init'.")
        else:
            print("Invalid command. Use 'db'.")
    else:
        print("Missing command. Use 'db'.")